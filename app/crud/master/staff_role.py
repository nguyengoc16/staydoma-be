from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.master.staff import StaffRole
from app.schemas.master.staff_role import StaffRoleCreate, StaffRoleUpdate
from uuid import UUID

class CRUDStaffRole:
    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(StaffRole))
        return result.scalars().all()

    async def get(self, db: AsyncSession, role_id: UUID):
        result = await db.execute(select(StaffRole).filter(StaffRole.id == role_id))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, data: StaffRoleCreate):
        role = StaffRole(**data.dict())
        db.add(role)
        await db.commit()
        await db.refresh(role)
        return role

    async def update(self, db: AsyncSession, role_id: UUID, data: StaffRoleUpdate):
        role = await self.get(db, role_id)
        if not role:
            return None
        for key, value in data.dict(exclude_unset=True).items():
            setattr(role, key, value)
        await db.commit()
        await db.refresh(role)
        return role

    async def delete(self, db: AsyncSession, role_id: UUID):
        role = await self.get(db, role_id)
        if not role:
            return False
        await db.delete(role)
        await db.commit()
        return True

staff_role_crud = CRUDStaffRole()
