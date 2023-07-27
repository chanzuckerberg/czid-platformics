import os
from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, AsyncEngine, async_sessionmaker)
from sqlalchemy.engine import create_engine, Engine
from sqlalchemy.orm import Session, sessionmaker
from typing import Union, Optional


class AsyncDB():
    def __init__(self, engine: AsyncEngine):
        self._engine = engine
        self._session_maker: Optional[async_sessionmaker[AsyncSession]] = None
    
    @property
    def engine(self) -> Union[Engine, AsyncEngine]:
        return self._engine

    @property
    def session(self) -> async_sessionmaker[AsyncSession]:
        if not self._session_maker:
            session = async_sessionmaker(
                self._engine, expire_on_commit=False
            )
            self._session_maker = session
        return self._session_maker

    def make_session(self) -> AsyncSession:
        session = self.session
        return session()


class SyncDB():
    def __init__(self, engine: Engine):
        self._engine = engine
        self._session_maker: Optional[sessionmaker[Session]] = None
    
    @property
    def engine(self) -> Engine:
        return self._engine

    @property
    def session(self) -> sessionmaker[Session]:
        if not self._session_maker:
            session = sessionmaker(bind=self._engine, expire_on_commit=False)
            self._session_maker = session
        return self._session_maker

    def make_session(self) -> Session:
        session = self.session
        return session()

def get_db_uri(protocol: str="postgresql", db_host: str=None, db_port: int=None, db_user: str=None, db_pass: str=None, db_name: str=None) -> str:
    db_uri = "{protocol}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}".format(
        protocol=protocol,
        db_host=db_host or os.getenv("DB_HOST"),
        db_port=db_port or os.getenv("DB_PORT"),
        db_user=db_user or os.getenv("DB_USER"),
        db_pass=db_pass or os.getenv("DB_PASS"),
        db_name=db_name or os.getenv("DB_NAME"),
    )
    return db_uri

def init_async_db(db_uri: Optional[str] = None, **kwargs) -> AsyncDB:
    if not db_uri:
        db_uri = get_db_uri("postgresql+asyncpg")
    engine = create_async_engine(
        db_uri, echo=False, pool_size=5, max_overflow=5, future=True, **kwargs
    )
    return AsyncDB(engine)


def init_sync_db(db_uri: Optional[str] = None) -> SyncDB:
    if not db_uri:
        db_uri = get_db_uri("postgresql")
    engine = create_engine(db_uri)
    return SyncDB(engine)