#!/usr/bin/env bash
# ==============================================================================
# GeoSentinel AWS App Runner Deployment Automation Script (Bash)
# ==============================================================================

set -euo pipefail

REGION="${AWS_REGION:-us-east-1}"
REPOSITORY_NAME="geosentinel"
SERVICE_NAME="geosentinel"

echo ">>> [1/5] Checking AWS Caller Identity..."
ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
echo "Authenticated as AWS Account: ${ACCOUNT_ID} in Region: ${REGION}"

ECR_URI="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPOSITORY_NAME}"

echo ">>> [2/5] Ensuring ECR Repository '${REPOSITORY_NAME}' exists..."
if ! aws ecr describe-repositories --repository-names "${REPOSITORY_NAME}" --region "${REGION}" >/dev/null 2>&1; then
    echo "Creating ECR repository '${REPOSITORY_NAME}'..."
    aws ecr create-repository --repository-name "${REPOSITORY_NAME}" --region "${REGION}"
else
    echo "ECR repository '${REPOSITORY_NAME}' already exists."
fi

echo ">>> [3/5] Authenticating Docker to ECR and Pushing Image..."
aws ecr get-login-password --region "${REGION}" | docker login --username AWS --password-stdin "${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com"
docker build -f docker/Dockerfile -t "${REPOSITORY_NAME}:latest" .
docker tag "${REPOSITORY_NAME}:latest" "${ECR_URI}:latest"
docker push "${ECR_URI}:latest"
echo "Pushed image to: ${ECR_URI}:latest"

echo ">>> [4/5] Checking IAM Role for App Runner ECR Access..."
ROLE_NAME="AppRunnerECRAccessRole"
ROLE_ARN="arn:aws:iam::${ACCOUNT_ID}:role/${ROLE_NAME}"

if ! aws iam get-role --role-name "${ROLE_NAME}" >/dev/null 2>&1; then
    echo "Creating IAM role ${ROLE_NAME} for App Runner..."
    ASSUME_ROLE_POLICY='{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"build.apprunner.amazonaws.com"},"Action":"sts:AssumeRole"}]}'
    aws iam create-role --role-name "${ROLE_NAME}" --assume-role-policy-document "${ASSUME_ROLE_POLICY}"
    aws iam attach-role-policy --role-name "${ROLE_NAME}" --policy-arn "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"
    sleep 10
fi

echo ">>> [5/5] Deploying / Updating AWS App Runner Service '${SERVICE_NAME}'..."
SOURCE_CONFIG=$(cat <<EOF
{
  "ImageRepository": {
    "ImageIdentifier": "${ECR_URI}:latest",
    "ImageConfiguration": {
      "Port": "8000",
      "RuntimeEnvironmentVariables": {
        "ENVIRONMENT": "production",
        "AWS_USE_ANONYMOUS": "true",
        "APP_PORT": "8000",
        "AWS_REGION": "${REGION}"
      }
    },
    "ImageRepositoryType": "ECR"
  },
  "AutoDeploymentsEnabled": true,
  "AuthenticationConfiguration": {
    "AccessRoleArn": "${ROLE_ARN}"
  }
}
EOF
)

SERVICE_ARN=$(aws apprunner list-services --region "${REGION}" --query "ServiceSummaryList[?ServiceName=='${SERVICE_NAME}'].ServiceArn" --output text)

if [ -n "${SERVICE_ARN}" ]; then
    echo "Updating existing App Runner service: ${SERVICE_ARN}..."
    aws apprunner update-service --service-arn "${SERVICE_ARN}" --source-configuration "${SOURCE_CONFIG}" --region "${REGION}"
    SERVICE_URL="https://$(aws apprunner describe-service --service-arn "${SERVICE_ARN}" --region "${REGION}" --query "Service.ServiceUrl" --output text)"
else
    echo "Creating new App Runner service '${SERVICE_NAME}'..."
    CREATE_RESP=$(aws apprunner create-service \
        --service-name "${SERVICE_NAME}" \
        --source-configuration "${SOURCE_CONFIG}" \
        --instance-configuration '{"Cpu": "1 vCPU", "Memory": "2 GB"}' \
        --health-check-configuration '{"Protocol": "HTTP", "Path": "/api/v1/health", "Interval": 10, "Timeout": 5, "HealthyThreshold": 1, "UnhealthyThreshold": 3}' \
        --region "${REGION}")
    SERVICE_URL="https://$(echo "${CREATE_RESP}" | jq -r .Service.ServiceUrl)"
fi

echo "================================================================="
echo "SUCCESS! App Runner deployment initiated."
echo "Public Service URL: ${SERVICE_URL}"
echo "Health Check:       ${SERVICE_URL}/api/v1/health"
echo "================================================================="
