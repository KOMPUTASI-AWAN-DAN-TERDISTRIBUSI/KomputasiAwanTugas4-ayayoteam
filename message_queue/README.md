# 📡 Message Queueing dengan ZeroMQ

## Deskripsi Program

Program ini merupakan implementasi **Message Queueing** menggunakan library **ZeroMQ (pyzmq)** dengan pola **PUB/SUB (Publisher/Subscriber)** dalam bahasa Python.

### Cara Kerja

- **Publisher** (`publisher.py`) bertindak sebagai pengirim data sensor dummy (suhu & kelembapan) secara berkala.
- **Subscriber** (`subscriber.py`) bertindak sebagai penerima yang mendengarkan dan menampilkan data sensor dari publisher.
- Komunikasi dilakukan melalui protokol **TCP** pada port **5555**.

### Data Sensor yang Dikirim

| Field         | Deskripsi                          |
|---------------|------------------------------------|
| `sensor_id`   | ID sensor (SENSOR-01 s/d SENSOR-04)|
| `temperature` | Suhu acak antara 20°C - 35°C      |
| `humidity`    | Kelembapan acak antara 40% - 80%   |
| `timestamp`   | Waktu pengiriman data              |

---

## Instalasi

### 1. Install Library yang Dibutuhkan

```bash
pip install pyzmq
```

Atau menggunakan file `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## Cara Menjalankan

### Skenario 1 Laptop

Publisher dan subscriber dijalankan di laptop yang sama. Subscriber memakai
host default `localhost`.

**Terminal 1** — jalankan publisher:

```bash
# Untuk testing (interval 10 detik - default)
python publisher.py

# Untuk tugas (interval 60 detik / 1 menit)
python publisher.py 60
```

**Terminal 2** — jalankan subscriber:

```bash
python subscriber.py
```

> **Catatan:** Publisher harus dijalankan **terlebih dahulu** sebelum subscriber agar tidak ada data yang terlewat.

---

## 🌐 Skenario 2 Laptop (Publisher & Subscriber Terpisah)

Publisher bind ke `tcp://*:5555` sehingga otomatis terlihat dari device lain.
Yang perlu diatur hanya subscriber, agar tahu IP device publisher.

1. Cek IP device publisher:

   ```bash
   ip addr   # Linux, atau:
   ipconfig  # Windows
   ```

   Catat IP-nya, misal `192.168.1.50`.

2. Jalankan publisher di **device publisher** seperti biasa:

   ```bash
   python publisher.py
   ```

3. Jalankan subscriber di **device subscriber** sambil memberitahu IP publisher,
   lewat salah satu cara berikut:

   ```bash
   # Cara 1: argumen CLI
   python subscriber.py 192.168.1.50

   # Cara 2: environment variable
   ZMQ_HOST=192.168.1.50 python subscriber.py    # Linux/macOS

   set ZMQ_HOST=192.168.1.50 && python subscriber.py   # Windows (cmd)
   ```

4. Izinkan port `5555/tcp` di firewall device publisher.

---

## 🐳 Cara Menjalankan dengan Docker

Semua service didefinisikan di `docker-compose.yml` di root project
(`docker-compose.yml`, `Dockerfile`). Tidak perlu install Python/library,
cukup jalankan perintah berikut dari **root project**.

### Jalankan Publisher + Subscriber (Container)

```bash
docker compose up -d mq-publisher mq-subscriber
```

- `mq-publisher` berjalan sebagai service background, publish tiap 10 detik,
  mengekspos port `5555`.
- `mq-subscriber` otomatis menerima dari publisher via hostname internal
  `mq-publisher` (diatur lewat environment `ZMQ_HOST`).

### Melihat Log & Menghentikan

```bash
docker compose logs -f mq-publisher    # lihat log publisher
docker compose logs -f mq-subscriber   # lihat log subscriber (data diterima)
docker compose down                    # hentikan semua service
```

> **Catatan:** Jika image belum pernah di-build, `docker compose up` akan
> build otomatis. Untuk build manual: `docker build -t ayayoteam-tugas4 .`
> Menyesuaikan interval: edit `docker-compose.yml` bagian `mq-publisher`,
> ubah `"10"` pada baris command menjadi, misal, `"60"` untuk 1 menit.

---

## Pengaturan Interval

| Perintah               | Interval      | Keterangan                     |
|------------------------|---------------|--------------------------------|
| `python publisher.py`    | 10 detik      | Default untuk testing cepat    |
| `python publisher.py 60` | 60 detik      | Sesuai spesifikasi tugas       |
| `python publisher.py 5`  | 5 detik       | Custom interval (contoh)       |

---

## Struktur File

```
message_queue/
├── publisher.py       # Program pengirim data sensor (PUB)
├── subscriber.py      # Program penerima data sensor (SUB)
├── requirements.txt   # Daftar library yang dibutuhkan
└── README.md          # Dokumentasi program
```

---

## Menghentikan Program

Tekan **Ctrl+C** pada masing-masing terminal untuk menghentikan publisher dan subscriber.
