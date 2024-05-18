from src.schemas.ArbitrageTrade import GetArbitrageTradeHistory
from src.utilities.utils import execute_query


def get_trade_history(req: GetArbitrageTradeHistory, match_exact_user_id: bool):
    res = execute_query("call usp_get_arbitrage_trade_history(_user_id => %s, _match_exact_user_id => %s, _token_id => %s, _between_date => %s::timestamptz[], _page_index => %s, _page_size => %s)",
                        (req.user_id, match_exact_user_id, req.token_id, [req.date_from if req.date_from != '' else None, req.date_to if req.date_to != '' else None], req.page_index, req.page_size))
    return res


def get_top_trades():
    res = execute_query("call usp_get_artbitrage_top_trades()")
    return res

