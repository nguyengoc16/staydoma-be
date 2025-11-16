from pydantic import BaseModel, UUID4, EmailStr
from datetime import datetime
from typing import Optional

class StaffUserBase(BaseModel):
    email: EmailStr
    role_id: UUID4

class StaffUserCreate(StaffUserBase):
    pass

class StaffUserUpdate(BaseModel):
    email: Optional[EmailStr]
    role_id: Optional[UUID4]

class StaffUserOut(StaffUserBase):
    id: UUID4
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        orm_mode = True
