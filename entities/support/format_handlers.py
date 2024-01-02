"""
Logic to validate that a file of a certain format is valid
"""

import io
import json
from abc import abstractmethod
from Bio import SeqIO
from typing import Protocol


class FileFormatHandler(Protocol):
    """
    Interface for a file format handler
    """

    @classmethod
    @abstractmethod
    def validate(cls, contents: str) -> None:
        raise NotImplementedError


class FastaHandler(FileFormatHandler):
    """
    Validate FASTA files. Note that even truncated FASTA files are supported:
    ">" is a valid FASTA file, and so is ">abc" (without a sequence).
    """

    @classmethod
    def validate(cls, contents: str) -> None:
        sequences = 0
        for _ in SeqIO.parse(io.StringIO(contents), "fasta"):
            sequences += 1
        assert sequences > 0


class FastqHandler(FileFormatHandler):
    """
    Validate FASTQ files. Can't use biopython directly because large file would be truncated.
    This removes truncated FASTQ records by assuming 1 read = 4 lines.
    """

    @classmethod
    def validate(cls, contents: str) -> None:
        # Load file and only keep non-truncated FASTQ records (4 lines per record)
        fastq = contents.split("\n")
        fastq = fastq[: len(fastq) - (len(fastq) % 4)]
        fastq = "\n".join(fastq)

        # Validate it with SeqIO
        reads = 0
        for _ in SeqIO.parse(io.StringIO(fastq), "fastq"):
            reads += 1
        assert reads > 0


class BedHandler(FileFormatHandler):
    """
    Validate BED files using basic checks.
    """

    @classmethod
    def validate(cls, contents: str) -> None:
        # Ignore last line since it could be truncated
        records = contents.split("\n")[:-1]
        assert len(records) > 0

        # BED files must have at least 3 columns - error out if the file incorrectly uses spaces instead of tabs
        num_cols = -1
        for record in records:
            assert len(record.split("\t")) >= 3
            # All rows should have the same number of columns
            if num_cols == -1:
                num_cols = len(record.split("\t"))
            else:
                assert num_cols == len(record.split("\t"))


class JsonHandler(FileFormatHandler):
    """
    Validate JSON files
    """

    @classmethod
    def validate(cls, contents: str) -> None:
        json.loads(contents)  # throws an exception for invalid JSON


def get_validator(format: str) -> type[FileFormatHandler]:
    """
    Returns the validator for a given file format
    """
    if format == "fasta":
        return FastaHandler
    elif format == "fastq":
        return FastqHandler
    elif format == "bed":
        return BedHandler
    elif format == "json":
        return JsonHandler
    else:
        raise Exception(f"Unknown file format '{format}'")
