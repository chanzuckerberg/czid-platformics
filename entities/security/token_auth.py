import json
from jwcrypto.jwk import JWK
from jwcrypto import jwe, jwt
import time
from typing import TypedDict


class ProjectRole(TypedDict):
    project_id: int
    roles: list[str]


def get_token_claims(private_key: JWK, token: str) -> dict:
    unpacked_token = jwe.JWE()
    unpacked_token.deserialize(token)
    unpacked_token.decrypt(private_key)
    decrypted_payload = unpacked_token.payload.decode("utf-8")
    required_claims = {"exp": None, "iat": None, "nbf": None}
    decoded_jwt = jwt.JWT(
        key=private_key, jwt=decrypted_payload, check_claims=required_claims
    )
    return json.loads(decoded_jwt.claims)


# TODO - this isn't going to be part of the entities service over the long term,
# it's just in our app for now to help us test the auth flow.
def create_token(
    private_key: JWK, userid: int, project_claims: list[ProjectRole]
) -> str:
    # Create a JWT that's signed by our private key. This proves *who wrote the message*
    jwt_payload = {
        "sub": str(userid),
        "iat": int(time.time()),
        "nbf": int(time.time()),
        "exp": int(time.time()) + 3600,  # 1 hour from now
        "iss": "https://api.example.com",
        "projects": project_claims,
    }
    jwt_headers = {
        "alg": "ES384",
        "typ": "JWT",
        "kid": private_key.thumbprint(),
    }
    jwt_token = jwt.JWT(header=jwt_headers, claims=jwt_payload)
    jwt_token.make_signed_token(private_key)
    jwe_payload = jwt_token.serialize(compact=True)

    # Ok, now we want to *encrypt* that jwt with a JWE wrapper so that only the intended recipient can read it.
    protected_header = {
        "alg": "ECDH-ES",
        "enc": "A256CBC-HS512",
        "typ": "JWE",
        "kid": private_key.thumbprint(),
    }
    jwe_token = jwe.JWE(jwe_payload, recipient=private_key, protected=protected_header)
    return jwe_token.serialize(compact=True)
