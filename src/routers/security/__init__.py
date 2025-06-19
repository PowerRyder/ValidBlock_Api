
from fastapi import APIRouter
from .two_factor_auth import router as twoFA
from .change_password import router as change_pass
from .setup_pin import router as setup_pin

router = APIRouter(
    prefix="/security"
)

router.include_router(twoFA)
router.include_router(change_pass)
router.include_router(setup_pin)
