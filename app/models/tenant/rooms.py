import uuid
from sqlalchemy import DECIMAL, Boolean, Column, Date, Integer, String, Text, JSON, TIMESTAMP, UUID, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import BaseTenant as Base

class RoomTypes(Base):
    __tablename__ = "room_types"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False)
    hotel_id = Column(UUID(as_uuid=True), ForeignKey("hotels.id"))
    name = Column(String, nullable=False)
    description = Column(Text)
    attributes = Column(JSON)
    created_at = Column(TIMESTAMP)

    hotel = relationship("Hotels", back_populates="room_types")
    rooms = relationship("Rooms", back_populates="room_type")
    pricing_rules = relationship("PricingRules", back_populates="room_type")


class Rooms(Base):
    __tablename__ = "rooms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False)
    room_type_id = Column(UUID(as_uuid=True), ForeignKey("room_types.id"))
    code = Column(String)
    base_price = Column(DECIMAL)
    capacity = Column(Integer)
    status = Column(String)
    amenities = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    room_type = relationship("RoomTypes", back_populates="rooms")
    availability_blocks = relationship("AvailabilityBlocks", back_populates="room")
    bookings = relationship("Bookings", back_populates="room")

class PricingRules(Base):
    __tablename__ = "pricing_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False)
    room_type_id = Column(UUID(as_uuid=True), ForeignKey("room_types.id"))
    valid_from = Column(Date)
    valid_to = Column(Date)
    pricing_json = Column(JSON)
    created_at = Column(TIMESTAMP)

    room_type = relationship("RoomTypes", back_populates="pricing_rules")