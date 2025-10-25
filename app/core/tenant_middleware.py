from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.core.db import MasterSessionLocal, tenant_sessionmakers
from app.models.master import Tenant as MasterTenant
from sqlalchemy import select
import json
import aioredis
from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

_redis = None

"""
simple middleware that reads subdomain from Host header or x-tenant-id
"""
async def get_redis():
    global _redis
    if _redis is None:
        _redis = await aioredis.from_url(settings.REDIS_URL)
    return _redis

def extract_subdomain(hostname: str) -> str | None:
    if not hostname:
        return None
    # dev: allow tenant.localhost or tenant.app.local
    parts = hostname.split(".")
    if "localhost" in hostname:
        return parts[0]
    # normal case: tenant.example.com -> tenant
    if len(parts) >= 3:
        return parts[0]
    return None

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        host = request.url.hostname or request.headers.get("host")
        subdomain = extract_subdomain(host)
        if not subdomain:
            subdomain = request.headers.get("x-tenant-id")

        tenant = None
        if subdomain:
            r = await get_redis()
            cache_key = f"tenant:{subdomain}"
            tenant_data = await r.get(cache_key)
            if tenant_data:
                tenant = json.loads(tenant_data)
            else:
                async with MasterSessionLocal() as session:
                    q = await session.execute(select(MasterTenant).where(MasterTenant.subdomain == subdomain))
                    t = q.scalar_one_or_none()
                    if t:
                        tenant = {"id": str(t.id), "db_connection": t.db_connection, "subdomain": t.subdomain}
                        await r.set(cache_key, json.dumps(tenant), ex=300)

        request.state.tenant = tenant

        # ensure tenant sessionmaker exists
        if tenant:
            tenant_id = tenant["id"]
            if tenant_id not in tenant_sessionmakers:
                engine = create_async_engine(tenant["db_connection"], future=True, echo=False)
                tenant_sessionmakers[tenant_id] = async_sessionmaker(engine, expire_on_commit=False)
            request.state.tenant_session = tenant_sessionmakers[tenant_id]
        else:
            request.state.tenant_session = None

        response = await call_next(request)
        return response
