from pydantic import BaseModel

from src.constants import VALIDATORS


class AddNews(BaseModel):
    news_id: int = 0
    user_type: str = VALIDATORS.USER_TYPE_ALL
    heading: str
    details: str
    priority: int = 1


class AddPopup(BaseModel):
    user_type: str = VALIDATORS.USER_TYPE_ALL
    image_base_64: str = VALIDATORS.REQUIRED
