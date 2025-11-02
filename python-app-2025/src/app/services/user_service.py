from typing import Optional, List
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from app.db import models


class UserService:
    def create_user(self, db: Session, user: UserCreate) -> models.User:
        hashed = get_password_hash(user.password)
        db_user = models.User(
            email=user.email,
            username=user.username,
            hashed_password=hashed,
            is_active=True,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def get_user_by_username(self, db: Session, username: str) -> Optional[models.User]:
        return db.query(models.User).filter(models.User.username == username).first()

    def get_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
        return db.query(models.User).offset(skip).limit(limit).all()
