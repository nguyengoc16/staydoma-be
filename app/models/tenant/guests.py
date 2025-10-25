import uuid
from sqlalchemy import Column, String, Boolean, Text, JSON, TIMESTAMP, UUID, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import BaseTenant as Base

class Guests(Base):
    __tablename__ = "guests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False)
    is_registered = Column(Boolean, default=False)
    full_name = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(Text)
    metad_ata = Column(JSON)
    created_at = Column(TIMESTAMP)

    login = relationship("GuestLogin", back_populates="guest", uselist=False)
    bookings = relationship("Bookings", back_populates="guest")


class GuestLogin(Base):
    __tablename__ = "guest_login"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    guest_id = Column(UUID(as_uuid=True), ForeignKey("guests.id"))
    password_hash = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP)

    guest = relationship("Guests", back_populates="login")
