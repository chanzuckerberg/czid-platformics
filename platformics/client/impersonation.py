import os
import logging
from platformics.settings import Settings
from platformics.security.token_auth import create_token

import httpx

IDENTITY_SERVICE_URL = os.environ["IDENTITY_SERVICE_BASE_URL"]

class ImpersonationClient:
    def __init__(self) -> None:
        settings = Settings.model_validate({})
        private_key = settings.JWK_PRIVATE_KEY
        self._token = create_token(private_key, None, None, 3600, "workflows")

    async def impersonate(self, user_id: int) -> str:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            logger = logging.getLogger()
            resp = await client.get(
                f"{IDENTITY_SERVICE_URL}/impersonate/?user_id={user_id}",
                headers={"Authorization": f"Bearer {self._token}"},
            )
            try:
                return resp.json()["token"]
            except Exception as e:
                logger.error(f"Unexpected response from identity endpoint: {resp.text}")
                raise e
