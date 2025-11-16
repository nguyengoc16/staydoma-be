from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.master.tenants import Tenants
from app.schemas.master.tenant import TenantCreate, TenantUpdate
from typing import List, Optional
from uuid import UUID

class CRUDTenant:
    async def get_all(self, db: AsyncSession) -> List[Tenants]:
        result = await db.execute(select(Tenants))
        return result.scalars().all()

    async def get(self, db: AsyncSession, tenant_id: UUID) -> Optional[Tenants]:
        result = await db.execute(select(Tenants).filter(Tenants.id == tenant_id))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, data: TenantCreate) -> Tenants:
        tenant = Tenants(**data.dict())
        db.add(tenant)
        await db.commit()
        await db.refresh(tenant)
        return tenant

    async def update(self, db: AsyncSession, tenant_id: UUID, data: TenantUpdate) -> Optional[Tenants]:
        tenant = await self.get(db, tenant_id)
        if not tenant:
            return None
        for key, value in data.dict(exclude_unset=True).items():
            setattr(tenant, key, value)
        await db.commit()
        await db.refresh(tenant)
        return tenant

    async def delete(self, db: AsyncSession, tenant_id: UUID) -> bool:
        tenant = await self.get(db, tenant_id)
        if not tenant:
            return False
        await db.delete(tenant)
        await db.commit()
        return True

tenant_crud = CRUDTenant()
