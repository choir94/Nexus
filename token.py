import random
import secrets
from web3 import Web3
from colorama import Fore, Style, init
import time

# Initialize colorama
init(autoreset=True)

# Nexus Token Configuration
RPC_URL = "rpc.nexus.xyz/http"
CHAIN_ID = 392
DECIMALS = 18  # Set to the token's decimals (commonly 18 for most tokens)

# ABI for the ERC-20 token contract (Standard ERC-20 ABI for transfers)
ERC20_ABI = [
    {
        "constant": False,
        "inputs": [
            {"name": "to", "type": "address"},
            {"name": "value", "type": "uint256"},
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    }
]

def print_header():
    print(Fore.MAGENTA + Style.BRIGHT + "=" * 50)
    print(Fore.MAGENTA + Style.BRIGHT + "Auto Send Tokens".center(50))
    print(Fore.YELLOW + "Telegram: @airdrop_node".center(50))
    print(Fore.CYAN + "Bot created by: https://t.me/airdrop_node".center(50))
    print(Fore.MAGENTA + Style.BRIGHT + "=" * 50)

# Fetch token symbol dynamically
def get_token_symbol(web3, token_address):
    try:
        token_contract = web3.eth.contract(address=token_address, abi=ERC20_ABI)
        return token_contract.functions.symbol().call()
    except Exception as e:
        print(Fore.RED + f"Gagal mengambil simbol token: {e}")
        return "NEX"

# Transfer ERC-20 tokens function
def transfer_token(sender, senderkey, recipient, amount, web3, token_address, token_symbol, retries=3):
    for attempt in range(retries):
        try:
            token_contract = web3.eth.contract(address=token_address, abi=ERC20_ABI)
            token_amount = int(amount * (10 ** DECIMALS))

            nonce = web3.eth.get_transaction_count(sender)
            base_gas_price = web3.eth.gas_price
            gas_price = int(base_gas_price * (1.2 + attempt * 0.1))

            transaction = {
                'chainId': CHAIN_ID,
                'from': sender,
                'gas': 200000,
                'gasPrice': gas_price,
                'nonce': nonce,
                'to': token_address,
                'data': token_contract.encodeABI(fn_name='transfer', args=[recipient, token_amount]),
            }

            signed_txn = web3.eth.account.sign_transaction(transaction, senderkey)
            print(Fore.CYAN + f'Memproses pengiriman {amount} {token_symbol} ke alamat: {recipient} ...')

            tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            txid = web3.to_hex(tx_hash)
            web3.eth.wait_for_transaction_receipt(tx_hash)

            print(Fore.GREEN + f'Pengiriman {amount} {token_symbol} ke {recipient} berhasil!')
            print(Fore.GREEN + f'TX-ID : {txid}')
            break
        except Exception as e:
            print(Fore.RED + f"Error pada percobaan {attempt + 1}: {e}")
            if 'replacement transaction underpriced' in str(e):
                print(Fore.YELLOW + "Gas price terlalu rendah. Meningkatkan gas price untuk percobaan berikutnya...")
            if attempt < retries - 1:
                print(Fore.YELLOW + f"Mencoba lagi dalam 60 detik... ({attempt + 1}/{retries})")
                time.sleep(60)
            else:
                print(Fore.RED + f"Transaksi gagal setelah {retries} percobaan.")

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
        if attempt == retries - 1:
            print(Fore.RED + f"Gagal terhubung ke RPC setelah {retries} percobaan.")
            return None

# Main execution
print_header()

# Ask the user for the token address
TOKEN_ADDRESS = input("Masukkan alamat kontrak ERC-20 token: ").strip()

# Use Nexus Token RPC URL
web3 = check_rpc_url(RPC_URL)

# Fetch token symbol dynamically
CURRENCY_SYMBOL = get_token_symbol(web3, TOKEN_ADDRESS)

# Ask the user for their private key
private_key = input("Masukkan private key Anda: ")
sender = web3.eth.account.from_key(private_key)

# Ask the user how many transactions to process
loop = int(input("Berapa banyak transaksi yang ingin diproses?: "))

# Ask the user how much to send per transaction
amount = float(input(f"Berapa banyak {CURRENCY_SYMBOL} yang akan dikirim per transaksi (contoh: 0.001)?: "))

# Ask the user for recipient addresses
recipients = []
for i in range(loop):
    recipient = input(f"Masukkan alamat penerima untuk transaksi {i + 1}: ").strip()
    recipients.append(recipient)

for i, recipient in enumerate(recipients):
    print(Fore.CYAN + f"\nMemproses Transaksi {i + 1}/{loop}")
    transfer_token(sender.address, private_key, recipient, amount, web3, TOKEN_ADDRESS, CURRENCY_SYMBOL)
    time.sleep(60)

print(Fore.GREEN + "\nSemua transaksi selesai.")
