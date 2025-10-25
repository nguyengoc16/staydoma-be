import uuid
from sqlalchemy import Column, Date, String, TIMESTAMP, UUID, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import BaseTenant as Base

class AvailabilityBlocks(Base):
    __tablename__ = "availability_blocks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False)
    room_id = Column(UUID(as_uuid=True), ForeignKey("rooms.id"))
    blocked_from = Column(Date)
    blocked_to = Column(Date)
    reason = Column(String)
    created_at = Column(TIMESTAMP)

    room = relationship("Rooms", back_populates="availability_blocks")
