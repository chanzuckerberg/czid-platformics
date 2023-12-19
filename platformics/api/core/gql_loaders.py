import typing
from collections import defaultdict
from typing import Any, Mapping, Optional, Tuple, Sequence
import database.models as db
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal
from platformics.database.connect import AsyncDB
from sqlalchemy.orm import RelationshipProperty
from strawberry.dataloader import DataLoader
from platformics.security.authorization import CerbosAction
from api.core.helpers import get_db_query, get_db_rows

E = typing.TypeVar("E", db.File, db.Entity)  # type: ignore
T = typing.TypeVar("T")


class Hashabledict(dict):
    def __hash__(self):  # type: ignore
        return hash(tuple(sorted(self.items())))


def make_hashable(somedict: dict) -> Hashabledict:
    res = {}
    for k, v in somedict.items():
        if type(v) == dict:
            v = hash(make_hashable(v))
        # NOTE - we're explicitly not supporting dicts inside lists since
        # our current where clause interface doesn't call for it.
        if type(v) == list:
            v = hash(frozenset(v))
        res[k] = v
    return Hashabledict(res)


class EntityLoader:
    """
    Creates DataLoader instances on-the-fly for SQLAlchemy relationships
    """

    _loaders: dict[RelationshipProperty, DataLoader]

    def __init__(self, engine: AsyncDB, cerbos_client: CerbosClient, principal: Principal) -> None:
        self._loaders = {}
        self.engine = engine
        self.cerbos_client = cerbos_client
        self.principal = principal

    async def resolve_nodes(self, cls: Any, node_ids: list[str]) -> Sequence[E]:
        """
        Given a list of node IDs from a Relay `node()` query, return corresponding entities
        """
        db_session = self.engine.session()
        where = {"entity_id": {"_in": node_ids}}
        rows = await get_db_rows(cls, db_session, self.cerbos_client, self.principal, where)
        await db_session.close()
        return rows

    def loader_for(self, relationship: RelationshipProperty, where: Optional[Any] = None) -> DataLoader:
        """
        Retrieve or create a DataLoader for the given relationship
        """
        if not where:
            where = {}
        where_str = make_hashable(where)
        try:
            return self._loaders[(relationship, where_str)]  # type: ignore
        except KeyError:
            related_model = relationship.entity.entity

            async def load_fn(keys: list[Any]) -> typing.Sequence[Any]:
                if not relationship.local_remote_pairs:
                    raise Exception("invalid relationship")
                filters = []
                for _, remote in relationship.local_remote_pairs:
                    filters.append(remote.in_(keys))
                order_by: list = []
                if relationship.order_by:
                    order_by = [relationship.order_by]
                query = get_db_query(
                    related_model, CerbosAction.VIEW, self.cerbos_client, self.principal, where  # type: ignore
                )
                for item in filters:
                    query = query.where(item)
                for item in order_by:
                    query = query.order_by(item)
                db_session = self.engine.session()
                rows = (await db_session.execute(query)).scalars().all()
                await db_session.close()

                def group_by_remote_key(row: Any) -> Tuple:
                    if not relationship.local_remote_pairs:
                        raise Exception("invalid relationship")
                    # TODO -- Technically, SA supports multiple field filters in a relationship! We'll need to handle this case
                    return [getattr(row, remote.key) for _, remote in relationship.local_remote_pairs if remote.key][0]

                grouped_keys: Mapping[Any, list[Any]] = defaultdict(list)
                for row in rows:
                    grouped_keys[group_by_remote_key(row)].append(row)
                if relationship.uselist:
                    return [grouped_keys[key] for key in keys]
                else:
                    return [grouped_keys[key][0] if grouped_keys[key] else None for key in keys]

            self._loaders[(relationship, where_str)] = DataLoader(load_fn=load_fn)  # type: ignore
            return self._loaders[(relationship, where_str)]  # type: ignore
