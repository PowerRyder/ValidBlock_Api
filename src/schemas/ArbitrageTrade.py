from pydantic import BaseModel


class GetArbitrageTradeHistory(BaseModel):
    user_id: str = ''
    date_from: str = ''
    date_to: str = ''
    token_id: int = 0
    page_index: int = 0
    page_size: int = 100
