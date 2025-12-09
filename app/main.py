from fastapi import FastAPI
from app.api.v1 import auth, health, tenants, staff_role, staff_user, support, auth_accounts, payment_methods, plans, rooms, subscriptions, system_logs

app = FastAPI(title="StayDoma API", version="1.0.0")
app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(tenants.router, prefix="/api/v1")
app.include_router(staff_role.router, prefix="/api/v1")
app.include_router(staff_user.router, prefix="/api/v1")
app.include_router(plans.router, prefix="/api/v1")
app.include_router(payment_methods.router, prefix="/api/v1")
app.include_router(subscriptions.router, prefix="/api/v1")
app.include_router(support.router, prefix="/api/v1")
app.include_router(system_logs.router, prefix="/api/v1")
app.include_router(auth_accounts.router, prefix="/api/v1")
