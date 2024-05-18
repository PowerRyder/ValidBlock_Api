from decimal import Decimal

from src.utilities.utils import execute_query


def topup_through_dapp(user_address: str, txn_hash: str, package_id: int, amount: Decimal):
    res = execute_query("call usp_topup_through_dapp(_user_id => %s, _package_id => %s, _pin_value => %s, "
                        "_txn_hash => %s, _by_user_id => %s, _by_user_type => %s)",
                        (user_address, package_id, amount, txn_hash, user_address, 'User'))
    return res
