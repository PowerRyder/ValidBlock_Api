from src.utilities.utils import execute_query


def get_bsc_validator_transactions(page_index: int, page_size: int):
    res = execute_query("call usp_get_bsc_validator_transactions(_page_index =>%s, _page_size => %s)",
                        (page_index, page_size))
    return res


def get_solana_validator_transactions(page_index: int, page_size: int):
    res = execute_query("call usp_get_solana_validator_transactions(_page_index =>%s, _page_size => %s)",
                        (page_index, page_size))
    return res
