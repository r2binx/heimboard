from typing import Optional
import jwt
from fastapi.security import HTTPBearer
from starlette.requests import Request
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_403_FORBIDDEN


class JWTValidator():
    def __init__(self, config):
        jwks_url = f'{config["URL"]}.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)
        self.config = config

    def verify(self, permission: str = None, query: bool = False):
        token_extractor = HTTPBearer()

        async def jwt_extractor(request: Request = None, token: Optional[str] = None):
            if not query:
                token = (await token_extractor(request)).credentials
            try:
                self.signing_key = self.jwks_client.get_signing_key_from_jwt(
                    token
                ).key
            except jwt.exceptions.PyJWKClientError as error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail=error.__str__()
                )
            except jwt.exceptions.DecodeError as error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail=error.__str__()
                )
            try:
                payload = jwt.decode(
                    token,
                    self.signing_key,
                    algorithms=["RS256", "ES256"],
                    audience=self.config["API_AUDIENCE"],
                    issuer=self.config["URL"],
                )
                if permission and not permission in payload["permissions"]:
                    raise HTTPException(
                        status_code=HTTP_403_FORBIDDEN,
                        detail="Invalid role",
                    )
                return payload
            except Exception as e:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail=str(e)
                )

        return jwt_extractor
