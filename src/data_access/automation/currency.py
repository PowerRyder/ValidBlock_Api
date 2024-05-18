from src.utilities.utils import execute_query


def update_currency_rates(_rates):
    res = execute_query("call usp_update_currency_rates(_rates => %s)", (_rates, ))
    return res

