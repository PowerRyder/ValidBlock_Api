
from fastapi import APIRouter, Depends
from src.business_layer.security.RightsChecker import RightsChecker
from src.constants.messages import DATABASE_CONNECTION_ERROR, NO_WALLET_FOUND, OK
from src.data_access.wallet import wallet as data_access

from src.business_layer.security.Jwt import get_current_user
from src.schemas.Wallet import WalletBalanceRequest, WalletCreditDebit, WalletTransactionsRequest, \
    AdminCreditDebitHistory
from src.utilities.utils import data_frame_to_json_object, get_error_message


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post('/get_wallet_balance', dependencies=[Depends(RightsChecker([46, 63, 79, 89]))])
def get_wallet_balance(req: WalletBalanceRequest, token_payload: any = Depends(get_current_user)):
    try:
        
        match_exact_user_id = False
        if token_payload["role"]!= "Admin":
            req.user_id = token_payload["user_id"]
            req.user_type = token_payload["role"]
            match_exact_user_id = True
        
        dataset = data_access.get_wallet_balance(req=req, match_exact_user_id=match_exact_user_id)
        if len(dataset)>0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}
            
        return {'success': False, 'message': NO_WALLET_FOUND }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/get_wallet_transactions', dependencies=[Depends(RightsChecker([89, 90, 91, 92]))])
async def get_wallet_transactions(req: WalletTransactionsRequest, token_payload:any = Depends(get_current_user)):
    try:
        if token_payload["role"]!= "Admin":
            req.user_id = token_payload["user_id"]
            req.user_type = token_payload["role"]
        # print(req)
        dataset = data_access.get_wallet_transactions(req=req)
        if len(dataset)>0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}
            
        return {'success' : False, 'message' : DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
    

@router.post('/credit_debit', dependencies=[Depends(RightsChecker([93]))])
async def credit_debit(req: WalletCreditDebit, token_payload:any = Depends(get_current_user)):
    try:
        by_admin_user_id = token_payload["user_id"]

        dataset = data_access.credit_debit(req=req, by_admin_user_id=by_admin_user_id)
        if len(dataset)>0:
            ds = dataset['rs']
            
            if ds.iloc[0].loc["success"]:
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success' : False, 'message' : DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/get_admin_credit_debit_history', dependencies=[Depends(RightsChecker([89, 90, 91, 92]))])
async def get_admin_credit_debit_history(req: AdminCreditDebitHistory, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.get_admin_credit_debit_history(req=req)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds),
                    'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
