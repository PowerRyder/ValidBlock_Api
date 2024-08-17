from decimal import Decimal

from eth_account import Account
from web3 import Web3, HTTPProvider
import requests
from web3.middleware import geth_poa_middleware

from src.constants.messages import OK
from src.utilities.aes import aes
from src.utilities.utils import get_error_message, amount_in_smallest_unit

network = "Polygon"
polygon_chain_id = 137
api_keys = [
    {"key": 'INU1QKCGBX3EMPEW8FIZ7BNWB5KYDBVU8H', 'used_count': 0},
    {"key": 'C22W9MVGWBH2KKJE64ITR7ZKJBWVJSM36V', 'used_count': 0}
]
provider_url = 'https://rpc-mainnet.matic.quiknode.pro'
req_gas_to_send_token = 84000


# def create_polygon_wallet():
#     w3 = Web3()
#     eth_account = w3.eth.account.create()
#
#     return {
#         "address": eth_account.address,
#         "private_key": eth_account.key.hex()
#     }


# def get_polygon_transactions(address: str, start_block: int):
#     normal_transactions = get_normal_transactions(address=address, start_block=start_block)
#     token_transactions = get_token_transactions(address=address, start_block=start_block)
#     transactions = normal_transactions + token_transactions
#     return transactions
#
#
# def get_normal_transactions(address: str, start_block: int):
#     try:
#         w3 = Web3()
#         api_key_index = 0  # get_least_used_api_key_index(api_keys)
#         url = ("https://api.polygonscan.com/api?module=account&action=txlist&address="
#                + address
#                + "&startblock="+str(start_block)+"&endblock=99999999&page=1&offset=10&sort=asc&apikey=" + api_keys[api_key_index]['key'])
#
#         api_keys[api_key_index]['used_count'] = api_keys[api_key_index]['used_count'] + 1
#
#         response = requests.request('GET', url=url)
#
#         # Parsing the response
#         data = response.json()
#
#         transactions = []
#
#         for transaction in data['result']:
#             # print(transaction)
#
#             if transaction['txreceipt_status'] == "1" and transaction['isError'] == "0" and int(
#                     transaction['value']) > 0:
#                 gas_fees_wei = int(transaction['gasPrice']) * int(transaction['gas'])
#
#                 txn = Transaction()
#                 txn.hash = transaction['hash']
#                 txn.time_stamp = transaction['timeStamp']
#                 txn.from_address = transaction['from']
#                 txn.to_address = transaction['to']
#                 txn.value = str(Decimal(w3.from_wei(int(transaction['value']), 'ether')))
#                 txn.fee_amount = str(Decimal(w3.from_wei(gas_fees_wei, 'ether')))
#                 txn.confirmation_count = int(transaction['confirmations'])
#                 txn.is_token_transaction = False
#                 txn.token_contract_address = ""
#                 txn.network = network
#                 txn.block_number = transaction['blockNumber']
#
#                 transactions.append(txn)
#             # print(transaction['hash'], transaction['timeStamp'], transaction['from'], transaction['to'], transaction['value'], transaction['confirmations'], transaction['txreceipt_status'])
#
#         return transactions
#
#     except Exception as e:
#         print(e.__str__())
#         return []


# def get_token_transactions(address: str, start_block: int):
#     try:
#         w3 = Web3()
#         dataset = data_access.get_supported_tokens_on_network(network=network)
#
#         transactions = []
#         if len(dataset) > 0 and len(dataset['rs']) > 0:
#             supported_currencies = dataset['rs']
#
#             for index, row in supported_currencies.iterrows():
#                 api_key_index = get_least_used_api_key_index(api_keys)
#                 url = ("https://api.polygonscan.com/api?module=account&action=tokentx&contractaddress=" + row[
#                         'contract_address'] +
#                        "&address=" + address +
#                        "&page=1&offset=10&startblock="+str(start_block)+"&endblock=99999999&sort=asc&apikey=" +
#                        api_keys[api_key_index]['key'])
#
#                 api_keys[api_key_index]['used_count'] = api_keys[api_key_index]['used_count'] + 1
#
#                 response = requests.request('GET', url=url)
#
#                 # Parsing the response
#                 data = response.json()
#
#                 for transaction in data['result']:
#                     # print(transaction)
#
#                     if int(transaction['value']) > 0:
#                         gas_fees_wei = int(transaction['gasPrice']) * int(transaction['gas'])
#
#                         txn = Transaction()
#                         txn.hash = transaction['hash']
#                         txn.time_stamp = transaction['timeStamp']
#                         txn.from_address = transaction['from']
#                         txn.to_address = transaction['to']
#                         txn.value = str(Decimal(transaction['value']) / Decimal(10 ** row['decimals']))
#                         txn.fee_amount = str(Decimal(w3.from_wei(gas_fees_wei, 'ether')))
#                         txn.confirmation_count = int(transaction['confirmations'])
#                         txn.is_token_transaction = True
#                         txn.token_contract_address = transaction['contractAddress']
#                         txn.network = network
#                         txn.block_number = transaction['blockNumber']
#                         # print(transaction['hash'], transaction['timeStamp'], transaction['from'], transaction['to'], transaction['value'], float(transaction['value'])/float(10 ** row['decimals']), transaction['confirmations'])
#
#                         transactions.append(txn)
#
#         return transactions
#
#     except Exception as e:
#         print(e.__str__())
#         return []
#
#
# def get_polygon_txn_processing_fee():
#     w3 = Web3(Web3.HTTPProvider(provider_url))
#     gas_price = w3.eth.gas_price.real
#     return round(Decimal(w3.from_wei(gas_price*21000, 'ether'))*Decimal(1.7), 6), round(Decimal(w3.from_wei(gas_price*121000, 'ether'))*5, 6)


def send_matic(from_private_key: str, to_address: str, amount: Decimal, max_fee: Decimal = None):
    try:
        w3 = Web3(Web3.HTTPProvider(provider_url))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        if not w3.is_connected():
            print("Failed to connect to the network")
            return

        # Set up the transaction details
        from_address = w3.eth.account.from_key(from_private_key).address
        nonce = w3.eth.get_transaction_count(from_address)
        value = w3.to_wei(amount, 'ether')  # Convert amount to Wei
        gas_price = w3.eth.gas_price*4
        gas_limit = 21000  # Standard gas limit for transaction

        if max_fee is not None and max_fee > 0:
            fee = Decimal(w3.from_wei(gas_price*gas_limit, 'ether'))
            if fee > max_fee:
                return {'success': False, 'message': 'Fee is too high!'}

        balance_eth = w3.from_wei(w3.eth.get_balance(from_address), 'ether')
        if Decimal(balance_eth) < (amount+(max_fee if max_fee is not None and max_fee > 0 else 0)):
            return {'success': False, 'message': 'Insufficient balance!'}

        # Construct the transaction
        txn = {
            'nonce': nonce,
            'chainId': polygon_chain_id,
            'to': Web3.to_checksum_address(to_address),
            'value': value,
            'gas': gas_limit,
            'gasPrice': gas_price,
        }

        # print(w3.eth.estimate_gas(transaction=txn))

        # Sign the transaction
        signed_txn = w3.eth.account.sign_transaction(txn, private_key=from_private_key)

        # Send the transaction
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash, timeout=1000)

        # print(f"Transaction sent! Hash: {txn_hash.hex()}")
        return {'success': True, 'message': OK, 'data': {'transaction_hash': txn_hash.hex(), 'success_status': txn_receipt['status']==1} }

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


# def send_token_on_polygon(private_key: str, to_address: str, amount: Decimal, token_contract_address: str, decimals: int, max_fee: Decimal = None):
#     try:
#         w3 = Web3(HTTPProvider(provider_url))
#         w3.middleware_onion.inject(geth_poa_middleware, layer=0)
#
#         if not w3.is_connected():
#             raise Exception("Failed to connect to the network")
#
#         # ERC-20 transfer function ABI
#         abi = erc20_token_contract_abi
#
#         # Set up the contract
#         contract = w3.eth.contract(address=Web3.to_checksum_address(token_contract_address), abi=abi)
#
#         # Prepare transaction
#         account = Account.from_key(private_key)
#         nonce = w3.eth.get_transaction_count(account.address)
#         amount = amount_in_smallest_unit(amount=amount, decimals=decimals)
#
#         balance = contract.functions.balanceOf(account.address).call()
#         if balance < amount:
#             return {'success': False, 'message': 'Insufficient token balance!'}
#
#         gas_price = w3.eth.gas_price
#         gas_estimate = contract.functions.transfer(Web3.to_checksum_address(to_address), amount).estimate_gas(
#             {'from': account.address})
#
#         fee = Decimal(w3.from_wei(gas_price * gas_estimate, 'ether'))
#         if max_fee is not None and max_fee>0:
#             if fee>max_fee:
#                 return {'success': False, 'message': 'Fee is too high!'}
#
#         request_fee_for_token_transfer(address=account.address, req_fee=fee)
#
#         txn = contract.functions.transfer(
#             Web3.to_checksum_address(to_address),
#             amount  # Note: this amount should be in the smallest unit of the token (like Wei for ETH)
#         ).build_transaction({
#             'chainId': polygon_chain_id,
#             'gas': gas_estimate,
#             'gasPrice': gas_price,
#             'nonce': nonce,
#         })
#
#         # Sign the transaction
#         signed_txn = w3.eth.account.sign_transaction(txn, private_key)
#
#         # Send the transaction
#         txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
#
#         # Wait for confirmation
#         txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
#
#         # return txn_receipt
#         return {'success': True, 'message': OK,
#                 'data': {'transaction_hash': txn_hash.hex(), 'success_status': txn_receipt['status'] == 1}}
#
#     except Exception as e:
#         print(e.__str__())
#         return {'success': False, 'message': get_error_message(e)}
#
#
# def request_fee_for_token_transfer(address, req_fee: Decimal):
#     w3 = Web3(Web3.HTTPProvider(provider_url))
#
#     balance = w3.eth.get_balance(address)
#     ether_balance = Decimal(w3.from_wei(balance, 'ether'))
#
#     if req_fee > ether_balance:
#
#         hot_wallet_address, hot_wallet_key_enc = get_hot_wallet(network=network)
#         send_matic(from_private_key=aes.decrypt(hot_wallet_key_enc), to_address=address, amount=req_fee-ether_balance)
#
#         return True
#
#     return False
#
#
# def get_matic_transfer_fee():
#     try:
#         w3 = Web3(Web3.HTTPProvider(provider_url))
#
#         if not w3.is_connected():
#             print("Failed to connect to the network")
#             return
#
#         gas_price = w3.eth.gas_price
#         gas_limit = 21000  # Standard gas limit for transaction
#
#         fee = Decimal(w3.from_wei(gas_price * gas_limit, 'ether'))
#
#         return {'success': True, 'message': OK, 'fee': fee}
#
#     except Exception as e:
#         print(e.__str__())
#         return {'success': False, 'message': get_error_message(e)}
