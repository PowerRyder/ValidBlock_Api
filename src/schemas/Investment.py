from pydantic import BaseModel

from src.constants import VALIDATORS


class PaymentInfo(BaseModel):
    amount: float = VALIDATORS.REQUIRED
    payment_mode: str = VALIDATORS.REQUIRED
    reference_number: str = VALIDATORS.REQUIRED
    image: str = VALIDATORS.REQUIRED
    remarks: str = ''
