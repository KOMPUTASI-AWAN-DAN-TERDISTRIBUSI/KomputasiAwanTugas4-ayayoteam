# 🖧 Program RPC — Bilangan Prima

## Tugas 04 Cloud Computing

Program ini mengimplementasikan **Remote Procedure Call (RPC)** menggunakan library bawaan Python yaitu `xmlrpc`. Program terdiri dari **server** dan **client** yang berkomunikasi melalui protokol XML-RPC.

---

## 📋 Deskripsi Program

| Komponen | File | Keterangan |
|----------|------|------------|
| **Server** | `server.py` | Menyediakan fungsi `get_prime_numbers(n)` yang mengembalikan daftar bilangan prima hingga `n` |
| **Client** | `client.py` | Menghubungi server dan memanggil fungsi tersebut secara remote |

### Cara Kerja

1. **Server** berjalan di port `8000` (bind `0.0.0.0` agar bisa diakses device lain) dan menunggu request dari client
2. **Client** menghubungi server, mengirim parameter `n` (batas angka)
3. **Server** menghitung bilangan prima dari 2 hingga `n` menggunakan algoritma *Sieve of Eratosthenes*
4. **Server** mengirim hasilnya kembali ke client melalui XML-RPC
5. **Client** menampilkan hasilnya di terminal

### Contoh

```
Input  : n = 20
Output : [2, 3, 5, 7, 11, 13, 17, 19]
```

---

## ⚙️ Persyaratan

- **Python 3.x** (sudah terinstall di sebagian besar sistem)
- **Tidak perlu install library tambahan** (`pip install` tidak diperlukan)
- Library `xmlrpc` sudah termasuk dalam Python standard library

---

## 🚀 Cara Menjalankan

### Skenario 1 Laptop

Server dan client dijalankan di laptop yang sama. Client memakai host
default `localhost`, jadi tidak perlu mengubah apa pun.

**Terminal pertama** — jalankan server:

```bash
cd rpc
python3 server.py
```

Server akan menampilkan pesan bahwa server aktif dan menunggu request:

```
╔═══════════════════════════════════════════════════╗
║        XML-RPC SERVER — BILANGAN PRIMA           ║
╠═══════════════════════════════════════════════════╣
║  Host    : 0.0.0.0                                 ║
║  Port    : 8000                                    ║
╠═══════════════════════════════════════════════════╣
║  Status  : Server AKTIF dan menunggu request...  ║
║  Tekan Ctrl+C untuk menghentikan server          ║
╚═══════════════════════════════════════════════════╝
```

> **Catatan:** Biarkan terminal ini tetap terbuka selama menggunakan program.

**Terminal kedua** — jalankan client:

```bash
cd rpc
python3 client.py
```

Client akan meminta input batas angka:

```
  Masukkan batas angka (atau 'q' untuk keluar): 20
```

Kemudian client akan menampilkan hasil bilangan prima yang diterima dari server.

### Cara Menghentikan Program

- Untuk keluar dari **client**: ketik `q` lalu tekan Enter
- Untuk menghentikan **server**: tekan `Ctrl+C` di terminal server

---

## 🌐 Skenario 2 Laptop (Server & Client Terpisah)

Server bind ke `0.0.0.0` sehingga otomatis terlihat dari device lain.
Yang perlu diatur hanya client, agar tahu IP device server.

1. Cek IP device server:

   ```bash
   ip addr   # Linux, atau:
   ipconfig  # Windows
   ```

   Catat IP-nya, misal `192.168.1.50`.

2. Jalankan server di **device server** seperti biasa:

   ```bash
   python3 server.py
   ```

3. Jalankan client di **device client** sambil memberitahu IP server,
   lewat salah satu cara berikut:

   ```bash
   # Cara 1: argumen CLI
   python3 client.py 192.168.1.50

   # Cara 2: environment variable
   RPC_HOST=192.168.1.50 python3 client.py    # Linux/macOS

   set RPC_HOST=192.168.1.50 && python3 client.py   # Windows (cmd)
   ```

4. Izinkan port `8000/tcp` di firewall device server.

---

## 🐳 Cara Menjalankan dengan Docker

Semua service didefinisikan di `docker-compose.yml` di root project
(`docker-compose.yml`, `Dockerfile`). Tidak perlu install Python/library,
cukup jalankan perintah berikut dari **root project**.

### Jalankan Server (Container)

```bash
docker compose up -d rpc-server
```

Server berjalan sebagai service background dan mengekspos port `8000`.

### Jalankan Client (Container Interaktif)

```bash
docker compose run --rm rpc-client
```

Client otomatis terhubung ke server via hostname internal `rpc-server`
(diatur lewat environment `RPC_HOST`), jadi tidak perlu mengubah IP.

### Melihat Log & Menghentikan

```bash
docker compose logs -f rpc-server    # lihat log server
docker compose down                  # hentikan semua service
```

> **Catatan:** Jika image belum pernah di-build, `docker compose up` akan
> build otomatis. Untuk build manual: `docker build -t ayayoteam-tugas4 .`

---

## 📁 Struktur File

```
rpc/
├── server.py    # Server XML-RPC
├── client.py    # Client XML-RPC
└── README.md    # Dokumentasi (file ini)
```

---

## 📖 Penjelasan Teknologi

### Apa itu RPC?

**Remote Procedure Call (RPC)** adalah mekanisme komunikasi yang memungkinkan sebuah program memanggil fungsi/prosedur yang berada di komputer/proses lain, seolah-olah fungsi tersebut ada di program lokal.

### Apa itu XML-RPC?

**XML-RPC** adalah protokol RPC yang menggunakan **XML** untuk meng-encode data dan **HTTP** sebagai mekanisme transport. Python menyediakan library bawaan `xmlrpc.server` dan `xmlrpc.client` untuk implementasi XML-RPC.

### Diagram Alur

```
┌──────────┐    HTTP Request (XML)     ┌──────────┐
│          │  ───────────────────────>  │          │
│  Client  │   get_prime_numbers(20)   │  Server  │
│          │  <───────────────────────  │          │
└──────────┘    HTTP Response (XML)    └──────────┘
                [2,3,5,7,11,13,17,19]
```
