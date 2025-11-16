# app/api/v1/support.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import MasterSessionLocal
from app.crud.master.support import support_crud
from app.schemas.master.support import SupportTicketCreate, SupportTicketOut, SupportTicketUpdate

router = APIRouter(prefix="/support_tickets", tags=["Support"])

async def get_db():
    async with MasterSessionLocal() as s:
        yield s

@router.get("/", response_model=List[SupportTicketOut])
async def list_tickets(db: AsyncSession = Depends(get_db)):
    return await support_crud.list(db)

@router.post("/", response_model=SupportTicketOut)
async def create_ticket(payload: SupportTicketCreate, db: AsyncSession = Depends(get_db)):
    return await support_crud.create(db, payload)

@router.get("/{ticket_id}", response_model=SupportTicketOut)
async def get_ticket(ticket_id: UUID, db: AsyncSession = Depends(get_db)):
    t = await support_crud.get(db, ticket_id)
    if not t:
        raise HTTPException(404, "Not found")
    return t

@router.put("/{ticket_id}", response_model=SupportTicketOut)
async def update_ticket(ticket_id: UUID, payload: SupportTicketUpdate, db: AsyncSession = Depends(get_db)):
    updated = await support_crud.update(db, ticket_id, payload)
    if not updated:
        raise HTTPException(404, "Not found")
    return updated

@router.delete("/{ticket_id}")
async def delete_ticket(ticket_id: UUID, db: AsyncSession = Depends(get_db)):
    ok = await support_crud.delete(db, ticket_id)
    if not ok:
        raise HTTPException(404, "Not found")
    return {"ok": True}
