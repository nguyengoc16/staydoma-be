import uuid
from sqlalchemy import Column, String, JSON, TIMESTAMP, UUID
from app.core.db import BaseTenant as Base

class AuditLogs(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True))
    source = Column(String)
    action = Column(String)
    details = Column(JSON)
    created_at = Column(TIMESTAMP)
