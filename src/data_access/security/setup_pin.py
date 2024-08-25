from src.utilities.utils import execute_query


def set_pin(user_id: str, pin: str, two_factor_auth_request_id: int = 0):
    res = execute_query(
        "call usp_set_pin(_user_id => %s, _pin => %s, _two_factor_auth_request_id => %s)",
        (user_id, pin, two_factor_auth_request_id))
    return res
