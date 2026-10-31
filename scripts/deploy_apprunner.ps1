# ==============================================================================
# GeoSentinel AWS App Runner Deployment Automation Script (PowerShell)
# ==============================================================================

param(
    [string]$Region = "us-east-1",
    [string]$RepositoryName = "geosentinel",
    [string]$ServiceName = "geosentinel"
)

$ErrorActionPreference = "Stop"

Write-Host ">>> [1/5] Checking AWS Caller Identity..." -ForegroundColor Cyan
try {
    $identityJson = aws sts get-caller-identity --output json
    $identity = $identityJson | ConvertFrom-Json
    $accountId = $identity.Account
    Write-Host "Authenticated as AWS Account: $accountId in Region: $Region" -ForegroundColor Green
} catch {
    Write-Error "Failed to obtain AWS identity. Please run 'aws configure' first."
    exit 1
}

$ecrUri = "$accountId.dkr.ecr.$Region.amazonaws.com/$RepositoryName"

Write-Host ">>> [2/5] Ensuring ECR Repository '$RepositoryName' exists..." -ForegroundColor Cyan
try {
    aws ecr describe-repositories --repository-names $RepositoryName --region $Region 2>$null
    Write-Host "ECR repository '$RepositoryName' already exists." -ForegroundColor Yellow
} catch {
    Write-Host "Creating ECR repository '$RepositoryName'..." -ForegroundColor Green
    aws ecr create-repository --repository-name $RepositoryName --region $Region
}

Write-Host ">>> [3/5] Authenticating Docker to ECR and Pushing Image..." -ForegroundColor Cyan
aws ecr get-login-password --region $Region | docker login --username AWS --password-stdin "$accountId.dkr.ecr.$Region.amazonaws.com"
docker build -f docker/Dockerfile -t "${RepositoryName}:latest" .
docker tag "${RepositoryName}:latest" "${ecrUri}:latest"
docker push "${ecrUri}:latest"
Write-Host "Pushed image to: ${ecrUri}:latest" -ForegroundColor Green

Write-Host ">>> [4/5] Checking IAM Role for App Runner ECR Access..." -ForegroundColor Cyan
$roleName = "AppRunnerECRAccessRole"
$roleArn = "arn:aws:iam::${accountId}:role/${roleName}"

try {
    aws iam get-role --role-name $roleName 2>$null
} catch {
    Write-Host "Creating IAM role $roleName for App Runner..." -ForegroundColor Green
    $assumeRolePolicy = @{
        Version = "2012-10-17"
        Statement = @(
            @{
                Effect = "Allow"
                Principal = @{ Service = "build.apprunner.amazonaws.com" }
                Action = "sts:AssumeRole"
            }
        )
    } | ConvertTo-Json -Depth 5

    aws iam create-role --role-name $roleName --assume-role-policy-document "$assumeRolePolicy"
    aws iam attach-role-policy --role-name $roleName --policy-arn "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"
    Start-Sleep -Seconds 10
}

Write-Host ">>> [5/5] Deploying / Updating AWS App Runner Service '$ServiceName'..." -ForegroundColor Cyan
$sourceConfig = @{
    ImageRepository = @{
        ImageIdentifier = "${ecrUri}:latest"
        ImageConfiguration = @{
            Port = "8000"
            RuntimeEnvironmentVariables = @{
                ENVIRONMENT = "production"
                AWS_USE_ANONYMOUS = "true"
                APP_PORT = "8000"
                AWS_REGION = $Region
            }
        }
        ImageRepositoryType = "ECR"
    }
    AutoDeploymentsEnabled = $true
    AuthenticationConfiguration = @{
        AccessRoleArn = $roleArn
    }
} | ConvertTo-Json -Compress

$instanceConfig = '{"Cpu": "1 vCPU", "Memory": "2 GB"}'
$healthConfig = '{"Protocol": "HTTP", "Path": "/api/v1/health", "Interval": 10, "Timeout": 5, "HealthyThreshold": 1, "UnhealthyThreshold": 3}'

try {
    $existing = aws apprunner list-services --region $Region --output json | ConvertFrom-Json
    $matched = $existing.ServiceSummaryList | Where-Object { $_.ServiceName -eq $ServiceName }

    if ($matched) {
        Write-Host "Updating existing App Runner service: $($matched.ServiceArn)..." -ForegroundColor Yellow
        aws apprunner update-service --service-arn $matched.ServiceArn --source-configuration "$sourceConfig" --region $Region
        $serviceUrl = "https://$($matched.ServiceUrl)"
    } else {
        Write-Host "Creating new App Runner service '$ServiceName'..." -ForegroundColor Green
        $createResp = aws apprunner create-service `
            --service-name $ServiceName `
            --source-configuration "$sourceConfig" `
            --instance-configuration "$instanceConfig" `
            --health-check-configuration "$healthConfig" `
            --region $Region --output json | ConvertFrom-Json
        $serviceUrl = "https://$($createResp.Service.ServiceUrl)"
    }

    Write-Host "=================================================================" -ForegroundColor Green
    Write-Host "SUCCESS! App Runner deployment initiated." -ForegroundColor Green
    Write-Host "Public Service URL: $serviceUrl" -ForegroundColor Cyan
    Write-Host "Health Check:       $serviceUrl/api/v1/health" -ForegroundColor Cyan
    Write-Host "=================================================================" -ForegroundColor Green
} catch {
    Write-Error "App Runner deployment failed: $_"
}
