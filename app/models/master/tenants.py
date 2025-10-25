import uuid
from sqlalchemy import Column, String, Text, Enum, Boolean, TIMESTAMP, UUID, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import BaseMaster as Base

class Tenants(Base):
    __tablename__ = "tenants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    subdomain = Column(String, unique=True)
    db_connection = Column(Text)
    db_mode = Column(String)  # e.g., 'shared', 'isolated'
    default_hotel_id = Column(UUID(as_uuid=True), nullable=True)
    plan = Column(String)
    status = Column(String)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    # Relationships
    subscriptions = relationship("Subscriptions", back_populates="tenant")
    support_tickets = relationship("SupportTickets", back_populates="tenant")
    system_logs = relationship("SystemLogs", back_populates="tenant")
