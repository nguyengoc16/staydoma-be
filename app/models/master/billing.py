import uuid
from sqlalchemy import Column, String, Text, DECIMAL, Boolean, Date, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.db import BaseMaster as Base
from sqlalchemy.orm import relationship


class Plans(Base):
    __tablename__ = "plans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    price_monthly = Column(DECIMAL)
    features_json = Column(Text)
    active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP)

    subscriptions = relationship("Subscriptions", back_populates="plan")
class PaymentMethods(Base):
    __tablename__ = "payment_methods"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    details_json = Column(Text)

    subscriptions = relationship("Subscriptions", back_populates="payment_method")


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
