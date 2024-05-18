
from src.schemas.Admin_Miscellaneous import AddNews
from src.utilities.utils import execute_query


def update_sponsor(user_id: str, sponsor_id: str, admin_user_id: str):
    res = execute_query("call usp_update_sponsor(_user_id => %s, _sponsor_user_id => %s, _admin_user_id => %s)",
    (user_id, sponsor_id, admin_user_id))
    return res


def get_sponsor_update_history(page_index: int, page_size: int):
    res = execute_query("call usp_get_sponsor_update_history(_page_index => %s, _page_size => %s)", (page_index, page_size))
    return res
