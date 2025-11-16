# app/crud/master/support.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.master.support_tickets import SupportTickets
from app.schemas.master.support import SupportTicketCreate, SupportTicketUpdate
from typing import List, Optional
from uuid import UUID

class CRUDSupport:
    async def list(self, db: AsyncSession) -> List[SupportTickets]:
        res = await db.execute(select(SupportTickets))
        return res.scalars().all()

    async def get(self, db: AsyncSession, ticket_id: UUID) -> Optional[SupportTickets]:
        res = await db.execute(select(SupportTickets).filter(SupportTickets.id == ticket_id))
        return res.scalar_one_or_none()

    async def create(self, db: AsyncSession, data: SupportTicketCreate) -> SupportTickets:
        t = SupportTickets(**data.dict())
        db.add(t)
        await db.commit()
        await db.refresh(t)
        return t

    async def update(self, db: AsyncSession, ticket_id: UUID, data: SupportTicketUpdate) -> Optional[SupportTickets]:
        t = await self.get(db, ticket_id)
        if not t:
            return None
        for k, v in data.dict(exclude_unset=True).items():
            setattr(t, k, v)
        await db.commit()
        await db.refresh(t)
        return t

    async def delete(self, db: AsyncSession, ticket_id: UUID) -> bool:
        t = await self.get(db, ticket_id)
        if not t:
            return False
        await db.delete(t)
        await db.commit()
        return True

support_crud = CRUDSupport()
