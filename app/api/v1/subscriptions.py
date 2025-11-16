# app/api/v1/subscriptions.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import MasterSessionLocal
from app.crud.master.subscriptions import subscriptions_crud
from app.schemas.master.subscriptions import SubscriptionCreate, SubscriptionOut, SubscriptionUpdate

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

async def get_db():
    async with MasterSessionLocal() as s:
        yield s

@router.get("/", response_model=List[SubscriptionOut])
async def list_subscriptions(db: AsyncSession = Depends(get_db)):
    return await subscriptions_crud.list(db)

@router.post("/", response_model=SubscriptionOut)
async def create_subscription(payload: SubscriptionCreate, db: AsyncSession = Depends(get_db)):
    return await subscriptions_crud.create(db, payload)

@router.get("/{sub_id}", response_model=SubscriptionOut)
async def get_subscription(sub_id: UUID, db: AsyncSession = Depends(get_db)):
    sub = await subscriptions_crud.get(db, sub_id)
    if not sub:
        raise HTTPException(404, "Not found")
    return sub

@router.put("/{sub_id}", response_model=SubscriptionOut)
async def update_subscription(sub_id: UUID, payload: SubscriptionUpdate, db: AsyncSession = Depends(get_db)):
    updated = await subscriptions_crud.update(db, sub_id, payload)
    if not updated:
        raise HTTPException(404, "Not found")
    return updated

@router.delete("/{sub_id}")
async def delete_subscription(sub_id: UUID, db: AsyncSession = Depends(get_db)):
    ok = await subscriptions_crud.delete(db, sub_id)
    if not ok:
        raise HTTPException(404, "Not found")
    return {"ok": True}
