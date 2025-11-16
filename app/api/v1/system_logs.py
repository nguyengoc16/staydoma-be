# app/api/v1/system_logs.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import MasterSessionLocal
from app.crud.master.system_logs import system_logs_crud
from app.schemas.master.system_logs import SystemLogCreate, SystemLogOut

router = APIRouter(prefix="/system_logs", tags=["System Logs"])

async def get_db():
    async with MasterSessionLocal() as s:
        yield s

@router.post("/", response_model=SystemLogOut)
async def create_log(payload: SystemLogCreate, db: AsyncSession = Depends(get_db)):
    return await system_logs_crud.create(db, payload)
