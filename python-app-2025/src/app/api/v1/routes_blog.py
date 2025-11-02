from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from typing import List, Optional
import os
from sqlalchemy.orm import Session

from app.schemas.blog import BlogCreate, BlogUpdate
from app.schemas.response import BaseResponse
from app.services.blog_service import BlogService
from app.core.security import get_current_user
from app.core.config import settings
from app.db.session import get_db

router = APIRouter(prefix="/blogs", tags=["blogs"])

# Use a single service instance
blog_service = BlogService()


@router.post("/", response_model=BaseResponse[dict])
async def create_blog(payload: BlogCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    author_username = current_user.get("username")
    # find author id (if exists)
    from app.services.user_service import UserService

    user_svc = UserService()
    author = user_svc.get_user_by_username(db, author_username)
    author_id = author.id if author else None
    blog = blog_service.create_blog(db, payload, author_id=author_id)
    return BaseResponse(data={"id": blog.id, "title": blog.title}, message="Blog created")


@router.get("/", response_model=BaseResponse[List[dict]])
async def list_blogs(
    q: Optional[str] = Query(None),
    sort: Optional[str] = Query(None),
    order: str = Query("desc"),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    skip = (page - 1) * size
    items = blog_service.list_blogs(db, q=q, sort=sort, order=order, skip=skip, limit=size)
    # convert tags to list
    result = []
    for b in items:
        tags = b.tags.split(",") if b.tags else []
        result.append({"id": b.id, "title": b.title, "tags": tags, "author_id": b.author_id})
    meta = {"page": page, "size": size, "total": len(result)}
    return BaseResponse(data=result, meta=meta)


@router.get("/{blog_id}", response_model=BaseResponse[dict])
async def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = blog_service.get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    tags = blog.tags.split(",") if blog.tags else []
    return BaseResponse(data={"id": blog.id, "title": blog.title, "content": blog.content, "tags": tags, "image": blog.image})


@router.put("/{blog_id}", response_model=BaseResponse[dict])
async def update_blog(blog_id: int, payload: BlogUpdate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    blog = blog_service.update_blog(db, blog_id, payload)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return BaseResponse(data={"id": blog.id, "title": blog.title}, message="Updated")


@router.delete("/{blog_id}", response_model=BaseResponse[dict])
async def delete_blog(blog_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    ok = blog_service.delete_blog(db, blog_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Blog not found")
    return BaseResponse(data={"id": blog_id}, message="Deleted")


@router.post("/{blog_id}/upload", response_model=BaseResponse[dict])
async def upload_image(blog_id: int, file: UploadFile = File(...), current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    blog = blog_service.get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    uploads_dir = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "uploads")
    uploads_dir = os.path.abspath(uploads_dir)
    os.makedirs(uploads_dir, exist_ok=True)

    filename = f"blog_{blog_id}_{file.filename}"
    dest_path = os.path.join(uploads_dir, filename)
    with open(dest_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # store relative path
    rel_path = os.path.relpath(dest_path, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
    blog = blog_service.set_image(db, blog_id, rel_path)
    return BaseResponse(data={"path": rel_path}, message="Uploaded")
