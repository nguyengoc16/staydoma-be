# app/crud/master/auth_accounts.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.master.auth_account import AuthAccounts
from app.schemas.master.auth import AuthAccountCreate, AuthAccountUpdate
from passlib.context import CryptContext
from uuid import UUID
from typing import List, Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

class CRUDAuthAccounts:
    async def list(self, db: AsyncSession) -> List[AuthAccounts]:
        res = await db.execute(select(AuthAccounts))
        return res.scalars().all()

    async def get(self, db: AsyncSession, acct_id: UUID) -> Optional[AuthAccounts]:
        res = await db.execute(select(AuthAccounts).filter(AuthAccounts.id == acct_id))
        return res.scalar_one_or_none()

    async def create(self, db: AsyncSession, data: AuthAccountCreate) -> AuthAccounts:
        payload = data.dict()
        password = payload.pop("password", None)
        acct = AuthAccounts(**payload)
        if password:
            acct.password_hash = hash_password(password)
        db.add(acct)
        await db.commit()
        await db.refresh(acct)
        return acct

    async def update(self, db: AsyncSession, acct_id: UUID, data: AuthAccountUpdate) -> Optional[AuthAccounts]:
        acct = await self.get(db, acct_id)
        if not acct:
            return None
        change = data.dict(exclude_unset=True)
        password = change.pop("password", None)
        for k, v in change.items():
            setattr(acct, k, v)
        if password:
            acct.password_hash = hash_password(password)
        await db.commit()
        await db.refresh(acct)
        return acct

    async def delete(self, db: AsyncSession, acct_id: UUID) -> bool:
        acct = await self.get(db, acct_id)
        if not acct:
            return False
        await db.delete(acct)
        await db.commit()
        return True

auth_accounts_crud = CRUDAuthAccounts()
