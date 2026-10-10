#!/usr/bin/env python3
# Node A - Pengirim Announce (Announcer). Mengirim announce berisi pesan + timestamp setiap 10 detik ke jaringan Reticulum.
import RNS
import time
import datetime
import sys


# Main — buat identity & destination, lalu kirim announce periodik.
def main():
    configdir = sys.argv[1] if len(sys.argv) > 1 else None  # Argumen opsional: direktori konfigurasi Reticulum (default ~/.reticulum)

    print("=" * 60)
    print("  NODE A - PENGIRIM ANNOUNCE (ANNOUNCER)")
    print("  Program Reticulum Announce")
    print("=" * 60)
    print()

    print("[INFO] Menginisialisasi Reticulum...")
    reticulum = RNS.Reticulum(configdir=configdir)
    print("[OK]   Reticulum berhasil diinisialisasi.\n")

    print("[INFO] Membuat Identity baru untuk Node A...")
    identity = RNS.Identity()
    print("[OK]   Identity berhasil dibuat.\n")

    app_name = "tugas_cloud"       # App name destination
    aspects = ["announce", "demo"] # Aspects destination

    print(f"[INFO] Membuat Destination...")
    print(f"       App Name : {app_name}")
    print(f"       Aspects  : {aspects}")

    destination = RNS.Destination(
        identity,
        RNS.Destination.IN,
        RNS.Destination.SINGLE,
        app_name,
        *aspects
    )

    dest_hash_hex = RNS.prettyhexrep(destination.hash)
    print(f"[OK]   Destination berhasil dibuat.")
    print(f"       Hash     : {dest_hash_hex}\n")

    print("-" * 60)
    print("  Mulai mengirim Announce setiap 10 detik...")
    print("  Tekan Ctrl+C untuk menghentikan.")
    print("-" * 60)
    print()

    counter = 0  # Penghitung jumlah announce yang dikirim

    try:
        while True:
            counter += 1

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            message = f"Hello dari Node A! Timestamp: {timestamp}"

            destination.announce(
                app_data=bytes(message, "utf-8")  # Kirim pesan sebagai app_data
            )

            print(f"[ANNOUNCE #{counter:03d}] Announce terkirim!")
            print(f"  Pesan     : {message}")
            print(f"  Waktu     : {timestamp}")
            print()

            time.sleep(10)  # Tunggu 10 detik sebelum announce berikutnya

    except KeyboardInterrupt:
        print("\n")
        print("=" * 60)
        print(f"  Program dihentikan oleh pengguna.")
        print(f"  Total announce terkirim: {counter}")
        print("=" * 60)


if __name__ == "__main__":
    main()