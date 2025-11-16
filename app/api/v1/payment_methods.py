# app/api/v1/payment_methods.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import MasterSessionLocal
from app.crud.master.payment_methods import payment_methods_crud
from app.schemas.master.payment_methods import PaymentMethodCreate, PaymentMethodOut, PaymentMethodUpdate

router = APIRouter(prefix="/payment_methods", tags=["Payment Methods"])

async def get_db():
    async with MasterSessionLocal() as s:
        yield s

@router.get("/", response_model=List[PaymentMethodOut])
async def list_pms(db: AsyncSession = Depends(get_db)):
    return await payment_methods_crud.list(db)

@router.post("/", response_model=PaymentMethodOut)
async def create_pm(payload: PaymentMethodCreate, db: AsyncSession = Depends(get_db)):
    return await payment_methods_crud.create(db, payload)

@router.get("/{pm_id}", response_model=PaymentMethodOut)
async def get_pm(pm_id: UUID, db: AsyncSession = Depends(get_db)):
    pm = await payment_methods_crud.get(db, pm_id)
    if not pm:
        raise HTTPException(404, "Not found")
    return pm

@router.put("/{pm_id}", response_model=PaymentMethodOut)
async def update_pm(pm_id: UUID, payload: PaymentMethodUpdate, db: AsyncSession = Depends(get_db)):
    updated = await payment_methods_crud.update(db, pm_id, payload)
    if not updated:
        raise HTTPException(404, "Not found")
    return updated

@router.delete("/{pm_id}")
async def delete_pm(pm_id: UUID, db: AsyncSession = Depends(get_db)):
    ok = await payment_methods_crud.delete(db, pm_id)
    if not ok:
        raise HTTPException(404, "Not found")
    return {"ok": True}
