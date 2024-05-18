
from src.utilities.utils import execute_query


def login(user_id: str, password: str, url: str, host: str, ip_details):
    res = execute_query("call usp_login(_user_id => %s, _password => %s, _url => %s, _ip_address =>%s, _ip_details => %s::json)", (user_id, password, url, host, ip_details))
    return res


def is_valid_login_id(login_id: str, user_id: str):
    return execute_query("call usp_is_valid_login_id(_login_id => %s, _user_id => %s)", (login_id, user_id))


def can_get_login_token(login_id: str, user_id: str):
    return execute_query("call usp_can_get_login_token(_login_id => %s, _user_id => %s)", (login_id, user_id))


def get_user_id_from_member_id(member_id: int):
    return execute_query("call usp_get_user_id_from_member_id(_member_id => %s)", (member_id, ))
