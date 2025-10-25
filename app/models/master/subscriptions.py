import uuid
from sqlalchemy import Column, Date, Enum, TIMESTAMP, UUID, ForeignKey, String
from sqlalchemy.orm import relationship
from app.core.db import BaseMaster as Base

class Subscriptions(Base):
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))
    plan_id = Column(UUID(as_uuid=True), ForeignKey("plans.id"))
    payment_method_id = Column(UUID(as_uuid=True), ForeignKey("payment_methods.id"))
    starts_at = Column(Date)
    ends_at = Column(Date)
    status = Column(String)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    tenant = relationship("Tenants", back_populates="subscriptions")
    plan = relationship("Plans", back_populates="subscriptions")
    payment_method = relationship("PaymentMethods", back_populates="subscriptions")
