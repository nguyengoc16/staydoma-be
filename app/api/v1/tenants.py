from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import MasterSessionLocal
from app.crud.master.tenant import tenant_crud
from app.schemas.master.tenant import TenantCreate, TenantUpdate, TenantOut
from typing import List
from uuid import UUID

router = APIRouter(prefix="/tenants", tags=["Tenants"])

async def get_db():
    async with MasterSessionLocal() as session:
        yield session

@router.get("/", response_model=List[TenantOut])
async def list_tenants(db: AsyncSession = Depends(get_db)):
    return await tenant_crud.get_all(db)

@router.post("/", response_model=TenantOut)
async def create_tenant(data: TenantCreate, db: AsyncSession = Depends(get_db)):
    return await tenant_crud.create(db, data)

@router.get("/{tenant_id}", response_model=TenantOut)
async def get_tenant(tenant_id: UUID, db: AsyncSession = Depends(get_db)):
    tenant = await tenant_crud.get(db, tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant

@router.put("/{tenant_id}", response_model=TenantOut)
async def update_tenant(tenant_id: UUID, data: TenantUpdate, db: AsyncSession = Depends(get_db)):
    updated = await tenant_crud.update(db, tenant_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return updated

@router.delete("/{tenant_id}")
async def delete_tenant(tenant_id: UUID, db: AsyncSession = Depends(get_db)):
    deleted = await tenant_crud.delete(db, tenant_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return {"ok": True}
