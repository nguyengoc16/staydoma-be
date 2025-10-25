import uuid
from sqlalchemy import Column, DECIMAL, String, JSON, TIMESTAMP, UUID, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import BaseTenant as Base

class PaymentMethodsTenant(Base):
    __tablename__ = "payment_methods_tenant"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    payment_method = Column(String)


class Payments(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True))
    booking_id = Column(UUID(as_uuid=True), ForeignKey("bookings.id"))
    amount = Column(DECIMAL)
    payment_method_id = Column(UUID(as_uuid=True), ForeignKey("payment_methods_tenant.id"))
    status = Column(String)
    transaction_ref = Column(String)
    gateway_response = Column(JSON)
    created_at = Column(TIMESTAMP)

    booking = relationship("Bookings", back_populates="payments")
    payment_method = relationship("PaymentMethodsTenant")
