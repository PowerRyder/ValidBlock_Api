import json
from fastapi import APIRouter
from web3 import Web3

from src.constants.messages import INVALID_AUTOMATION_KEY
from src.utilities.utils import get_error_message, config
from src.business_layer import arbitrage_service
import requests

router = APIRouter()


@router.get('/fetch_arbitrage_contract_transactions')
def fetch_arbitrage_contract_transactions(key: str):
    try:
        if key == config['AutomationKey']:
            arbitrage_config = config['ArbitrageTrade']

            url = ("https://api.polygonscan.com/api?module=account&action=txlist&address="
                   + arbitrage_config['ContractAddress']
                   + "&startblock="+str(arbitrage_config['StartBlock'])
                   + "&endblock=99999999&page=1&offset=10&sort=desc&apikey="
                   + config['PolygonScan']['ApiKey'])

            response = requests.request('GET', url=url)
            data = response.json()

            for transaction in data['result']:
                if transaction['methodId'] == "0xaf89f091":
                    input_data = transaction['input']
                    request_id = arbitrage_service.decode_input_data_for_request_id(input_data=input_data)

                    if transaction['txreceipt_status'] == "1" and transaction['isError'] == "0":
                        arbitrage_service.update_trade_transaction_status(request_id=request_id, txn_hash=transaction['hash'], status='Success')
                    else:
                        arbitrage_service.update_trade_transaction_status(request_id=request_id, txn_hash=transaction['hash'], status='Failed')

            return {'success': False, 'message': 'Transactions saved successfully!'}
        return {'success': False, 'message': INVALID_AUTOMATION_KEY}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}

