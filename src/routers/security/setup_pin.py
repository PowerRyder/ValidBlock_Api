from fastapi import APIRouter, Depends
from src.business_layer.security.RightsChecker import RightsChecker
from src.business_layer.security.Jwt import get_current_user
from src.constants.messages import DATABASE_CONNECTION_ERROR
from src.data_access.security import setup_pin as data_access
from src.utilities.utils import get_error_message
from src.utilities.aes import aes

router = APIRouter(
    tags=["Change PIN"]
)


@router.get('/change_user_pin', dependencies=[Depends(RightsChecker([24, 25, 61]))])
def change_user_pin(new_pin: str, two_factor_auth_request_id: str, token_payload: any = Depends(get_current_user)):
    try:
        user_id = token_payload["user_id"]

        if two_factor_auth_request_id != '':
            two_factor_auth_request_id = int(aes.decrypt(two_factor_auth_request_id))
        else:
            two_factor_auth_request_id = 0

        dataset = data_access.set_pin(user_id=user_id, pin=new_pin, two_factor_auth_request_id=two_factor_auth_request_id)

        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']

            if ds.iloc[0].loc["success"]:
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}


    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}

