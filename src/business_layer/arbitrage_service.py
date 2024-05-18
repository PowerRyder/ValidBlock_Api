import json
from web3 import Web3
from src.data_access.arbitrage_trade import trade as data_access
from src.constants.messages import DATABASE_CONNECTION_ERROR
from src.utilities.utils import config


def decode_input_data_for_request_id(input_data):
    arbitrage_config = config['ArbitrageTrade']
    with open(arbitrage_config['AbiJsonPath']) as f:
        contract_abi = json.load(f)

    w3 = Web3()
    contract = w3.eth.contract(abi=contract_abi)

    function_signature, function_params = contract.decode_function_input(input_data)

    function_name = function_signature.function_identifier

    if function_name == 'InitiateTrade':
        request_id = function_params['nonce']
        return request_id

    raise Exception('Invalid method!')


def update_trade_transaction_status(request_id: int, txn_hash: str, status: str):
    if status == 'Success':
        dataset = data_access.update_trade_status(request_id=request_id, txn_hash=txn_hash, status=status)

        if len(dataset) > 0 and len(dataset['rs']):
            return {'success': bool(dataset['rs'].iloc[0]['success']), 'message': dataset['rs'].iloc[0]['message']}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    else:
        dataset = data_access.update_trade_status(request_id=request_id, txn_hash=txn_hash, status=status)

        if len(dataset) > 0 and len(dataset['rs']):
            return {'success': bool(dataset['rs'].iloc[0]['success']), 'message': dataset['rs'].iloc[0]['message']}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
