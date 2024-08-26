
from fastapi import APIRouter, Depends
from src.data_access.income import reward as data_access
from src.constants.messages import (DATABASE_CONNECTION_ERROR, OK)
from src.business_layer.security.Jwt import get_current_user
from src.business_layer.security.RightsChecker import RightsChecker
from src.schemas.Income import GetRankDetails_Request, GetRewardIncome_Request
from src.utilities.utils import data_frame_to_json_object, get_error_message



router = APIRouter(dependencies=[Depends(get_current_user)])

@router.post('/get_reward_income', dependencies=[Depends(RightsChecker([10, 11]))])
def get_reward_income(req: GetRewardIncome_Request, token_payload: any = Depends(get_current_user)):
    try:
        match_exact_user_id = False
        if(token_payload["role"]=='User'):
            req.user_id = token_payload["user_id"]
            match_exact_user_id = True
            
        dataset = data_access.get_reward_income(req=req, match_exact_user_id=match_exact_user_id)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}
            
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_ranks', dependencies=[Depends(RightsChecker([10, 11]))])
def get_ranks(token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.get_ranks()
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds)}
            
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/get_rank_details', dependencies=[Depends(RightsChecker([10, 11]))])
def get_rank_details(req: GetRankDetails_Request, token_payload: any = Depends(get_current_user)):
    try:
        if token_payload["role"] == 'User':
            req.user_id = token_payload["user_id"]

        dataset = data_access.get_rank_details(req=req)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}
            
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_user_rank_qualification_details', dependencies=[Depends(RightsChecker([11]))])
def get_user_rank_qualification_details(user_id: str, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.get_user_rank_qualification_details(user_id=user_id)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds)}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
