# Panduan Instalasi Nexus pada VPS

Berikut adalah langkah-langkah manual untuk menginstal Nexus pada VPS.

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
sudo apt update && sudo apt install -y protobuf-compiler && protoc --version && cargo build --release
```
```bash
source $HOME/.cargo/env
export PATH="$HOME/.cargo/bin:$PATH"
```
## 3. Instal Nexus CLI
Gunakan perintah berikut untuk mengunduh dan menginstal Nexus CLI:
```bash
curl https://cli.nexus.xyz/ | sh
```
Tunggu instalasi, CTRL+C 
## 4. Ubah Prover ID
Secara default, Nexus akan menghasilkan Prover ID secara acak. Jika ingin menggantinya dengan Prover ID milikmu

Edit Prover ID: Buka file konfigurasi yang berisi Prover ID:
```bash
nano ~/.nexus/prover-id
```
Ubah Prover ID: Hapus Prover ID yang dihasilkan secara acak dan ganti dengan ID milikmu sendiri.

Tekan Ctrl + X untuk keluar.

Tekan Y untuk mengonfirmasi perubahan.

Tekan Enter untuk menyimpan dan keluar dari editor.
## 5. Jalankan Nexus di Sesi Screen
Untuk menjalankan Nexus di latar belakang agar tetap berjalan meskipun kamu keluar dari terminal, gunakan screen:

Buat sesi screen baru:
```bash
screen -S nexus
```
Jalankan ulang Nexus CLI dengan perintah berikut:
```bash
curl https://cli.nexus.xyz/ | sh
```
## Done
## Support Airdrop Node

https://trakteer.id/AirdropNode/tip

## Join Telegram Airdrop Node:  

[Telegram Airdrop Node]
(https://t.me/airdrop_node)
