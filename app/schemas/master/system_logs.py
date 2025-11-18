# app/schemas/master/system_logs.py
from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime

class SystemLogBase(BaseModel):
    tenant_id: Optional[UUID4]
    event_type: str
    details: Optional[dict]

class SystemLogCreate(SystemLogBase):
    pass

class SystemLogOut(SystemLogBase):
    id: UUID4
    created_at: datetime

    class Config:
        from_attributes = True
