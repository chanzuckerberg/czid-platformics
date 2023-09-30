import types
import typing
import uuid
from typing import Any, Awaitable, Callable, Generic, Optional, TypeVar, cast

import strawberry
from platformics.thirdparty.strawberry_sqlalchemy_mapper import (
    SSAPlugin, StrawberrySQLAlchemyMapper)
from platformics.thirdparty.strawberry_sqlalchemy_mapper.mapper import \
    _IS_GENERATED_RESOLVER_KEY
from sqlalchemy import inspect
from sqlalchemy.orm import Mapper, RelationshipProperty
from sqlalchemy.orm.state import InstanceState
from strawberry import input
from strawberry.annotation import StrawberryAnnotation
from strawberry.arguments import StrawberryArgument
from strawberry.field import StrawberryField
from strawberry.types import Info
from typing_extensions import TypedDict

T = TypeVar("T")


operator_map = {
    "_eq": "__eq__",
    "_neq": "__ne__",
    "_in_": "in_",
    "_nin": "not_in",
    "_is_null": "IS_NULL",
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
            if sa_comparator == "IS_NULL":
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


class FancySQLAlchemyMapper(StrawberrySQLAlchemyMapper):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    def make_connection_wrapper_resolver(
        self, resolver: Callable[..., Awaitable[Any]], type_name: str
    ) -> Callable[..., Awaitable[Any]]:
        """
        Wrap a resolver that returns an array of model types to return
        a Connection instead.
        """
        connection_type = self._connection_type_for(type_name)
        edge_type = self._edge_type_for(type_name)
        try:
            print(f"got live where clause type {type_name}")
            where_clause = self.where_clause_builder._cached_where_args[type_name]
        except KeyError:
            print(f"bbb where key error sadface {type_name}")
            where_clause = str

        async def wrapper(self, info: Info, where: Optional[str] = strawberry.UNSET):
            return connection_type(
                edges=[
                    edge_type(
                        node=related_object,
                    )
                    for related_object in await resolver(self, info, where)
                ]
            )

        setattr(wrapper, _IS_GENERATED_RESOLVER_KEY, True)

        return wrapper

    def relationship_resolver_for(self, relationship: RelationshipProperty) -> Callable[..., Awaitable[Any]]:
        """
        Return an async field resolver for the given relationship,
        so as to avoid n+1 query problem.
        """
        type_name = (self.model_to_type_or_interface_name(relationship.entity.entity),)
        where_clause = str

        async def resolve(self, info: Info, where: Optional[str] = strawberry.UNSET):
            print(f"WHERE DATA IS {where}")
            instance_state = cast(InstanceState, inspect(self))
            if relationship.key not in instance_state.unloaded:
                related_objects = getattr(self, relationship.key)
            else:
                relationship_key = tuple([getattr(self, local.key) for local, _ in relationship.local_remote_pairs])
                if any(item is None for item in relationship_key):
                    if relationship.uselist:
                        return []
                    else:
                        return None
                if isinstance(info.context, dict):
                    loader = info.context["sqlalchemy_loader"]
                else:
                    loader = info.context.sqlalchemy_loader
                related_objects = await loader.loader_for(relationship, where).load(relationship_key)
            return related_objects

        setattr(resolve, _IS_GENERATED_RESOLVER_KEY, True)

        return resolve


class WhereClauseBuilder(SSAPlugin):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self._cached_where_args: dict[str, Any] = {}
        self._todo_where_args: list[Any] = []

    def build_where_argument(
        self, strawberry_sqlalchemy_mapper: StrawberrySQLAlchemyMapper, sa_mapper: Mapper, mapped_type: Any
    ):
        try:
            return self._cached_where_args[mapped_type.__name__]
        except KeyError:
            pass
        where_type = types.new_class(f"{mapped_type.__name__}WhereFilter", (TypedDict,), {})
        for item in sa_mapper.columns:
            # Generate new where clause thingie
            key = item.key
            setattr(where_type, key, None)
            where_type.__annotations__[key] = Optional[StrComparators]
        self._cached_where_args[mapped_type.__name__] = input(where_type)
        return self._cached_where_args[mapped_type.__name__]

    def on_type_definition(
        self, strawberry_sqlalchemy_mapper: StrawberrySQLAlchemyMapper, sa_mapper: Mapper, mapped_type: T
    ) -> T:
        self.build_where_argument(strawberry_sqlalchemy_mapper, sa_mapper, mapped_type)
        return mapped_type

    def mutate_connection_type(
        self,
        strawberry_sqlalchemy_mapper: StrawberrySQLAlchemyMapper,
        strawberry_type,
        field: StrawberryField,
        relationship: RelationshipProperty,
    ) -> None:
        relationship_model = relationship.entity.entity
        type_name = strawberry_sqlalchemy_mapper.model_to_type_or_interface_name(relationship_model)
        try:
            whereclause = None
            try:
                whereclause = strawberry_type._where_clause_
            except:
                pass
            if not whereclause:
                whereclause = self._cached_where_args[type_name]
            field.arguments.append(
                StrawberryArgument("where", "where", StrawberryAnnotation(Optional[whereclause]), None)
            )
        except KeyError:
            self._todo_where_args.append((type_name, field))

    def finalize(self, strawberry_sqlalchemy_mapper: StrawberrySQLAlchemyMapper):
        for type_name, field in self._todo_where_args:
            whereclause = self._cached_where_args[type_name]
            field.arguments.append(
                StrawberryArgument("where", "where", StrawberryAnnotation(Optional[whereclause]), None)
            )


# TODO this initialize-on-import is gross but we can refactor it later :'(
where_clause_builder = WhereClauseBuilder()
strawberry_sqlalchemy_mapper: FancySQLAlchemyMapper = FancySQLAlchemyMapper(global_plugins=[where_clause_builder])
strawberry_sqlalchemy_mapper.where_clause_builder = where_clause_builder
