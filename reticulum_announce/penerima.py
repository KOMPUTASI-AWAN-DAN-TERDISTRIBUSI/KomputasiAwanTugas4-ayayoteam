#!/usr/bin/env python3
# Node B - Penerima Announce (Receiver). Mendengarkan announce dari Node A dan menampilkan informasi yang diterima.
import RNS
import time
import datetime
import sys


# Handler untuk menangani announce yang diterima, dipanggil saat announce sesuai aspect_filter masuk.
class AnnounceHandler:
    aspect_filter = "tugas_cloud.announce.demo"  # Filter aspek target (format app.aspek1.aspek2), harus penuh agar hash cocok dengan destination Node A

    def __init__(self):
        self.counter = 0  # Penghitung jumlah announce yang diterima

    def received_announce(self, destination_hash, announced_identity, app_data):
        self.counter += 1

        timestamp_diterima = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        hash_hex = RNS.prettyhexrep(destination_hash)

        if app_data is not None:
            pesan = app_data.decode("utf-8")
        else:
            pesan = "(tidak ada data)"

        print("+" + "-" * 58 + "+")
        print(f"| ANNOUNCE DITERIMA #{self.counter:03d}")
        print("+" + "-" * 58 + "+")
        print(f"| Hash Pengirim   : {hash_hex}")
        print(f"| Pesan (App Data): {pesan}")
        print(f"| Waktu Diterima  : {timestamp_diterima}")
        print("+" + "-" * 58 + "+")
        print()


# Main — inisialisasi Reticulum, daftarkan handler, lalu tunggu announce dari Node A.
def main():
    configdir = sys.argv[1] if len(sys.argv) > 1 else None  # Argumen opsional: direktori konfigurasi Reticulum (default ~/.reticulum)

    print("=" * 60)
    print("  NODE B - PENERIMA ANNOUNCE (RECEIVER)")
    print("  Program Reticulum Announce")
    print("=" * 60)
    print()

    print("[INFO] Menginisialisasi Reticulum...")
    reticulum = RNS.Reticulum(configdir=configdir)
    print("[OK]   Reticulum berhasil diinisialisasi.\n")

    print("[INFO] Mendaftarkan Announce Handler...")
    print(f"       Aspect Filter: {AnnounceHandler.aspect_filter}")

    handler = AnnounceHandler()
    RNS.Transport.register_announce_handler(handler)

    print("[OK]   Announce Handler berhasil didaftarkan.\n")

    print("-" * 60)
    print("  Menunggu announce dari Node A...")
    print("  Pastikan pengirim.py sudah dijalankan di terminal lain.")
    print("  Tekan Ctrl+C untuk menghentikan.")
    print("-" * 60)
    print()

    try:
        while True:
            time.sleep(1)  # Loop utama menjaga program tetap berjalan

    except KeyboardInterrupt:
        print("\n")
        print("=" * 60)
        print(f"  Program dihentikan oleh pengguna.")
        print(f"  Total announce diterima: {handler.counter}")
        print("=" * 60)


if __name__ == "__main__":
    main()