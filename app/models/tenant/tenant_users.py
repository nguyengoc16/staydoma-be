import uuid
from enum import IntFlag
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, String, BigInteger, Text, UUID
from sqlalchemy.orm import relationship
from app.core.db import BaseTenant as Base


class Action(IntFlag):
    CREATE = 1 << 0  # 0001
    VIEW   = 1 << 1  # 0010
    UPDATE = 1 << 2  # 0100
    DELETE = 1 << 3  # 1000


TABLE_BIT_OFFSETS = {
    "HOTELS": 0,
    "ROOM_TYPES": 4,
    "ROOMS": 8,
    "BOOKINGS": 12,
    "GUESTS": 16,
    "PAYMENTS": 20,
    "TENANT_USERS": 24,
    "WEBSITE_SETTINGS": 28,
    "AUDIT_LOGS": 32,
}


def calculate_permission(table_name: str, actions: list[Action]) -> int:
    """Return combined bitmask for a given table and action list."""
    offset = TABLE_BIT_OFFSETS[table_name]
    mask = 0
    for action in actions:
        mask |= action << offset
    return mask


def has_permission(role_permission: int, table_name: str, action: Action) -> bool:
    """Check if role_permission includes the given table and action."""
    offset = TABLE_BIT_OFFSETS[table_name]
    mask = action << offset
    return (role_permission & mask) != 0


class TenantRole(Base):
    __tablename__ = "tenant_role"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role = Column(String, nullable=False)
    description = Column(Text)
    permission = Column(BigInteger, nullable=False, default=0)

    users = relationship("TenantUsers", back_populates="role")

class TenantUsers(Base):
    __tablename__ = "tenant_users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True))
    role_id = Column(UUID(as_uuid=True), ForeignKey("tenant_role.id"))
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

    role = relationship("TenantRole", back_populates="users")
    login = relationship("TenantLogin", back_populates="user", uselist=False)

class TenantLogin(Base):
    __tablename__ = "tenant_login"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_user_id = Column(UUID(as_uuid=True), ForeignKey("tenant_users.id"))
    password_hash = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP)

    user = relationship("TenantUsers", back_populates="login")