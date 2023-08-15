from collections import defaultdict
from typing import Any, Dict, List, Mapping, Tuple

from sqlalchemy import tuple_
from sqlalchemy.orm import RelationshipProperty
from strawberry.dataloader import DataLoader
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, ResourceDesc
from thirdparty.cerbos_sqlalchemy.query import get_query


class EntityLoader:
    """
    Creates DataLoader instances on-the-fly for SQLAlchemy relationships
    """

    _loaders: Dict[RelationshipProperty, DataLoader]

    def __init__(
        self, engine, cerbos_client: CerbosClient, principal: Principal
    ) -> None:
        self._loaders = {}
        self.engine = engine
        self.cerbos_client = cerbos_client
        self.principal = principal

    def loader_for(self, relationship: RelationshipProperty) -> DataLoader:
        """
        Retrieve or create a DataLoader for the given relationship
        """
        try:
            return self._loaders[relationship]
        except KeyError:
            related_model = relationship.entity.entity

            async def load_fn(keys: List[Tuple]) -> List[Any]:
                rd = ResourceDesc(related_model.__tablename__)
                plan = self.cerbos_client.plan_resources("view", self.principal, rd)

                query = get_query(
                    plan,
                    related_model,
                    {
                        "request.resource.attr.owner_user_id": related_model.owner_user_id,
                        "request.resource.attr.collection_id": related_model.collection_id,
                    },
                    [],
                )
                query = query.filter(
                    tuple_(
                        *[remote for _, remote in relationship.local_remote_pairs]
                    ).in_(keys)
                )
                async with self.engine.session() as session:
                    if relationship.order_by:
                        query = query.order_by(*relationship.order_by)
                    rows = (await session.execute(query)).scalars().all()

                    def group_by_remote_key(row: Any) -> Tuple:
                        return tuple(
                            [
                                getattr(row, remote.key)
                                for _, remote in relationship.local_remote_pairs
                            ]
                        )

                    grouped_keys: Mapping[Tuple, List[Any]] = defaultdict(list)
                    for row in rows:
                        grouped_keys[group_by_remote_key(row)].append(row)
                if relationship.uselist:
                    return [grouped_keys[key] for key in keys]
                else:
                    return [
                        grouped_keys[key][0] if grouped_keys[key] else None
                        for key in keys
                    ]

            self._loaders[relationship] = DataLoader(load_fn=load_fn)
            return self._loaders[relationship]
