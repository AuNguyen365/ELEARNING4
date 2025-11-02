from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.schemas.user import UserCreate
from app.services.user_service import UserService
from app.schemas.response import BaseResponse
from app.db.session import get_db

router = APIRouter(prefix="/users", tags=["users"])

user_service = UserService()


@router.post("/", response_model=BaseResponse[dict])
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
	db_user = user_service.create_user(db, user)
	return BaseResponse(data={"id": db_user.id, "email": db_user.email, "username": db_user.username}, message="User created")


@router.get("/", response_model=BaseResponse[List[dict]])
async def read_users(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
	users = user_service.get_users(db)
	# Do not return hashed passwords
	safe = [{"id": u.id, "email": u.email, "username": u.username} for u in users]
	return BaseResponse(data=safe)

