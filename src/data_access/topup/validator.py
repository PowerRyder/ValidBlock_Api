
from src.utilities.utils import execute_query


def request_for_validator(user_id: str, package_id: int, wallet_id: int):
    res = execute_query("call usp_request_for_validator(_user_id => %s, _package_id => %s, _wallet_id => %s)",
                        (user_id, package_id, wallet_id))
    return res


def vote_for_validator(validator_user_id: str, by_user_id: str):
    res = execute_query("call usp_vote_for_validator(_validator_user_id => %s, _by_user_id => %s)",
                        (validator_user_id, by_user_id))
    return res
