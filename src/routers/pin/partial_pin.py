
from fastapi import APIRouter, Depends
from src.business_layer.security.Jwt import get_current_user
from src.business_layer.security.RightsChecker import RightsChecker
from src.schemas.Pin import PayPartialPinAmountRequest
from src.constants.messages import DATABASE_CONNECTION_ERROR
from src.data_access.pin import partial_pin as data_access
from src.utilities.utils import get_error_message


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.post('/pay_partial_pin_amount', dependencies=[Depends(RightsChecker([46, 47, 48, 49]))])
def pay_partial_pin_amount(req: PayPartialPinAmountRequest, token_payload: any = Depends(get_current_user)):
    try:

        dataset = data_access.pay_partial_pin_amount(req=req, admin_user_id=token_payload["user_id"])
        # print(dataset)
        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']
            if(ds.iloc[0].loc["success"]):
                return {'success': True, 'message': ds.iloc[0].loc["message"] }
            
            return {'success': False, 'message': ds.iloc[0].loc["message"] }
        
        return {'success' : False, 'message' : DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success' : False, 'message' : get_error_message(e)}
    