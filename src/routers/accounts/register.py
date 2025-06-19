from fastapi import APIRouter

from src.data_access.accounts import register as register_data_access
from src.data_access.user import details as user_details_data_access
from src.constants import VALIDATORS
from src.constants.messages import DATABASE_CONNECTION_ERROR, INVALID_USER_ID, JOINING_INFO_ALREADY_SENT, \
    JOINING_INFO_SEND_ERROR, OK
from src.business_layer.email_service import send_joining_mail
from src.business_layer.sms_service import send_joining_sms
from src.routers.docs.welcome_letter import get_welcome_letter_pdf_bytes
from src.schemas.Accounts import Register
from src.utilities.aes import aes
from src.utilities.utils import addCurrencySymbol, data_frame_to_json_object
from src.utilities.utils import company_details, get_error_message, hide_email_address, hide_mobile_no

router = APIRouter(
    tags=["Register"]
)


@router.post('/register')
def register(request: Register):
    try:
        dataset = register_data_access.register(request)
        # print(dataset)
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                
                send_joining_mail_and_sms(aes.encrypt(ds.iloc[0].loc["user_id"]))
                # end_time = time.time()
                # print("--- %s seconds ---" % (end_time - start_time))
                return {'success': True, 'message': ds.iloc[0].loc["message"], 'user_id': ds.iloc[0].loc["user_id"]}
        
            return {'success': False, 'message': ds.iloc[0].loc["message"]}
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/is_sponsor_valid')
def is_sponsor_valid(sponsor_id: str = VALIDATORS.USER_ID):
    try:
        dataset = register_data_access.is_sponsor_valid(sponsor_id=sponsor_id)
        # print(dataset)

        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            ds = data_frame_to_json_object(ds)
            return {'success': True, 'message': OK, 'data': ds }
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/is_upline_valid')
def is_upline_valid(upline_user_id: str = VALIDATORS.USER_ID):
    try:
        dataset = register_data_access.is_upline_valid(upline_user_id=upline_user_id)
        # print(dataset)
        
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            ds = data_frame_to_json_object(ds)
            return {'success': True, 'message': OK, 'data': ds }
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/does_user_id_exist')
def does_user_id_exist(user_id: str = VALIDATORS.USER_ID):
    try:
        dataset = register_data_access.does_user_id_exist(user_id=user_id)
        # print(dataset)
        
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            ds = data_frame_to_json_object(ds)
            return {'success': True, 'message': OK, 'data': ds }
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/send_joining_mail_and_sms')
def send_joining_mail_and_sms(id_enc: str):
    try:
        user_id = aes.decrypt(id_enc)

        dataset = user_details_data_access.get_user_details(user_id=user_id)
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["valid"]:
                is_email_sent=False
                is_sms_sent=False

                if ds.iloc[0].loc["is_joining_mail_sent"] and ds.iloc[0].loc["is_joining_sms_sent"]:
                    return {'success': False, 'message': JOINING_INFO_ALREADY_SENT }

                email_id = ds.iloc[0].loc['email_id']
                if not ds.iloc[0].loc["is_joining_mail_sent"]:
                    pdf_bytes = get_welcome_letter_pdf_bytes(ds.iloc[0].loc["user_id"])
                    is_email_sent, sent_message = send_joining_mail(user_id=ds.iloc[0].loc['user_id'],
                                                                    password=ds.iloc[0].loc['password'],
                                                                    user_name=ds.iloc[0].loc['name'],
                                                                    email_id=email_id,
                                                                    joining_amount=addCurrencySymbol(str(round(ds.iloc[0].loc['joining_amount'], int(company_details['round_off_digits'])))),
                                                                    sponsor_id=ds.iloc[0].loc['sponsor_id'],
                                                                    referral_link=ds.iloc[0].loc['referral_link'])

                mobile_no = ds.iloc[0].loc['mobile_no']
                if not ds.iloc[0].loc["is_joining_sms_sent"]:
                    is_sms_sent, sent_message = send_joining_sms(user_id=ds.iloc[0].loc['user_id'], user_name=ds.iloc[0].loc['name'], mobile_no=mobile_no)
                
                register_data_access.update_joining_mail_and_sms_status(user_id=user_id, is_email_sent=is_email_sent, is_sms_sent=is_sms_sent)

                if is_email_sent or is_sms_sent:
                    msg = "Your joining info is sent to your" + ((" mobile number" + hide_mobile_no(mobile_no=mobile_no)) if(is_sms_sent) else "") + (" and " if(is_sms_sent and is_email_sent) else "") + (" email id "+ hide_email_address(email_id=email_id) if(is_sms_sent) else "") +"."
                    return {'success': True, 'message': msg }

                return {'success': False, 'message': JOINING_INFO_SEND_ERROR }

            return {'success': False, 'message': INVALID_USER_ID }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
