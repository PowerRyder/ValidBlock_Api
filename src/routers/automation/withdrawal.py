import time
from decimal import Decimal

import requests
from fastapi import APIRouter
from web3 import Web3

from src.business_layer.blockchain_service import get_current_block_timestamp
from src.business_layer.email_service import send_withdrawal_successful_mail
from src.business_layer.polygon import send_matic
from src.data_access.automation import withdrawal as data_access
from src.constants.messages import INVALID_AUTOMATION_KEY
from src.data_access.withdrawal.withdrawal import save_withdrawal_transaction
from src.utilities.utils import get_error_message, config

router = APIRouter()


@router.get('/reject_pending_withdrawals')
def reject_pending_withdrawals(key: str):
    try:
        if key == config['AutomationKey']:

            current_block_timestamp = get_current_block_timestamp()

            data_access.reject_pending_withdrawals(timestamp=current_block_timestamp)

            return {'success': False, 'message': 'Execution successful!'}
        return {'success': False, 'message': INVALID_AUTOMATION_KEY}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_withdrawals')
def get_withdrawals(key: str):
    try:
        if key == config['AutomationKey']:
            pv_key = config['PvKey']

            w3 = Web3()
            from_address = str(w3.eth.account.from_key(pv_key).address)

            url = ("https://api.polygonscan.com/api?module=account&action=txlist&address="
                   + from_address
                   + "&startblock=0&endblock=99999999&page=1&offset=50&sort=desc&apikey="
                   + config['PolygonScan']['ApiKey'])

            response = requests.request('GET', url=url)
            data = response.json()


            result = data['result'][::-1]
            for transaction in result:
                if str(transaction['txreceipt_status']) == "1" and str(transaction['from']).lower() == from_address.lower():
                    txn = {
                                'hash': transaction['hash'],
                                'to': transaction['to'],
                                'value': w3.from_wei(int(transaction['value']), 'ether')
                            }

                    save_withdrawal_transaction(txn_hash=txn['hash'], to_address=txn['to'], amount=txn['value'])
            #     process_dapp_contract_transaction(txn_hash=transaction['hash'])

            return {'success': True, 'message': 'Transactions saved successfully!'}
        return {'success': False, 'message': INVALID_AUTOMATION_KEY}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/process_withdrawals')
def process_withdrawals(key: str):
    try:
        if key == config['AutomationKey']:
            dataset = data_access.get_withdrawal_queue()

            if len(dataset) > 0 and len(dataset['rs']) and dataset['rs'].iloc[0].loc["success"] and len(dataset['rs1']) > 0:
                ds = dataset['rs1']
                for index, dr in ds.iterrows():
                    try:
                        time.sleep(4)
                        data = send_matic(from_private_key=config['PvKey'], to_address=dr.loc["token_withdrawal_address"], amount=Decimal(dr.loc["token_amount"]))  # 0x38645362C36AD2C21c3661088E87cC1d608D9Ffc

                        if data['success']:
                            d = data['data']
                            if d['success_status']:
                                data_access.update_withdrawal_queue_status(queue_id=dr.loc["queue_id"], status='Success', txn_hash=d['transaction_hash'])
                                send_withdrawal_successful_mail(dr.loc["user_id"], dr.loc["user_name"], dr.loc["email_id"], dr.loc["token_amount"], txn_hash=d['transaction_hash'])

                    except Exception as e:
                        print(e.__str__())
                        get_error_message(e)

                data_access.update_withdrawal_queue_batch_status(batch_id=int(dataset['rs'].iloc[0].loc["batch_id"]))

            return {'success': True, 'message': 'Withdrawals processed successfully!'}
        return {'success': False, 'message': INVALID_AUTOMATION_KEY}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


