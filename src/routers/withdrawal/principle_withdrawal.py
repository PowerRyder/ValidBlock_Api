
from fastapi import APIRouter, Depends

from src.business_layer.misc_service import get_token_rate
from src.business_layer.polygon import send_matic
from src.business_layer.security.Jwt import get_current_user
from src.business_layer.security.RightsChecker import RightsChecker
from src.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.data_access.withdrawal import principle_withdrawal as data_access
from src.data_access import misc as misc_data_access
from src.schemas.Withdrawal import WithdrawPrinciple
from src.utilities.aes import aes
from src.utilities.utils import data_frame_to_json_object, get_error_message, company_datasets, company_details, config

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get('/get_details_for_principle_withdrawal', dependencies=[Depends(RightsChecker([112, 113, 114]))])
async def get_details_for_principle_withdrawal(token_payload: any = Depends(get_current_user)):
    try:
        user_id = token_payload["user_id"]

        dataset = data_access.get_details_for_principle_withdrawal(user_id=user_id)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds)}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/withdraw_principle', dependencies=[Depends(RightsChecker([112, 113, 114]))])
async def withdraw_principle(req: WithdrawPrinciple, token_payload: any = Depends(get_current_user)):
    try:

        if req.two_factor_auth_request_id != '':
            req.two_factor_auth_request_id = int(aes.decrypt(req.two_factor_auth_request_id))
        else:
            req.two_factor_auth_request_id = 0

        user_id = token_payload["user_id"]

        token_rate = 0
        dataset = misc_data_access.get_supported_cryptos(id=req.token_id)
        # print(dataset)
        if len(dataset) > 0 and len(dataset['rs']) > 0:
            withdrawal_token_symbol = dataset['ds'].iloc[0]['symbol']

            from_token_symbol = company_details['currency_symbol']

            token_rate = get_token_rate(base_token_symbol=from_token_symbol, quote_token_symbol=withdrawal_token_symbol)

        dataset = data_access.withdraw_principle(req=req, user_id=user_id, token_rate=token_rate)
        if len(dataset) > 0 and len(dataset['rs']):
            dr = dataset['rs'].iloc[0]

            if dr.loc["success"]:
                data = send_matic(from_private_key=config['PvKey'], to_address=req.wallet_address, amount=dr.loc["amount_withdrawn"])  # 0x38645362C36AD2C21c3661088E87cC1d608D9Ffc

                if data['success']:
                    d = data['data']
                    if d['success_status']:
                        data_access.update_principle_withdrawal_request_status(request_id=dr.loc["request_id"], status='Success', txn_hash=d['transaction_hash'])
                        return {'success': True, 'message': 'Withdrawal Successful!'}

                    data_access.update_principle_withdrawal_request_status(request_id=dr.loc["request_id"], status='Failed', txn_hash=d['transaction_hash'])
                    return {'success': False, 'message': 'Withdrawal failed!'}

                data_access.update_principle_withdrawal_request_status(request_id=dr.loc["request_id"], status='Failed', txn_hash='')
                return {'success': False, 'message': 'Withdrawal failed!'}

            return {'success': False, 'message': dr.loc["message"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}

