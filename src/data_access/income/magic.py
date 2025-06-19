
from src.schemas.Income import GetScratchCards_Request
from src.utilities.utils import execute_query


def get_scratch_cards(req: GetScratchCards_Request, match_exact_user_id: bool = False):
    res = execute_query("call usp_get_scratch_cards(_user_id => %s, _match_exact_user_id => %s, _between_date => %s::timestamptz[], _magic_income_id => %s, _page_index => %s, _page_size => %s)",
                        (req.user_id, match_exact_user_id, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.magic_income_id, req.page_index, req.page_size))
    return res


def process_magic_income_on_scratch(user_id: str, scratch_card_id: int):
    res = execute_query("call usp_process_magic_income_on_scratch(_user_id => %s, _scratch_card_id => %s)", (user_id, scratch_card_id))
    return res
