import requests
from src.utilities.utils import config


def get_current_block_timestamp():
    url = ("https://api.polygonscan.com/api?module=proxy&action=eth_blockNumber&apikey=" + config['PolygonScan']['ApiKey'])

    response = requests.request('GET', url=url)
    data = response.json()

    block_number_hex = data['result']
    print(block_number_hex)
    block_number = int(block_number_hex, 16)
    print(block_number)

    timestamp = None
    while timestamp is None:
        url = (
            f"https://api.polygonscan.com/api?module=block&action=getblockreward&blockno={block_number - 5}&apikey={config['PolygonScan']['ApiKey']}")

        response = requests.request('GET', url=url)
        data = response.json()

        timestamp = data['result']['timeStamp']
        print(timestamp)
        block_number = block_number - 1

    return timestamp
