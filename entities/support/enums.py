import strawberry
import enum


@strawberry.enum
class FileStatus(enum.Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PENDING = "PENDING"


@strawberry.enum
class FileAcessProtocol(enum.Enum):
    s3 = "s3"


@strawberry.enum
class Nucleotide(enum.Enum):
    RNA = "RNA"
    DNA = "DNA"


@strawberry.enum
class SequencingProtocol(enum.Enum):
    MNGS = "MNGS"
    TARGETED = "TARGETED"
    MSSPE = "MSSPE"
