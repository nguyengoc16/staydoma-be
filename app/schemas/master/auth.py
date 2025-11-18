# app/schemas/master/auth.py
from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional
from datetime import datetime

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
