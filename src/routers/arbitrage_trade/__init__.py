
from fastapi import APIRouter
from .trade import router as trade_router
from .details import router as details_router


router = APIRouter(
    prefix="/arbitrage",
    tags=["Arbitrage Trade"]
)

router.include_router(trade_router)
router.include_router(details_router)
