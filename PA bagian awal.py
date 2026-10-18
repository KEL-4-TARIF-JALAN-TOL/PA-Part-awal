import json
import os
import time
import pwinput
from prettytable import PrettyTable

FILE_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "PA_Tarif_tol.json")

DATABASE = {"users": {}, "tarif": [], "transaksi": []}

MAX_LOGIN = 3
MIN_TOPUP = 10000
MAX_SALDO = 5000000

GOLONGAN = (
    ("I", "Sedan, Jip, Pick Up, Bus Kecil", 1.0),
    ("II", "Truk 2 Gandar", 1.5),
    ("III", "Truk 3 Gandar", 1.5),
    ("IV", "Truk 4 Gandar", 2.0),
    ("V", "Truk 5 Gandar", 2.0),
)


#FUNGSI UTILITAS 
def bersihkan_layar():
    os.system("cls" if os.name == "nt" else "clear")

def format_rupiah(angka):
    return f"Rp {angka:,}".replace(",", ".")

def waktu_sekarang():
    return time.strftime("%Y-%m-%d %H:%M:%S")

def input_int(pesan, minimum=None, maksimum=None):
    while True:
        try:
            nilai = int(input(pesan).strip())
        except ValueError:
            print("Input harus berupa angka bulat!")
            continue
        if minimum is not None and nilai < minimum:
            print(f"Nilai minimal {minimum}.")
        elif maksimum is not None and nilai > maksimum:
            print(f" Nilai maksimal {maksimum}.")
        else:
            return nilai

def input_teks(pesan):
    while True:
        teks = input(pesan).strip()
        if teks:
            return teks
        print("Input tidak boleh kosong!")


# PENYIMPANAN DATA (JSON)
def data_default_users():
    return {
        "admin": {"password":"admin123", "role": "admin", "saldo": 0}
    }

def data_default_tarif():
    return [
        {"id": "R001", "asal": "Cawang", "tujuan": "Tomang", "tarif_dasar": 10000},
        {"id": "R002", "asal": "Tomang", "tujuan": "Cengkareng", "tarif_dasar": 9500},
        {"id": "R003", "asal": "Jakarta", "tujuan": "Cikampek", "tarif_dasar": 17000},
        {"id": "R004", "asal": "Cikampek", "tujuan": "Palimanan", "tarif_dasar": 50000},
        {"id": "R005", "asal": "Semarang", "tujuan": "Solo", "tarif_dasar": 38000},
        {"id": "R006", "asal": "Surabaya", "tujuan": "Gempol", "tarif_dasar": 12500},
    ]

def data_default():
    return {
        "users": data_default_users(),
        "tarif": data_default_tarif(),
        "transaksi": [],
    }

def simpan_data():
    try:
        with open(FILE_DATA, "w", encoding="utf-8") as file:
            json.dump(DATABASE, file, indent=4)
    except OSError as err:
        print(f"Gagal menyimpan {FILE_DATA}: {err}")

def muat_data():
    try:
        with open(FILE_DATA, "r", encoding="utf-8") as file:
            data = json.load(file)
        if not (isinstance(data["users"], dict) and isinstance(data["tarif"], list)
                and isinstance(data["transaksi"], list)):
            raise ValueError("Struktur data tidak sesuai")
    except FileNotFoundError:
        print("PA_Tarif_tol.json belum ada, membuat file baru...")
        data = data_default()
    except (json.JSONDecodeError, ValueError, KeyError, TypeError):
        print("PA_Tarif_tol.json rusak/tidak valid, dibuat ulang dengan data default.")
        data = data_default()

    DATABASE["users"] = data["users"]
    DATABASE["tarif"] = data["tarif"]
    DATABASE["transaksi"] = data["transaksi"]
    simpan_data()
    return DATABASE["users"], DATABASE["tarif"], DATABASE["transaksi"]


#  VALIDASI
def cari_username(username, users):
    for nama in users:
        if nama.lower() == username.lower():
            return nama
    return None


def validasi_username(username, users):
    """Return (valid: bool, pesan: str)."""
    if len(username) < 4 or len(username) > 15:
        return False, "Username harus 4-15 karakter."
    if not username.replace("_", "").isalnum():
        return False, "Username hanya boleh huruf, angka, dan underscore (_)."
    if cari_username(username, users) is not None:
        return False, "Username sudah dipakai, pilih yang lain."
    return True, "OK"

def validasi_password(password):
    """Return (valid: bool, pesan: str)."""
    if len(password) < 5:
        return False, "Password minimal 5 karakter."
    if not any(char.isalpha() for char in password) or not any(char.isdigit() for char in password):
        return False, "Password harus mengandung huruf dan angka."
    return True, "OK"


# AUTENTIKASI 
def registrasi(users):
    """Registrasi akun User baru. Return username jika berhasil, else None."""
    print("=== REGISTRASI AKUN ===")
    username = input_teks("Username (4-15 karakter) : ")
    valid, pesan = validasi_username(username, users)
    if not valid:
        print(f" {pesan}")
        return None

    password = pwinput.pwinput("Password (min 5, huruf+angka): ")
    valid, pesan = validasi_password(password)
    if not valid:
        print (f"{pesan}")
        return None

    ulang = pwinput.pwinput("Ulangi password : ")
    if ulang != password:
        print("Password tidak sama!")
        return None

    users[username] = {"password": pwinput(password), "role": "user", "saldo": 0}
    simpan_data()
    print(f"Registrasi berhasil! Silakan login, {username}.")
    return username


def login(users):
    print("=== LOGIN ===")
    for percobaan in range(1, MAX_LOGIN + 1):
        username = input("Username : ").strip()
        password = pwinput.pwinput("Password : ")
        nama = cari_username(username, users)
        if nama is not None and users[nama]["password"] == password:
            print(f"Login berhasil. Selamat datang, {nama}!")
            return nama
        else:
            print(f"Username/password salah. Sisa percobaan: {MAX_LOGIN - percobaan}")
    print("Login gagal 3x. Kembali ke menu utama.")
    time.sleep(2)
    return None

def menu_admin(username_admin, users, tarif, tranksaksi):
    while True:
        print("SELAMAT DATANG DI MENU ADMIN")
        pilihan = int(input("pilih nomor 1-5: "))

        if pilihan == 1:
            menu_crud_tarif(tarif)
        elif pilihan == "2":
            print(tampilkan_daftar_user)
        elif pilihan == "3":
            print(tampilkan_semua_tranksaksi)
        elif pilihan == "4":
            print("log out berhasil. Kembali ke menu utama")
        time.sleep(1)
        break
    

def menu_crud_tarif(tarif):
    while True:
        print("KELOLA TARIF TOL PILIHAN 1-5")
        pilihan = int(input("pilihlah angka dari 1 sampai 5: "))

        if pilihan == 1:
            tampilkan_tarif(tarif)
        elif pilihan == 2: 
            tambah_tarif(tarif)
        elif pilihan == 3:
            ubah_tarif(tarif)
        elif pilihan == 4:
            hapus_tarif(tarif)
        elif pilihan == 5:
            break



def tambah_tarif(tarif):
    print("TAMBAH TARIF TOL BARU")
    while True:
        id_baru = input_teks("Masukan ID Rute (misal: R007): ")
        duplicate = False 
        for item in tarif:
            if item["id"].lower() == id_baru.lower():
                duplicate = True
                break
        if duplicate:
            print("ID SUDAH TERDAFTAR")
        else:
            break
    asal = input("kota/gerbang asal: ")
    tujuan = input("kota/gerbang tujuan: ")
    tarif_dasar = input_int("tarif dasar golongan I (Rp): ", 1000, 1000000)

    data_baru =      {
        "id" : id_baru,
        "asal" : asal,
        "tujuan" : tujuan,
        "tarif_dasar" : tarif_dasar
        }
    tarif.append(data_baru)
    simpan_data()

    print("data tarif berhasil ditambahkan")
    time.sleep(2)

def tampilkan_tarif(tarif):
    if len(tarif) == 0:
        print("belum ada data tarif tol")
        return

    table = PrettyTable()
    table.field_names = ["id", "Asal", "Tujuan", "Tarif Dasar (Gol 1)"]

    for i in tarif:
        table.add_row([i["id"], i["asal"], i["tujuan"], format_rupiah(i["tarif_dasar"])])
    print(table)
    input("\n tekan enter untuk melanjutkan")

def ubah_tarif(tarif):
    tampilkan_tarif(tarif)
    if len(tarif) == 0:
        print("belum ada data tarif yang bisa diubah")
        return
    id_cari = input_teks("masukan id rute yang ingin diubah: ")
    found = False
    for i in tarif:
        if i["id"].lower() == id_cari.lower():

            found = True 
            print("DATA DITEMUKAN. MASUKAN DATA BARU (KOSONGKAN ATAU ISI ULANG): ")

            i["asal"] = input_teks(f"Asal [{i['asal']}]: ")
            i["tujuan"] = input_teks(f"Tujuan [{i['tujuan']}]: ")
            i["tarif_dasar"] = input_int(f"Tarif Dasar [{i['tarif_dasar']}]: ", 1000, 10000000)
            break

    if found:
        simpan_data()
        print("data tarif tol berhasil di perbarui")
    else:
        print("id ga ketemu pale")

def hapus_tarif(tarif):
    if len(tarif) == 0:
        print("Belum ada data tarif yang bisa di hapus")
        time.sleep(2)
        return
    id_hapus = input_teks("masukan id rute yang mau dihapus: ")
    found = False

    for i in tarif:
        if i["id"].lower() == id_hapus.lower():
            found = True
            print("Data ditemukan")
            print("asal: " + i["asal"])
            print("tujuan: " + i["tujuan"])

            konfirmasi = input("apakah anda yakin ingin menghapus data ini? (y/n): ")
            if konfirmasi == "y" or konfirmasi == "Y":
                tarif.remove(i)
                simpan_data()
                print("\n data tol berhasil dihapus")
            else:
                print("\n penghapusan dibatalkan")
            time.sleep(2)
            break

    if not found:
        print(f"\n ID rute '{id_hapus}' tidak ditemukan!")
        time.sleep(2)

if __name__ == "__main__":
    # Muat data dari file JSON saat program pertama kali dibuka
    users, tarif, transaksi = muat_data()
    
    while True:
        bersihkan_layar()
        print("1. Login")
        print("2. Registrasi Akun Baru")
        print("3. Keluar Program")
        
        menu_awal = input_int("Pilih menu (1-3): ", 1, 3)
        
        if menu_awal == 1:
            bersihkan_layar()
            nama_user = login(users)
            if nama_user:
                # Cek role user yang login
                if users[nama_user]["role"] == "admin":
                    menu_admin(nama_user, users, tarif, transaksi)
                else:
                    print(f"Halo {nama_user}! Menu User akan segera dibuat.")
                    time.sleep(2)
        elif menu_awal == 2:
            bersihkan_layar()
            registrasi(users)
            time.sleep(2)
        elif menu_awal == 3:
            print("Terima kasih telah menggunakan program ini!")
            break



        
    
