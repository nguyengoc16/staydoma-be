import uuid
from sqlalchemy import Column, String, JSON, TIMESTAMP, UUID, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import BaseMaster as Base

class SystemLogs(Base):
    __tablename__ = "system_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))
    event_type = Column(String)
    details = Column(JSON)
    created_at = Column(TIMESTAMP)

    tenant = relationship("Tenants", back_populates="system_logs")
