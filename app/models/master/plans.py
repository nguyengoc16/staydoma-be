import uuid
from sqlalchemy import Column, String, DECIMAL, Boolean, TIMESTAMP, UUID, Text
from sqlalchemy.orm import relationship
from app.core.db import BaseMaster as Base

class Plans(Base):
    __tablename__ = "plans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    price_monthly = Column(DECIMAL)
    features_json = Column(Text)
    active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP)

    subscriptions = relationship("Subscriptions", back_populates="plan")
