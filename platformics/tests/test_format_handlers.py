"""
Validate that format handlers work as expected
"""

import pytest
from platformics.support.format_handlers import get_validator

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


@pytest.mark.parametrize("format", ["fasta", "fastq", "bed", "json"])
def test_validation_valid_files(format: str) -> None:
    validator = get_validator(format)
    for test_case in CASES_VALID_FILES[format]:
        validator.validate(test_case)


@pytest.mark.parametrize("format", ["fasta", "fastq", "bed", "json"])
def test_validation_invalid_files(format: str) -> None:
    validator = get_validator(format)
    for test_case in CASES_INVALID_FILES[format]:
        with pytest.raises(Exception):
            validator.validate(test_case)
