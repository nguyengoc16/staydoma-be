from pydantic import BaseModel, UUID4
from typing import Optional

class StaffRoleBase(BaseModel):
    role: str
    permission: int = 0

class StaffRoleCreate(StaffRoleBase):
    pass

class StaffRoleUpdate(BaseModel):
    role: Optional[str]
    permission: Optional[int]

class StaffRoleOut(StaffRoleBase):
    id: UUID4

    class Config:
        from_attributes = True
