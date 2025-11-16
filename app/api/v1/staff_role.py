from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import MasterSessionLocal
from app.crud.master.staff_role import staff_role_crud
from app.schemas.master.staff_role import StaffRoleCreate, StaffRoleUpdate, StaffRoleOut
from typing import List
from uuid import UUID

router = APIRouter(prefix="/staff_roles", tags=["Staff Roles"])

async def get_db():
    async with MasterSessionLocal() as session:
        yield session

@router.get("/", response_model=List[StaffRoleOut])
async def list_roles(db: AsyncSession = Depends(get_db)):
    return await staff_role_crud.get_all(db)

@router.post("/", response_model=StaffRoleOut)
async def create_role(data: StaffRoleCreate, db: AsyncSession = Depends(get_db)):
    return await staff_role_crud.create(db, data)

@router.get("/{role_id}", response_model=StaffRoleOut)
async def get_role(role_id: UUID, db: AsyncSession = Depends(get_db)):
    role = await staff_role_crud.get(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.put("/{role_id}", response_model=StaffRoleOut)
async def update_role(role_id: UUID, data: StaffRoleUpdate, db: AsyncSession = Depends(get_db)):
    updated = await staff_role_crud.update(db, role_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Role not found")
    return updated

@router.delete("/{role_id}")
async def delete_role(role_id: UUID, db: AsyncSession = Depends(get_db)):
    deleted = await staff_role_crud.delete(db, role_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"ok": True}
