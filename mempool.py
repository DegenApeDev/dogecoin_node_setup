import subprocess
import json

def run_dogecoin_cli(command):
    try:
        result = subprocess.run(['dogecoin-cli', command], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None

def run_curl(txid):
    api_url = f'http://127.0.0.1:3000/tx/{txid}'
    try:
        result = subprocess.run(['curl', api_url], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running curl command: {e}")
        return None

# Get raw mempool transactions
raw_mempool_output = run_dogecoin_cli('getrawmempool')

if raw_mempool_output is not None:
    # Parse the JSON output
    try:
        mempool_transactions = json.loads(raw_mempool_output)
        print("Mempool Transactions:")
        for txid in mempool_transactions:
            print(f"{txid}")

            curl_result = run_curl(txid)

            if curl_result is not None:
                print("Curl Result:")
                print(curl_result)
            # If you want more details about each transaction, you can use 'getrawtransaction'
            # raw_transaction = run_dogecoin_cli(f'getrawtransaction {txid}')
            # parsed_transaction = json.loads(raw_transaction)
            # Process the details as needed
            print()
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
