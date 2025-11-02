from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.services.auth_service import AuthService
from app.core.security import create_access_token, oauth2_scheme
from app.core import globals as app_globals
from app.schemas.response import BaseResponse
from app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=BaseResponse[dict])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	auth_service = AuthService()
	user = auth_service.authenticate_user(db, form_data.username, form_data.password)
	if not user:
		return BaseResponse(success=False, message="Invalid credentials")
	access_token = create_access_token(data={"sub": user.username})
	return BaseResponse(data={"access_token": access_token, "token_type": "bearer"})


@router.post("/logout", response_model=BaseResponse[dict])
async def logout(token: str = Depends(oauth2_scheme)):
	# Add token to blacklist
	app_globals.blacklist_token(token)
	return BaseResponse(data={}, message="Logged out")

