import bcrypt

# bcrypt max input length is 72 bytes
MAX_BCRYPT_BYTES = 72


def _normalize_password(password: str) -> bytes:
    if not isinstance(password, str):
        password = str(password)
    return password.encode("utf-8")[:MAX_BCRYPT_BYTES]


def hash_password(password: str) -> str:
    password_bytes = _normalize_password(password)
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        plain_bytes = _normalize_password(plain)
        hashed_bytes = hashed.encode("utf-8")
        return bcrypt.checkpw(plain_bytes, hashed_bytes)
    except Exception:
        return False
