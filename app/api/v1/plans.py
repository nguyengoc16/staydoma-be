# app/api/v1/plans.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.db import MasterSessionLocal
from app.crud.master.plans import plans_crud
from app.schemas.master.plans import PlanCreate, PlanUpdate, PlanOut

router = APIRouter(prefix="/plans", tags=["Plans"])

async def get_db():
    async with MasterSessionLocal() as s:
        yield s

@router.get("/", response_model=List[PlanOut])
async def list_plans(db: AsyncSession = Depends(get_db)):
    return await plans_crud.get_all(db)

@router.post("/", response_model=PlanOut)
async def create_plan(payload: PlanCreate, db: AsyncSession = Depends(get_db)):
    return await plans_crud.create(db, payload)

@router.get("/{plan_id}", response_model=PlanOut)
async def get_plan(plan_id: UUID, db: AsyncSession = Depends(get_db)):
    plan = await plans_crud.get(db, plan_id)
    if not plan:
        raise HTTPException(404, "Plan not found")
    return plan

@router.put("/{plan_id}", response_model=PlanOut)
async def update_plan(plan_id: UUID, payload: PlanUpdate, db: AsyncSession = Depends(get_db)):
    updated = await plans_crud.update(db, plan_id, payload)
    if not updated:
        raise HTTPException(404, "Plan not found")
    return updated

@router.delete("/{plan_id}")
async def delete_plan(plan_id: UUID, db: AsyncSession = Depends(get_db)):
    ok = await plans_crud.delete(db, plan_id)
    if not ok:
        raise HTTPException(404, "Plan not found")
    return {"ok": True}
