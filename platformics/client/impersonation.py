import os

import boto3
import httpx

IDENTITY_SERVICE_URL = os.environ["IDENTITY_SERVICE_BASE_URL"]
SECRET_NAME = os.environ["SERVICE_IDENTITY_SECRET_NAME"]

class ImpersonationClient:
    def __init__(self) -> None:
        client = boto3.client(service_name="secretsmanager", endpoint_url=os.getenv("BOTO_ENDPOINT_URL"))
        get_secret_value_response = client.get_secret_value(SecretId=SECRET_NAME)

        # Decrypts secret using the associated KMS key and stores the private key in a pem file.
        self._token = get_secret_value_response["SecretString"]

    async def impersonate(self, user_id: int) -> str:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{IDENTITY_SERVICE_URL}/impersonate/?user_id={user_id}",
                headers={"Authorization": f"Bearer {self._token}"},
            )
            return resp.json()["token"]

