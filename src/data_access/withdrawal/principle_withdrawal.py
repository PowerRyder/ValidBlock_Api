from decimal import Decimal

from src.schemas.Withdrawal import WithdrawPrinciple
from src.utilities.utils import execute_query


def get_details_for_principle_withdrawal(user_id: str):
    res = execute_query("call usp_get_details_for_principle_withdrawal(_user_id => %s)", (user_id, ))
    return res


def withdraw_principle(req: WithdrawPrinciple, user_id: str, token_rate: Decimal):
    res = execute_query("call usp_withdraw_principle(_user_id => %s, _remarks => %s, _two_factor_auth_request_id => %s, _token_id => %s, _token_rate > %s, _withdrawal_address => %s)",
    (user_id, req.remarks, req.two_factor_auth_request_id, req.token_id, token_rate, req.wallet_address))
    return res


def update_principle_withdrawal_request_status(request_id: int, status: str, txn_hash: str):
    res = execute_query("call usp_update_principle_withdrawal_request_status(_request_id => %s, _status => %s, _txn_hash => %s)",
    (request_id, status, txn_hash))
    return res
