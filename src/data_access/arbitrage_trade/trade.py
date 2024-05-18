from decimal import Decimal

from src.schemas.ArbitrageTrade import GetArbitrageTradeHistory
from src.utilities.utils import execute_query


def get_arbitrage_tokens():
    res = execute_query("call usp_get_arbitrage_tokens()")
    return res


def get_trade_pairs(user_id: str):
    res = execute_query("call usp_get_arbitrage_trade_pairs(_user_id => %s)", (user_id, ))
    return res


def request_arbitrage_trade(user_id: str, user_address: str, from_token_symbol: str, to_token_symbol: str, amount: Decimal):
    res = execute_query("call usp_request_arbitrage_trade(_user_id => %s, _user_address => %s, _from_token_symbol => %s, _to_token_symbol => %s, _amount => %s)",
                        (user_id, user_address, from_token_symbol, to_token_symbol, amount))
    return res


def update_trade_status(request_id: int, txn_hash: str, status: str):
    res = execute_query("call usp_update_arbitrage_trade_status(_request_id => %s, _txn_hash => %s, _status => %s)",
                        (request_id, txn_hash, status))
    return res

