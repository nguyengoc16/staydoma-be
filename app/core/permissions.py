# app/core/permissions.py
from fastapi import Depends, HTTPException, status
from app.core.deps import get_current_account
from app.models.master.staff import has_permission as has_perm_fn, Action
from app.core.db import MasterSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.master.staff import StaffUsers
from app.models.master.staff import StaffRole

async def get_db():
    async with MasterSessionLocal() as s:
        yield s
        
async def require_permission(table_name: str, action: Action, account = Depends(get_current_account), db: AsyncSession = Depends(get_db)):
    """
    Usage: Depends(lambda: require_permission("TENANTS", Action.VIEW))
    """
    # if token contains permissions claim, you can skip DB lookup and trust it (less secure if token not short-lived)
    # Let's load staff_user -> role -> permission
    staff_user_id = getattr(account, "staff_user_id", None)
    if not staff_user_id:
        raise HTTPException(status_code=403, detail="No staff association")

    q = await db.execute(select(StaffUsers).filter(StaffUsers.id == staff_user_id))
    staff = q.scalars().first()
    if not staff:
        raise HTTPException(status_code=403, detail="Staff user not found")

    role = staff.role
    if not role:
        raise HTTPException(status_code=403, detail="Role not assigned")

    if not has_perm_fn(int(role.permission), table_name, action):
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    return True
