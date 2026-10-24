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

def konfir():
    input( "\nTekan enter untuk melanjutkan...")

def input_int(pesan, minimum=None, maksimum=None):
    while True:
        try:
            nilai = int(input(pesan).strip())
        except ValueError:
            print("Input harus berupa angka bulat!")
            continue
        if minimum is not None and nilai < minimum:
            print(f"input minimal {minimum}.")
        elif maksimum is not None and nilai > maksimum:
            print(f" input maksimal {maksimum}.")
        else:
            return nilai

def input_teks(pesan):
    while True:
        teks = input(pesan).strip()
        if teks:
            return teks
        print("Input tidak boleh kosong!")

def input_ya_tidak(pesan):
    while True:
        jawab = input(pesan).strip().lower()
        if jawab == "y":
                return True
        elif jawab == "n":
            return False
        print("Jawab dengan y atau n saja!")


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

def validasi_id_rute(id_rute):
    """Format ID rute harus seperti R001. Return (valid, pesan)."""
    if len(id_rute) != 4:
        return False, "ID harus 4 karakter (contoh: R001)."
    if not id_rute.startswith("R"):
        return False, "ID harus diawali huruf R."
    if not id_rute[1:].isdigit():
        return False, "Setelah huruf R harus 3 digit angka (contoh: R001)."
    return True, "OK"


def cari_rute(tarif, id_rute):
    """Cari rute berdasarkan ID. Return datanya (dictionary) atau None."""
    for rute in tarif:
        if rute["id"].lower() == id_rute.lower():
            return rute
    return None



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

    users[username] = {"password": password, "role": "user", "saldo": 0}
    simpan_data()
    print(f"Registrasi berhasil! Silakan login, {username}.")
    return username


def login(users):
    print("=== LOGIN ===")
    for percobaan in range(1, MAX_LOGIN + 1):
        username = input_teks("Username : ").strip()
        password = pwinput.pwinput("Password : ")
        nama = cari_username(username, users)
        if nama is not None and users[nama]["password"] == (password):
            print(f"[✓] Login berhasil. Selamat datang, {nama}!")
            return nama
        print(f"[!] Username/password salah. Sisa percobaan: {MAX_LOGIN - percobaan}")
    print("[!] Login gagal 3x. Kembali ke menu utama.")
    time.sleep(1)
    return None

def menu_admin(users, tarif, transaksi):
    while True:
        bersihkan_layar()
        print("SELAMAT DATANG DI MENU ADMIN")
        print("1. Menu pengelolaan tarif")
        print("2. Daftar user")
        print("3. Riwayat tranksaksi")
        print("4. Laporan ringkas")
        print("5. Logout")
        pilihan = input_int("pilih nomor 1-5: ", 1, 5)

        bersihkan_layar()
        if pilihan == 1:
            menu_crud_tarif(tarif)
        elif pilihan == 2:
            daftar_user(users)
        elif pilihan == 3:
            riwayat_transaksi(transaksi)
        elif pilihan == 4:
            laporan(transaksi)
        else:
            print("Log out berhasil. Kembali ke menu utama")
            return

#-------------PILIHAN 1 MENU ADMIN----------------
def menu_crud_tarif(tarif):
    while True:
        bersihkan_layar()
        print("===KELOLA TARIF TOL===")
        print("1. Tampilkan tarif")
        print("2. Tambah tarif")
        print("3. Ubah tarif")
        print("4. Hapus tarif")
        print("5. kembali ke menu admin ")
        pilihan = input_int("pilihlah menu (1-5): ", 1, 5)

        if pilihan == 1:
            tampilkan_tarif(tarif)
        elif pilihan == 2: 
            tambah_tarif(tarif)
        elif pilihan == 3:
            ubah_tarif(tarif)
        elif pilihan == 4:
            hapus_tarif(tarif)
        else:
            print("kembali ke menu admin")
            konfir()
            break

def tambah_tarif(tarif):
    print("TAMBAH TARIF TOL BARU")
    while True:
        id_baru = input_teks("Masukan ID Rute (misal: R007): ").upper()
        
        if len(id_baru) != 4:
            print("format harus empat karakter")
            continue
        if not id_baru.startswith("R"):
            print("id harus diawali dengan R")
            continue
        angka_bagian = id_baru[1:]
        if not angka_bagian.isdigit():
            print("Setelah huruf 'R' harus berupa 3 digit angka (Contoh: R001)!")
            continue
        duplicate = False 
        for item in tarif:
            if item["id"] == id_baru.upper():
                duplicate = True
                break
        if duplicate:
            print("ID SUDAH TERDAFTAR")
        else:
            break
    asal = input_teks("kota/gerbang asal: ")
    tujuan = input_teks("kota/gerbang tujuan: ")
    tarif_dasar = input_int("tarif dasar golongan I (Rp): ", 10000, 1000000)
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
    konfir()


def ubah_tarif(tarif):
    tampilkan_tarif(tarif)
    if len(tarif) == 0:
        print("belum ada data tarif yang bisa diubah")
        return
    id_cari = input_teks("masukan id rute yang ingin diubah: ")
    if len(id_cari) != 4:
        print("format harus empat karakter")
    if not id_cari.startswith("R"):
        print("id harus diawali dengan R")
    angka_bagian = id_cari[1:]
    if not angka_bagian.isdigit():
        print("Setelah huruf 'R' harus berupa 3 digit angka (Contoh: R001)!")
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


#-------------PILIHAN 2 MENU ADMIN--------------
def daftar_user(users):
    tabel = PrettyTable(["No", "Username", "Role", "Saldo"])
    nomor = 1
    for nama in users:
        tabel.add_row([nomor, nama, users[nama]["role"], format_rupiah(users[nama]["saldo"])])
        nomor += 1
    print(tabel)
    konfir()


#-------------PILIHAN 3 MENU ADMIN-------------

def riwayat_transaksi(transaksi, username=None):
    """Kalau username diisi -> riwayat milik user itu saja. Kalau tidak -> semua (admin)."""
    print("=== RIWAYAT TRANSAKSI ===")
    tabel = PrettyTable(["Kode", "Waktu", "User", "Tipe", "Nominal", "Keterangan"])
    ada_data = False
    for trx in transaksi:
        if username is None or trx["username"] == username:
            tabel.add_row([trx["kode"], trx["waktu"], trx["username"],
                        trx["tipe"], format_rupiah(trx["nominal"]), trx["keterangan"]])
            ada_data = True

    if ada_data:
        print(tabel)
    else:
        print("Belum ada transaksi.")
    konfir()



#-------------PILIHAN 4 MENU ADMIN-------------
def laporan(transaksi):
    pendapatan = 0        # total uang dari transaksi bayar tol
    jumlah_bayar = 0      # berapa kali transaksi bayar
    total_topup = 0       # total uang top up yang masuk

    for trx in transaksi:
        if trx["tipe"] == "BAYAR":
            pendapatan += trx["nominal"]
            jumlah_bayar += 1
        elif trx["tipe"] == "TOPUP":
            total_topup += trx["nominal"]

    print("=== LAPORAN RINGKAS ===")
    print(f"Total pendapatan tol   : {format_rupiah(pendapatan)}")
    print(f"Jumlah transaksi bayar : {jumlah_bayar}")
    print(f"Total top up masuk     : {format_rupiah(total_topup)}")
    konfir()

# ============================================================
#  MENU USER
# ============================================================
def menu_user(username, users, tarif, transaksi):
    while True:
        bersihkan_layar()
        print(f"=== MENU USER ({username}) ===")
        print("1. Cek saldo")
        print("2. Top up saldo")
        print("3. Bayar tol")
        print("4. Riwayat transaksi saya")
        print("5. Logout")
        pilihan = input_int("Pilih nomor (1-5): ", 1, 5)

        bersihkan_layar()
        if pilihan == 1:
            print(f"Saldo Anda: {format_rupiah(users[username]['saldo'])}")
            konfir()
        elif pilihan == 2:
            top_up(username, users, transaksi)
        elif pilihan == 3:
            bayar_tol(username, users, tarif, transaksi)
        elif pilihan == 4:
            riwayat_transaksi(transaksi, username)
        else:
            print("Logout berhasil. Kembali ke menu utama.")
            time.sleep(1)
            return


def top_up(username, users, transaksi):
    print("=== TOP UP SALDO ===")
    print(f"Saldo saat ini : {format_rupiah(users[username]['saldo'])}")
    nominal = input_int(f"Nominal top up (min {format_rupiah(MIN_TOPUP)}): ", MIN_TOPUP)

    # Saldo tidak boleh melebihi batas maksimal
    if users[username]["saldo"] + nominal > MAX_SALDO:
        print(f"[!] Gagal. Saldo maksimal adalah {format_rupiah(MAX_SALDO)}.")
        konfir()
        return

    users[username]["saldo"] += nominal
    data = catat_transaksi(transaksi, username, "TOPUP", nominal, "Top up saldo")
    print("[✓] Top up berhasil!")
    cetak_invoice(data, users[username]["saldo"])
    konfir()

def cetak_tabel_tarif(tarif):
    """Hanya mencetak tabel (tanpa konfirmasi), dipakai di banyak tempat."""
    table = PrettyTable()
    table.field_names = ["ID", "Asal", "Tujuan", "Tarif Dasar (Gol I)"]
    for rute in tarif:
        table.add_row([rute["id"], rute["asal"], rute["tujuan"], format_rupiah(rute["tarif_dasar"])])
    print(table)


def bayar_tol(username, users, tarif, transaksi):
    print("=== BAYAR TOL ===")
    if len(tarif) == 0:
        print("Belum ada data tarif tol.")
        konfir()
        return

    # 1. Pilih rute
    cetak_tabel_tarif(tarif)
    id_rute = input_teks("\nMasukkan ID rute yang dilewati: ")
    rute = cari_rute(tarif, id_rute)
    if rute is None:
        print(f"[!] ID rute '{id_rute}' tidak ditemukan.")
        konfir()
        return

    # 2. Pilih golongan kendaraan
    tabel = PrettyTable(["No", "Golongan", "Jenis Kendaraan", "Pengali Tarif"])
    nomor = 1
    for gol in GOLONGAN:
        tabel.add_row([nomor, gol[0], gol[1], gol[2]])
        nomor += 1
    print(tabel)
    pilihan = input_int(f"Pilih golongan (1-{len(GOLONGAN)}): ", 1, len(GOLONGAN))
    golongan = GOLONGAN[pilihan - 1]       # index mulai dari 0, jadi dikurangi 1

    # 3. Hitung biaya = tarif dasar x pengali golongan
    biaya = int(rute["tarif_dasar"] * golongan[2])
    saldo = users[username]["saldo"]

    print(f"\nRute      : {rute['asal']} - {rute['tujuan']}")
    print(f"Golongan  : {golongan[0]} ({golongan[1]})")
    print(f"Biaya     : {format_rupiah(biaya)}")
    print(f"Saldo Anda: {format_rupiah(saldo)}")

    # 4. Saldo tidak boleh jadi negatif
    if saldo < biaya:
        print(f"[!] Saldo tidak cukup. Kurang {format_rupiah(biaya - saldo)}. Silakan top up dulu.")
        konfir()
        return

    # 5. Konfirmasi lalu bayar
    if not input_ya_tidak("Lanjutkan pembayaran? (y/n): "):
        print("Pembayaran dibatalkan.")
        konfir()
        return

    users[username]["saldo"] -= biaya
    keterangan = f"{rute['asal']} - {rute['tujuan']} (Gol {golongan[0]})"
    data = catat_transaksi(transaksi, username, "BAYAR", biaya, keterangan)
    print("[✓] Pembayaran berhasil!")
    cetak_invoice(data, users[username]["saldo"])
    konfir()




# ============================================================
#  FUNGSI TRANSAKSI (dipakai Admin & User)
# ============================================================
def buat_kode_transaksi(transaksi):
    """Bikin kode unik: TRX0001, TRX0002, dst."""
    nomor = len(transaksi) + 1
    return "TRX" + str(nomor).zfill(4)


def catat_transaksi(transaksi, username, tipe, nominal, keterangan):
    """Simpan 1 transaksi ke list lalu ke file JSON. Return data transaksinya."""
    data = {
        "kode": buat_kode_transaksi(transaksi),
        "waktu": waktu_sekarang(),
        "username": username,
        "tipe": tipe,              # "BAYAR" atau "TOPUP"
        "nominal": nominal,
        "keterangan": keterangan,
    }
    transaksi.append(data)
    simpan_data()
    return data


def cetak_invoice(data, saldo_akhir):
    """Tampilkan struk/invoice setelah transaksi berhasil."""
    print("\n" + "=" * 38)
    print("              INVOICE")
    print("=" * 38)
    print(f"Kode       : {data['kode']}")
    print(f"Waktu      : {data['waktu']}")
    print(f"Username   : {data['username']}")
    print(f"Jenis      : {data['tipe']}")
    print(f"Keterangan : {data['keterangan']}")
    print(f"Nominal    : {format_rupiah(data['nominal'])}")
    print(f"Saldo akhir: {format_rupiah(saldo_akhir)}")
    print("=" * 38)



# MENU UTAMAA
def main():
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
                    menu_admin(users, tarif, transaksi)
                else:
                    print(f"Halo {nama_user}! Menu User akan segera dibuat.")
                time.sleep(2)
        elif menu_awal == 2:
            bersihkan_layar()
            registrasi(users)
            time.sleep(2)
        elif menu_awal == 3:
            bersihkan_layar()
            print("Terima kasih telah menggunakan program ini!")
            break

if __name__ == "__main__":
    main()
