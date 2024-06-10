
from pydantic import BaseModel

from src.constants import VALIDATORS


class WithdrawFund(BaseModel):
    token_id: int = 0
    wallet_id: int
    amount: float
    remarks: str = ''
    two_factor_auth_request_id: str = ''
    wallet_address: str = ''


class GetWithdrawalRequests(BaseModel):
    user_id: str
    user_type: str = VALIDATORS.USER_TYPE_ALL
    date_from: str = ''
    date_to: str = ''
    status: str = 'All'
    page_index: int
    page_size: int


class WithdrawalRequestApproveRejectDataItem(BaseModel):
    RequestId: int
    Remarks: str = ''
    Status: str = VALIDATORS.STATUS_APPROVED_REJECTED
    TxnHash: str = ''


class WithdrawPrinciple(BaseModel):
    token_id: int = 0
    remarks: str = ''
    two_factor_auth_request_id: str = ''
    wallet_address: str = ''



class GetPrincipleWithdrawalRequests(BaseModel):
    user_id: str
    date_from: str = ''
    date_to: str = ''
    status: str = 'All'
    page_index: int
    page_size: int
