# XML-RPC Server — bilangan prima. Server menyediakan fungsi RPC get_prime_numbers(n) untuk menghitung bilangan prima hingga n.
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import datetime

# Konfigurasi server. Bind ke 0.0.0.0 agar dapat diakses dari device lain (untuk lokal saja, ganti ke "localhost").
HOST = "0.0.0.0"
PORT = 8000


# Fungsi mencari bilangan prima dari 2 hingga n (Sieve of Eratosthenes).
def get_prime_numbers(n):
    """Mengembalikan daftar bilangan prima dari 2 hingga n (inklusif)."""
    waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("=" * 55)
    print(f"  [LOG] Fungsi dipanggil oleh client")
    print(f"  [LOG] Waktu       : {waktu}")
    print(f"  [LOG] Parameter n : {n}")
    print("=" * 55)

    if n < 2:
        print(f"  [LOG] Hasil       : [] (tidak ada prima < 2)")
        print()
        return []

    sieve = [True] * (n + 1)
    sieve[0] = False  # 0 bukan bilangan prima
    sieve[1] = False  # 1 bukan bilangan prima

    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False

    daftar_prima = [i for i in range(2, n + 1) if sieve[i]]

    print(f"  [LOG] Jumlah prima: {len(daftar_prima)} bilangan")
    print(f"  [LOG] Hasil       : {daftar_prima}")
    print()

    return daftar_prima


# Batasi path request hanya ke /RPC2 (keamanan dasar).
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)


# Main — menjalankan server XML-RPC.
def main():
    server = SimpleXMLRPCServer(
        (HOST, PORT),
        requestHandler=RequestHandler,
        logRequests=True  # Aktifkan log request HTTP
    )

    server.register_function(get_prime_numbers, "get_prime_numbers")

    print()
    print("╔═══════════════════════════════════════════════════╗")
    print("║        XML-RPC SERVER — BILANGAN PRIMA           ║")
    print("║        Tugas 04 Cloud Computing                  ║")
    print("╠═══════════════════════════════════════════════════╣")
    print(f"║  Host    : {HOST:<39} ║")
    print(f"║  Port    : {PORT:<39} ║")
    print(f"║  URL     : http://{HOST}:{PORT}/RPC2{' ' * 17}║")
    print("╠═══════════════════════════════════════════════════╣")
    print("║  Status  : Server AKTIF dan menunggu request...  ║")
    print("║  Tekan Ctrl+C untuk menghentikan server          ║")
    print("╚═══════════════════════════════════════════════════╝")
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
        print("=" * 55)
        print("  [INFO] Server dihentikan oleh pengguna (Ctrl+C)")
        print("=" * 55)
        server.shutdown()


if __name__ == "__main__":
    main()