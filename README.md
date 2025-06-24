# Panduan Instalasi Nexus pada VPS

Berikut adalah langkah-langkah manual untuk menginstal Nexus pada VPS.
## 0. One Click

```bash
wget https://raw.githubusercontent.com/choir94/Nexus/refs/heads/main/Nexus.sh
chmod +x Nexus.sh
./Nexus.sh
```

## 1. Hapus Folder .nexus (Jika Ada)

Jika kamu ingin membersihkan instalasi sebelumnya, hapus folder `.nexus` dengan perintah berikut:

```bash
rm -rf ~/.nexus
```
## 2. Perbarui Paket Sistem
Untuk memastikan bahwa sistem kamu sudah terbarui, jalankan perintah berikut:
```bash
sudo apt update && sudo apt upgrade -y
```
Setelah itu, instal beberapa dependensi yang diperlukan untuk kompilasi dan instalasi Nexus CLI:
```bash
sudo apt install build-essential pkg-config libssl-dev git-all -y
```
```bash
sudo apt update
sudo apt install -y protobuf-compiler
```
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```
```bash
source $HOME/.cargo/env
export PATH="$HOME/.cargo/bin:$PATH"
```
```bash
curl -LO https://github.com/protocolbuffers/protobuf/releases/download/v25.2/protoc-25.2-linux-x86_64.zip
unzip protoc-25.2-linux-x86_64.zip -d $HOME/.local
export PATH="$HOME/.local/bin:$PATH"
```

## 3. Jalankan Nexus di Sesi Screen
Untuk menjalankan Nexus di latar belakang agar tetap berjalan meskipun kamu keluar dari terminal, gunakan screen:

Buat sesi screen baru:
```bash
screen -S nexus
```
Jalankan ulang Nexus CLI dengan perintah berikut:
```bash
curl https://cli.nexus.xyz/ | sh
```
Masukkan Node ID

Untuk menemukan node-id, buka https://app.nexus.xyz/nodes
Klik Add Node, klik Add CLI Nodedan salin node-id dan tempel di terminal

## Done

## Join Telegram Airdrop Node:  

[Telegram Airdrop Node]
(https://t.me/airdrop_node)
