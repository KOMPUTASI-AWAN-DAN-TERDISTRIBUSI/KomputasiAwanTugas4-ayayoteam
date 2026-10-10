#!/usr/bin/env python3
# ZeroMQ Publisher — mengirim data sensor dummy secara berkala via protokol ZeroMQ PUB/SUB.
import zmq
import json
import time
import random
import sys
from datetime import datetime

# Konfigurasi warna terminal (ANSI escape codes).
HIJAU = "\033[92m"
KUNING = "\033[93m"
BIRU = "\033[94m"
CYAN = "\033[96m"
MERAH = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Konfigurasi default: topik, alamat bind, dan interval pengiriman.
TOPIK = "sensor_data"                # Topik untuk publish data
ALAMAT_BIND = "tcp://*:5555"         # Alamat binding publisher
INTERVAL_DEFAULT = 10                # Interval default (detik) untuk testing
INTERVAL_TUGAS = 60                  # Interval sesuai tugas (60 detik / 1 menit)


# Membuat data sensor dummy acak berisi sensor_id, suhu, kelembapan, dan timestamp.
def buat_data_sensor():
    sensor_id = random.choice(["SENSOR-01", "SENSOR-02", "SENSOR-03", "SENSOR-04"])

    data = {
        "sensor_id": sensor_id,
        "temperature": round(random.uniform(20.0, 35.0), 2),   # Suhu dalam °C (20-35)
        "humidity": round(random.uniform(40.0, 80.0), 2),       # Kelembapan dalam % (40-80)
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Waktu pengiriman
    }
    return data


# Menampilkan header program di terminal.
def tampilkan_header():
    print(f"\n{BOLD}{BIRU}{'=' * 60}{RESET}")
    print(f"{BOLD}{BIRU}  ╔══════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}{BIRU}  ║     🚀  ZeroMQ PUBLISHER - Data Sensor  🚀     ║{RESET}")
    print(f"{BOLD}{BIRU}  ║          Message Queueing System                ║{RESET}")
    print(f"{BOLD}{BIRU}  ╚══════════════════════════════════════════════════╝{RESET}")
    print(f"{BOLD}{BIRU}{'=' * 60}{RESET}\n")


# Menampilkan data sensor yang telah dikirim dalam format rapi.
def tampilkan_pesan_terkirim(nomor, data):
    print(f"{CYAN}┌──────────────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}│{RESET} {BOLD}{HIJAU}📤 Pesan #{nomor} Terkirim!{RESET}")
    print(f"{CYAN}│{RESET}  ├─ Sensor ID   : {KUNING}{data['sensor_id']}{RESET}")
    print(f"{CYAN}│{RESET}  ├─ Suhu        : {KUNING}{data['temperature']}°C{RESET}")
    print(f"{CYAN}│{RESET}  ├─ Kelembapan  : {KUNING}{data['humidity']}%{RESET}")
    print(f"{CYAN}│{RESET}  └─ Waktu       : {KUNING}{data['timestamp']}{RESET}")
    print(f"{CYAN}└──────────────────────────────────────────────────┘{RESET}\n")


# Main — parse argumen interval, bind socket PUB, lalu kirim data sensor berkala.
def main():
    if len(sys.argv) > 1:
        try:
            interval = int(sys.argv[1])
        except ValueError:
            print(f"{MERAH}[ERROR] Argumen harus berupa angka (detik).{RESET}")
            print(f"{KUNING}Contoh: python publisher.py 60{RESET}")
            sys.exit(1)
    else:
        interval = INTERVAL_DEFAULT

    tampilkan_header()

    context = zmq.Context()
    socket = context.socket(zmq.PUB)

    try:
        socket.bind(ALAMAT_BIND)
        print(f"{HIJAU}[✔] Publisher berhasil di-bind ke: {BOLD}{ALAMAT_BIND}{RESET}")
        print(f"{HIJAU}[✔] Topik publish: {BOLD}{TOPIK}{RESET}")
        print(f"{HIJAU}[✔] Interval pengiriman: {BOLD}{interval} detik{RESET}")
        print(f"{KUNING}[ℹ] Gunakan 'python publisher.py 60' untuk interval 1 menit (sesuai tugas){RESET}")
        print(f"{KUNING}[ℹ] Tekan Ctrl+C untuk menghentikan publisher\n{RESET}")

        time.sleep(1)  # Tunggu sebentar agar subscriber sempat connect

        nomor_pesan = 0  # Counter pesan yang dikirim

        while True:
            nomor_pesan += 1

            data_sensor = buat_data_sensor()

            pesan_json = json.dumps(data_sensor)

            socket.send_string(f"{TOPIK} {pesan_json}")  # Format: [topik] [data_json] agar subscriber bisa filter

            tampilkan_pesan_terkirim(nomor_pesan, data_sensor)

            time.sleep(interval)  # Tunggu sesuai interval sebelum kirim pesan berikutnya

    except KeyboardInterrupt:
        print(f"\n{KUNING}{'=' * 60}{RESET}")
        print(f"{KUNING}[⏹] Publisher dihentikan oleh pengguna.{RESET}")
        print(f"{KUNING}[ℹ] Total pesan terkirim: {BOLD}{nomor_pesan}{RESET}")
        print(f"{KUNING}{'=' * 60}{RESET}")
    except zmq.ZMQError as e:
        print(f"{MERAH}[✘] ZeroMQ Error: {e}{RESET}")
    finally:
        socket.close()
        context.term()  # Tutup socket dan context untuk membersihkan resource
        print(f"{HIJAU}[✔] Resource berhasil dibersihkan. Selesai.{RESET}\n")


if __name__ == "__main__":
    main()