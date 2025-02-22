import secrets
import time
from web3 import Web3
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Nexus Network Configuration
RPC_URL = "rpc.nexus.xyz/http"
CHAIN_ID = 392
DECIMALS = 18  # Set to the token's decimals (commonly 18 for most tokens)

# List of recipient addresses
RECIPIENTS = [
    "0x175dB51A58F12cfa1BD5A1096c8D6E7F31faAdf0",
    "0x4a9B045e4395371066De4deD1b8EAFD9f2e621EE",
    "0xE73d3CA82b36662FC740f48341Ab4b0C6aCa7E93",
    "0xE73d3CA82b36662FC740f48341Ab4b0C6aCa7E93"
]

# Function to send native Nexus tokens
def send_native_nexus(sender, senderkey, recipient, web3, retries=3):
    amount = 1  # Sending exactly 1 NEX per transaction
    for attempt in range(retries):
        try:
            nonce = web3.eth.get_transaction_count(sender)
            base_gas_price = web3.eth.gas_price
            gas_price = int(base_gas_price * (1.2 + attempt * 0.1))

            transaction = {
                'chainId': CHAIN_ID,
                'nonce': nonce,
                'to': recipient,
                'value': int(amount * (10 ** DECIMALS)),
                'gas': 21000,
                'gasPrice': gas_price,
            }

            signed_txn = web3.eth.account.sign_transaction(transaction, senderkey)
            print(Fore.CYAN + f'Memproses pengiriman {amount} NEX ke alamat: {recipient} ...')

            tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            txid = web3.to_hex(tx_hash)
            web3.eth.wait_for_transaction_receipt(tx_hash)

            print(Fore.GREEN + f'Pengiriman {amount} NEX ke {recipient} berhasil!')
            print(Fore.GREEN + f'TX-ID : {txid}')
            break
        except Exception as e:
            print(Fore.RED + f"Error pada percobaan {attempt + 1}: {e}")
            if attempt < retries - 1:
                print(Fore.YELLOW + f"Mencoba lagi dalam 60 detik... ({attempt + 1}/{retries})")
                time.sleep(60)
            else:
                print(Fore.RED + f"Transaksi gagal setelah {retries} percobaan.")

# Function to check RPC connection
def check_rpc_url(rpc_url, retries=3):
    for attempt in range(retries):
        try:
            web3 = Web3(Web3.HTTPProvider(rpc_url))
            if web3.is_connected():
                print(Fore.GREEN + "Terhubung ke RPC dengan sukses!")
                print(Fore.CYAN + f"Chain ID: {web3.eth.chain_id}")
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
private_key = input("Masukkan private key Anda: ")
sender = web3.eth.account.from_key(private_key)

for recipient in RECIPIENTS:
    print(Fore.CYAN + f"\nMemproses pengiriman ke {recipient}")
    send_native_nexus(sender.address, private_key, recipient, web3)
    time.sleep(60)

print(Fore.GREEN + "\nSemua transaksi selesai.")

