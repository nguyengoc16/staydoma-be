import uuid
import enum
from sqlalchemy import Column, String, Text, Enum, TIMESTAMP, UUID, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import BaseMaster as Base


class TicketStatus(enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"

class TicketPriority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class SupportTickets(Base):
    __tablename__ = "support_tickets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))
    submitter_account_id = Column(UUID(as_uuid=True))
    subject = Column(String)
    message = Column(Text)
    status = Column(String)
    priority = Column(String)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    tenant = relationship("Tenants", back_populates="support_tickets")
