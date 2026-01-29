from pydantic import BaseModel, EmailStr,Field

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str = Field(min_length=12)

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class PasswordChangeRequiredResponse(BaseModel):
    require_password_change: bool
    password_reset_token: str
    message: str

class TokenPayload(BaseModel):
    id: int
    email: str
    role: str
    token_type: str
    exp: int
