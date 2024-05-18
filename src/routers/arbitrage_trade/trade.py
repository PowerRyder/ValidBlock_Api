import time
from decimal import Decimal

from fastapi import APIRouter, Depends
from web3 import Web3

from src.business_layer.arbitrage_service import decode_input_data_for_request_id, update_trade_transaction_status
from src.business_layer.security.Jwt import get_current_user
from src.business_layer.security.RightsChecker import RightsChecker
from src.constants.messages import OK, DATABASE_CONNECTION_ERROR
from src.data_access.arbitrage_trade import trade as data_access
from src.utilities.utils import get_error_message, data_frame_to_json_object, config, amount_in_smallest_unit

router = APIRouter()


@router.get('/get_arbitrage_tokens')
def get_arbitrage_tokens():
    try:
        dataset = data_access.get_arbitrage_tokens()
        if len(dataset) > 0:
            if len(dataset['rs']) > 0:
                ds = dataset['rs']
                return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds)}

            return {'success': False, 'message': 'No tokens supported!'}
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_trade_pairs', dependencies=[Depends(RightsChecker([222]))])
def get_trade_pairs(token_payload: any = Depends(get_current_user)):
    try:
        user_id_token = token_payload["user_id"]
        dataset = data_access.get_trade_pairs(user_id=user_id_token)
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds)}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_trade_data', dependencies=[Depends(RightsChecker([222]))])
def get_trade_data(user_address: str, from_token_symbol: str, to_token_symbol: str, amount: Decimal, token_payload: any = Depends(get_current_user)):
    try:
        user_id_token = token_payload["user_id"]
        user_address = Web3.to_checksum_address(user_address)
        # print(user_id_token, user_address, from_token_symbol, to_token_symbol, amount)
        dataset = data_access.request_arbitrage_trade(user_id=user_id_token,
                                                      user_address=user_address,
                                                      from_token_symbol=from_token_symbol,
                                                      to_token_symbol=to_token_symbol,
                                                      amount=amount)
        if len(dataset) > 0 and len(dataset['rs']):
            dr = dataset['rs'].iloc[0]

            if not dr['success']:
                return {'success': False, 'message': dr['message']}

            w3 = Web3()

            config_data = config['ArbitrageTrade']
            private_key = config_data['PrivateKey']
            # account = w3.eth.account.privateKeyToAccount(private_key)

            contract_address = Web3.to_checksum_address(config_data['ContractAddress'])
            token_address = Web3.to_checksum_address(dr['from_token_address'])
            amount = amount_in_smallest_unit(amount=amount, decimals=dr['from_token_decimals'])
            dex_list = [1, 3]
            pairs = [Web3.to_checksum_address(dr['from_token_address']), Web3.to_checksum_address(dr['to_token_address']), Web3.to_checksum_address(dr['from_token_address'])]
            profit = amount_in_smallest_unit(amount=dr['profit'], decimals=dr['from_token_decimals'])
            timestamp = int(time.time() + 60)
            nonce = int(dr['request_id'])

            # print([contract_address, user_address, token_address, amount, dex_list, pairs, profit, timestamp, nonce])
            message_hash = Web3.solidity_keccak(
                ['bytes'],
                [Web3.to_bytes(text='\x19Ethereum Signed Message:\n32') +
                 Web3.solidity_keccak(
                     ['address', 'address', 'address', 'uint256', 'uint8[]', 'address[]', 'uint256', 'uint256', 'uint256'],
                     [contract_address, user_address, token_address, amount, dex_list, pairs, profit, timestamp, nonce])]
            )

            signed_message = w3.eth.account.signHash(message_hash, private_key=private_key)

            return_data = {
                'success': True,
                'message': OK,
                'data': {
                    'contract_address': contract_address,
                    'user_address': user_address,
                    'token_address': token_address,
                    'amount': str(amount),
                    'from_token_symbol': from_token_symbol,
                    'from_token_decimals': int(dr['from_token_decimals']),
                    'dex_list': dex_list,
                    'pairs': pairs,
                    'profit': str(profit),
                    'timestamp': str(timestamp),
                    'nonce': str(nonce),
                    'signature': signed_message.signature.hex()
                }}
            # print(return_data)
            return return_data

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/update_trade_status', dependencies=[Depends(RightsChecker([222]))])
def update_trade_status(txn_hash):
    try:

        w3 = Web3(Web3.HTTPProvider('https://rpc-mainnet.matic.quiknode.pro'))

        retry_count = 1
        while retry_count <= 10:
            receipt = w3.eth.get_transaction_receipt(txn_hash)

            if receipt is not None:
                tx = w3.eth.get_transaction(txn_hash)
                request_id = decode_input_data_for_request_id(input_data=tx['input'])
                return update_trade_transaction_status(request_id=request_id, txn_hash=txn_hash, status=('Success' if receipt.status == 1 else 'Failed'))

            time.sleep(3)
            retry_count = retry_count+1

        return {'success': False, 'message': 'Invalid transaction hash!'}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
