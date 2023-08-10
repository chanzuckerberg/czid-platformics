from functools import cached_property

from jwcrypto import jwk
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Pydantic Settings object - do not instantiate it directly, please use get_settings() as a dependency where possible"""

    SERVICE_NAME: str = "Platformics Entities"

    # Hardcoded vars"
    DB_DRIVER: str = "postgresql+asyncpg"
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 0
    DB_ECHO: bool = False
    DEBUG: bool = False

    # Pydantic automatically tries to load settings with matching names from the environment if available.
    # It also supports creating more methods of fetching secrets (ex: secrets manager, disk, etc) but we
    # don't need that just yet.

    # Properties usually read from env vars
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    JWK_PUBLIC_KEY_FILE: str
    JWK_PRIVATE_KEY_FILE: str

    ####################################################################################
    # Computed properties

    @cached_property
    def JWK_PRIVATE_KEY(self) -> jwk.JWK:
        key = None
        with open(self.JWK_PRIVATE_KEY_FILE) as fh:
            key = fh.read().strip()
        private_key = jwk.JWK.from_pem(key.encode("utf-8"))
        return private_key

    @cached_property
    def JWK_PUBLIC_KEY(self) -> jwk.JWK:
        key = None
        with open(self.JWK_PUBLIC_KEY_FILE) as fh:
            key = fh.read().strip()
        public_key = jwk.JWK.from_pem(key.encode("utf-8"))
        return public_key

    @cached_property
    def DB_URI(self) -> str:
        db_uri = (
            "{protocol}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}".format(
                protocol=self.DB_DRIVER,
                db_host=self.DB_HOST,
                db_port=self.DB_PORT,
                db_user=self.DB_USER,
                db_pass=self.DB_PASS,
                db_name=self.DB_NAME,
            )
        )
        return db_uri

    @cached_property
    def SYNC_DB_URI(self) -> str:
        db_uri = "postgresql+psycopg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}".format(
            db_host=self.DB_HOST,
            db_port=self.DB_PORT,
            db_user=self.DB_USER,
            db_pass=self.DB_PASS,
            db_name=self.DB_NAME,
        )
        return db_uri


class APISettings(Settings):
    ...


class CLISettings(Settings):
    ...
