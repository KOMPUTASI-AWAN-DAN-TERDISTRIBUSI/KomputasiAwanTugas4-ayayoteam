# 🐳 Panduan Docker — Tugas 04 Cloud Computing

Panduan menjalankan ketiga program tugas (RPC, Message Queue, Reticulum
Announce) menggunakan **Docker** dan **Docker Compose**. Tidak perlu install
Python maupun library — semua dependency dipasang di dalam image.

---

## 📋 Prasyarat

- **Docker Desktop** terinstall dan **berjalan** (daemon aktif).
- Docker Compose v2 (sudah include di Docker Desktop, perintah `docker compose`).

Cek kedua-duanya:

```bash
docker --version
docker compose version
```

> Jika muncul error `failed to connect to the docker API ... is the daemon
> running?`, buka Docker Desktop dulu sampai statusnya "Running".

---

## 📁 File Docker

| File | Keterangan |
|------|------------|
| `Dockerfile` | Membuat image Python 3.14-slim, install `pyzmq` + `rns`, copy project ke `/app` |
| `docker-compose.yml` | Definisi semua service (server, client, publisher, subscriber, pengirim, penerima) |
| `.dockerignore` | Mengecualikan `venv/`, `__pycache__/`, `.DS_Store`, dan folder runtime RNS agar tidak masuk image |

---

## 🔧 Service yang Tersedia

| Service | Program | Port | Ketergantungan |
|---------|---------|:----:|----------------|
| `rpc-server` | `rpc/server.py` | 8000 | — |
| `rpc-client` | `rpc/client.py` (interaktif) | — | `rpc-server` |
| `mq-publisher` | `message_queue/publisher.py` | 5555 | — |
| `mq-subscriber` | `message_queue/subscriber.py` | — | `mq-publisher` |
| `reticulum-pengirim` | `reticulum_announce/pengirim.py` | 49000 | — |
| `reticulum-penerima` | `reticulum_announce/penerima.py` | — | `reticulum-pengirim` |

> Antar container saling terhubung lewat **nama service** (mis. `rpc-server`),
> bukan IP atau `localhost`. Nilai ini diatur otomatis lewat environment
> (`RPC_HOST`, `ZMQ_HOST`) dan config khusus Docker
> (`reticulum_announce/config_client_docker/`).

---

## 🚀 Cara Menjalankan

Semua perintah dijalankan dari **root project** (folder yang berisi
`docker-compose.yml`).

### 1. Build Image

```bash
docker build -t ayayoteam-tugas4 .
```

> Sebenarnya langkah ini opsional: `docker compose up` akan build otomatis
> jika image belum ada.

### 2. Jalankan Semua Service

```bash
docker compose up -d
```

Opsi `-d` (detached) menjalankan semua service di background.

### 3. Menjalankan per Tugas

**RPC** — server background, client interaktif:

```bash
docker compose up -d rpc-server
docker compose run --rm rpc-client
```

Saat client jalan, masukkan batas angka (mis. `20`), lalu `q` untuk keluar.

**Message Queue** — publisher + subscriber:

```bash
docker compose up -d mq-publisher mq-subscriber
docker compose logs -f mq-subscriber
```

**Reticulum Announce** — pengirim + penerima:

```bash
docker compose up -d reticulum-pengirim reticulum-penerima
docker compose logs -f reticulum-penerima
```

---

## 🔍 Melihat Log & Memonitor

```bash
docker compose logs -f                 # semua service
docker compose logs -f rpc-server      # satu service
docker compose ps                      # status & port container
```

---

## 🛑 Menghentikan

```bash
docker compose stop                    # hentikan tanpa hapus container
docker compose down                    # hentikan + hapus container
docker compose down --rmi local        # + hapus image hasil build
```

---

## ⚙️ Penyesuaian

**Ganti interval publisher** (default 10 detik → sesuai tugas 60 detik):
edit `docker-compose.yml`, pada service `mq-publisher` ubah bagian command
`["python", "publisher.py", "10"]` menjadi `["python", "publisher.py", "60"]`,
lalu:

```bash
docker compose up -d mq-publisher
```

**Port bentrok dengan aplikasi lain:** ubah bagian `ports` pada
`docker-compose.yml`, mis. `"8000:8000"` → `"18000:8000"` (kiri = port host,
kanan = port container). Untuk client/aplikasi lain di host, pakai port host
yang baru.

---

## 🌐 Menjalankan Antar 2 Device dengan Docker

Untuk memisahkan service di dua mesin, jalankan bagian **server/publisher/
pengirim** di device pertama dengan port yang di-`-p` (expose), lalu arahkan
**client/subscriber/penerima** ke IP device pertama:

- **RPC:** jalankan client dari device lain dengan `RPC_HOST=<IP-device-server>`.
- **Message Queue:** jalankan subscriber dengan `ZMQ_HOST=<IP-device-publisher>`.
- **Reticulum:** edit `target_host` pada `reticulum_announce/config_client/config`
  menjadi IP device pengirim.

Pastikan port (`8000`, `5555`, `49000`) diizinkan di firewall device server.

---

## ❗ Troubleshooting

| Masalah | Solusi |
|---------|--------|
| `failed to connect to the docker API` | Docker Desktop belum jalan — buka sampai status Running |
| `port is already allocated` | Ubah pemetaan port host di `docker-compose.yml` |
| Penerima tidak menerima announce | Pastikan `reticulum-pengirim` jalan dan tunggu ~10 detik siklus announce |
| Subscriber tidak menerima data | Publisher harus jalan lebih dulu; cek log publisher |
| Image stale setelah ubah kode | `docker compose build` lalu `docker compose up -d` |