import requests
from fastapi import APIRouter, Depends
from src.constants.messages import DATABASE_CONNECTION_ERROR, INVALID_IFSC, OK
from src.data_access import misc as data_access
from src.business_layer.security.Jwt import get_current_user
from src.business_layer.security.RightsChecker import RightsChecker
from src.business_layer import misc_service
from src.utilities.utils import data_frame_to_json_object, get_error_message, config
from src.constants import VALIDATORS
import pyqrcode


router = APIRouter(
    prefix="/misc",
    tags=["Miscellaneous"]
)


@router.get('/get_countries')
def get_countries():
    try:
        dataset = data_access.get_countries()

        if len(dataset) > 0:
            df = dataset['rs']

            if len(df) > 0:
                df = data_frame_to_json_object(df)
                return {'success': True, 'message': OK, 'data': df }
                
            return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_states_by_country_id')
def get_states_by_country_id(country_id: int):
    try:
        dataset = data_access.get_states_by_country_id(country_id=country_id)
        # print(dataset)
        if len(dataset) > 0:
            df = dataset['rs']

            if len(df) > 0:
                df = data_frame_to_json_object(df)
                return {'success': True, 'message': OK, 'data': df }
                
            return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_bank_details_by_ifsc')
def get_bank_details_by_ifsc(ifsc: str = VALIDATORS.IFSCODE):
    try:
        dataset = data_access.get_bank_details_by_ifsc(ifsc=ifsc)
        # print(dataset)
        if len(dataset) > 0:
            df = dataset['rs']

            if len(df) > 0:
                df = data_frame_to_json_object(df)
                return {'success': True, 'message': OK, 'data': df}
                
            return {'success': False, 'message': INVALID_IFSC, 'data': []}
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_supported_cryptos')
def get_supported_cryptos(action: str = VALIDATORS.CRYPTO_ACTION, id: int = 0, chain_id: int = -1):
    try:
        dataset = data_access.get_supported_cryptos(action=action, id=id, chain_id=chain_id)
        # print(dataset)
        if len(dataset) > 0:
            df = dataset['rs']

            if len(df) > 0:
                df = data_frame_to_json_object(df)
                return {'success': True, 'message': OK, 'data': df}
                
            return {'success': False, 'message': INVALID_IFSC, 'data': []}
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_qr')
def get_qr(value: str):
    try:
        qr = pyqrcode.create(value)
        # print(dataset)
        return {'success': True, 'message': OK, 'qr': "data:image/png;base64,"+qr.png_as_base64_str(scale=5) }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_column_details')
def get_column_details(report_name: str):
    try:
        dataset = data_access.get_column_details(report_name=report_name)
        # print(dataset)
        if len(dataset) > 0:
            df = dataset['rs']

            if len(df) > 0:
                df = data_frame_to_json_object(df)
                return {'success': True, 'message': OK, 'data': df}
                
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/filter_user_ids', dependencies=[Depends(RightsChecker([104]))])
def filter_user_ids(filter_value: str, user_type: str = VALIDATORS.USER_TYPE, token_payload: any = Depends(get_current_user)):
    try:

        # start_time = time.time()
        if token_payload['role'] == 'User':
            user_type = 'User'

        dataset = data_access.filter_user_ids(filter_value=filter_value, user_type=user_type)
        # print(dataset)
        if len(dataset) > 0:
            df = dataset['rs']
            # end_time = time.time()
            # print("--- %s seconds ---" % (end_time - start_time))
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(df)}
                
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_token_rate')
def get_token_rate(base_token_symbol: str, quote_token_symbol: str):
    return misc_service.get_token_rate(base_token_symbol=base_token_symbol, quote_token_symbol=quote_token_symbol)

