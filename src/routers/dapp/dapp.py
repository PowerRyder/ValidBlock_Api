
from fastapi import APIRouter
from src.routers.automation.dapp import process_dapp_contract_transaction

router = APIRouter()


@router.get('/process_transaction')
def process_transaction(txn_hash: str):
    return process_dapp_contract_transaction(txn_hash=txn_hash)
