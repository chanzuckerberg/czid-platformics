import json
import time
import logging
import click

from jwcrypto import jwe, jwk, jwt
from jwcrypto.common import json_decode
from api.core.settings import CLISettings


@click.group()
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Enable debug output",
)
@click.pass_context
def cli(ctx, debug):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    if debug:
        logger.setLevel(logging.DEBUG)
    ctx.ensure_object(dict)
    ctx.obj["settings"] = CLISettings()


@cli.group()
def keypair():
    pass


@keypair.command("create")
@click.pass_context
def keypair_create(ctx):
    public_key = jwk.JWK()
    private_key = jwk.JWK.generate(kty="EC", crv="P-384")
    public_key.import_key(**json_decode(private_key.export_public()))
    print(public_key.export_to_pem().decode("utf-8"))
    print(private_key.export_to_pem(private_key=True, password=None).decode("utf-8"))


@cli.group()
def authtoken():
    pass


@authtoken.command("create")
@click.option("--userid", help="userid to encode in the token", default=123, type=int)
@click.option(
    "--projects",
    help="project_id:role associations to include in the header",
    type=list[str],
    default=["123:admin", "123:member", "456:member"],
    multiple=True,
)
@click.pass_context
def authtoken_create(ctx, userid: int, projects: list[str]):
    private_key = ctx.obj["settings"].JWK_PRIVATE_KEY

    # Create a JWT that's signed by our private key. This proves *who wrote the message*
    jwt_payload = {
        "iat": int(time.time()),
        "nbf": int(time.time()),
        "exp": int(time.time()) + 3600,  # 1 hour from now
        "iss": "https://api.example.com",
        "projects": {123: ["admin", "member"], 456: ["member"]},
    }
    jwt_headers = {
        "alg": "ES384",
        "typ": "JWT",
        "kid": private_key.thumbprint(),
    }
    jwt_token = jwt.JWT(header=jwt_headers, claims=jwt_payload)
    jwt_token.make_signed_token(private_key)
    jwe_payload = jwt_token.serialize(compact=True)

    print("JWT:")
    print(jwe_payload)

    # Ok, now we want to *encrypt* that jwt with a JWE wrapper so that only the intended recipient can read it.
    protected_header = {
        "alg": "ECDH-ES",
        "enc": "A256CBC-HS512",
        "typ": "JWE",
        "kid": private_key.thumbprint(),
    }
    jwe_token = jwe.JWE(jwe_payload, recipient=private_key, protected=protected_header)
    enc = jwe_token.serialize(compact=True)
    print("JWE Token:")
    print(enc)


@authtoken.command("decode")
@click.argument("jwe_token", required=True)
@click.pass_context
def authtoken_decode(ctx, jwe_token):
    private_key = ctx.obj["settings"].JWK_PRIVATE_KEY
    unpacked_token = jwe.JWE()
    unpacked_token.deserialize(jwe_token)
    unpacked_token.decrypt(private_key)
    decrypted_payload = unpacked_token.payload.decode("utf-8")
    print("===")
    print(decrypted_payload)
    required_claims = {"exp": None, "iat": None, "nbf": None}
    decoded_jwt = jwt.JWT(
        key=private_key, jwt=decrypted_payload, check_claims=required_claims
    )
    claims = json.loads(decoded_jwt.claims)
    print(claims)
    print(type(claims))


if __name__ == "__main__":
    cli()
