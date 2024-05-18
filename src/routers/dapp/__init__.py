
from fastapi import APIRouter
from .dapp import router as dapp_router

router = APIRouter(
    prefix="/dapp",
    tags=["DApp"]
)

router.include_router(dapp_router)
