import requests
from fastapi import APIRouter

from src.business_layer.blockchain_service import get_current_block_timestamp
from src.data_access.automation import withdrawal as data_access
from src.constants.messages import INVALID_AUTOMATION_KEY
from src.utilities.utils import get_error_message, config

router = APIRouter()


@router.get('/reject_pending_withdrawals')
def reject_pending_withdrawals(key: str):
    try:
        if key == config['AutomationKey']:

            current_block_timestamp = get_current_block_timestamp()

            data_access.reject_pending_withdrawals(timestamp=current_block_timestamp)

            return {'success': False, 'message': 'Execution successful!'}
        return {'success': False, 'message': INVALID_AUTOMATION_KEY}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}

