# app/schemas/master/support.py
from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime

class SupportTicketBase(BaseModel):
    tenant_id: UUID4
    submitter_account_id: Optional[UUID4]
    subject: str
    message: str

class SupportTicketCreate(SupportTicketBase):
    priority: Optional[str] = "medium"

class SupportTicketUpdate(BaseModel):
    status: Optional[str]
    priority: Optional[str]
    message: Optional[str]

class SupportTicketOut(SupportTicketBase):
    id: UUID4
    status: str
    priority: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
