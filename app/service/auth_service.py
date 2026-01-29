from pydantic import EmailStr
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.users_model import User
from app.security.password_hash import verify_password,hash_password
from app.security.jwt_utils import create_access_token, create_refresh_token,create_password_reset_token

def login_user(db: Session, email: EmailStr, password: str):
    user = db.query(User).filter(User.email == email).first()

    print(user.role)

    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User inactive")

    if user.must_change_password:
        return {
            "require_password_change": True,
            "password_reset_token": create_password_reset_token(user),
            "message": "Password change required"
        }

    return {
        "access_token": create_access_token(user),
        "refresh_token": create_refresh_token(user),
    }

def change_password_first_login_service(
    *,
    db: Session,
    user_id: int,
    old_password: str,
    new_password: str
) -> None:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.must_change_password:
        raise HTTPException(
            status_code=400,
            detail="Password change not required"
        )

    if not verify_password(old_password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Old password incorrect"
        )

    user.password = hash_password(new_password)
    user.must_change_password = False

    db.commit()
