
from fastapi import APIRouter, Depends
from src.data_access.user import profile as data_access
from src.schemas.User import UserPersonalDetailsUpdateRequest, UserContactDetailsUpdateRequest, UserNomineeDetailsUpdateRequest
from src.business_layer.security.Jwt import get_current_user
from src.business_layer.security.RightsChecker import RightsChecker
from src.utilities.utils import get_error_message
from src.utilities.aes import aes


router = APIRouter(
    dependencies=[Depends(get_current_user), Depends(RightsChecker([13,18]))]
)


@router.put('/update_personal_details')
def update_personal_details(req: UserPersonalDetailsUpdateRequest, token_payload:any = Depends(get_current_user)):
    try:
        user_id = token_payload["user_id"]
        user_type = token_payload["role"]

        is_by_admin = False
        admin_user_id = ''

        if(user_type=="User"):
            req.user_id = user_id
        else:
            is_by_admin = True
            admin_user_id = user_id

        dataset = data_access.update_user_personal_details(user_id=req.user_id, name=req.name, dob=req.dob, gender=req.gender, marital_status=req.marital_status, is_by_admin=is_by_admin, by_admin_user_id=admin_user_id)
        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']
            if(ds.iloc[0].loc["success"]):
                return {'success': True, 'message': ds.iloc[0].loc["message"] }
            
            return {'success': False, 'message': ds.iloc[0].loc["message"] }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.put('/update_contact_details')
def update_contact_details(req: UserContactDetailsUpdateRequest, token_payload:any = Depends(get_current_user)):
    try:
        user_id = token_payload["user_id"]
        user_type = token_payload["role"]

        is_by_admin = False
        admin_user_id = ''

        if(user_type=="User"):
            req.user_id = user_id
        else:
            is_by_admin = True
            admin_user_id = user_id

        if(req.two_factor_auth_request_id!=''):
            req.two_factor_auth_request_id = int(aes.decrypt(req.two_factor_auth_request_id))
        else:
            req.two_factor_auth_request_id = 0
            
        dataset = data_access.update_user_contact_details(user_id=req.user_id, email_id=req.email_id, mobile_no=req.mobile_no, address=req.address, district=req.district, pin_code=req.pin_code, country=req.country, state=req.state, is_by_admin=is_by_admin, by_admin_user_id=admin_user_id, two_factor_auth_request_id=req.two_factor_auth_request_id)
        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']
            if(ds.iloc[0].loc["success"]):
                return {'success': True, 'message': ds.iloc[0].loc["message"] }
            
            return {'success': False, 'message': ds.iloc[0].loc["message"] }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.put('/update_nominee_details')
def update_nominee_details(req: UserNomineeDetailsUpdateRequest, token_payload:any = Depends(get_current_user)):
    try:
        user_id = token_payload["user_id"]
        user_type = token_payload["role"]

        is_by_admin = False
        admin_user_id = ''

        if(user_type=="User"):
            req.user_id = user_id
        else:
            is_by_admin = True
            admin_user_id = user_id

        dataset = data_access.update_user_nominee_details(user_id=req.user_id, nominee_title=req.nominee_title, nominee_name=req.nominee_name, nominee_relationship=req.nominee_relationship, is_by_admin=is_by_admin, by_admin_user_id=admin_user_id)
        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']
            if(ds.iloc[0].loc["success"]):
                return {'success': True, 'message': ds.iloc[0].loc["message"] }
            
            return {'success': False, 'message': ds.iloc[0].loc["message"] }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
