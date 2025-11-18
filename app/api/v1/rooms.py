from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic  import BaseModel

router = APIRouter()

class RoomCreate(BaseModel):
    number: str
    price: float

async def get_tenant_session(request: Request):
    if not request.state.tenant_session:
        raise HTTPException(status_code=400, detail="Tenant not resolved")
    # yield an AsyncSession context manager
    async with request.state.tenant_session() as session:
        yield session

@router.post("/")
async def create_room(payload: RoomCreate, session = Depends(get_tenant_session)):
    from app.models.tenant import Room
    new = Room(number=payload.number, price=payload.price)
    session.add(new)
    await session.commit()
    await session.refresh(new)
    return {"id": new.id, "number": new.number}
