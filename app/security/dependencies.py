from fastapi import Depends, HTTPException, status
# from app.security.oauth import oauth2_scheme

from app.security.jwt_utils import decode_jwt
from app.pydantics.auth_pydantic import TokenPayload
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from app.security.securityBearer import security


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    payload = decode_jwt(token, is_refresh=False)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    if payload.get("token_type") != "access":
        raise HTTPException(status_code=401, detail="Invalid access token")

    return payload


def get_password_reset_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    payload = decode_jwt(token, is_refresh=False)

    if not payload or payload.get("token_type") != "password_reset":
        raise HTTPException(status_code=401, detail="Invalid password reset token")
    return payload
