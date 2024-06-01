from src.schemas.Topup import GetRequestsForValidator
from src.utilities.utils import execute_query


def request_for_validator(user_id: str, package_id: int, wallet_id: int):
    res = execute_query("call usp_request_for_validator(_user_id => %s, _package_id => %s, _wallet_id => %s)",
                        (user_id, package_id, wallet_id))
    return res


def vote_for_validator(validator_user_id: str, by_user_id: str):
    res = execute_query("call usp_vote_for_validator(_validator_user_id => %s, _by_user_id => %s)",
                        (validator_user_id, by_user_id))
    return res


def get_requests_for_validator(req: GetRequestsForValidator, match_exact_user_id: bool):
    res = execute_query("call usp_get_requests_for_validator(_user_id => %s, _match_exact_user_id => %s, "
                        "_request_date => %s::timestamptz[], _status => %s, _page_index => %s, _page_size => %s)",
                        (req.user_id, match_exact_user_id, [req.date_from if req.date_from != '' else None, req.date_to if req.date_to != '' else None], req.status, req.page_index, req.page_size))
    return res


def update_request_for_validator(request_id: int, status: str, remarks: str, by_user_id: str):
    res = execute_query("call usp_update_validator_request_status(_request_id => %s, _status => %s, _remarks => %s, _by_admin_user_id => %s)",
                        (request_id, status, remarks, by_user_id))
    return res


def update_validator_package_discount_percentage(percentage: float, by_user_id: str):
    res = execute_query("call usp_update_validator_package_discount_percentage(_percentage => %s, _by_admin_id => %s)",
                        (percentage, by_user_id))
    return res
