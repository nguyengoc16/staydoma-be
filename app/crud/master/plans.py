# app/crud/master/plans.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.master.billing import Plans
from app.schemas.master.plans import PlanCreate, PlanUpdate
from uuid import UUID
from typing import List, Optional

class CRUDPlans:
    async def get_all(self, db: AsyncSession) -> List[Plans]:
        res = await db.execute(select(Plans))
        return res.scalars().all()

    async def get(self, db: AsyncSession, plan_id: UUID) -> Optional[Plans]:
        res = await db.execute(select(Plans).filter(Plans.id == plan_id))
        return res.scalar_one_or_none()

    async def create(self, db: AsyncSession, data: PlanCreate) -> Plans:
        plan = Plans(**data.dict())
        db.add(plan)
        await db.commit()
        await db.refresh(plan)
        return plan

    async def update(self, db: AsyncSession, plan_id: UUID, data: PlanUpdate) -> Optional[Plans]:
        plan = await self.get(db, plan_id)
        if not plan:
            return None
        for k, v in data.dict(exclude_unset=True).items():
            setattr(plan, k, v)
        await db.commit()
        await db.refresh(plan)
        return plan

    async def delete(self, db: AsyncSession, plan_id: UUID) -> bool:
        plan = await self.get(db, plan_id)
        if not plan:
            return False
        await db.delete(plan)
        await db.commit()
        return True

plans_crud = CRUDPlans()
