import uuid
from sqlalchemy import Column, String, Text, UUID
from sqlalchemy.orm import relationship
from app.core.db import BaseMaster as Base

class PaymentMethods(Base):
    __tablename__ = "payment_methods"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    details_json = Column(Text)

    subscriptions = relationship("Subscriptions", back_populates="payment_method")
