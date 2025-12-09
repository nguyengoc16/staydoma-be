# app/schemas/master/auth.py
from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: Optional[int]

class TokenData(BaseModel):
    sub: Optional[str] = None
    # you can add extra fields if you include them in token

class RegisterIn(BaseModel):
    email: EmailStr
    password: str
    auth_scope: Optional[str] = "staff"
    # optional staff_user_id or role_id if you want to create linked staff user
    staff_user_id: Optional[str] = None
    role_id: Optional[str] = None

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: int
    refresh_token: Optional[str] = None
    refresh_expires_at: Optional[int] = None

class MeOut(BaseModel):
    id: str
    email: EmailStr
    auth_scope: str
    is_active: bool
    last_login: Optional[datetime]
    
class AuthAccountBase(BaseModel):
    ref_id: UUID4
    auth_scope: str
    email: EmailStr

class AuthAccountCreate(AuthAccountBase):
    password: Optional[str]  # can be None for external logins

class AuthAccountUpdate(BaseModel):
    password: Optional[str]
    is_active: Optional[bool]

class AuthAccountOut(AuthAccountBase):
    id: UUID4
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True
