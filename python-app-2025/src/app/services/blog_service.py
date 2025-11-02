from typing import List, Optional
from sqlalchemy.orm import Session
from app.schemas.blog import BlogCreate, BlogUpdate
from app.db import models


class BlogService:
    def create_blog(self, db: Session, payload: BlogCreate, author_id: Optional[int] = None) -> models.Blog:
        tags = ",".join(payload.tags or []) if payload.tags else None
        blog = models.Blog(
            title=payload.title,
            content=payload.content,
            tags=tags,
            author_id=author_id,
        )
        db.add(blog)
        db.commit()
        db.refresh(blog)
        return blog

    def get_blog(self, db: Session, blog_id: int) -> Optional[models.Blog]:
        return db.query(models.Blog).filter(models.Blog.id == blog_id).first()

    def update_blog(self, db: Session, blog_id: int, payload: BlogUpdate) -> Optional[models.Blog]:
        blog = self.get_blog(db, blog_id)
        if not blog:
            return None
        if payload.title is not None:
            blog.title = payload.title
        if payload.content is not None:
            blog.content = payload.content
        if payload.tags is not None:
            blog.tags = ",".join(payload.tags)
        db.add(blog)
        db.commit()
        db.refresh(blog)
        return blog

    def delete_blog(self, db: Session, blog_id: int) -> bool:
        blog = self.get_blog(db, blog_id)
        if not blog:
            return False
        db.delete(blog)
        db.commit()
        return True

    def list_blogs(
        self,
        db: Session,
        q: Optional[str] = None,
        sort: Optional[str] = None,
        order: str = "desc",
        skip: int = 0,
        limit: int = 10,
    ) -> List[models.Blog]:
        query = db.query(models.Blog)
        if q:
            ql = f"%{q}%"
            query = query.filter((models.Blog.title.ilike(ql)) | (models.Blog.content.ilike(ql)))
        if sort:
            col = getattr(models.Blog, sort, None)
            if col is not None:
                if order.lower() == "asc":
                    query = query.order_by(col.asc())
                else:
                    query = query.order_by(col.desc())
        return query.offset(skip).limit(limit).all()

    def set_image(self, db: Session, blog_id: int, image_path: str) -> Optional[models.Blog]:
        blog = self.get_blog(db, blog_id)
        if not blog:
            return None
        blog.image = image_path
        db.add(blog)
        db.commit()
        db.refresh(blog)
        return blog
