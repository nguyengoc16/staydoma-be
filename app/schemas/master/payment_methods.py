# app/schemas/master/payment_methods.py
from pydantic import BaseModel, UUID4
from typing import Optional

class PaymentMethodBase(BaseModel):
    name: str
    details_json: Optional[str]

class PaymentMethodCreate(PaymentMethodBase):
    pass

class PaymentMethodUpdate(BaseModel):
    name: Optional[str]
    details_json: Optional[str]

class PaymentMethodOut(PaymentMethodBase):
    id: UUID4

    class Config:
        orm_mode = True
