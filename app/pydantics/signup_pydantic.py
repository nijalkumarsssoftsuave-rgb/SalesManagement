# app/pydantic/signup.py
from pydantic import BaseModel, EmailStr, Field

class AdminCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class ManagerCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str | None = None
    address: str | None = None


class TeamMemberCreate(BaseModel):
    name: str
    email: EmailStr
    password: str