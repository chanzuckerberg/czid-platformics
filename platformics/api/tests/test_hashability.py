"""
Basic tests to check that we can hash where-clause dicts reliably
"""

from platformics.api.core.gql_loaders import make_hashable


def test_hash_consistency() -> None:
    where_1 = {
        "description": {"key1": "kaboom", "_ilike": {"not": {"nested": "%b%"}}},
        "list_thing": ["10", "11", "12"],
    }
    where_2 = {
        "description": {"_ilike": {"not": {"nested": "%b%"}}, "key1": "kaboom"},
        "list_thing": ["10", "11", "12"],
    }
    assert hash(make_hashable(where_1)) == hash(make_hashable(where_2))


def test_hash_inconsistency() -> None:
    where_1 = {
        "description": {"key1": "kaboom", "_ilike": {"not": {"nested": "%c%"}}},
        "list_thing": ["10", "11", "12"],
    }
    where_2 = {
        "description": {"_ilike": {"not": {"nested": "%b%"}}, "key1": "kaboom"},
        "list_thing": ["10", "11", "12"],
    }
    assert hash(make_hashable(where_1)) != hash(make_hashable(where_2))
