"""
GraphQL enums

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/support/enums.py.j2 instead.
"""

import strawberry
import enum


@strawberry.enum
class FileStatus(enum.Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PENDING = "PENDING"


@strawberry.enum
class FileAccessProtocol(enum.Enum):
    s3 = "s3"


@strawberry.enum
class FileUploadClient(enum.Enum):
    browser = "browser"
    cli = "cli"
    s3 = "s3"
    basespace = "basespace"


@strawberry.enum
class NucleicAcid(enum.Enum):
    RNA = "RNA"
    DNA = "DNA"


@strawberry.enum
class SequencingProtocol(enum.Enum):
    MNGS = "MNGS"
    TARGETED = "TARGETED"
    MSSPE = "MSSPE"


@strawberry.enum
class SequencingTechnology(enum.Enum):
    Illumina = "Illumina"
    Nanopore = "Nanopore"


@strawberry.enum
class AlignmentTool(enum.Enum):
    bowtie2 = "bowtie2"
    minimap2 = "minimap2"
    ncbi = "ncbi"


@strawberry.enum
class TaxonLevel(enum.Enum):
    species = "species"
    genus = "genus"
    family = "family"
