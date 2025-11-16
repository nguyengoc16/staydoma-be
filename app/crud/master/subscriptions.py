# app/crud/master/subscriptions.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.master.subscriptions import Subscriptions
from app.schemas.master.subscriptions import SubscriptionCreate, SubscriptionUpdate
from typing import List, Optional
from uuid import UUID

class CRUDSubscriptions:
    async def list(self, db: AsyncSession) -> List[Subscriptions]:
        res = await db.execute(select(Subscriptions))
        return res.scalars().all()

    async def get(self, db: AsyncSession, sub_id: UUID) -> Optional[Subscriptions]:
        res = await db.execute(select(Subscriptions).filter(Subscriptions.id == sub_id))
        return res.scalar_one_or_none()

    async def create(self, db: AsyncSession, data: SubscriptionCreate) -> Subscriptions:
        sub = Subscriptions(**data.dict())
        db.add(sub)
        await db.commit()
        await db.refresh(sub)
        return sub

    async def update(self, db: AsyncSession, sub_id: UUID, data: SubscriptionUpdate) -> Optional[Subscriptions]:
        sub = await self.get(db, sub_id)
        if not sub:
            return None
        for k, v in data.dict(exclude_unset=True).items():
            setattr(sub, k, v)
        await db.commit()
        await db.refresh(sub)
        return sub

    async def delete(self, db: AsyncSession, sub_id: UUID) -> bool:
        sub = await self.get(db, sub_id)
        if not sub:
            return False
        await db.delete(sub)
        await db.commit()
        return True

subscriptions_crud = CRUDSubscriptions()
