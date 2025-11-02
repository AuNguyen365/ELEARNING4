"""
Standard response models used across the API.

Provides generic wrappers so every endpoint can return a consistent shape:

    {
      "success": true,
      "message": "Optional human-readable message",
      "data": ...,
      "meta": { ... }
    }

Designed to work with Pydantic v2 and FastAPI.
"""
from __future__ import annotations

from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel


T = TypeVar("T")


class Meta(BaseModel):
    total: Optional[int] = None
    page: Optional[int] = None
    size: Optional[int] = None


class BaseResponse(GenericModel, Generic[T]):
    success: bool = True
    message: Optional[str] = None
    data: Optional[T] = None
    meta: Optional[Meta] = None


class ListResponse(BaseResponse[List[T]], Generic[T]):
    data: List[T] = []


class ErrorResponse(BaseModel):
    success: bool = False
    message: Optional[str] = None
    detail: Optional[str] = None
    code: Optional[int] = None
