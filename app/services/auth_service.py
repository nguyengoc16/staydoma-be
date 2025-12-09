# app/services/auth_service.py
from app.core.db import MasterSessionLocal
from sqlalchemy.future import select
from app.models.master.auth_account import AuthAccounts
from app.core.hash import hash_password, verify_password
from app.core.security import (
    create_access_token, create_refresh_token,
    decode_token, blacklist_token, store_refresh_token,
    check_refresh_token, revoke_refresh_token
)
from datetime import datetime
from uuid import UUID
from typing import Optional, Dict, Any

# create account
async def register_account(email: str, password: str, auth_scope: str = "staff", staff_user_id: str | None = None, role_id: str | None = None):
    async with MasterSessionLocal() as db:
        # check existing email
        q = await db.execute(select(AuthAccounts).filter(AuthAccounts.email == email))
        if q.scalars().first():
            raise ValueError("email exists")

        acct = AuthAccounts(
            email=email,
            auth_scope=auth_scope,
            is_active=True
        )
        acct.password_hash = hash_password(password)
        # optionally link staff_user_id or role
        if staff_user_id:
            acct.staff_user_id = UUID(staff_user_id)
        if role_id:
            acct.role_id = UUID(role_id) if hasattr(acct, "role_id") else None

        db.add(acct)
        await db.commit()
        await db.refresh(acct)
        return acct

# authenticate and issue tokens
async def authenticate_and_issue(email: str, password: str):
    async with MasterSessionLocal() as db:
        q = await db.execute(select(AuthAccounts).filter(AuthAccounts.email == email))
        acct = q.scalars().first()
        if not acct:
            return None, "invalid"
        if not acct.password_hash or not verify_password(password, acct.password_hash):
            return None, "invalid"
        if not acct.is_active:
            return None, "disabled"

        # last_login update
        acct.last_login = datetime.utcnow()
        await db.commit()

        # create tokens
        extra_claims = {"scope": acct.auth_scope}
        # include role/permissions if available to reduce DB hits
        try:
            role_perm = None
            if getattr(acct, "staff_user_id", None):
                # load staff user and role
                from app.models.master.staff import StaffUsers
                q2 = await db.execute(select(StaffUsers).filter(StaffUsers.id == acct.staff_user_id))
                staff = q2.scalars().first()
                if staff and staff.role:
                    extra_claims["role_id"] = str(staff.role.id)
                    extra_claims["permissions"] = int(getattr(staff.role, "permission", 0))
        except Exception:
            pass

        access = create_access_token(str(acct.id), extra_claims=extra_claims)
        refresh = create_refresh_token(str(acct.id))
        # store refresh token in redis (keyed by user and jti)
        await store_refresh_token(str(acct.id), refresh["jti"], refresh["expires_at"])
        return {
            "access_token": access["token"],
            "access_jti": access["jti"],
            "access_expires_at": access["expires_at"],
            "refresh_token": refresh["token"],
            "refresh_jti": refresh["jti"],
            "refresh_expires_at": refresh["expires_at"],
        }, None

# logout (blacklist access token + revoke refresh)
async def logout_token(access_payload: dict, refresh_jti: Optional[str] = None):
    # access_payload is decoded token payload
    jti = access_payload.get("jti")
    exp = access_payload.get("exp")
    if jti and exp:
        await blacklist_token(jti, exp)
    # revoke refresh token if provided
    if refresh_jti and access_payload.get("sub"):
        await revoke_refresh_token(access_payload.get("sub"), refresh_jti)
