import typing

import boto3
from botocore.client import Config
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal
from fastapi import Depends
from mypy_boto3_s3.client import S3Client
from mypy_boto3_sts.client import STSClient
from platformics.database.connect import AsyncDB, init_async_db
from platformics.security.token_auth import get_token_claims
from platformics.settings import APISettings
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from platformics.api.core.errors import PlatformicsException


def get_settings(request: Request) -> APISettings:
    """Get the settings object from the app state"""
    return request.app.state.entities_settings


async def get_engine(
    settings: APISettings = Depends(get_settings),
) -> typing.AsyncGenerator[AsyncDB, None]:
    """Wrap resolvers in a DB engine"""
    engine = init_async_db(settings.DB_URI)
    try:
        yield engine
    finally:
        pass


async def get_db_session(
    engine: AsyncDB = Depends(get_engine),
) -> typing.AsyncGenerator[AsyncSession, None]:
    """Wrap resolvers in a sqlalchemy-compatible db session"""
    session = engine.session()
    try:
        yield session
    finally:
        await session.close()  # type: ignore


def get_cerbos_client(settings: APISettings = Depends(get_settings)) -> CerbosClient:
    return CerbosClient(host=settings.CERBOS_URL)


def get_auth_principal(request: Request, settings: APISettings = Depends(get_settings)) -> typing.Optional[Principal]:
    auth_header = request.headers.get("authorization")
    if auth_header:
        parts = auth_header.split()
    if not auth_header or len(parts) != 2:
        return None
    if parts[0].lower() != "bearer":
        return None

    try:
        claims = get_token_claims(settings.JWK_PRIVATE_KEY, parts[1])
    except:  # noqa
        return None

    if "project_roles" not in claims:
        raise PlatformicsException("Unauthorized")

    project_claims = claims["project_roles"]

    try:
        for role, project_ids in project_claims.items():
            assert role in ["member", "owner", "viewer"]
            assert isinstance(project_ids, list)
            for item in project_ids:
                assert int(item)
    except Exception:
        raise PlatformicsException("Unauthorized")

    return Principal(
        claims["sub"],
        roles=["user"],
        attr={
            "user_id": int(claims["sub"]),
            "owner_projects": project_claims.get("owner", []),
            "member_projects": project_claims.get("member", []),
            "viewer_projects": project_claims.get("viewer", []),
            "service_identity": claims["service_identity"],
        },
    )


def require_auth_principal(
    principal: typing.Optional[Principal] = Depends(get_auth_principal),
) -> Principal:
    if not principal:
        raise PlatformicsException("Unauthorized")
    return principal


def is_system_user(principal: Principal = Depends(require_auth_principal)) -> bool:
    if principal.attr.get("service_identity"):
        return True
    return False


def require_system_user(principal: Principal = Depends(require_auth_principal)) -> None:
    if principal.attr.get("service_identity"):
        return None
    raise PlatformicsException("Unauthorized")


def get_s3_client(
    settings: APISettings = Depends(get_settings),
) -> S3Client:
    return boto3.client(
        "s3",
        region_name=settings.AWS_REGION,
        endpoint_url=settings.BOTO_ENDPOINT_URL,
        config=Config(signature_version="s3v4"),
    )


def get_sts_client(
    settings: APISettings = Depends(get_settings),
) -> STSClient:
    return boto3.client("sts", region_name=settings.AWS_REGION, endpoint_url=settings.BOTO_ENDPOINT_URL)
