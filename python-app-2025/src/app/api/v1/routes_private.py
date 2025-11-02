from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.schemas.response import BaseResponse

router = APIRouter(prefix="/private", tags=["private"])


@router.get("/me", summary="Get current user", response_model=BaseResponse[dict])
async def private_me(current_user: dict = Depends(get_current_user)):
    # `get_current_user` returns a lightweight user dict in this scaffold
    return BaseResponse(data={"user": current_user})


@router.get("/secret", summary="Secret data", response_model=BaseResponse[dict])
async def secret(current_user: dict = Depends(get_current_user)):
    return BaseResponse(data={"secret": "only for authenticated users", "username": current_user.get("username")})
