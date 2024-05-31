
from fastapi import APIRouter
from .topup import router as topup_router
from .crypto_deposit import router as crypto_deposit_router
from .validator import router as validator_router


router = APIRouter(
    prefix="/topup",
    tags=["Topup"]
)

router.include_router(topup_router)
router.include_router(crypto_deposit_router)
router.include_router(validator_router)

