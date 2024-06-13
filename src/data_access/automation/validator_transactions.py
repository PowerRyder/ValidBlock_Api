from src.utilities.utils import execute_query


def save_bsc_validator_transactions(transactions):
    res = execute_query("call usp_save_bsc_validator_transactions(_transactions => %s::jsonb)", (transactions, ))
    return res


def save_solana_validator_transactions(transactions):
    res = execute_query("call usp_save_solana_validator_transactions(_transactions => %s::jsonb)", (transactions, ))
    return res

