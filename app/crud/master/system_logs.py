# app/crud/master/system_logs.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.master.system_logs import SystemLogs
from app.schemas.master.system_logs import SystemLogCreate
from uuid import UUID

class CRUDSystemLogs:
    async def create(self, db: AsyncSession, data: SystemLogCreate) -> SystemLogs:
        log = SystemLogs(**data.dict())
        db.add(log)
        await db.commit()
        await db.refresh(log)
        return log

system_logs_crud = CRUDSystemLogs()
