
from fastapi import APIRouter
from .transactions import router as transactions_router

router = APIRouter(
    prefix="/validator",
    tags=["Validator"]
)

router.include_router(transactions_router)
