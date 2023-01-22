from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .jwt_token import decodeJWT


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials | None = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            if not self.verify_jwt(credentials.credentials):
                print(credentials.credentials + " :Credentials in JWTBearer Class")
                print(self.verify_jwt(credentials.credentials), "Verification")
                # print(
                #     self.get_current_active_user(credentials.credentials),
                #     "Getting username",
                # )
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
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

    # to get the id username of active user
    # def get_current_active_user(self, jwtoken: str):
    #     try:
    #         print(jwtoken, " :JWT token parsed fro verification")
    #         payload = decodeJWT(jwtoken)
    #     except:
    #         raise HTTPException(status_code=400, detail="User in active.")
    #     if payload:
    #         return payload["sub"]
