#!/bin/bash

# Skrip instalasi logo
curl -s https://raw.githubusercontent.com/choir94/Airdropguide/main/logo.sh | bash
sleep 5

# Warna untuk output
BLUE='\033[0;34m'
WHITE='\033[0;97m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RESET='\033[0m'

# Direktori skrip saat ini
SCRIPT_DIR="$(cd "$(dirname \"${BASH_SOURCE[0]}\")" && pwd)"
cd "$SCRIPT_DIR" || exit

# Fungsi instalasi dependensi
install_dependencies() {
    echo -e "${YELLOW}Menginstal dependensi...${RESET}"
    
    if [ ! -d ".git" ]; then
        echo -e "${YELLOW}Menginisialisasi repository Git...${RESET}"
        git init
    fi
    
    if ! command -v forge &> /dev/null; then
        echo -e "${YELLOW}Menginstal Foundry...${RESET}"
        source <(wget -O - https://raw.githubusercontent.com/choir94/Airdropguide/main/Foundry.sh)
    fi
}

# Fungsi input detail yang diperlukan
input_required_details() {
    echo -e "${YELLOW}-----------------------------------${RESET}"
    
    [ -f "$SCRIPT_DIR/token_deployment/.env" ] && rm "$SCRIPT_DIR/token_deployment/.env"
    
    read -p "Masukkan Private Key Anda: " PRIVATE_KEY
    read -p "Masukkan Nama Token: " TOKEN_NAME
    read -p "Masukkan Symbol Token: " TOKEN_SYMBOL
    
    RPC_URL="https://rpc.nexus.xyz/"
    EXPLORER_URL="https://explorer.nexus.xyz"
    
    mkdir -p "$SCRIPT_DIR/token_deployment"
    cat <<EOL > "$SCRIPT_DIR/token_deployment/.env"
PRIVATE_KEY="$PRIVATE_KEY"
TOKEN_NAME="$TOKEN_NAME"
TOKEN_SYMBOL="$TOKEN_SYMBOL"
RPC_URL="$RPC_URL"
EXPLORER_URL="$EXPLORER_URL"
EOL
}

# Fungsi untuk deploy kontrak
deploy_contract() {
    echo -e "${YELLOW}-----------------------------------${RESET}"
    source "$SCRIPT_DIR/token_deployment/.env"

    mkdir -p "$SCRIPT_DIR/src"
    cat <<EOL > "$SCRIPT_DIR/src/AirdropNode.sol"
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract AirdropNode is ERC20 {
    constructor() ERC20("$TOKEN_NAME", "$TOKEN_SYMBOL") {
        _mint(msg.sender, 1000 * (10 ** decimals()));
    }
}
EOL

    echo -e "${BLUE}Mengompilasi kontrak...${RESET}"
    forge build || { echo -e "${RED}Kompilasi gagal.${RESET}"; exit 1; }

    echo -e "${BLUE}Mendeploy kontrak...${RESET}"
    DEPLOY_OUTPUT=$(forge create "$SCRIPT_DIR/src/AirdropNode.sol:AirdropNode" \
        --rpc-url "$RPC_URL" \
        --private-key "$PRIVATE_KEY" \
        --broadcast)

    if [[ $? -ne 0 ]]; then
        echo -e "${RED}Deploy kontrak gagal.${RESET}"
        exit 1
    fi

    CONTRACT_ADDRESS=$(echo "$DEPLOY_OUTPUT" | grep -oP 'Deployed to: \K(0x[a-fA-F0-9]{40})')
    echo -e "${YELLOW}Kontrak berhasil di-deploy di alamat: $CONTRACT_ADDRESS${RESET}"
    echo -e "${WHITE}Lihat kontrak di: ${BLUE}$EXPLORER_URL/address/$CONTRACT_ADDRESS${RESET}"

    echo -e "${BLUE}Memverifikasi kontrak...${RESET}"
    forge verify-contract \
      --rpc-url "$RPC_URL" \
      --verifier blockscout \
      --verifier-url "$EXPLORER_URL/api/" \
      "$CONTRACT_ADDRESS" \
      "$SCRIPT_DIR/src/AirdropNode.sol:AirdropNode"
}

install_dependencies
input_required_details
deploy_contract

echo -e "${YELLOW}-----------------------------------${RESET}"
echo -e "${BLUE}Gabung di channel Telegram untuk update dan bantuan: https://t.me/airdrop_node${RESET}"
