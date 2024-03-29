from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .jwt_token import decodeJWT


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials | None = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            print(jwtoken, " :JWT token parsed fro verification")
            payload = decodeJWT(jwtoken)
            print(payload, " try: Payload in verify_jwt")
        except:
            payload = None
            print(payload, " exception: Payload in verify_jwt")
        if payload:
            isTokenValid = True
        return isTokenValid

    def get_username(self, jwtoken: str) -> str:
        try:
            payload = decodeJWT(jwtoken)
            print(payload, " try: Payload called in get_username")
            return payload["sub"]
        except:
            raise HTTPException(status_code=403, detail="Invalid token or expired token.")


# https://testdriven.io/blog/fastapi-jwt-auth/#securing-routes
# https://www.freecodecamp.org/news/how-to-add-jwt-authentication-in-fastapi/
