from fastapi import APIRouter, Depends

from src.schemas.Admin_Miscellaneous import AddNews
from src.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.data_access.admin.miscellaneous import update_sponsor as data_access
from src.business_layer.security.Jwt import get_current_user
from src.business_layer.security.RightsChecker import RightsChecker
from src.utilities.utils import data_frame_to_json_object, get_error_message


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get('/update_sponsor', dependencies=[Depends(RightsChecker([237]))])
def update_sponsor(user_id: str, sponsor_id: str, token_payload: any = Depends(get_current_user)):
    try:
        by_admin_id = token_payload["user_id"]

        dataset = data_access.update_sponsor(user_id=user_id, sponsor_id=sponsor_id, admin_user_id=by_admin_id)
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_sponsor_update_history', dependencies=[Depends(RightsChecker([237]))])
def get_sponsor_update_history(page_index: int, page_size: int, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.get_sponsor_update_history(page_index=page_index, page_size=page_size)
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}

