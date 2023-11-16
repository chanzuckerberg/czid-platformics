from abc import abstractmethod
from mypy_boto3_s3.client import S3Client
from Bio import SeqIO
from io import StringIO
from typing import Protocol


class FileFormatHandler(Protocol):
    @classmethod
    @abstractmethod
    def validate(cls, client: S3Client, bucket: str, file_path: str) -> int:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def convert_to(cls, client: S3Client, bucket: str, file_path: str, format: dict) -> str:
        raise NotImplementedError


class FastqHandler(FileFormatHandler):
    @classmethod
    def validate(cls, client: S3Client, bucket: str, file_path: str) -> int:
        # Overly simplistic validator for fastq filees checks whether the first 1mb of a file are a valid fastq
        data = client.get_object(Bucket=bucket, Key=file_path, Range="bytes=0-1000000")["Body"].read()
        records = 0
        for _ in SeqIO.parse(StringIO(data.decode("ascii")), "fastq"):
            records += 1
        assert records > 0
        return client.head_object(Bucket=bucket, Key=file_path)["ContentLength"]

    @classmethod
    def convert_to(cls, client: S3Client, bucket: str, file_path: str, format: dict) -> str:
        return ""


def get_validator(format: str) -> type[FileFormatHandler]:
    if format == "fastq":
        return FastqHandler
    else:
        raise Exception("Unknown file format")
