# app/schemas/master/subscriptions.py
from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import date, datetime

class SubscriptionBase(BaseModel):
    tenant_id: UUID4
    plan_id: UUID4
    payment_method_id: Optional[UUID4]

class SubscriptionCreate(SubscriptionBase):
    starts_at: Optional[date]
    ends_at: Optional[date]

class SubscriptionUpdate(BaseModel):
    starts_at: Optional[date]
    ends_at: Optional[date]
    status: Optional[str]

class SubscriptionOut(SubscriptionBase):
    id: UUID4
    status: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
