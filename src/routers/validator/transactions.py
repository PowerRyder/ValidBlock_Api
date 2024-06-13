from fastapi import APIRouter, Depends
from src.business_layer.security.RightsChecker import RightsChecker
from src.constants.messages import NO_TRANSACTIONS_FOUND, OK
from src.data_access.validator import transactions as data_access

from src.business_layer.security.Jwt import get_current_user
from src.utilities.utils import data_frame_to_json_object, get_error_message

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get('/get_bsc_validator_transactions', dependencies=[Depends(RightsChecker([10, 11]))])
def get_bsc_validator_transactions(page_index: int = 0, page_size: int = 10, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.get_bsc_validator_transactions(page_index=page_index, page_size=page_size)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds),
                    'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

        return {'success': False, 'message': NO_TRANSACTIONS_FOUND}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}



@router.get('/get_solana_validator_transactions', dependencies=[Depends(RightsChecker([10, 11]))])
def get_solana_validator_transactions(page_index: int = 0, page_size: int = 10, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.get_solana_validator_transactions(page_index=page_index, page_size=page_size)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds),
                    'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

        return {'success': False, 'message': NO_TRANSACTIONS_FOUND}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}

