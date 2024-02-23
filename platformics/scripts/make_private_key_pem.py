import boto3
import sys
import os
from botocore.exceptions import ClientError


PRIVATE_KEY_PATH = os.environ.get("JWK_PRIVATE_KEY_FILE", "/tmp/private_key.pem")
ENVIRONMENTS = ["dev", "sandbox", "staging", "prod"]


def fetch_private_key(environment: str) -> None:
    if os.path.isfile(PRIVATE_KEY_PATH):
        return
    if environment not in ENVIRONMENTS:
        raise ValueError(f"Private key argument {environment} is not one of {str(ENVIRONMENTS)}")

    secret_name = f"{environment}/czid-services-private-key"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name="us-west-2")

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e

    # Decrypts secret using the associated KMS key and stores the private key in a pem file.
    secret = get_secret_value_response["SecretString"]
    if secret:
        with open(PRIVATE_KEY_PATH, "w") as f:
            f.write(secret)


if __name__ == "__main__":
    environment = sys.argv[1]
    fetch_private_key(environment)
