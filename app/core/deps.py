# app/core/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_token, is_token_blacklisted, get_redis
from app.core.db import MasterSessionLocal
from app.models.master.auth_account import AuthAccounts
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

security = HTTPBearer(auto_error=False)

async def get_db() -> AsyncSession:
    async with MasterSessionLocal() as s:
        yield s

async def get_current_account(
    token: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> AuthAccounts:
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        payload = decode_token(token.credentials)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    # ensure token type is access
    if payload.get("typ") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

    jti = payload.get("jti")
    if not jti:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    # check blacklist
    if await is_token_blacklisted(jti):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    q = await db.execute(select(AuthAccounts).filter(AuthAccounts.id == user_id))
    acct = q.scalars().first()
    if not acct:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Account not found")
    return acct
