import random
import secrets
from web3 import Web3
from colorama import Fore, Style, init
import time

# Initialize colorama
init(autoreset=True)

# Monad Token Configuration
RPC_URL = "https://rpc.monad.xyz"
CHAIN_ID = 80085
DECIMALS = 18  # Set to the token's decimals (commonly 18 for most tokens)
SYMBOL = "MON"  # Native token symbol

# Check if the RPC URL is valid
def check_rpc_url(rpc_url, retries=3):
    for attempt in range(retries):
        try:
            web3 = Web3(Web3.HTTPProvider(rpc_url))
            if web3.is_connected():
                print(Fore.GREEN + "Terhubung ke RPC dengan sukses!")
                chain_id = web3.eth.chain_id
                print(Fore.CYAN + f"Chain ID: {chain_id}")
                return web3
            else:
                print(Fore.RED + "Gagal terhubung ke RPC. Periksa URL dan coba lagi.")
                if attempt < retries - 1:
                    print(Fore.YELLOW + f"Mencoba ulang dalam 5 detik... ({attempt + 1}/{retries})")
                    time.sleep(5)
        except Exception as e:
            print(Fore.RED + f"Error menghubungkan ke RPC pada percobaan {attempt + 1}: {e}")
            if attempt < retries - 1:
                print(Fore.YELLOW + f"Mencoba ulang dalam 5 detik... ({attempt + 1}/{retries})")
                time.sleep(5)
    print(Fore.RED + f"Gagal terhubung ke RPC setelah {retries} percobaan.")
    return None

# Main execution
web3 = check_rpc_url(RPC_URL)
if web3 is None:
    exit()

# Ask the user for the private key
private_key = input("Masukkan private key Anda: ").strip()

# Ask the user for the recipient addresses
recipient_addresses = input("Masukkan alamat penerima (pisahkan dengan koma jika lebih dari satu): ").strip().split(',')
recipient_addresses = [addr.strip() for addr in recipient_addresses]

# Save the details to a file
with open("transaction_details.txt", "w") as file:
    for recipient in recipient_addresses:
        file.write(f"Recipient Address: {recipient}\n")

def send_native_token(senderkey, recipients, amount, web3):
    try:
        sender = web3.eth.account.from_key(senderkey).address
        nonce = web3.eth.get_transaction_count(sender)
        gas_price = web3.eth.gas_price
        amount_wei = Web3.to_wei(1, 'ether')
        
        for recipient in recipients:
            transaction = {
                'chainId': CHAIN_ID,
                'to': recipient,
                'value': amount_wei,
                'gas': 21000,
                'gasPrice': gas_price,
                'nonce': nonce
            }
            signed_txn = web3.eth.account.sign_transaction(transaction, senderkey)
            print(Fore.CYAN + f'Memproses pengiriman {Web3.from_wei(amount_wei, "ether")} {SYMBOL} ke alamat: {recipient} ...')
            
            tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            txid = web3.to_hex(tx_hash)
            web3.eth.wait_for_transaction_receipt(tx_hash)
            
            print(Fore.GREEN + f'Pengiriman {Web3.from_wei(amount_wei, "ether")} {SYMBOL} ke {recipient} berhasil!')
            print(Fore.GREEN + f'TX-ID : {txid}')
            
            nonce += 1  # Increment nonce for each transaction
            time.sleep(60)  # Add 60 seconds delay between transactions
    except Exception as e:
        print(Fore.RED + f"Gagal mengirim token: {e}")

# Perform the transfer
send_native_token(private_key, recipient_addresses, 1, web3)
