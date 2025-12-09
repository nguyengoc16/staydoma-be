# app/core/security.py
from __future__ import annotations
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import jwt, JWTError
from pathlib import Path
import uuid
import json

from app.core.config import settings
import redis.asyncio as redis  # redis-py asyncio

# load keys lazily
_PRIVATE_KEY: Optional[str] = None
_PUBLIC_KEY: Optional[str] = None

def _load_private_key() -> str:
    global _PRIVATE_KEY
    if _PRIVATE_KEY is None:
        _PRIVATE_KEY = Path(settings.JWT_PRIVATE_KEY_PATH).read_text()
    return _PRIVATE_KEY

def _load_public_key() -> str:
    global _PUBLIC_KEY
    if _PUBLIC_KEY is None:
        _PUBLIC_KEY = Path(settings.JWT_PUBLIC_KEY_PATH).read_text()
    return _PUBLIC_KEY

def make_jti() -> str:
    return uuid.uuid4().hex

def create_access_token(subject: str, *, expires_minutes: Optional[int] = None, extra_claims: Optional[Dict[str,Any]] = None) -> Dict[str,Any]:
    now = datetime.utcnow()
    expires = now + timedelta(minutes=(expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    jti = make_jti()
    payload = {
        "sub": str(subject),
        "iat": int(now.timestamp()),
        "exp": int(expires.timestamp()),
        "jti": jti,
        "typ": "access",
    }
    if extra_claims:
        payload.update(extra_claims)
    token = jwt.encode(payload, _load_private_key(), algorithm=settings.JWT_ALGORITHM)
    return {"token": token, "jti": jti, "expires_at": int(expires.timestamp())}

def create_refresh_token(subject: str, *, expires_days: Optional[int] = None) -> Dict[str,Any]:
    now = datetime.utcnow()
    expires = now + timedelta(days=(expires_days or settings.REFRESH_TOKEN_EXPIRE_DAYS))
    jti = make_jti()
    payload = {
        "sub": str(subject),
        "iat": int(now.timestamp()),
        "exp": int(expires.timestamp()),
        "jti": jti,
        "typ": "refresh",
    }
    token = jwt.encode(payload, _load_private_key(), algorithm=settings.JWT_ALGORITHM)
    return {"token": token, "jti": jti, "expires_at": int(expires.timestamp())}

def decode_token(token: str) -> Dict[str,Any]:
    try:
        data = jwt.decode(token, _load_public_key(), algorithms=[settings.JWT_ALGORITHM])
        return data
    except JWTError as e:
        raise

# Redis helpers: blacklist access tokens and store refresh tokens
_redis_client: Optional[redis.Redis] = None

def get_redis() -> redis.Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis_client

async def blacklist_token(jti: str, expires_at_ts: int) -> None:
    """Store jti in redis blacklist with TTL until expires_at"""
    r = get_redis()
    ttl = max(0, expires_at_ts - int(datetime.utcnow().timestamp()))
    if ttl <= 0:
        return
    # key design: "jwt:blacklist:{jti}"
    await r.setex(f"jwt:blacklist:{jti}", ttl, "1")

async def is_token_blacklisted(jti: str) -> bool:
    r = get_redis()
    v = await r.get(f"jwt:blacklist:{jti}")
    return v is not None

async def store_refresh_token(user_id: str, refresh_jti: str, expires_at_ts: int) -> None:
    r = get_redis()
    ttl = max(0, expires_at_ts - int(datetime.utcnow().timestamp()))
    key = f"refresh:{user_id}:{refresh_jti}"
    await r.setex(key, ttl, "1")

async def check_refresh_token(user_id: str, refresh_jti: str) -> bool:
    r = get_redis()
    key = f"refresh:{user_id}:{refresh_jti}"
    v = await r.get(key)
    return v is not None

async def revoke_refresh_token(user_id: str, refresh_jti: str):
    r = get_redis()
    key = f"refresh:{user_id}:{refresh_jti}"
    await r.delete(key)
