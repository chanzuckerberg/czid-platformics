"""
Logic to validate that a file of a certain format is valid
"""

import gzip
import json
import tempfile
import typing
from abc import abstractmethod
from mypy_boto3_s3.client import S3Client
from Bio import SeqIO
from typing import Protocol


class FileFormatHandler(Protocol):
    """
    Interface for a file format handler
    """

    @classmethod
    @abstractmethod
    def validate(cls, client: S3Client, bucket: str, file_path: str) -> None:
        raise NotImplementedError


class BioPythonHandler(FileFormatHandler):
    """
    Validate files using BioPython (supports FASTQ, FASTA, and others: https://biopython.org/wiki/SeqIO#file-formats)
    """

    format: str

    @classmethod
    def validate(cls, client: S3Client, bucket: str, file_path: str) -> None:
        fp = get_file_preview(client, bucket, file_path)
        assert len([read for read in SeqIO.parse(fp, BioPythonHandler.format)]) > 0


class JSONHandler(FileFormatHandler):
    """
    Validate JSON files
    """

    @classmethod
    def validate(cls, client: S3Client, bucket: str, file_path: str) -> None:
        with get_file_preview(client, bucket, file_path) as fp:
            file_content = fp.read()  # works with plain text and gzip
        json.loads(file_content)  # throws an exception for invalid JSON


def get_file_preview(client: S3Client, bucket: str, file_path: str) -> typing.TextIO:
    """
    Get first 1MB of a file and save it in a temporary file
    """
    data = client.get_object(Bucket=bucket, Key=file_path, Range="bytes=0-1000000")["Body"].read()
    fp = tempfile.NamedTemporaryFile("w+b")
    fp.write(data)
    fp.flush()

    try:
        data.decode("utf-8")
        return open(fp.name, "r")
    except UnicodeDecodeError:
        return gzip.open(fp.name, "rt")


def get_validator(format: str) -> type[FileFormatHandler]:
    """
    Returns the validator for a given file format
    """
    if format in ["fastq", "fasta"]:
        BioPythonHandler.format = format
        return BioPythonHandler
    elif format == "bed":
        pass
    elif format == "json":
        return JSONHandler
    else:
        raise Exception(f"Unknown file format '{format}'")
