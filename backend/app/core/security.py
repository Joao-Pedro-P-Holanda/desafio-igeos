from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, SecurityScopes
from fastapi import Depends
import jwt
from .config import config
from ..exceptions.auth import UnauthenticatedException

# source: https://auth0.com/blog/build-and-secure-fastapi-server-with-auth0/

token_auth_scheme = HTTPBearer()

jwks_url = f"https://{config.AUTH0_DOMAIN}/.well-known/jwks.json"
# Validating web keys over Auth0's key set
jwks_client = jwt.PyJWKClient(jwks_url)


def validate_token(
    security_scopes: SecurityScopes,
    token: HTTPAuthorizationCredentials | None = Depends(token_auth_scheme),
):
    if not token:
        raise UnauthenticatedException("Authorization header not found")

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token.credentials).key
    except (jwt.exceptions.PyJWKClientError, jwt.exceptions.DecodeError) as error:
        raise UnauthenticatedException(str(error))

    try:
        payload = jwt.decode(
            token.credentials,
            signing_key,
            algorithms=config.AUTH0_ALGORITHM,
            audience=config.AUTH0_AUDIENCE,
            issuer=config.AUTH0_ISSUER,
        )
        return payload
    except Exception as error:
        raise UnauthenticatedException(str(error))
