import os
from datetime import datetime, timedelta, timezone
from jose import jwt
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 43200))

def create_access_token(user):
    expire = datetime.now(tz=timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "token_type": "access",
        "exp": expire,
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user):
    expire = datetime.now(tz=timezone.utc) + timedelta(
        minutes=REFRESH_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "token_type": "refresh",
        "exp": expire,
    }
    return jwt.encode(payload, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt(token: str, is_refresh: bool):
    try:
        key = JWT_REFRESH_SECRET_KEY if is_refresh else JWT_SECRET_KEY
        return jwt.decode(token, key, algorithms=[ALGORITHM])
    except Exception:
        return None

def create_password_reset_token(user):
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=10)

    payload = {
        "id": user.id,
        "email": user.email,
        "token_type": "password_reset",
        "exp": expire
    }

    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)
