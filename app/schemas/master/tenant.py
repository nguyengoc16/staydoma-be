from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional

class TenantBase(BaseModel):
    name: str
    subdomain: str
    db_connection: str

class TenantCreate(TenantBase):
    db_mode: str
    plan: Optional[str] = "free"

class TenantUpdate(BaseModel):
    name: Optional[str]
    subdomain: Optional[str]
    plan: Optional[str]
    status: Optional[str]
    is_deleted: Optional[bool]

class TenantOut(TenantBase):
    id: UUID4
    db_mode: str
    plan: str
    status: str
    is_deleted: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
