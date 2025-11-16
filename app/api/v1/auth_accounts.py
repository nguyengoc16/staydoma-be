# app/api/v1/auth_accounts.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import MasterSessionLocal
from app.crud.master.auth_accounts import auth_accounts_crud
from app.schemas.master.auth import AuthAccountCreate, AuthAccountOut, AuthAccountUpdate

router = APIRouter(prefix="/auth_accounts", tags=["Auth Accounts"])

async def get_db():
    async with MasterSessionLocal() as s:
        yield s

@router.get("/", response_model=List[AuthAccountOut])
async def list_accounts(db: AsyncSession = Depends(get_db)):
    return await auth_accounts_crud.list(db)

@router.post("/", response_model=AuthAccountOut)
async def create_account(payload: AuthAccountCreate, db: AsyncSession = Depends(get_db)):
    acct = await auth_accounts_crud.create(db, payload)
    return acct

@router.get("/{acct_id}", response_model=AuthAccountOut)
async def get_account(acct_id: UUID, db: AsyncSession = Depends(get_db)):
    acct = await auth_accounts_crud.get(db, acct_id)
    if not acct:
        raise HTTPException(404, "Not found")
    return acct

@router.put("/{acct_id}", response_model=AuthAccountOut)
async def update_account(acct_id: UUID, payload: AuthAccountUpdate, db: AsyncSession = Depends(get_db)):
    updated = await auth_accounts_crud.update(db, acct_id, payload)
    if not updated:
        raise HTTPException(404, "Not found")
    return updated

@router.delete("/{acct_id}")
async def delete_account(acct_id: UUID, db: AsyncSession = Depends(get_db)):
    ok = await auth_accounts_crud.delete(db, acct_id)
    if not ok:
        raise HTTPException(404, "Not found")
    return {"ok": True}
