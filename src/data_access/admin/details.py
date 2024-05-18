
from src.utilities.utils import execute_query


def get_admin_details(admin_user_id: str):
    res = execute_query("call usp_get_admin_details(_admin_user_id => %s)", (admin_user_id,))
    return res

    
def get_admin_dashboard_details(admin_user_id: str):
    res = execute_query("call usp_get_admin_dashboard_details(_admin_user_id => %s)", (admin_user_id,))
    return res


def get_admin_dashboard_chart_details(duration: str):
    res = execute_query("call usp_get_admin_dashboard_chart_details(_duration => %s)", (duration, ))
    return res


def get_top_earners(page_index: int = 0, page_size: int = 10):
    res = execute_query("call usp_get_top_earners(_page_index => %s, _page_size => %s)", (page_index, page_size))
    return res
