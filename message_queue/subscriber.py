#!/usr/bin/env python3
# ZeroMQ Subscriber — menerima data sensor dari publisher via protokol ZeroMQ PUB/SUB.
import zmq
import json
import sys
import os
from datetime import datetime

# Konfigurasi warna terminal (ANSI escape codes).
HIJAU = "\033[92m"
KUNING = "\033[93m"
BIRU = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
MERAH = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Konfigurasi default: topik yang di-subscribe dan alamat publisher. Host publisher: argumen CLI > env ZMQ_HOST > default localhost (127.0.0.1 = 1 laptop, IP lain = 2 laptop/docker).
TOPIK = "sensor_data"                        # Topik yang di-subscribe
PUB_HOST = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("ZMQ_HOST", "localhost")
ALAMAT_CONNECT = f"tcp://{PUB_HOST}:5555"    # Alamat publisher


# Menampilkan header program di terminal.
def tampilkan_header():
    print(f"\n{BOLD}{MAGENTA}{'=' * 60}{RESET}")
    print(f"{BOLD}{MAGENTA}  ╔══════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}{MAGENTA}  ║    📡  ZeroMQ SUBSCRIBER - Data Sensor  📡     ║{RESET}")
    print(f"{BOLD}{MAGENTA}  ║          Message Queueing System                ║{RESET}")
    print(f"{BOLD}{MAGENTA}  ╚══════════════════════════════════════════════════╝{RESET}")
    print(f"{BOLD}{MAGENTA}{'=' * 60}{RESET}\n")


# Menampilkan data sensor yang diterima dalam format rapi dengan warna suhu.
def tampilkan_pesan_diterima(nomor, data, waktu_terima):
    suhu = data.get("temperature", 0)
    if suhu >= 30:
        warna_suhu = MERAH       # Suhu tinggi -> merah
        ikon_suhu = "🔴"
    elif suhu >= 25:
        warna_suhu = KUNING      # Suhu sedang -> kuning
        ikon_suhu = "🟡"
    else:
        warna_suhu = HIJAU       # Suhu rendah -> hijau
        ikon_suhu = "🟢"

    print(f"{BIRU}┌──────────────────────────────────────────────────────┐{RESET}")
    print(f"{BIRU}│{RESET} {BOLD}{CYAN}📥 Pesan #{nomor} Diterima!{RESET}")
    print(f"{BIRU}│{RESET}  ├─ Sensor ID     : {HIJAU}{data.get('sensor_id', 'N/A')}{RESET}")
    print(f"{BIRU}│{RESET}  ├─ Suhu          : {warna_suhu}{suhu}°C {ikon_suhu}{RESET}")
    print(f"{BIRU}│{RESET}  ├─ Kelembapan    : {HIJAU}{data.get('humidity', 'N/A')}%{RESET}")
    print(f"{BIRU}│{RESET}  ├─ Waktu Kirim   : {KUNING}{data.get('timestamp', 'N/A')}{RESET}")
    print(f"{BIRU}│{RESET}  └─ Waktu Terima  : {KUNING}{waktu_terima}{RESET}")
    print(f"{BIRU}└──────────────────────────────────────────────────────┘{RESET}\n")


# Main — connect ke publisher, subscribe topik, lalu terima dan tampilkan data sensor.
def main():
    tampilkan_header()

    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    try:
        socket.connect(ALAMAT_CONNECT)
        print(f"{HIJAU}[✔] Subscriber terhubung ke: {BOLD}{ALAMAT_CONNECT}{RESET}")

        socket.setsockopt_string(zmq.SUBSCRIBE, TOPIK)  # Filter hanya pesan topik 'sensor_data'
        print(f"{HIJAU}[✔] Subscribe ke topik: {BOLD}{TOPIK}{RESET}")
        print(f"{KUNING}[ℹ] Menunggu data dari publisher...{RESET}")
        print(f"{KUNING}[ℹ] Tekan Ctrl+C untuk menghentikan subscriber\n{RESET}")

        nomor_pesan = 0  # Counter pesan yang diterima

        while True:
            pesan_mentah = socket.recv_string()  # Format pesan: "[topik] [data_json]"

            waktu_terima = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            bagian = pesan_mentah.split(" ", 1)

            if len(bagian) < 2:
                print(f"{MERAH}[✘] Format pesan tidak valid: {pesan_mentah}{RESET}")
                continue

            topik = bagian[0]
            data_json = bagian[1]

            try:
                data_sensor = json.loads(data_json)
                nomor_pesan += 1

                tampilkan_pesan_diterima(nomor_pesan, data_sensor, waktu_terima)

            except json.JSONDecodeError as e:
                print(f"{MERAH}[✘] Gagal parse JSON: {e}{RESET}")
                print(f"{MERAH}    Data mentah: {data_json}{RESET}\n")

    except KeyboardInterrupt:
        print(f"\n{KUNING}{'=' * 60}{RESET}")
        print(f"{KUNING}[⏹] Subscriber dihentikan oleh pengguna.{RESET}")
        print(f"{KUNING}[ℹ] Total pesan diterima: {BOLD}{nomor_pesan}{RESET}")
        print(f"{KUNING}{'=' * 60}{RESET}")
    except zmq.ZMQError as e:
        print(f"{MERAH}[✘] ZeroMQ Error: {e}{RESET}")
        print(f"{MERAH}    Pastikan publisher sudah berjalan di port 5555.{RESET}")
    except Exception as e:
        print(f"{MERAH}[✘] Error tidak terduga: {e}{RESET}")
    finally:
        socket.close()
        context.term()  # Tutup socket dan context untuk membersihkan resource
        print(f"{HIJAU}[✔] Resource berhasil dibersihkan. Selesai.{RESET}\n")


if __name__ == "__main__":
    main()