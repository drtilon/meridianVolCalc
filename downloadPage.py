import requests
import csv
import time

# Replace with your actual API key
API_KEY = 'Y95N4ITKG65TZ821QVWE17J9F2A7JX7RGI'
API_URL = 'https://api.taikoscan.io/api'
# Token address
token_address = '0xa3f248a1779364fb8b6b59304395229ea8241229'

def fetch_transactions(token_address, start_block, end_block, api_key):
    transactions = []
    page = 1
    while True:
        params = {
            'module': 'account',
            'action': 'tokentx',
            'address': token_address,
            'startblock': start_block,
            'endblock': end_block,
            'page': page,
            'offset': 1000,  # Number of transactions per page
            'apikey': api_key
        }
        response = requests.get(API_URL, params=params)
        time.sleep(7)
        
        # Print status code and response text for debugging
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        
        try:
            data = response.json()
        except ValueError:
            print("Error: Response is not valid JSON.")
            return transactions  # Return what we have so far

        if data['status'] == '1' and 'result' in data:
            result = data['result']
            if not result:
                break
            transactions.extend(result)
            page += 1
        else:
            print(f"API Error: {data.get('message', 'Unknown error')}")
            break
    return transactions

# Example usage
start_block = 305421
end_block =  338360  # Set to the latest block or adjust as needed
transactions = []

while start_block < end_block:
    if start_block > end_block:
        transactions += fetch_transactions(token_address, start_block, end_block, API_KEY)
    else:
        transactions += fetch_transactions(token_address, start_block, start_block+5000, API_KEY)
    start_block += 5000

# Save to CSV
with open('transactions.csv', 'w', newline='') as csvfile:
    fieldnames = ['blockNumber', 'timeStamp', 'hash', 'from', 'to', 'value', 'tokenName', 'tokenSymbol']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for tx in transactions:
        writer.writerow({
            'blockNumber': tx.get('blockNumber'),
            'timeStamp': tx.get('timeStamp'),
            'hash': tx.get('hash'),
            'from': tx.get('from'),
            'to': tx.get('to'),
            'value': tx.get('value'),
            'tokenName': tx.get('tokenName'),
            'tokenSymbol': tx.get('tokenSymbol'),
        })

print(f"Fetched and saved {len(transactions)} transactions.")

