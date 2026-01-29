from fastapi import Depends, HTTPException
from app.constants.roles import ROLE_LEVEL
from app.security.dependencies import get_current_user

def require_min_role(role: str):
    def checker(user=Depends(get_current_user)):
        if ROLE_LEVEL[user.role] < ROLE_LEVEL[role]:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return checker
