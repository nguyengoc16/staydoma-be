import uuid
from sqlalchemy import Column, Date, Integer, DECIMAL, Text, String, TIMESTAMP, UUID, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import BaseTenant as Base

class Bookings(Base):
    __tablename__ = "bookings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True))
    hotel_id = Column(UUID(as_uuid=True), ForeignKey("hotels.id"))
    room_id = Column(UUID(as_uuid=True), ForeignKey("rooms.id"))
    guest_id = Column(UUID(as_uuid=True), ForeignKey("guests.id"))
    check_in = Column(Date)
    check_out = Column(Date)
    nights = Column(Integer)
    subtotal = Column(DECIMAL)
    taxes = Column(DECIMAL)
    total_price = Column(DECIMAL)
    status = Column(String)
    payment_status = Column(String)
    external_reference = Column(String)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    cancellation_reason = Column(Text)

    guest = relationship("Guests", back_populates="bookings")
    room = relationship("Rooms", back_populates="bookings")
    payments = relationship("Payments", back_populates="booking")
