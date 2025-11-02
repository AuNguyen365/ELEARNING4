from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    content: str
    tags: Optional[list[str]] = []


class BlogCreate(BlogBase):
    pass


class BlogUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[list[str]] = None


class BlogOut(BlogBase):
    id: int
    author: Optional[str] = None
    image: Optional[str] = None

    class Config:
        from_attributes = True
