# XML-RPC Client — memanggil fungsi get_prime_numbers secara remote dari server XML-RPC.
import xmlrpc.client
import sys
import os

# URL server. Host diambil dari: argumen CLI > env RPC_HOST > default localhost (127.0.0.1 = 1 laptop, IP lain = 2 laptop/docker).
HOST = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("RPC_HOST", "localhost")
SERVER_URL = f"http://{HOST}:8000/RPC2"


# Menampilkan header program di terminal.
def tampilkan_header():
    print()
    print("╔═══════════════════════════════════════════════════╗")
    print("║        XML-RPC CLIENT — BILANGAN PRIMA           ║")
    print("║        Tugas 04 Cloud Computing                  ║")
    print("╠═══════════════════════════════════════════════════╣")
    print(f"║  Server  : {SERVER_URL:<39} ║")
    print("╚═══════════════════════════════════════════════════╝")
    print()


# Menampilkan hasil bilangan prima dari server dalam format rapi.
def tampilkan_hasil(n, daftar_prima):
    print()
    print("╔═══════════════════════════════════════════════════╗")
    print("║                 HASIL DARI SERVER                ║")
    print("╠═══════════════════════════════════════════════════╣")
    print(f"║  Batas angka       : {n:<30}║")
    print(f"║  Jumlah prima      : {len(daftar_prima):<30}║")
    print("╠═══════════════════════════════════════════════════╣")

    if daftar_prima:
        print("║  Daftar bilangan prima:                          ║")
        print("║                                                   ║")

        baris = ""
        for i, prima in enumerate(daftar_prima):
            baris += f"{prima:>5}"
            if (i + 1) % 8 == 0 or i == len(daftar_prima) - 1:
                print(f"║  {baris:<49} ║")
                baris = ""
    else:
        print("║  Tidak ada bilangan prima dalam rentang ini.      ║")

    print("╚═══════════════════════════════════════════════════╝")
    print()


# Main — program utama client: koneksi ke server lalu minta input angka berulang kali.
def main():
    tampilkan_header()

    try:
        proxy = xmlrpc.client.ServerProxy(SERVER_URL)
        print("  [INFO] Menghubungi server...")
        print()
    except Exception as e:
        print(f"  [ERROR] Gagal membuat koneksi: {e}")
        sys.exit(1)

    while True:
        try:
            print("-" * 53)
            user_input = input("  Masukkan batas angka (atau 'q' untuk keluar): ")

            if user_input.lower() in ("q", "quit", "exit", "keluar"):
                print()
                print("  [INFO] Terima kasih! Program client ditutup.")
                print()
                break

            n = int(user_input)

            if n < 0:
                print("  [PERINGATAN] Masukkan bilangan bulat positif!\n")
                continue

            print(f"  [INFO] Memanggil server: get_prime_numbers({n})")
            hasil = proxy.get_prime_numbers(n)

            tampilkan_hasil(n, hasil)

        except ValueError:
            print("  [ERROR] Input tidak valid! Masukkan bilangan bulat.\n")

        except ConnectionRefusedError:
            print()
            print("  [ERROR] Tidak dapat terhubung ke server!")
            print("  [ERROR] Pastikan server.py sudah dijalankan terlebih dahulu.")
            print()
            break

        except xmlrpc.client.Fault as fault:
            print(f"  [ERROR] Server fault: {fault.faultString}\n")

        except Exception as e:
            print(f"  [ERROR] Terjadi kesalahan: {e}\n")
            break


if __name__ == "__main__":
    main()