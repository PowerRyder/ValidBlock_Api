from fastapi import APIRouter, Depends
from src.data_access.income import validator as data_access
from src.constants.messages import (DATABASE_CONNECTION_ERROR, OK)
from src.business_layer.security.Jwt import get_current_user
from src.business_layer.security.RightsChecker import RightsChecker
from src.schemas.Income import GetROILevelIncome_Request, GetRoiIncome_Request
from src.utilities.utils import data_frame_to_json_object, get_error_message


router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post('/get_validator_roi_income', dependencies=[Depends(RightsChecker([140, 141]))])
def get_validator_roi_income(req: GetRoiIncome_Request, token_payload: any = Depends(get_current_user)):
    try:
        match_exact_user_id = False
        if (token_payload["role"] == 'User'):
            req.user_id = token_payload["user_id"]
            match_exact_user_id = True

        dataset = data_access.get_validator_roi_income(req=req, match_exact_user_id=match_exact_user_id)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds),
                    'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/get_validator_roi_level_income', dependencies=[Depends(RightsChecker([143, 142]))])
def get_validator_roi_level_income(req: GetROILevelIncome_Request, token_payload: any = Depends(get_current_user)):
    try:
        # print(req)
        if (token_payload["role"] == 'User'):
            req.user_id = token_payload["user_id"]
            req.match_exact_user_id = True

        dataset = data_access.get_validator_roi_level_income(req=req, match_exact_user_id=req.match_exact_user_id)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds),
                    'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}

