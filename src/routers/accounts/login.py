
from fastapi import APIRouter, Request

from src.data_access.accounts import login as data_access
from src.constants import VALIDATORS
from src.constants.messages import DATABASE_CONNECTION_ERROR, INVALID_CREDENTIALS, OK
from src.business_layer.login_service import member_id_to_user_id
from src.business_layer.security.Jwt import create_access_token
from src.business_layer.security.TokenData import TokenData
from src.routers.accounts.register import send_joining_mail_and_sms
from src.schemas.Accounts import LoginRequest
from src.utilities.aes import aes
from src.utilities.utils import get_error_message, get_ip_info, to_json_obj, config, company_details

router = APIRouter(
    tags=["Login"]
)


@router.post('/login')
def login(data: LoginRequest, request: Request):
    try:
        url = dict(request.scope["headers"]).get(b"referer", b"").decode()  # request.base_url.__str__()
        
        if request.client is None:
            client_ip_address = request.headers['x-forwarded-for']
        else:
            client_ip_address = request.client.host

        ip_details = None
        if not config['IsDevelopment']:
            ip_details = get_ip_info(client_ip_address)

        if company_details['is_decentralized']:
            data.username = member_id_to_user_id(member_id=data.username)

        if data.user_type == "AdminVal456##$@":
            data.user_type = 'Admin'

        dataset = data_access.login(user_id=data.username, 
                                    password=data.password, 
                                    url=url, 
                                    host=client_ip_address, 
                                    ip_details=ip_details,
                                    user_type=data.user_type)

        if len(dataset) > 0:

            login_info_df = dataset['rs']

            if len(login_info_df) > 0:
                if login_info_df.iloc[0].loc['valid']:  # credentials are valid

                    login_id = aes.encrypt(str(login_info_df.iloc[0].loc['login_id']))

                    return {
                        'success': True,
                        'message': OK,
                        'data': {
                            'user_id': login_info_df.iloc[0].loc['user_id'],
                            'user_type': login_info_df.iloc[0].loc['user_type'],
                            'login_id': login_id
                        }}

                return {'success': False, 'message': INVALID_CREDENTIALS}
            return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/request_login_token')
def request_login_token(user_id: str = VALIDATORS.USER_ID, login_id: str = VALIDATORS.LOGIN_ID):
    try:
        login_id = aes.decrypt(login_id)
        dataset = data_access.can_get_login_token(user_id=user_id, login_id=login_id)

        if len(dataset) > 0:

            login_info_df = dataset['rs']

            if len(login_info_df) > 0:
                if login_info_df.iloc[0].loc['valid']:  # login_id is valid

                    access_token = ""
                    if login_info_df.iloc[0].loc['can_get_token']:  # is eligible to get login token
                        payload = TokenData()
                        payload.user_id = login_info_df.iloc[0].loc['user_id']
                        payload.role = login_info_df.iloc[0].loc['user_type']
                        payload.access_rights = login_info_df.iloc[0].loc['access_rights']

                        access_token = create_access_token(data={"payload": to_json_obj(payload)})

                        if login_info_df.iloc[0].loc['user_type'] == 'User':
                            send_joining_mail_and_sms(aes.encrypt(user_id))

                    two_factor_auth_request_id = ""
                    if login_info_df.iloc[0].loc["is_two_factor_auth_enabled"] and login_info_df.iloc[0].loc['two_factor_auth_request_id'] > 0:
                        two_factor_auth_request_id = aes.encrypt(str(login_info_df.iloc[0].loc['two_factor_auth_request_id']))

                    return {
                        'success': True,
                        'message': login_info_df.iloc[0].loc['message'],
                        'data': {
                            'token': access_token,
                            'can_get_token': bool(login_info_df.iloc[0].loc['can_get_token']),
                            'code': int(login_info_df.iloc[0].loc['code']),
                            'user_id': login_info_df.iloc[0].loc['user_id'],
                            'user_type': login_info_df.iloc[0].loc['user_type'],
                            'access_rights': login_info_df.iloc[0].loc['access_rights'],
                            'profile_image_url': login_info_df.iloc[0].loc['profile_image_url'],
                            'is_two_factor_auth_enabled': bool(login_info_df.iloc[0].loc['is_two_factor_auth_enabled']),
                            'is_two_factor_auth_successful': bool(login_info_df.iloc[0].loc['is_two_factor_auth_successful']),
                            'two_factor_auth_request_id': two_factor_auth_request_id,
                            'is_email_verification_required': bool(login_info_df.iloc[0].loc['is_email_verification_required']),
                            'is_email_verified': bool(login_info_df.iloc[0].loc['is_email_verified']),
                            'is_mobile_verification_required': bool(login_info_df.iloc[0].loc['is_mobile_verification_required']),
                            'is_mobile_verified': bool(login_info_df.iloc[0].loc['is_mobile_verified']),
                            'email_id': login_info_df.iloc[0].loc['email_id'],
                            'mobile_no': login_info_df.iloc[0].loc['mobile_no']
                        }}

                return {'success': False, 'message': login_info_df.iloc[0].loc['message']}
            return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}

