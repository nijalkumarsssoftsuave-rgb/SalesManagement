from fastapi import Depends, HTTPException
from app.constants.roles import ROLE_LEVEL
from app.security.dependencies import get_current_user

# def require_min_role(role: str):
#     def checker(user=Depends(get_current_user)):
#         user_role = user.get("role")
#
#         if not user_role:
#             raise HTTPException(status_code=403, detail="Role not found in token")
#
#         if ROLE_LEVEL[user_role] < ROLE_LEVEL[role]:
#             raise HTTPException(status_code=403, detail="Forbidden")
#
#         return user
#     return checker

def require_min_role(required_role: str):
    def checker(user=Depends(get_current_user)):
        user_role = user.get("role")

        if not user_role:
            raise HTTPException(status_code=403, detail="Role missing in token")

        if user_role not in ROLE_LEVEL:
            raise HTTPException(
                status_code=403,
                detail=f"Invalid role: {user_role}"
            )

        if required_role not in ROLE_LEVEL:
            raise HTTPException(
                status_code=500,
                detail=f"RBAC misconfigured for role: {required_role}"
            )

        if ROLE_LEVEL[user_role] < ROLE_LEVEL[required_role]:
            raise HTTPException(status_code=403, detail="Forbidden")

        return user

    return checker