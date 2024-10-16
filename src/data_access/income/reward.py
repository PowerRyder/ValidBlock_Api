
from src.schemas.Income import GetRankDetails_Request, GetRewardIncome_Request
from src.utilities.utils import execute_query


def get_reward_income(req: GetRewardIncome_Request, match_exact_user_id: bool = False):
    res = execute_query("call usp_get_reward_income(_user_id => %s, _match_exact_user_id => %s, _on_date => %s::timestamptz[], _rank_id => %s, _page_index => %s, _page_size => %s)", 
                        (req.user_id, match_exact_user_id, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.rank_id, req.page_index, req.page_size))
    return res


def get_ranks():
    res = execute_query("call usp_get_ranks()")
    return res


def get_rewards():
    res = execute_query("call usp_get_rewards()")
    return res


def get_rank_details(req: GetRankDetails_Request):
    res = execute_query("call usp_get_rank_details(_user_id => %s, _on_date => %s::timestamptz[], _rank_id => %s, _page_index => %s, _page_size => %s)", 
                        (req.user_id, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.rank_id, req.page_index, req.page_size))
    return res


def get_reward_details(req: GetRankDetails_Request):
    res = execute_query("call usp_get_reward_details(_user_id => %s, _on_date => %s::timestamptz[], _rank_id => %s, _page_index => %s, _page_size => %s)",
                        (req.user_id, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.rank_id, req.page_index, req.page_size))
    return res



def get_reward_qualification_details(req: GetRankDetails_Request):
    res = execute_query("call usp_get_rank_details(_user_id => %s, _on_date => %s::timestamptz[], _rank_id => %s, _page_index => %s, _page_size => %s)",
                        (req.user_id, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.rank_id, req.page_index, req.page_size))
    return res


def get_hong_kong_qualifiers(req: GetRankDetails_Request):
    res = execute_query("call usp_get_hong_kong_qualifiers(_user_id => %s, _between_date => %s::timestamptz[], _page_index => %s, _page_size => %s)",
                        (req.user_id, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.page_index, req.page_size))
    return res


def get_user_rank_qualification_details(user_id: str):
    res = execute_query("call usp_get_user_rank_qualification_details(_user_id => %s)", (user_id, ))
    return res


def get_hong_kong_qualification_details(user_id: str):
    res = execute_query("call usp_get_hong_kong_qualification_details(_user_id => %s)", (user_id, ))
    return res


def get_dubai_qualifiers(req: GetRankDetails_Request):
    res = execute_query("call usp_get_dubai_qualifiers(_user_id => %s, _on_date => %s::timestamptz[], _page_index => %s, _page_size => %s)",
                        (req.user_id, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.page_index, req.page_size))
    return res
