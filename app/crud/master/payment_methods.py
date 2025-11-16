# app/crud/master/payment_methods.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.master.payments import PaymentMethods
from app.schemas.master.payment_methods import PaymentMethodCreate, PaymentMethodUpdate
from typing import List, Optional
from uuid import UUID

class CRUDPaymentMethods:
    async def list(self, db: AsyncSession) -> List[PaymentMethods]:
        res = await db.execute(select(PaymentMethods))
        return res.scalars().all()

    async def get(self, db: AsyncSession, pm_id: UUID) -> Optional[PaymentMethods]:
        res = await db.execute(select(PaymentMethods).filter(PaymentMethods.id == pm_id))
        return res.scalar_one_or_none()

    async def create(self, db: AsyncSession, data: PaymentMethodCreate) -> PaymentMethods:
        pm = PaymentMethods(**data.dict())
        db.add(pm)
        await db.commit()
        await db.refresh(pm)
        return pm

    async def update(self, db: AsyncSession, pm_id: UUID, data: PaymentMethodUpdate) -> Optional[PaymentMethods]:
        pm = await self.get(db, pm_id)
        if not pm:
            return None
        for k, v in data.dict(exclude_unset=True).items():
            setattr(pm, k, v)
        await db.commit()
        await db.refresh(pm)
        return pm

    async def delete(self, db: AsyncSession, pm_id: UUID) -> bool:
        pm = await self.get(db, pm_id)
        if not pm:
            return False
        await db.delete(pm)
        await db.commit()
        return True

payment_methods_crud = CRUDPaymentMethods()
