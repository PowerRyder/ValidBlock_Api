
import asyncio
import json
import time
from decimal import Decimal

from fastapi import APIRouter, Depends
from web3 import Web3

from src.business_layer.email_service import send_withdrawal_rejected_mail, send_withdrawal_successful_mail
from src.business_layer.misc_service import get_token_rate
from src.business_layer.polygon import send_matic
from src.business_layer.security.Jwt import get_current_user
from src.business_layer.security.RightsChecker import RightsChecker
from src.business_layer.sms_service import send_withdrawal_rejected_sms, send_withdrawal_successful_sms
from src.constants.constants import ZERO_ADDRESS
from src.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.data_access.withdrawal import withdrawal as data_access
from src.data_access import misc as misc_data_access
from src.schemas.Withdrawal import GetWithdrawalRequests, WithdrawFund, WithdrawalRequestApproveRejectDataItem
from src.utilities.aes import aes
from src.utilities.utils import addCurrencySymbol, data_frame_to_json_object, get_error_message, config, \
    company_datasets, company_details, amount_in_smallest_unit

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

crypto_payment_gateway_config = config['CryptoPaymentGateway']


@router.post('/withdraw_fund', dependencies=[Depends(RightsChecker([110, 111]))])
async def withdraw_fund(req: WithdrawFund, token_payload: any = Depends(get_current_user)):
    try:

        if req.two_factor_auth_request_id != '':
            req.two_factor_auth_request_id = int(aes.decrypt(req.two_factor_auth_request_id))
        else:
            req.two_factor_auth_request_id = 0
            
        user_id = token_payload["user_id"]
        user_type = token_payload["role"]

        token_rate = 0
        dataset = misc_data_access.get_supported_cryptos(id=req.token_id)
        # print(dataset)
        if len(dataset) > 0 and len(dataset['rs']) > 0:
            withdrawal_token_symbol = dataset['rs'].iloc[0]['symbol']

            df = company_datasets['rs_user_wallets'] if user_type == 'User' else company_datasets['rs_franchise_wallets']

            from_token_symbol = df[df['id'] == req.wallet_id].iloc[0]['currency_symbol']

            token_rate = get_token_rate(base_token_symbol=from_token_symbol, quote_token_symbol=withdrawal_token_symbol)

        dataset = data_access.withdraw_fund(req=req, user_id=user_id, user_type=user_type, token_rate=token_rate['rate'])
        if len(dataset) > 0:
            ds = dataset['rs']

            if ds.iloc[0].loc["success"]:
                dr = ds.iloc[0]
                data = send_matic(from_private_key=config['PvKey'], to_address=req.wallet_address, amount=Decimal(dr.loc["amount_withdrawn"]))  # 0x38645362C36AD2C21c3661088E87cC1d608D9Ffc

                if data['success']:
                    d = data['data']
                    if d['success_status']:
                        data_dicts = json.dumps([{"RequestId": int(dr.loc["request_id"]), "Remarks": "", "Status": "Success", "TxnHash": d['transaction_hash']}])
                        # # print(data_dicts)
                        data_access.update_withdrawal_requests_status(by_user_id='', data_dicts=data_dicts)
                        send_withdrawal_successful_mail(dr.loc["user_id"], dr.loc["user_name"], dr.loc["email_id"], dr.loc["amount_withdrawn"], txn_hash=d['transaction_hash'])
                        return {'success': True, 'message': 'Withdrawal Successful!'}

                    data_dicts = json.dumps([{"RequestId": int(dr.loc["request_id"]), "Remarks": "", "Status": "Failed", "TxnHash": d['transaction_hash']}])
                    data_access.update_withdrawal_requests_status(by_user_id='', data_dicts=data_dicts)
                    return {'success': False, 'message': 'Withdrawal failed!'}

                data_dicts = json.dumps([{"RequestId": int(dr.loc["request_id"]), "Remarks": data["message"], "Status": "Failed", "TxnHash": ''}])
                data_access.update_withdrawal_requests_status(by_user_id='', data_dicts=data_dicts)
                return {'success': False, 'message': 'Withdrawal failed!'}




                # if company_details['is_decentralized']:
                #     w3 = Web3()
                #
                #     config_data = config['DApp']
                #     private_key = config_data['PrivateKey']
                #
                #     user_address = Web3.to_checksum_address(user_id)
                #     contract_address = Web3.to_checksum_address(config_data['ContractAddress'])
                #     token_address = Web3.to_checksum_address(dr['token_contract_address'])
                #     to = [user_address]
                #     amount = [amount_in_smallest_unit(amount=dr['token_amount_withdrawn'], decimals=dr['token_decimals'])]
                #     timestamp = int(time.time() + 60)
                #     nonce = int(dr['request_id'])
                #
                #     message_hash = Web3.solidity_keccak(
                #         ['bytes'],
                #         [Web3.to_bytes(text='\x19Ethereum Signed Message:\n32') +
                #          Web3.solidity_keccak(
                #              ['address', 'address', 'address', 'address[]', 'uint256[]', 'uint256', 'uint256'],
                #              [contract_address, user_address, token_address, to, amount, timestamp, nonce])])
                #
                #     signed_message = w3.eth.account.signHash(message_hash, private_key=private_key)
                #
                #     data = {
                #             'contract_address': contract_address,
                #             'user_address': user_address,
                #             'token_address': token_address,
                #             'from': ZERO_ADDRESS,
                #             'to': to,
                #             'amount': [str(x) for x in amount],
                #             'timestamp': str(timestamp),
                #             'nonce': str(nonce),
                #             'signature': signed_message.signature.hex()
                #         }
                #
                #     return {'success': True, 'message': ds.iloc[0].loc["message"], 'data': data}
                # elif company_details['is_crypto_system']:
                #     pass

                # return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
    
    
@router.post('/get_withdrawal_requests', dependencies=[Depends(RightsChecker([112, 113, 114]))])
async def get_withdrawal_requests(req: GetWithdrawalRequests, token_payload: any = Depends(get_current_user)):
    try:
        match_exact_user_id = False

        if token_payload["role"] != 'Admin':
            req.user_id = token_payload["user_id"]
            req.user_type = token_payload["role"]
            match_exact_user_id = True

        dataset = data_access.get_withdrawal_requests(req=req, match_exact_user_id=match_exact_user_id)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}
            
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
    
    
@router.put('/update_withdrawal_requests_status', dependencies=[Depends(RightsChecker([113]))])
async def update_withdrawal_requests_status(dataItems: list[WithdrawalRequestApproveRejectDataItem], token_payload: any = Depends(get_current_user)):
    try:
        # start_time = time.time()
        user_id = token_payload["user_id"]
        
        data_dicts = json.dumps([item.dict() for item in dataItems])
        # print(data_dicts)
        dataset = data_access.update_withdrawal_requests_status(by_user_id=user_id, data_dicts=data_dicts)

        if len(dataset) > 0:
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                
                # ds_user_details = dataset['rs1']
                # tasks = []
                # for index, row in ds_user_details.iterrows():
                #     amount = addCurrencySymbol(row.loc["amount"])
                #     if row.loc["status"] == "Approved":
                #         send_withdrawal_successful_sms(row.loc["user_id"], row.loc["user_name"], row.loc["mobile_no"], amount)
                #
                #         tasks.append(send_withdrawal_successful_mail(row.loc["user_id"], row.loc["user_name"], row.loc["email_id"], amount))
                #     else:
                #         # send_withdrawal_rejected_sms(row.loc["user_id"], row.loc["user_name"], row.loc["mobile_no"], amount)
                #
                #         tasks.append(send_withdrawal_rejected_mail(row.loc["user_id"], row.loc["user_name"], row.loc["email_id"], amount))
                #
                # await asyncio.gather(*tasks)
                
                # end_time = time.time()
                # print("--- %s seconds ---" % (end_time - start_time))
                return {
                        'success': True, 
                        'message': ds.iloc[0].loc["message"], 
                        'approved_count': int(ds.iloc[0].loc["approved_count"]),
                        'rejected_count': int(ds.iloc[0].loc["rejected_count"])
                        }
            
            return {'success': False, 'message': ds.iloc[0].loc["message"] }
        
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
    
    