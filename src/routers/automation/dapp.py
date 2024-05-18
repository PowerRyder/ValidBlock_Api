import requests
from fastapi import APIRouter

from src.business_layer.dapp_service import process_dapp_contract_transaction
from src.constants.messages import INVALID_AUTOMATION_KEY
from src.utilities.utils import get_error_message, config

router = APIRouter()


@router.get('/fetch_dapp_contract_transactions')
def fetch_dapp_contract_transactions(key: str):
    try:
        if key == config['AutomationKey']:
            arbitrage_config = config['DApp']

            url = ("https://api.polygonscan.com/api?module=account&action=txlist&address="
                   + arbitrage_config['ContractAddress']
                   + "&startblock="+str(arbitrage_config['StartBlock'])
                   + "&endblock=99999999&page=1&offset=10&sort=desc&apikey="
                   + config['PolygonScan']['ApiKey'])

            response = requests.request('GET', url=url)
            data = response.json()

            for transaction in data['result']:
                process_dapp_contract_transaction(txn_hash=transaction['hash'])

            return {'success': False, 'message': 'Transactions saved successfully!'}
        return {'success': False, 'message': INVALID_AUTOMATION_KEY}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}

