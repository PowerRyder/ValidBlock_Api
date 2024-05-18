
from fastapi import APIRouter
from .withdrawal import router as withdrawal_router

router = APIRouter(
    prefix="/withdrawal",
    tags=["Withdrawal"]
)

router.include_router(withdrawal_router)
