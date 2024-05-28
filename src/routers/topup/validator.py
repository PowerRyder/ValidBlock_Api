import requests
from fastapi import APIRouter, Depends

from src.data_access.topup import validator as data_access
from src.constants.messages import (DATABASE_CONNECTION_ERROR, OK)
from src.business_layer.security.Jwt import get_current_user
from src.business_layer.security.RightsChecker import RightsChecker
from src.utilities.utils import get_error_message, config

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
