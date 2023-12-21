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


class FastaHandler(FileFormatHandler):
    """
    Validate FASTA files. Note that even truncated FASTA files are supported:
    ">" is a valid FASTA file, and so is ">abc" (without a sequence).
    """

    @classmethod
    def validate(cls, client: S3Client, bucket: str, file_path: str) -> None:
        with get_file_preview(client, bucket, file_path) as fp:
            sequences = 0
            for _ in SeqIO.parse(fp, "fasta"):
                sequences += 1
            assert sequences > 0


# FIXME: Add tests for FASTA, FASTQ, JSON, BED
class FastqHandler(FileFormatHandler):
    """
    Validate FASTQ files. Ignores truncated lines by assuming 1 read = 4 lines.
    """

    @classmethod
    def validate(cls, client: S3Client, bucket: str, file_path: str) -> None:
        with get_file_preview(client, bucket, file_path) as fp:
            # Load file in memory and only keep a total number of lines that % 4 == 0
            # FIXME: cleanup code
            f = fp.read()
            f = f.split("\n")
            f = f[: len(f) - (len(f) % 4)]
            f = "\n".join(f)
            fp = tempfile.NamedTemporaryFile("w+b")
            fp.write(f.encode("utf-8"))
            fp.flush()

            # Check it with SeqIO:
            reads = 0
            for _ in SeqIO.parse(fp, "fastq"):
                reads += 1
            assert reads > 0


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
    if format == "fasta":
        return FastaHandler
    elif format == "fastq":
        return FastqHandler
    # FIXME: validate BED files (SeqIO.parse() doesn't support BED files)
    elif format == "bed":
        pass
    elif format == "json":
        return JSONHandler
    else:
        raise Exception(f"Unknown file format '{format}'")
