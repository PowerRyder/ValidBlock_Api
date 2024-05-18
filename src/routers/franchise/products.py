
from fastapi import APIRouter, Depends
from src.constants.messages import OK, DATABASE_CONNECTION_ERROR
from src.data_access.franchise import products as data_access
from src.business_layer.security.Jwt import get_current_user
from src.business_layer.security.RightsChecker import RightsChecker
from src.schemas.Franchise import GetFranchiseProducts_Request, GetFranchiseProductStockTransactions_Request
from src.utilities.utils import data_frame_to_json_object, get_error_message

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post('/get_franchise_products', dependencies=[Depends(RightsChecker([210, 211, 212, 213]))])
def get_franchise_products(req: GetFranchiseProducts_Request, token_payload: any = Depends(get_current_user)):
    try:
        match_exact_user_id = False
        if token_payload["role"] != 'Admin':
            req.franchise_id = token_payload["user_id"]
            match_exact_user_id = True

        dataset = data_access.get_franchise_products(req=req, match_exact_user_id=match_exact_user_id)

        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/get_franchise_product_stock_transactions', dependencies=[Depends(RightsChecker([210, 211, 212, 213]))])
def get_franchise_product_stock_transactions(req: GetFranchiseProductStockTransactions_Request, token_payload: any = Depends(get_current_user)):
    try:
        match_exact_user_id = False
        if token_payload["role"] != 'Admin':
            req.franchise_id = token_payload["user_id"]
            match_exact_user_id = True

        print(req)

        dataset = data_access.get_franchise_product_stock_transactions(req=req, match_exact_user_id=match_exact_user_id)

        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
