from typing import Optional
from sqlalchemy.orm import Session
from app.core.security import verify_password
from app.services.user_service import UserService


class AuthService:
    def __init__(self):
        self.user_service = UserService()

    def authenticate_user(self, db: Session, username: str, password: str) -> Optional[object]:
        user = self.user_service.get_user_by_username(db, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
