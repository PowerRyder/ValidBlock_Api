
from src.utilities.utils import execute_query


def get_user_details(user_id:str):
    res = execute_query("call usp_get_user_details(_user_id => %s)", (user_id,))
    return res

    
def get_user_dashboard_details(user_id:str):
    res = execute_query("call usp_get_user_dashboard_details(_user_id => %s)", (user_id,))
    return res


def get_user_dashboard_chart_details(user_id:str, duration: str):
    res = execute_query("call usp_get_user_dashboard_chart_details(_user_id => %s, _duration => %s)", (user_id, duration))
    return res


def get_user_rank_details(user_id:str):
    res = execute_query("call usp_get_member_rank_details(_user_id => %s)", (user_id,))
    return res


def get_user_reward_qualification_details(user_id:str):
    res = execute_query("call usp_get_member_reward_qualification_details(_user_id => %s)", (user_id,))
    return res


def update_pol_address(user_id:str, pol_address: str, by_user_id: str, by_user_type: str):
    res = execute_query("call usp_update_user_pol_address(_user_id => %s, _by_user_id => %s, _by_user_type => %s, _pol_address => %s)",
                        (user_id, by_user_id, by_user_type, pol_address))
    return res
