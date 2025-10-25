import uuid
from sqlalchemy import Column, String, Text, Boolean, TIMESTAMP, UUID, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import BaseTenant as Base

class Hotels(Base):
    __tablename__ = "hotels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    address = Column(Text)
    city = Column(String)
    country = Column(String)
    phone = Column(String)
    email = Column(String)
    website = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    room_types = relationship("RoomTypes", back_populates="hotel")
    website_settings = relationship("WebsiteSettings", back_populates="hotel", uselist=False)
