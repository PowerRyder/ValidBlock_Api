
from fastapi import APIRouter, Depends

from src.data_access.pin import pin_product_dispatch as data_access
from src.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.business_layer.security.Jwt import get_current_user
from src.business_layer.security.RightsChecker import RightsChecker
from src.schemas.Pin import PinProductDispatchDetailsRequest, PinProductDispatchStatusUpdateRequest
from src.utilities.utils import data_frame_to_json_object, get_error_message

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.post('/get_pin_product_dispatch_details', dependencies=[Depends(RightsChecker([70, 71, 72]))])
async def get_pin_product_dispatch_details(req: PinProductDispatchDetailsRequest, token_payload: any = Depends(get_current_user)):
    try:
        match_exact_user_id = False

        if (token_payload["role"] == "User"):
            req.user_id = token_payload["user_id"]
            match_exact_user_id = True

        if (token_payload["role"] == "Franchise"):
            req.by_user_id = token_payload["user_id"]
            req.by_user_type = token_payload["role"]

        dataset = data_access.get_pin_product_dispatch_details(req, match_exact_user_id)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds),
                    'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}

@router.put('/update_pin_product_dispatch_status', dependencies=[Depends(RightsChecker([70, 71, 72]))])
async def update_pin_product_dispatch_status(req: PinProductDispatchStatusUpdateRequest, token_payload: any = Depends(get_current_user)):
    try:
        by_user_id = token_payload["user_id"]
        by_user_type = token_payload["role"]
        print(req)
        dataset = data_access.update_pin_product_dispatch_status(req=req, by_user_id=by_user_id, by_user_type=by_user_type)
        if len(dataset) > 0:
            ds = dataset['rs']
            if(ds.iloc[0].loc["success"]):
                return {'success': True, 'message': ds.iloc[0].loc["message"] }

            return {'success': False, 'message': ds.iloc[0].loc["message"] }

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
