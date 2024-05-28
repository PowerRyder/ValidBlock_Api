
from src.utilities.utils import execute_query


def request_for_validator(user_id: str, package_id: int, wallet_id: int):
    res = execute_query("call usp_request_for_validator(_user_id => %s, _package_id => %s, _wallet_id => %s)",
                        (user_id, package_id, wallet_id))
    return res
