import requests
import os
import subprocess
import sys

def download_file(url, filename):
    """Download file from a URL and save it locally"""
    r = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(r.content)

def create_or_verify_wallet():
    """Check existing wallet balance and create a new one if necessary"""
    keypair_path = '/root/.config/solana/id2.json'
    min_balance = 1.0  # Minimum balance in SOL required to use an existing wallet

    # Check if the keypair file exists and get balance
    if os.path.exists(keypair_path):
        result = subprocess.run(['solana', 'balance', keypair_path, '--url', 'https://api.devnet.solana.com'], capture_output=True, text=True)
        balance_output = result.stdout.strip()
        try:
            balance = float(balance_output.split()[0])  # Extract the numeric balance
            if balance >= min_balance:
                print(f"Existing wallet has sufficient balance: {balance} SOL")
                return keypair_path
        except (IndexError, ValueError):
            print("Failed to parse balance. Proceeding with new wallet creation.")

    # Create a new wallet if the existing one doesn't have sufficient balance or doesn't exist
    print("Creating new wallet or existing wallet has insufficient balance.")
    subprocess.run(['solana-keygen', 'new', '--outfile', keypair_path], check=True)
    subprocess.run(['solana', 'airdrop', '1', keypair_path, '--url', 'https://api.devnet.solana.com'], check=True)
    return keypair_path

# The rest of your code remains unchanged

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 script.py <Ethereum Address>")
        sys.exit(1)
    eth_address = sys.argv[1]
    keypair_path = create_or_verify_wallet()
    setup_solana_client(eth_address, keypair_path)
