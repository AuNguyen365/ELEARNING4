"""
Common request models (pagination / query) so endpoints can accept a consistent shape.

These are lightweight helpers. Individual endpoints can still declare their own request
models when necessary.
"""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class Pagination(BaseModel):
    page: int = 1
    size: int = 20


class QueryParams(BaseModel):
    q: Optional[str] = None
    page: int = 1
    size: int = 20


class LoginRequest(BaseModel):
    username: str
    password: str
