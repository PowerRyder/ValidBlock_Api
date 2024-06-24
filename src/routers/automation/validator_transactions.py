import json
from decimal import Decimal

import requests
from fastapi import APIRouter

from src.data_access.automation import validator_transactions as data_access
from src.constants.messages import INVALID_AUTOMATION_KEY
from src.utilities.utils import get_error_message, config

router = APIRouter()


@router.get('/fetch_bsc_validator_transactions')
def fetch_bsc_validator_transactions(key: str):
    try:
        if key == config['AutomationKey']:
            url = f"https://api.bscscan.com/api?module=account&action=txlist&address=0x978F05CED39A4EaFa6E8FD045Fe2dd6Da836c7DF&startblock=0&endblock=99999999&page=1&offset=20&sort=desc&apikey=RWISWAUD35N3CB6SZTYUI8I6CET2RT2WG2"
            response = requests.get(url)
            if response.status_code == 200:
                transactions = response.json().get('result')

                txn_dict = [{'txn_hash': tx['hash'], 'block_number': tx['blockNumber'], 'timestamp': tx['timeStamp'], 'value': str(Decimal(tx['value'])/(10**18))} for tx in transactions]

                # print(json.dumps(txn_dict))
                data_access.save_bsc_validator_transactions(transactions=json.dumps(txn_dict))
            return {'success': True, 'message': 'Transactions saved successfully!'}
        return {'success': False, 'message': INVALID_AUTOMATION_KEY}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/fetch_polygon_validator_transactions')
def fetch_polygon_validator_transactions(key: str):
    try:
        if key == config['AutomationKey']:
            url = f'https://api.polygonscan.com/api?module=account&action=getminedblocks&address=0x1B0840519a581f3779D0a10B77593d6D3894a76a&blocktype=blocks&page=1&offset=20&sort=desc&apikey=3SB2XW22QI625JPAXMN9MGMA12I1N12RQR'

            response = requests.get(url)
            if response.status_code == 200:
                blocks = response.json().get('result')

                txn_dict = [{'txn_hash': '', 'block_number': tx['blockNumber'], 'timestamp': tx['timeStamp'], 'value': str(Decimal(tx['blockReward'])/(10**18))} for tx in blocks]

                # print(json.dumps(txn_dict))
                data_access.save_polygon_validator_transactions(transactions=json.dumps(txn_dict))
            return {'success': True, 'message': 'Transactions saved successfully!'}
        return {'success': False, 'message': INVALID_AUTOMATION_KEY}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/fetch_solana_validator_transactions')
def fetch_solana_validator_transactions(key: str):
    try:
        if key == config['AutomationKey']:
            url = "https://api.mainnet-beta.solana.com"
            headers = {
                "Content-Type": "application/json"
            }
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getSignaturesForAddress",
                "params": [
                    "7QQGNm3ptwinipDCyaCF7jY5katgmFUu1ieP2f7nwLpE",  # Replace with actual Solana address
                    {"limit": 100}
                ]
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                transactions = response.json().get('result')
                txn_dict = []

                for tx in transactions:
                    signature = tx['signature']
                    slot = tx['slot']
                    block_time = tx.get('blockTime', 'N/A')

                    txn_dict.append({
                        'txn_hash': signature,
                        'block_number': slot,
                        'timestamp': block_time,
                        'value': str(0)
                    })
                    # Fetch detailed transaction information
                    # tx_detail_payload = {
                    #     "jsonrpc": "2.0",
                    #     "id": 1,
                    #     "method": "getTransaction",
                    #     "params": [signature]
                    # }
                    # tx_detail_response = requests.post(url, json=tx_detail_payload, headers=headers)
                    # if tx_detail_response.status_code == 200:
                    #     tx_detail = tx_detail_response.json().get('result')
                    #     if tx_detail:
                    #         value = Decimal(tx_detail['meta']['preBalances'][0]) / (10**9)  # Adjust as per Solana decimal units
                    #         txn_dict.append({
                    #             'txn_hash': signature,
                    #             'block_number': slot,
                    #             'timestamp': block_time,
                    #             'value': str(value)
                    #         })

                # print(json.dumps(txn_dict))
                data_access.save_solana_validator_transactions(transactions=json.dumps(txn_dict))
                return {'success': True, 'message': 'Transactions saved successfully!'}
            return {'success': False, 'message': 'Error fetching transactions from Solana'}
        return {'success': False, 'message': INVALID_AUTOMATION_KEY}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}