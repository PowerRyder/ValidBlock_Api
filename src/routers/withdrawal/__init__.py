
from fastapi import APIRouter
from .withdrawal import router as withdrawal_router
from .principle_withdrawal import router as principle_withdrawal_router

router = APIRouter(
    prefix="/withdrawal",
    tags=["Withdrawal"]
)

router.include_router(withdrawal_router)
router.include_router(principle_withdrawal_router)
