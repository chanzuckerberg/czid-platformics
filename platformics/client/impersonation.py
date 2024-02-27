import os
from platformics.settings import Settings
from platformics.security.token_auth import create_token

import httpx

IDENTITY_SERVICE_URL = os.environ["IDENTITY_SERVICE_BASE_URL"]
SECRET_NAME = os.environ["SERVICE_IDENTITY_SECRET_NAME"]

class ImpersonationClient:
    def __init__(self) -> None:
        settings = Settings.model_validate({})
        private_key = settings.JWK_PRIVATE_KEY
        self._token = create_token(private_key, None, None, 3600, "workflows")

    async def impersonate(self, user_id: int) -> str:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{IDENTITY_SERVICE_URL}/impersonate/?user_id={user_id}",
                headers={"Authorization": f"Bearer {self._token}"},
            )
            return resp.json()["token"]

