import os

import pytest
from pydantic import ValidationError

from manifest.manifest import Manifest, EntityInput


def test_valid_parse() -> None:
    """
    This is a happy path test that parses and serializes a valid manifest.
    It also contains tests for several default value cases.
    """

    path = os.path.join(os.path.dirname(__file__), "test_manifests/valid.yaml")
    with open(path) as f:
        manifest = Manifest.from_yaml(f)
    json_str = manifest.model_dump_json()
    Manifest.model_validate_json(json_str)

    sample_input_loader = [loader for loader in manifest.input_loaders][0]
    assert (
        sample_input_loader.inputs["sample"] == "sample"
    ), "Null input loader inputs should default to their loader input name"

    kindness_input_loader = [loader for loader in manifest.input_loaders if loader.name == "kindness"][0]
    assert list(kindness_input_loader.version.filter(["0.0.0", "0.0.1"])) == ["0.0.1"], "Version filter should work"
    assert (
        kindness_input_loader.inputs["mood"] == "mood"
    ), "Null input loader inputs should default to their loader input name"


def test_bad_references() -> None:
    """
    Input and output loaders take in inputs that must be defined elsewhere in the manifest.
    The model has logic to ensure these references are valid. This tests for that logic as well
    as the logic that returns appropriate error messages for every invalid reference.
    """
    path = os.path.join(os.path.dirname(__file__), "test_manifests/bad_references.yaml")
    with pytest.raises(ValidationError) as e, open(path) as f:
        Manifest.from_yaml(f)
    errors = e.value.errors()
    messages = [error["msg"] for error in errors]
    # we want outputs in the order they appear
    assert messages == [
        "Value error, Invalid reference at input_loaders.kindness.ranking:score (not found)",
        "Value error, Invalid reference at output_loaders.sequencing_read.bleep:bleep (not found)",
    ]


def test_bad_options() -> None:
    """
    Tests some of the validation for our options property for raw inputs
    """
    path = os.path.join(os.path.dirname(__file__), "test_manifests/bad_options.yaml")
    with pytest.raises(ValidationError) as e, open(path) as f:
        Manifest.from_yaml(f)
    errors = e.value.errors()
    messages = [error["msg"] for error in errors]
    assert messages == [
        "Value error, Default value for 'Mood': overjoyed is not in options: ['happy', 'neutral', 'sad']",
        "Value error, Invalid option type for 1 (int)",
        "Value error, Invalid option type for False (bool)",
    ]


def test_malformed() -> None:
    """
    Some of our custom logic operates before the model is validated. This test ensures we still
    get sensible errors if these values are malformed.
    """
    path = os.path.join(os.path.dirname(__file__), "test_manifests/malformed.yaml")
    with pytest.raises(ValidationError) as e, open(path) as f:
        Manifest.from_yaml(f)
    errors = e.value.errors()
    messages = [error["msg"] for error in errors]
    assert messages == [
        "Value error, Default value for 'Mood': 1 is not of type str",
        "Input should be a valid dictionary",
        "Input should be a valid dictionary",
    ]


def test_duplicate_inputs() -> None:
    """
    Input names must be unique between entity_inputs and raw_inputs. Ensure issues
    with this are caught.
    """
    path = os.path.join(os.path.dirname(__file__), "test_manifests/duplicate_inputs.yaml")
    with pytest.raises(ValidationError) as e, open(path) as f:
        Manifest.from_yaml(f)
    errors = e.value.errors()
    messages = [error["msg"] for error in errors]
    assert messages == ["Value error, Raw input names duplicate entity input names: ['sample']"]


def test_validate_input() -> None:
    """
    Tests the validation logic entity and raw inputs
    """
    path = os.path.join(os.path.dirname(__file__), "test_manifests/valid.yaml")
    with open(path) as f:
        manifest = Manifest.from_yaml(f)

    entity_inputs: dict[str, EntityInput | list[EntityInput]] = {
        # Entity input with the wrong type
        "sample": EntityInput(entity_type="sequencing_read", entity_id="123"),
        # Entity input that isn't expected
        "missing": EntityInput(entity_type="sample", entity_id="123"),
    }

    raw_inputs = {
        # Raw input with a value not in options
        "mood": "exstatic",
        # Raw input with incorrect type
        "ranking": 1.2,
    }

    errors = [error.message() for error in manifest.validate_inputs(entity_inputs, raw_inputs)]
    assert errors == [
        "Invalid type for entity input: Sample (expected sample, got sequencing_read)",
        "Entity input not found: missing",
        "Missing required Entity input: sequencing_read",
        "Invalid value for raw input: Mood (input not in options)",
        "Invalid type for raw input: Ranking (expected int, got float)",
    ]


def test_normalize_inputs() -> None:
    """
    Tests that validation works the same when providing inputs as a list
    """
    path = os.path.join(os.path.dirname(__file__), "test_manifests/valid_multivalue.yaml")
    with open(path) as f:
        manifest = Manifest.from_yaml(f)

    dict_entity_inputs: dict[str, EntityInput | list[EntityInput]] = {
        # Entity input with the wrong type
        "sample": [
            EntityInput(entity_type="sample", entity_id="123"),
            EntityInput(entity_type="sample", entity_id="124"),
        ],
        # Entity input that isn't expected
        "sequencing_reads": [
            EntityInput(entity_type="sequencing_read", entity_id="123"),
            EntityInput(entity_type="sequencing_read", entity_id="124"),
        ],
    }

    list_entity_inputs = Manifest.normalize_inputs(
        [
            ("sample", EntityInput(entity_type="sample", entity_id="123")),
            ("sample", EntityInput(entity_type="sample", entity_id="124")),
            ("sequencing_reads", EntityInput(entity_type="sequencing_read", entity_id="123")),
            ("sequencing_reads", EntityInput(entity_type="sequencing_read", entity_id="124")),
        ]
    )

    dict_errors = [error.message() for error in manifest.validate_inputs(dict_entity_inputs, {})]
    list_errors = [error.message() for error in manifest.validate_inputs(list_entity_inputs, {})]
    assert dict_errors == list_errors


def test_multivalued() -> None:
    """
    Tests the validation logic for multivalue inputs
    """
    path = os.path.join(os.path.dirname(__file__), "test_manifests/valid_multivalue.yaml")
    with open(path) as f:
        manifest = Manifest.from_yaml(f)

    entity_inputs: dict[str, EntityInput | list[EntityInput]] = {
        # Entity input with the wrong type
        "sample": [
            EntityInput(entity_type="sample", entity_id="123"),
            EntityInput(entity_type="sample", entity_id="124"),
        ],
        # Entity input that isn't expected
        "sequencing_reads": [
            EntityInput(entity_type="sequencing_read", entity_id="123"),
            EntityInput(entity_type="sequencing_read", entity_id="124"),
        ],
    }

    errors = [error.message() for error in manifest.validate_inputs(entity_inputs, {})]
    assert errors == [
        "Invalid value for entity input: Sample (expected single input but recieved a list)",
    ]
