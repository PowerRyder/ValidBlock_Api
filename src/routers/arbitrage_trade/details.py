from fastapi import APIRouter, Depends

from src.business_layer.security.Jwt import get_current_user
from src.business_layer.security.RightsChecker import RightsChecker
from src.constants.messages import OK, DATABASE_CONNECTION_ERROR
from src.data_access.arbitrage_trade import details as data_access
from src.schemas.ArbitrageTrade import GetArbitrageTradeHistory
from src.utilities.utils import get_error_message, data_frame_to_json_object

router = APIRouter()


@router.post('/get_trade_history', dependencies=[Depends(RightsChecker([222, 226]))])
def get_trade_history(req: GetArbitrageTradeHistory, token_payload: any = Depends(get_current_user)):
    try:
        match_exact_user_id = False
        if token_payload["role"] == 'User':
            req.user_id = token_payload["user_id"]
            match_exact_user_id = True

        dataset = data_access.get_trade_history(req=req, match_exact_user_id=match_exact_user_id)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds),
                    'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_top_trades')
def get_top_trades():
    try:
        dataset = data_access.get_top_trades()
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds)}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
