
from pydantic import BaseModel
from src.constants import VALIDATORS


class AdminDetailsUpdateRequest(BaseModel):
    user_id: str = VALIDATORS.USER_ID
    email_id: str = VALIDATORS.EMAIL_ID
    mobile_no: str = VALIDATORS.MOBILE_NO
    two_factor_auth_request_id: str = ''


class AddNewAdminRequest(BaseModel):
    admin_user_id: str = VALIDATORS.USER_ID
    password: str = VALIDATORS.PASSWORD
    email_id: str = VALIDATORS.EMAIL_ID
    mobile_no: str = VALIDATORS.MOBILE_NO
    

class AdminAccessRightsUpdateRequest(BaseModel):
    user_id: str = VALIDATORS.USER_ID
    access_rights: str = VALIDATORS.ACCESS_RIGHTS
