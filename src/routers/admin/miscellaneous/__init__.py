
from fastapi import APIRouter
from .virtual_business import router as virtual_business_router
from .news import router as news_router
from .popup import router as popup_router
from .update_sponsor import router as update_sponsor_router

router = APIRouter(
    prefix="/misc",
    tags=["Misc Settings"]
)

router.include_router(virtual_business_router)
router.include_router(news_router)
router.include_router(popup_router)
router.include_router(update_sponsor_router)
