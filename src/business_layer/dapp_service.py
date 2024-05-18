import json
import time
from decimal import Decimal

from web3 import Web3

from src.constants.constants import ZERO_ADDRESS
from src.constants.messages import DATABASE_CONNECTION_ERROR
from src.data_access.accounts import register as register_data_access
from src.data_access.dapp.deposit import topup_through_dapp
from src.schemas.Accounts import Register
from src.schemas.Withdrawal import WithdrawalRequestApproveRejectDataItem
from src.utilities.utils import get_error_message, config, company_details, amount_from_smallet_unit
from src.data_access.withdrawal import withdrawal as withdrawal_data_access


def process_dapp_contract_transaction(txn_hash: str):
    try:
        print(txn_hash)
        function_name, function_params, user_address, timestamp = decode_input_data_for_dapp_contract(txn_hash=txn_hash)
        print(function_name, function_params)

        package_id = function_params['packageId']
        amount = amount_from_smallet_unit(amount=function_params['amount'], decimals=config['DApp']['PaymentTokenDecimals'])
        if function_name == "Deposit":
            return register(user_address=user_address,
                            sponsor_address=function_params['referral'],
                            upline_address=function_params['upline'],
                            side=function_params['side'],
                            txn_hash=txn_hash,
                            package_id=package_id,
                            amount=amount)

        elif function_name == "Redeposit":
            return topup(user_address=user_address, txn_hash=txn_hash, package_id=package_id, amount=amount)

        elif function_name == "Withdraw":
            return update_withdrawal_status(request_id=function_params['nonce'], txn_hash=txn_hash)

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


def decode_input_data_for_dapp_contract(txn_hash):
    dapp_config = config['DApp']
    with open(dapp_config['AbiJsonPath']) as f:
        contract_abi = json.load(f)

    w3 = Web3(Web3.HTTPProvider('https://data-seed-prebsc-1-s1.binance.org:8545/'))  # ('https://rpc-mainnet.matic.quiknode.pro'))
    contract = w3.eth.contract(abi=contract_abi)

    retry_count = 1
    while retry_count <= 10:
        receipt = w3.eth.get_transaction_receipt(txn_hash)

        if receipt is not None:
            if receipt.status != 1:
                raise Exception('Invalid transaction!')

            tx = w3.eth.get_transaction(txn_hash)
            print(tx)

            if tx['to'].lower() != dapp_config['ContractAddress'].lower():
                raise Exception('Invalid transaction!')

            function_signature, function_params = contract.decode_function_input(tx['input'])

            function_name = function_signature.function_identifier

            return function_name, function_params, tx['from'], tx['timestamp']

        time.sleep(3)
        retry_count = retry_count + 1

    raise Exception('Invalid transaction! Timed out!')


def register(user_address: str, sponsor_address: str, upline_address: str, side: str, txn_hash: str, package_id: int, amount: Decimal):
    dataset = register_data_access.does_user_id_exist(user_id=user_address)
    # print(dataset)

    if len(dataset) > 0 and len(dataset['rs']) > 0:
        ds = dataset['rs']

        if not ds.iloc[0]['valid']:
            data = Register()
            data.userId = user_address
            data.referralId = sponsor_address

            if company_details['is_binary_system']:
                data.uplineId = upline_address if upline_address != ZERO_ADDRESS else ''
                data.side = side

            dataset = register_data_access.register(data=data)

            if len(dataset) > 0 and len(dataset['rs']) > 0:
                ds = dataset['rs']
                if not ds.iloc[0].loc["success"]:
                    return {'success': False, 'message': ds.iloc[0].loc["message"]}

            else:
                return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

        return topup(user_address=user_address, txn_hash=txn_hash, package_id=package_id, amount=amount)
    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}


def topup(user_address: str, txn_hash: str, package_id: int, amount: Decimal):
    dataset = register_data_access.does_user_id_exist(user_id=user_address)
    # print(dataset)

    if len(dataset) > 0 and len(dataset['rs']):
        ds = dataset['rs']

        if not ds.iloc[0]['valid']:
            data = Register()
            data.userId = user_address
            ds = register_data_access.register(data=data)
            if not ds.iloc[0].loc["success"]:
                return {'success': False, 'message': ds.iloc[0].loc["message"]}

        dataset = topup_through_dapp(user_address=user_address, txn_hash=txn_hash, package_id=package_id, amount=amount)

        if len(dataset) > 0 and len(dataset['rs']) > 0:
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                return {'success': True, 'message': ds.iloc[0].loc["message"], 'user_address': user_address, 'amount': amount}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}


def update_withdrawal_status(request_id: int, txn_hash: str):
    item = WithdrawalRequestApproveRejectDataItem()
    item.RequestId = request_id
    item.Status = 'Success'
    item.TxnHash = txn_hash

    data_dicts = json.dumps([item.dict()])
    # print(data_dicts)
    dataset = withdrawal_data_access.update_withdrawal_requests_status(by_user_id='', data_dicts=data_dicts)

    if len(dataset) > 0:
        ds = dataset['rs']
        if ds.iloc[0].loc["success"]:
            return {'success': True, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': ds.iloc[0].loc["message"]}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

