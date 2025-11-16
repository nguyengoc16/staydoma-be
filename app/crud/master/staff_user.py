from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.master.staff import StaffUsers
from app.schemas.master.staff_user import StaffUserCreate, StaffUserUpdate
from uuid import UUID

class CRUDStaffUser:
    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(StaffUsers))
        return result.scalars().all()

    async def get(self, db: AsyncSession, user_id: UUID):
        result = await db.execute(select(StaffUsers).filter(StaffUsers.id == user_id))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, data: StaffUserCreate):
        user = StaffUsers(**data.dict())
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def update(self, db: AsyncSession, user_id: UUID, data: StaffUserUpdate):
        user = await self.get(db, user_id)
        if not user:
            return None
        for key, value in data.dict(exclude_unset=True).items():
            setattr(user, key, value)
        await db.commit()
        await db.refresh(user)
        return user

    async def delete(self, db: AsyncSession, user_id: UUID):
        user = await self.get(db, user_id)
        if not user:
            return False
        await db.delete(user)
        await db.commit()
        return True

staff_user_crud = CRUDStaffUser()
