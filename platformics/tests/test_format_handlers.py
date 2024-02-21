"""
Validate that format handlers work as expected
"""

import pytest
from platformics.support.format_handlers import get_validator
from typing import Generator

import boto3
from moto import mock_s3
from mypy_boto3_s3 import S3Client

CASES_VALID_FILES = {
    "fasta": [
        ">seq1\nACGT\n",
        ">seq2\n",
    ],
    "fastq": [
        "@read1\nACGT\n+\nAAAA\n",
    ],
    "bed": [
        "chr1\t123\t456\n",
    ],
    "json": [
        '{"a": 1, "b": 2}',
    ],
}

CASES_INVALID_FILES = {
    "fasta": [
        "@seq1\nACGT\n",
    ],
    "fastq": [
        "@read1\nACGT\n+\nAAA\n",  # sequence field should be same length as quality field
        "@read1\nACGT\n",  # truncated
    ],
    "bed": [
        "chr1\t123\n",  # need at least 3 columns
        "chr1\t123\t456\tABC\nchr2\t111\t222\n",  # all rows should have the same number of columns
    ],
    "json": [
        '{"a": 1, "b": }',  # bad JSON (not testing it much because using json.loads() as validator)
    ],
}

BUCKET = "local-bucket"

@mock_s3
@pytest.fixture()
def moto_client() -> Generator[S3Client, None, None]:
    client = boto3.client("s3")
    client.create_bucket(Bucket="local-bucket")
    yield client 

@pytest.mark.parametrize("format", ["fasta", "fastq", "bed", "json"])
def test_validation_valid_files(format: str, moto_client: S3Client) -> None:
    for i, value in enumerate(CASES_VALID_FILES[format]):
        moto_client.put_object(Bucket=BUCKET, Key=f"valid-{i}.{format}", Body=value)
        validator = get_validator(format)(moto_client, BUCKET, f"valid.{format}")
        validator.validate()


@pytest.mark.parametrize("format", ["fasta", "fastq", "bed", "json"])
def test_validation_invalid_files(format: str, moto_client: S3Client) -> None:
    for i, value in enumerate(CASES_INVALID_FILES[format]):
        moto_client.put_object(Bucket=BUCKET, Key=f"invalid-{i}.{format}", Body=value)
        validator = get_validator(format)(moto_client, BUCKET, f"invalid-{i}.{format}")
        with pytest.raises(Exception):
            validator.validate()
