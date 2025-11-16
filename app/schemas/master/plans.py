# app/schemas/master/plans.py
from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime
from decimal import Decimal

class PlanBase(BaseModel):
    name: str
    price_monthly: Decimal
    features_json: Optional[str]

class PlanCreate(PlanBase):
    pass

class PlanUpdate(BaseModel):
    name: Optional[str]
    price_monthly: Optional[Decimal]
    features_json: Optional[str]
    active: Optional[bool]

class PlanOut(PlanBase):
    id: UUID4
    active: bool
    created_at: datetime

    class Config:
        orm_mode = True
