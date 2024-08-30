from web3 import Web3

taiko_rpc_url = 'https://rpc.taiko.xyz'  
web3 = Web3(Web3.HTTPProvider(taiko_rpc_url))
from_block = web3.to_hex(305421)
to_block = web3.to_hex(305432)


contract_address = '0xa3f248A1779364FB8B6b59304395229ea8241229'

event_signature = web3.keccak(text='Transfer(address,address,uint256)').hex()

filter_params = {
    'fromBlock': from_block,
    'toBlock': to_block,
    'address': contract_address
}
total_amount = 0
# Fetch logs
try:
    logs = web3.eth.get_logs(filter_params)
    for log in logs:
        amount_hex = log['data'].hex()  # Convert HexBytes to hex string
        amount = int(amount_hex, 16)
        tx_hash = log['transactionHash'].hex()
        #print(f"Transaction Hash: {tx_hash}")
        print(f"Amount Transferred: {amount}")
        total_amount += amount
        
except Exception as e:
    print(f"An error occurred: {e}")

