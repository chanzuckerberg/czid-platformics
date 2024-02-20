"""
Validate that format handlers work as expected
"""

from typing import Generator
import pytest
from platformics.support.format_handlers import get_validator

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

@mock_s3
@pytest.fixture
def s3_info() -> Generator[tuple[S3Client, str], None, None]:
    s3 = boto3.client("s3", region_name="us-east-1")
    bucket = "mybucket"
    for name, values in CASES_VALID_FILES.items():
        for i, value in enumerate(values):
            s3.put_object(Bucket=bucket, Key=f"valid-{i}.{name}", Body=value)
    for name, values in CASES_INVALID_FILES.items():
        for i, value in enumerate(values):
            s3.put_object(Bucket=bucket, Key=f"invalid-{i}.{name}", Body=value)
    yield s3, bucket


@mock_s3
@pytest.mark.parametrize("format", ["fasta", "fastq", "bed", "json"])
def test_validation_valid_files(format: str, s3_info: tuple[S3Client, str]) -> None:
    s3, bucket = s3_info
    for i, _ in enumerate(CASES_VALID_FILES[format]):
        validator = get_validator(format)(s3, bucket, f"valid-{i}.{format}")
        validator.validate()


@mock_s3
@pytest.mark.parametrize("format", ["fasta", "fastq", "bed", "json"])
def test_validation_invalid_files(format: str, s3_info: tuple[S3Client, str]) -> None:
    s3, bucket = s3_info
    for i, _ in enumerate(CASES_INVALID_FILES[format]):
        validator = get_validator(format)(s3, bucket, f"valid-{i}.{format}")
        with pytest.raises(Exception):
            validator.validate()
