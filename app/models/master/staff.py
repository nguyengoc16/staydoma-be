import uuid
from sqlalchemy import Column, String, UUID, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import BaseMaster as Base


class StaffRole(Base):
    __tablename__ = "staff_role"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role = Column(String, nullable=False)

    users = relationship("StaffUsers", back_populates="role")
    permissions = relationship("StaffRolePermissions", back_populates="role")


class StaffPermissions(Base):
    __tablename__ = "staff_permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, unique=True)

    role_permissions = relationship("StaffRolePermissions", back_populates="permission")


class StaffRolePermissions(Base):
    __tablename__ = "staff_role_permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_id = Column(UUID(as_uuid=True), ForeignKey("staff_role.id"))
    permisson_id = Column(UUID(as_uuid=True), ForeignKey("staff_permissions.id"))

    role = relationship("StaffRole", back_populates="permissions")
    permission = relationship("StaffPermissions", back_populates="role_permissions")


class StaffUsers(Base):
    __tablename__ = "staff_users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey("staff_role.id"))
    last_login = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP)

    role = relationship("StaffRole", back_populates="users")
    auth_accounts = relationship("AuthAccounts", back_populates="staff_user")
