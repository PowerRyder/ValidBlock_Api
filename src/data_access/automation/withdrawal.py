from src.utilities.utils import execute_query


def reject_pending_withdrawals(timestamp: int):
    res = execute_query("call usp_reject_pending_withdrawals(_timestamp => %s)", (timestamp, ))
    return res
