
from fastapi import APIRouter, Depends
from src.constants.messages import INVALID_USER_ID, OK, DATABASE_CONNECTION_ERROR
from src.data_access.admin import details as data_access
from src.business_layer.security.Jwt import get_current_user
from src.business_layer.security.RightsChecker import RightsChecker
from src.utilities.utils import data_frame_to_json_object, get_error_message
from src.constants import VALIDATORS


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get('/details', dependencies=[Depends(RightsChecker([11]))])
def details(admin_user_id: str = VALIDATORS.USER_ID, token_payload: any = Depends(get_current_user)):
    try:
        user_id_token = token_payload["user_id"]

        if admin_user_id == user_id_token:
            dataset = data_access.get_admin_details(admin_user_id=admin_user_id)
            if len(dataset) > 0 and len(dataset['rs']):
                ds = dataset['rs']
                if ds.iloc[0].loc["valid"]:
                    return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds)}
                
            return {'success': False, 'message': INVALID_USER_ID }
        return {'success': False, 'message': INVALID_USER_ID }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/dashboard_details', dependencies=[Depends(RightsChecker([15]))])
def dashboard_details(token_payload: any = Depends(get_current_user)):
    try:
        user_id = token_payload["user_id"]

        dataset = data_access.get_admin_dashboard_details(admin_user_id=user_id)
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["valid"]:
                return {
                    'success': True,
                    'message': OK,
                    'data': data_frame_to_json_object(ds),
                    'income_distribution': data_frame_to_json_object(dataset['rs_income_distribution']),
                    'packages_sales': data_frame_to_json_object(dataset['rs_packages_sales'])
                }
            
            return {'success': False, 'message': INVALID_USER_ID }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/dashboard_chart_details', dependencies=[Depends(RightsChecker([15]))])
def dashboard_chart_details(duration: str = VALIDATORS.CHART_DURATION, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.get_admin_dashboard_chart_details(duration=duration)

        if len(dataset):
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(dataset['rs'])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_top_earners', dependencies=[Depends(RightsChecker([15]))])
def get_top_earners(page_index: int = 0, page_size: int = 10, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.get_top_earners(page_index=page_index, page_size=page_size)
        if len(dataset) > 0 and len(dataset['rs']) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}

