import typing
import uuid
from typing import TypeVar
from typing_extensions import TypedDict
import strawberry

T = TypeVar("T")

@strawberry.input
class EnumComparators(TypedDict, typing.Generic[T]):
    _eq: T
    _neq: T
    _in_: list[T]
    _nin: list[T]
    _gt: T
    _gte: T
    _lt: T
    _lte: T
    _is_null: T

@strawberry.input
class BoolComparators(TypedDict):
    _eq: int
    _neq: int
    _in_: list[int]
    _nin: list[int]
    _gt: int
    _gte: int
    _lt: int
    _lte: int
    _is_null: int

@strawberry.input
class IntComparators(TypedDict):
    _eq: int
    _neq: int
    _in_: list[int]
    _nin: list[int]
    _gt: int
    _gte: int
    _lt: int
    _lte: int
    _is_null: int

@strawberry.input
class UUIDComparators(TypedDict):
    _eq: uuid.UUID
    _neq: uuid.UUID
    _in_: list[uuid.UUID]
    _nin: list[uuid.UUID]
    _gt: uuid.UUID
    _gte: uuid.UUID
    _lt: uuid.UUID
    _lte: uuid.UUID

@strawberry.input
class StrComparators(TypedDict):
    _eq: str
    _neq: str
    _in_: list[str]
    _nin: list[str]
    _is_null: int
    _gt: str
    _gte: str
    _lt: str
    _lte: str
    _like: str
    _nlike: str
    _ilike: str
    _nilike: str
    _regex: str
    _nregex: str
    _iregex: str
    _niregex: str