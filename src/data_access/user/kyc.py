from src.schemas.KYC import KYCRequest, GetKYCRequest
from src.utilities.utils import execute_query


def request_for_kyc(user_id:str, req: KYCRequest):
    res = execute_query("call usp_insert_kyc_details(_user_id => %s, _name => %s, _date_of_birth => %s, _aadhaar_number => %s, _aadhaar_front_image => %s, _aadhaar_back_image => %s, _pan_number => %s, _pan_image => %s)",
                        (user_id, req.name, req.date_of_birth, req.aadhaar_number, req.aadhaar_front_image, req.aadhaar_back_image, req.pan_number, req.pan_image))
    return res


def get_kyc_requests(req: GetKYCRequest, match_exact_user_id: bool = False):
    res = execute_query("call usp_get_kyc_requests(_user_id => %s, _match_exact_user_id => %s, _between_date => %s::timestamptz[], _status => %s, _page_index => %s, _page_size => %s)",
                        (req.user_id, match_exact_user_id, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.status, req.page_index, req.page_size))
    return res


def update_kyc_requests_status(by_user_id: str, data_dicts):
    res = execute_query("call usp_update_kyc_request_status(_by_admin_id => %s, _data => %s::jsonb)",
                        (by_user_id, data_dicts))
    return res
