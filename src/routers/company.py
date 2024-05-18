import json

from fastapi import APIRouter
from src.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.utilities.utils import data_frame_to_json_object, get_error_message, company_details, company_datasets, config

router = APIRouter(
    prefix="/company",
    tags=["Company"]
    )


@router.get('/details')
def get_details():
    try:
        dataset = company_details.to_dict()

        with open(config['ERC20']['AbiJsonPath']) as f:
            erc20_token_contract_abi = json.load(f)

        with open(config['ArbitrageTrade']['AbiJsonPath']) as f:
            arbitrage_contract_abi = json.load(f)
        arbitrage_contract_address = config['ArbitrageTrade']['ContractAddress']

        with open(config['DApp']['AbiJsonPath']) as f:
            dapp_contract_abi = json.load(f)
        dapp_contract_address = config['DApp']['ContractAddress']
        payment_token_contract_address = config['DApp']['PaymentTokenContractAddress']

        if dataset:
            return {
                'success': True, 
                'message': OK, 
                'data': dataset, 
                'user_wallets': data_frame_to_json_object(company_datasets['rs_user_wallets']),
                'franchise_wallets': data_frame_to_json_object(company_datasets['rs_franchise_wallets']),
                'incomes_list': data_frame_to_json_object(company_datasets['rs_incomes']),
                'packages': data_frame_to_json_object(company_datasets['rs_packages']),
                'erc20_token_contract_abi': erc20_token_contract_abi,
                'arbitrage_contract_abi': arbitrage_contract_abi,
                'arbitrage_contract_address': arbitrage_contract_address,
                'dapp_contract_abi': dapp_contract_abi,
                'dapp_contract_address': dapp_contract_address,
                'payment_token_contract_address': payment_token_contract_address
                }
            
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }
    except Exception as e:
        print(e.__str__())
        return {'success' : False, 'message' : get_error_message(e)}
    
