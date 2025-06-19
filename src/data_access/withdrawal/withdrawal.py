from decimal import Decimal

from src.schemas.Withdrawal import GetWithdrawalRequests, WithdrawFund
from src.utilities.utils import execute_query


def withdraw_fund(req: WithdrawFund, user_id: str, user_type: str, token_rate: Decimal):
    res = execute_query("call usp_withdraw_fund(_user_id => %s, _user_type => %s,_wallet_id => %s, _amount => %s, "
                        "_remarks => %s, _two_factor_auth_request_id => %s, _token_id => %s, _token_rate => %s, "
                        "_withdrawal_address => %s)",
    (user_id, user_type, req.wallet_id, req.amount, req.remarks, req.two_factor_auth_request_id, req.token_id, token_rate, req.wallet_address))
    return res


def get_withdrawal_requests(req: GetWithdrawalRequests, match_exact_user_id: bool):
    res = execute_query("call usp_get_withdrawal_requests(_user_id => %s, _user_type => %s, _match_exact_user_id => %s, _request_date => %s::timestamptz[], _status => %s, _page_index => %s, _page_size => %s)",
                        (req.user_id, req.user_type, match_exact_user_id, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.status, req.page_index, req.page_size))
    return res


def update_withdrawal_requests_status(by_user_id: str, data_dicts):
    res = execute_query("call usp_update_withdrawal_request_status(_by_user_id => %s, _data => %s::jsonb)",
                        (by_user_id, data_dicts))
    return res


def save_withdrawal_transaction(txn_hash: str, to_address: str, amount: Decimal):
    res = execute_query("call usp_save_withdrawal_transaction(_txn_hash => %s, _to_address => %s, _amount => %s)",
                        (txn_hash, to_address, amount))
    return res
