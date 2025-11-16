import uuid
from enum import IntFlag
from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, BigInteger, UUID
from sqlalchemy.orm import relationship
from app.core.db import BaseMaster as Base


class Action(IntFlag):
    CREATE = 1 << 0  # 0001
    VIEW   = 1 << 1  # 0010
    UPDATE = 1 << 2  # 0100
    DELETE = 1 << 3  # 1000


TABLE_BIT_OFFSETS = {
    "TENANTS": 0,        # bits 0–3
    "STAFF_USERS": 4,    # bits 4–7
    "PLANS": 8,          # bits 8–11
    "PAYMENT_METHODS": 12,
    "SUBSCRIPTIONS": 16,
    "SUPPORT_TICKETS": 20,
    "SYSTEM_LOGS": 24,
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


class StaffRole(Base):
    __tablename__ = "staff_role"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role = Column(String, nullable=False, unique=True)
    permission = Column(BigInteger, nullable=False, default=0)

    users = relationship("StaffUsers", back_populates="role")

class StaffUsers(Base):
    __tablename__ = "staff_users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("staff_role.id"))
    last_login = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP)

    role = relationship("StaffRole", back_populates="users")
    auth_accounts = relationship("AuthAccounts", back_populates="staff_user")
