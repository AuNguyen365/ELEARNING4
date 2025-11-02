from fastapi import APIRouter
from app.schemas.response import BaseResponse

router = APIRouter(tags=["public"])


@router.get("/health", summary="Health check", response_model=BaseResponse[dict])
async def health():
    return BaseResponse(data={"status": "healthy"}, message="OK")


@router.get("/open", summary="Public endpoint", response_model=BaseResponse[dict])
async def open_endpoint():
    return BaseResponse(data={"message": "This is a public endpoint"})
