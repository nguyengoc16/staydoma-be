from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import MasterSessionLocal
from app.crud.master.staff_user import staff_user_crud
from app.schemas.master.staff_user import StaffUserCreate, StaffUserUpdate, StaffUserOut
from typing import List
from uuid import UUID

router = APIRouter(prefix="/staff_users", tags=["Staff Users"])

async def get_db():
    async with MasterSessionLocal() as session:
        yield session

@router.get("/", response_model=List[StaffUserOut])
async def list_staff(db: AsyncSession = Depends(get_db)):
    return await staff_user_crud.get_all(db)

@router.post("/", response_model=StaffUserOut)
async def create_staff(data: StaffUserCreate, db: AsyncSession = Depends(get_db)):
    return await staff_user_crud.create(db, data)

@router.get("/{user_id}", response_model=StaffUserOut)
async def get_staff(user_id: UUID, db: AsyncSession = Depends(get_db)):
    user = await staff_user_crud.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Staff not found")
    return user

@router.put("/{user_id}", response_model=StaffUserOut)
async def update_staff(user_id: UUID, data: StaffUserUpdate, db: AsyncSession = Depends(get_db)):
    updated = await staff_user_crud.update(db, user_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Staff not found")
    return updated

@router.delete("/{user_id}")
async def delete_staff(user_id: UUID, db: AsyncSession = Depends(get_db)):
    deleted = await staff_user_crud.delete(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Staff not found")
    return {"ok": True}
