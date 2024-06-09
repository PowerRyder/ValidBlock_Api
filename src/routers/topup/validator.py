import requests
from fastapi import APIRouter, Depends

from src.data_access.topup import validator as data_access
from src.constants.messages import (DATABASE_CONNECTION_ERROR, OK)
from src.business_layer.security.Jwt import get_current_user
from src.business_layer.security.RightsChecker import RightsChecker
from src.schemas.Topup import GetRequestsForValidator
from src.utilities.utils import get_error_message, config, data_frame_to_json_object

router = APIRouter()


@router.get('/request_for_validator', dependencies=[Depends(RightsChecker([245]))])
async def request_for_validator(package_id: int, wallet_id: int, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.request_for_validator(user_id=token_payload["user_id"], package_id=package_id, wallet_id=wallet_id)
        # print(dataset)
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:

                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/vote_for_validator', dependencies=[Depends(RightsChecker([245]))])
async def vote_for_validator(validator_user_id: str, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.vote_for_validator(validator_user_id=validator_user_id, by_user_id=token_payload["user_id"])
        # print(dataset)
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:

                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/get_requests_for_validator', dependencies=[Depends(RightsChecker([245, 11]))])
async def get_requests_for_validator(req: GetRequestsForValidator, token_payload: any = Depends(get_current_user)):
    try:
        match_exact_user_id = False
        if token_payload["role"] == 'User':
            req.user_id = token_payload["user_id"]
            match_exact_user_id = True

        dataset = data_access.get_requests_for_validator(req=req, match_exact_user_id=match_exact_user_id)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/update_request_for_validator', dependencies=[Depends(RightsChecker([245, 11]))])
async def update_request_for_validator(request_id: int, status: str, remarks: str, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.update_request_for_validator(request_id=request_id, status=status, remarks=remarks, by_user_id=token_payload["user_id"])
        # print(dataset)
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:

                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/update_validator_package_discount_percentage', dependencies=[Depends(RightsChecker([245, 11]))])
async def update_validator_package_discount_percentage(percentage: float, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.update_validator_package_discount_percentage(percentage=percentage, by_user_id=token_payload["user_id"])
        # print(dataset)
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:

                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
