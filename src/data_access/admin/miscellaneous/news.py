
from src.schemas.Admin_Miscellaneous import AddNews
from src.utilities.utils import execute_query


def add_news(req: AddNews, admin_user_id: str):
    res = execute_query("call usp_add_news(_news_id => %s, _user_type => %s, _heading => %s, _details => %s, _priority => %s, _admin_user_id => %s)",
    (req.news_id, req.user_type, req.heading, req.details, req.priority, admin_user_id))
    return res


def get_news(page_index: int, page_size: int):
    res = execute_query("call usp_get_news(_page_index => %s, _page_size => %s)", (page_index, page_size))
    return res


def delete_news(news_id: int):
    res = execute_query("call usp_delete_news(_news_id => %s)", (news_id, ))
    return res
