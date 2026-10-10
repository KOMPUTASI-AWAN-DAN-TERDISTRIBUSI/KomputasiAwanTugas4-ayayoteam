# Program Reticulum Announce - Tugas Cloud Computing

## Deskripsi

Program ini mendemonstrasikan fitur **Announce** pada **Reticulum Network Stack** menggunakan dua node yang saling berkomunikasi:

- **Node A (Announcer)** — Mengirim announce secara periodik setiap 10 detik ke jaringan Reticulum. Setiap announce berisi pesan beserta timestamp pengiriman.
- **Node B (Receiver)** — Mendengarkan announce dari Node A dan menampilkan informasi yang diterima, termasuk hash pengirim, pesan (app_data), dan waktu penerimaan.

Kedua node menggunakan `app_name='tugas_cloud'` dengan `aspects=['announce', 'demo']` untuk memastikan hanya announce yang relevan yang diterima.

---

## Instalasi

### 1. Pastikan Python 3 Terinstal

```bash
python3 --version
```

### 2. Install Dependency

```bash
pip install -r requirements.txt
```

Atau langsung:

```bash
pip install rns
```

---

## Cara Menjalankan

> **Penting:** Di jaringan yang memblokir multicast (umumnya WiFi/AP kantor,
> dan beberapa konfigurasi firewall Windows), interface bawaan Reticulum
> (`AutoInterface`) **tidak akan menemukan node lain**. Gejalanya di log:
> `WinError 10042` dan `No multicast echoes received`.
>
> Solusinya: gunakan **TCP interface** (lihat skenario di bawah). Dua direktori
> konfigurasi sample sudah disediakan: `config_server/` (untuk pengirim) dan
> `config_client/` (untuk penerima).

### Skenario 1 Laptop

Kedua node dijalankan di laptop yang sama. `config_client/` sudah mengarah
ke `127.0.0.1:49000` (loopback), jadi langsung jalan tanpa edit.

**Terminal 1** — jalankan penerima:

```bash
python3 penerima.py config_client
```

**Terminal 2** — jalankan pengirim:

```bash
python3 pengirim.py config_server
```

### Skenario 2 Laptop (Dua Node Terpisah)

`config_server/` dipakai di device pengirim, `config_client/` di device
penerima. Yang perlu diubah: arahkan client ke IP device pengirim.

1. Cek IP device pengirim:

   ```bash
   ip addr   # Linux, atau:
   ipconfig  # Windows
   ```

   Catat IP-nya, misal `192.168.1.50`.

2. Di file `config_client/config`, ganti `target_host`:

   ```ini
   [[TCP Client]]
     type = TCPClientInterface
     enabled = Yes
     target_host = 192.168.1.50
     target_port = 49000
   ```

3. Jalankan di masing-masing device:

   ```bash
   # Device pengirim
   python3 pengirim.py config_server

   # Device penerima
   python3 penerima.py config_client
   ```

4. Izinkan port `49000/tcp` di firewall device pengirim.

### Skenario Docker

Masing-masing node jalan di container. Semua service didefinisikan di
`docker-compose.yml` di root project. Jalankan kedua node sekaligus:

```bash
# Dari root project
docker compose up -d reticulum-pengirim reticulum-penerima
```

- `reticulum-pengirim` mengekspos port `49000` (TCP server).
- `reticulum-penerima` memakai `config_client_docker/` yang mengarah ke
  hostname internal `reticulum-pengirim` (bukan `127.0.0.1`, karena tiap
  container punya loopback sendiri).

Melihat announce diterima di penerima:

```bash
docker compose logs -f reticulum-penerima
```

Menghentikan:

```bash
docker compose down
```

> **Catatan:** Folder `config_*` di-copy ke image saat build, jadi
> `storage/` & `interfaces/` dibuat di dalam container dan tidak mengotori
> host. Argumen direktori konfigurasi bersifat opsional (default
> `~/.reticulum`). Saat build, `.dockerignore` mengecualikan folder runtime
> RNS agar tidak ikut masuk image.

> **Catatan:** Argumen direktori konfigurasi bersifat opsional. Jika tidak
> diberikan, Reticulum memakai konfigurasi default di `~/.reticulum`. Bila
> hanya menjalankan kedua node di **satu device** yang sama secara bersamaan,
> selalu pakai dua direktori konfigurasi berbeda, karena keduanya tidak boleh
> berbagi instance Reticulum yang sama.
>
> **Catatan:** Saat pertama kali dijalankan, Reticulum akan membuat folder
> `storage/` dan `interfaces/` di dalam `config_server/` dan `config_client/`
> secara otomatis. Folder itu normal dan boleh dibiarkan.

### Menghentikan Program

Tekan `Ctrl+C` di masing-masing terminal untuk menghentikan program.

---

## Contoh Output

### Terminal Node A (Announcer)

```
============================================================
  NODE A - PENGIRIM ANNOUNCE (ANNOUNCER)
  Program Reticulum Announce
============================================================

[INFO] Menginisialisasi Reticulum...
[OK]   Reticulum berhasil diinisialisasi.

[INFO] Membuat Identity baru untuk Node A...
[OK]   Identity berhasil dibuat.

[INFO] Membuat Destination...
       App Name : tugas_cloud
       Aspects  : ['announce', 'demo']
[OK]   Destination berhasil dibuat.
       Hash     : <a1b2c3d4e5f6>

------------------------------------------------------------
  Mulai mengirim Announce setiap 10 detik...
  Tekan Ctrl+C untuk menghentikan.
------------------------------------------------------------

[ANNOUNCE #001] Announce terkirim!
  Pesan     : Hello dari Node A! Timestamp: 2026-10-06 14:05:00
  Waktu     : 2026-10-06 14:05:00

[ANNOUNCE #002] Announce terkirim!
  Pesan     : Hello dari Node A! Timestamp: 2026-10-06 14:05:10
  Waktu     : 2026-10-06 14:05:10
```

### Terminal Node B (Receiver)

```
============================================================
  NODE B - PENERIMA ANNOUNCE (RECEIVER)
  Program Reticulum Announce
============================================================

[INFO] Menginisialisasi Reticulum...
[OK]   Reticulum berhasil diinisialisasi.

[INFO] Mendaftarkan Announce Handler...
       Aspect Filter: tugas_cloud
[OK]   Announce Handler berhasil didaftarkan.

------------------------------------------------------------
  Menunggu announce dari Node A...
  Pastikan pengirim.py sudah dijalankan di terminal lain.
  Tekan Ctrl+C untuk menghentikan.
------------------------------------------------------------

+----------------------------------------------------------+
| ANNOUNCE DITERIMA #001
+----------------------------------------------------------+
| Hash Pengirim   : <a1b2c3d4e5f6>
| Pesan (App Data): Hello dari Node A! Timestamp: 2026-10-06 14:05:00
| Waktu Diterima  : 2026-10-06 14:05:00
+----------------------------------------------------------+

+----------------------------------------------------------+
| ANNOUNCE DITERIMA #002
+----------------------------------------------------------+
| Hash Pengirim   : <a1b2c3d4e5f6>
| Pesan (App Data): Hello dari Node A! Timestamp: 2026-10-06 14:05:10
| Waktu Diterima  : 2026-10-06 14:05:10
+----------------------------------------------------------+
```

---

## Struktur File

```
reticulum_announce/
├── pengirim.py            # Pengirim Announce
├── penerima.py            # Penerima Announce
├── config_server/         # Konfigurasi pengirim (TCP server, port 49000)
├── config_client/         # Konfigurasi penerima (TCP client ke 127.0.0.1:49000)
├── requirements.txt       # Dependency Python
└── README.md              # Dokumentasi (file ini)
```

---

## Teknologi yang Digunakan

- **Python 3**
- **Reticulum Network Stack (RNS)** — Framework jaringan terdesentralisasi yang mendukung komunikasi aman dan anonim.
