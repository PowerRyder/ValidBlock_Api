from src.utilities.utils import execute_query


def reject_pending_withdrawals(timestamp: int):
    res = execute_query("call usp_reject_pending_withdrawals(_timestamp => %s)", (timestamp, ))
    return res


def get_withdrawal_queue():
    res = execute_query("call usp_get_withdrawal_queue()")
    return res


def update_withdrawal_queue_status(queue_id: int, status: str, txn_hash: str):
    res = execute_query("call usp_update_withdrawal_queue_status(_queue_id => %s, _status => %s, _txn_hash => %s)",
                        (queue_id, status, txn_hash))
    return res


def update_withdrawal_queue_batch_status(batch_id: int):
    res = execute_query("call usp_update_withdrawal_queue_batch_status(_batch_id => %s)", (batch_id, ))
    return res
