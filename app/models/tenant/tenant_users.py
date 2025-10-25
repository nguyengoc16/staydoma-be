import uuid
from sqlalchemy import Column, String, Text, Boolean, TIMESTAMP, UUID, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import BaseTenant as Base

class TenantUsers(Base):
    __tablename__ = "tenant_users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True))
    role_id = Column(UUID(as_uuid=True), ForeignKey("tenant_role.id"))
    name = Column(String)
    email = Column(String)

    login = relationship("TenantLogin", back_populates="tenant_user", uselist=False)
    role = relationship("TenantRole", back_populates="users")


class TenantLogin(Base):
    __tablename__ = "tenant_login"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_user_id = Column(UUID(as_uuid=True), ForeignKey("tenant_users.id"))
    password_hash = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP)

    tenant_user = relationship("TenantUsers", back_populates="login")

class TenantRole(Base):
    __tablename__ = "tenant_role"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role = Column(String)
    description = Column(Text)

    users = relationship("TenantUsers", back_populates="role")
    permissions = relationship("TenantRolePermissions", back_populates="role")


class TenantPermissions(Base):
    __tablename__ = "tenant_permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, unique=True)

    roles = relationship("TenantRolePermissions", back_populates="permission")

class TenantRolePermissions(Base):
    __tablename__ = "tenant_role_permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_role_id = Column(UUID(as_uuid=True), ForeignKey("tenant_role.id"))
    tenant_permission_id = Column(UUID(as_uuid=True), ForeignKey("tenant_permissions.id"))

    role = relationship("TenantRole", back_populates="permissions")
    permission = relationship("TenantPermissions", back_populates="roles")