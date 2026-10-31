"""AWS package for GeoSentinel."""
from .s3_client import aws_s3_client, AwsS3Client
from .registry import get_all_datasets, get_dataset_by_id, EARTH_OBSERVATION_DATASETS
from .location_service import amazon_location, AmazonLocationHelper

__all__ = [
    "aws_s3_client",
    "AwsS3Client",
    "get_all_datasets",
    "get_dataset_by_id",
    "EARTH_OBSERVATION_DATASETS",
    "amazon_location",
    "AmazonLocationHelper"
]
