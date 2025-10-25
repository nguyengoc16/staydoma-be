from typing import Dict
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import declarative_base
from app.core.config import settings


# ======================
# Base Declarations
# ======================
BaseMaster = declarative_base()
BaseTenant = declarative_base()


# ======================
# Master DB
# ======================
master_engine = create_async_engine(
    settings.DATABASE_URL_MASTER,
    echo=False,
    future=True,
)

MasterSessionLocal = async_sessionmaker(
    master_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ======================
# Tenant DB (Dynamic)
# ======================
_tenant_sessionmakers: Dict[str, async_sessionmaker] = {}


def get_tenant_sessionmaker(tenant_db_url: str) -> async_sessionmaker:
    """
    Return or create an async_sessionmaker for a given tenant DB URL.
    This prevents re-creating engines for the same tenant repeatedly.
    """
    if tenant_db_url not in _tenant_sessionmakers:
        engine = create_async_engine(tenant_db_url, echo=False, future=True)
        _tenant_sessionmakers[tenant_db_url] = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _tenant_sessionmakers[tenant_db_url]


# ======================
# FastAPI Dependency
# ======================
async def get_master_session() -> AsyncSession:
    """FastAPI dependency: yield a master DB session."""
    async with MasterSessionLocal() as session:
        yield session


async def get_tenant_session(tenant_db_url: str) -> AsyncSession:
    """Yield a tenant DB session for a specific tenant connection."""
    session_maker = get_tenant_sessionmaker(tenant_db_url)
    async with session_maker() as session:
        yield session
