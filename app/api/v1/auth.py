# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Body
from app.schemas.master.auth import RegisterIn, LoginIn, TokenOut, MeOut
from app.services.auth_service import register_account, authenticate_and_issue, logout_token
from app.core.deps import get_current_account, get_db
from app.core.security import decode_token, is_token_blacklisted, get_redis
from app.core.db import MasterSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict
from jose import JWTError

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=MeOut, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterIn):
    """
    Register local account (creates AuthAccounts). You can optionally pass `staff_user_id` to link.
    """
    try:
        acct = await register_account(payload.email, payload.password, payload.auth_scope, payload.staff_user_id, payload.role_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {
        "id": str(acct.id),
        "email": acct.email,
        "auth_scope": acct.auth_scope,
        "is_active": acct.is_active,
        "last_login": acct.last_login
    }

@router.post("/login", response_model=TokenOut)
async def login(payload: LoginIn):
    data, err = await authenticate_and_issue(payload.email, payload.password)
    if err:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {
        "access_token": data["access_token"],
        "token_type": "bearer",
        "expires_at": data["access_expires_at"],
        "refresh_token": data["refresh_token"],
        "refresh_expires_at": data["refresh_expires_at"],
    }

@router.post("/logout")
async def logout(token: str = Body(..., embed=True)):
    """
    Logout by blacklisting the provided access token and deleting associated refresh token if provided.
    Request body: { "token": "<access token>", "refresh_jti": "<optional refresh jti>" }
    """
    # decode token
    try:
        payload = decode_token(token)
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
    await logout_token(payload, None)
    return {"ok": True}

@router.post("/refresh", response_model=TokenOut)
async def refresh(refresh_token: str = Body(..., embed=True)):
    """
    Exchange refresh token for new access + optionally new refresh token.
    """
    try:
        payload = decode_token(refresh_token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if payload.get("typ") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    user_id = payload.get("sub")
    jti = payload.get("jti")
    if not (user_id and jti):
        raise HTTPException(status_code=401, detail="Invalid token")

    # check redis to ensure refresh exists
    from app.core.security import check_refresh_token, create_access_token, create_refresh_token, store_refresh_token, revoke_refresh_token
    if not await check_refresh_token(user_id, jti):
        raise HTTPException(status_code=401, detail="Refresh token revoked")

    # issue new tokens (rotate refresh token)
    access = create_access_token(user_id)
    new_refresh = create_refresh_token(user_id)
    # store new refresh and remove old
    await store_refresh_token(user_id, new_refresh["jti"], new_refresh["expires_at"])
    await revoke_refresh_token(user_id, jti)
    return {
        "access_token": access["token"],
        "token_type": "bearer",
        "expires_at": access["expires_at"],
        "refresh_token": new_refresh["token"],
        "refresh_expires_at": new_refresh["expires_at"],
    }

@router.get("/me", response_model=MeOut)
async def me(current=Depends(get_current_account)):
    return {
        "id": str(current.id),
        "email": current.email,
        "auth_scope": current.auth_scope,
        "is_active": current.is_active,
        "last_login": current.last_login
    }
