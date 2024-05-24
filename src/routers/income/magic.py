
from fastapi import APIRouter, Depends
from src.data_access.income import magic as data_access
from src.constants.messages import (DATABASE_CONNECTION_ERROR, OK)
from src.business_layer.security.Jwt import get_current_user
from src.business_layer.security.RightsChecker import RightsChecker
from src.schemas.Income import GetScratchCards_Request
from src.utilities.utils import data_frame_to_json_object, get_error_message


router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post('/get_scratch_cards', dependencies=[Depends(RightsChecker([136, 137, 138, 139]))])
def get_scratch_cards(req: GetScratchCards_Request, token_payload: any = Depends(get_current_user)):
    try:
        match_exact_user_id = False
        if token_payload["role"] == 'User':
            req.user_id = token_payload["user_id"]
            match_exact_user_id = True
            
        dataset = data_access.get_scratch_cards(req=req, match_exact_user_id=match_exact_user_id)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}
            
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/process_magic_income_on_scratch', dependencies=[Depends(RightsChecker([136, 137, 138, 139]))])
def process_magic_income_on_scratch(scratch_card_id: int, token_payload: any = Depends(get_current_user)):
    try:
        user_id = token_payload["user_id"]
        
        dataset = data_access.process_magic_income_on_scratch(user_id=user_id, scratch_card_id=scratch_card_id)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}

