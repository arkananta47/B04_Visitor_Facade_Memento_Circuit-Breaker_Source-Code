import time

class CircuitBreakerOpenException(Exception):
    pass

class CircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_time=5):
        self.failure_threshold = failure_threshold  # Batas maksimal gagal
        self.recovery_time = recovery_time          # Waktu tunggu (detik)
        self.failure_count = 0
        self.state = "CLOSED"
        self.last_failure_time = None

    def execute(self, func, *args, **kwargs):
        current_time = time.time()

        # Cek apakah sirkuit bisa dipindahkan dari OPEN ke HALF-OPEN
        if self.state == "OPEN":
            if current_time - self.last_failure_time > self.recovery_time:
                self.state = "HALF-OPEN"
                print("[Sirkuit] Status berubah menjadi: HALF-OPEN (Uji Coba)")
            else:
                print("[Sirkuit] Status: OPEN. Request diblokir otomatis (Fail-Fast)!")
                raise CircuitBreakerOpenException("Sirkuit sedang terbuka. Layanan tidak tersedia.")

        try:
            # Eksekusi fungsi subsistem/API eksternal
            result = func(*args, **kwargs)
            
            # Jika sukses di status HALF-OPEN, reset kembali ke CLOSED
            if self.state == "HALF-OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
                print("[Sirkuit] Sukses! Status kembali ke: CLOSED (Normal)")
            return result

        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = current_time
            print(f"[Sirkuit] Terjadi kegagalan ({self.failure_count}/{self.failure_threshold}): {e}")

            # Jika kegagalan menembus batas, buka sirkuit (OPEN)
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                print("[Sirkuit] Peringatan! Batas tercapai. Status berubah menjadi: OPEN")
            
            raise e


# SIMULASI PENGUJIAN STATUS (CLOSED -> OPEN -> HALF-OPEN)
if __name__ == "__main__":
    cb = CircuitBreaker(failure_threshold=2, recovery_time=3)
    
    # Simulasi API / Database rusak
    def api_eksternal_rusak():
        raise RuntimeError("Koneksi Database Server Timeout (504)!")

    # Simulasi API / Database sembuh
    def api_eksternal_normal():
        return "Data Berhasil Diambil!"

    print("FASE SIRKUIT: CLOSED (NORMAL)")
    # Percobaan 1: gagal pertama kali
    try:
        cb.execute(api_eksternal_rusak)
    except Exception:
        pass

    # Percobaan 2: gagal kedua kali maka akan memicu sirkuit menjadi OPEN
    try:
        cb.execute(api_eksternal_rusak)
    except Exception:
        pass


    print("\nFASE SIRKUIT: OPEN (FAIL-FAST)")
    # Percobaan 3: request langsung diblokir otomatis tanpa mengeksekusi fungsi
    try:
        cb.execute(api_eksternal_rusak)
    except Exception as e:
        print(f"Aplikasi Menangkap Error: {e}")


    print("\nMENUNGGU RECOVERY TIME (3 DETIK)...")
    time.sleep(4)


    print("\nFASE SIRKUIT: HALF-OPEN (UJI COBA)")
    # Percobaan 4: ditest menembakkan fungsi yang sudah normal lagi
    try:
        hasil = cb.execute(api_eksternal_normal)
        print(f"Hasil dari Server: {hasil}")
    except Exception as e:
        print(f"Aplikasi Menangkap Error: {e}")