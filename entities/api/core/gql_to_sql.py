from typing import Optional, Generic
import uuid
from typing import TypeVar
from typing_extensions import TypedDict
import strawberry

T = TypeVar("T")

operator_map = {
    "_eq": "__eq__",
    "_neq": "__ne__",
    "_in_": "in_",
    "_nin": "not_in",
    "_is_null": "SPECIAL",
    "_gt": "__gt__",
    "_gte": "__ge__",
    "_lt": "__lt__",
    "_lte": "__le__",
    "_like": "like",
    "_nlike": "notlike",
    "_ilike": "ilike",
    "_nilike": "notilike",
    "_regex": "regexp_match",
    # "_nregex": Optional[str] # TODO
    # "_iregex": Optional[str]# TODO
    # "_niregex": Optional[str]# TODO
}


def convert_where_clauses_to_sql(query, sa_model, whereClause):
    for k, v in whereClause.items():
        for comparator, value in v.items():
            sa_comparator = operator_map[comparator]
            if sa_comparator == "SPECIAL":
                query = query.filter(getattr(sa_model, k).is_(None))
            else:
                query = query.filter(getattr(getattr(sa_model, k), sa_comparator)(value))
    return query


@strawberry.input()
class EnumComparators(TypedDict, Generic[T]):
    _eq: Optional[T]
    _neq: Optional[T]
    _in: Optional[list[T]]
    _nin: Optional[list[T]]
    _gt: Optional[T]
    _gte: Optional[T]
    _lt: Optional[T]
    _lte: Optional[T]
    _is_null: Optional[T]


@strawberry.input
class BoolComparators(TypedDict):
    _eq: Optional[int]
    _neq: Optional[int]
    _in: Optional[list[int]]
    _nin: Optional[list[int]]
    _gt: Optional[int]
    _gte: Optional[int]
    _lt: Optional[int]
    _lte: Optional[int]
    _is_null: Optional[int]


@strawberry.input
class IntComparators(TypedDict):
    _eq: Optional[int]
    _neq: Optional[int]
    _in: Optional[list[int]]
    _nin: Optional[list[int]]
    _gt: Optional[int]
    _gte: Optional[int]
    _lt: Optional[int]
    _lte: Optional[int]
    _is_null: Optional[int]


@strawberry.input
class UUIDComparators(TypedDict):
    _eq: Optional[uuid.UUID]
    _neq: Optional[uuid.UUID]
    _in: Optional[list[uuid.UUID]]
    _nin: Optional[list[uuid.UUID]]
    _gt: Optional[uuid.UUID]
    _gte: Optional[uuid.UUID]
    _lt: Optional[uuid.UUID]
    _lte: Optional[uuid.UUID]


@strawberry.input
class StrComparators(TypedDict):
    _eq: Optional[str]
    _neq: Optional[str]
    _in: Optional[list[str]]
    _nin: Optional[list[str]]
    _is_null: Optional[int]
    _gt: Optional[str]
    _gte: Optional[str]
    _lt: Optional[str]
    _lte: Optional[str]
    _like: Optional[str]
    _nlike: Optional[str]
    _ilike: Optional[str]
    _nilike: Optional[str]
    _regex: Optional[str]
    _nregex: Optional[str]
    _iregex: Optional[str]
    _niregex: Optional[str]
