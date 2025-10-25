import uuid
from sqlalchemy import Column, String, Text, Boolean, TIMESTAMP, UUID, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import BaseMaster as Base


class AuthAccounts(Base):
    __tablename__ = "auth_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ref_id = Column(UUID(as_uuid=True))
    auth_scope = Column(String)  # e.g., 'staff', 'tenant', etc.
    login_type_id = Column(UUID(as_uuid=True), nullable=True)
    email = Column(String, unique=True)
    password_hash = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP)
    last_login = Column(TIMESTAMP)

    staff_user = relationship("StaffUsers", back_populates="auth_accounts", uselist=False)
