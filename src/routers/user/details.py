
from fastapi import APIRouter, Depends
from src.business_layer.security.RightsChecker import RightsChecker
from src.constants.messages import INVALID_USER_ID, OK, DATABASE_CONNECTION_ERROR
from src.data_access.user import details as data_access
from src.constants import VALIDATORS

from src.business_layer.security.Jwt import get_current_user
from src.schemas.User import UpdatePOL_Address
from src.utilities.utils import data_frame_to_json_object, get_error_message


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get('/details', dependencies=[Depends(RightsChecker([10, 11, 59]))])
def details(user_id: str = VALIDATORS.USER_ID, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.get_user_details(user_id=user_id)
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["valid"]:
                return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds)}

        return {'success': False, 'message': INVALID_USER_ID }

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/dashboard_details', dependencies=[Depends(RightsChecker([12]))])
def dashboard_details(token_payload: any = Depends(get_current_user)):
    try:
        user_id = token_payload["user_id"]

        dataset = data_access.get_user_dashboard_details(user_id=user_id)
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["valid"]:
                return {'success': True,
                        'message': OK,
                        'data': data_frame_to_json_object(ds),
                        'income': data_frame_to_json_object(dataset['rs1']),
                        'wallet_balances': data_frame_to_json_object(dataset['rs2']),
                        'news': data_frame_to_json_object(dataset['rs_news']),
                        'rank_details': data_frame_to_json_object(dataset['rs_rank']),
                        'reward_qualification_details': data_frame_to_json_object(dataset['rs_reward_qualification']),
                        'hong_kong_qualification_details': data_frame_to_json_object(dataset['rs_hong_kong_qualification'])}
            
            return {'success': False, 'message': INVALID_USER_ID }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/dashboard_chart_details', dependencies=[Depends(RightsChecker([12]))])
def dashboard_chart_details(duration: str = VALIDATORS.CHART_DURATION, token_payload: any = Depends(get_current_user)):
    try:
        user_id = token_payload["user_id"]

        dataset = data_access.get_user_dashboard_chart_details(user_id=user_id, duration=duration)
        if len(dataset):
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(dataset['rs'])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/rank_details', dependencies=[Depends(RightsChecker([10, 11, 59]))])
def rank_details(token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.get_user_rank_details(user_id=token_payload["user_id"])
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds)}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/reward_qualification_details', dependencies=[Depends(RightsChecker([10, 11, 59]))])
def reward_qualification_details(token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.get_user_reward_qualification_details(user_id=token_payload["user_id"])
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds)}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/update_pol_address', dependencies=[Depends(RightsChecker([10, 11]))])
def update_pol_address(req: UpdatePOL_Address, token_payload: any = Depends(get_current_user)):
    try:
        if token_payload["role"] == 'User':
            req.user_id = token_payload["user_id"]


        dataset = data_access.update_pol_address(user_id=req.user_id,
                                                 by_user_id=token_payload["user_id"],
                                                 by_user_type=token_payload["role"],
                                                 pol_address=req.pol_Address)

        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': INVALID_USER_ID }

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
