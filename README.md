# Sistem Tarif Jalan Tol
# Anggota & Peran
- Fahri Julian Perdana: coding (menu admin dan user)
- Muhammad Thoriq Kamil: coding (data, register, login)
- Muhammad Zacky Dwi Putra: coding (top up, pembayaran, invoice) & laporan
- Khasya Fatlaikha: Flowchart
# deskripsi & tujuan
- Deskripsi: Sistem tarif jalan tol ini dibuat dengan menggunakan bahasa pemograman Python untuk mengelola rute perjalanan jalan tol, pengaturan tarif dasarm serta transaksi pembayaran secara terpusat dan dinamis. Program ini menggunakan struktur data berbasis JSON untuk penyimpanan data. Serta dilengkapi dengan sistem keamanan autentikasi akun (login dan register), manajemen saldo, serta fitur kalkulasi tarif otomatis berdasarkan golongan kendaraan.
- Tujuan:
Otomatisasi Pengelolaan Tarif: Memudahkan Administrator dalam melakukan operasi CRUD (Create, Read, Update, Delete) data rute dan tarif dasar jalan tol secara efisien.

Kalkulasi Golongan Kendaraan Dinamis: Menerapkan sistem perhitungan tarif otomatis berdasarkan faktor pengali (multiplier) untuk berbagai golongan kendaraan (Golongan I sampai V) tanpa redundansi data di dalam database.

Manajemen Transaksi Pengguna: Memfasilitasi pengguna (User) untuk melakukan pengecekan saldo, top-up saldo dengan validasi batas aman, serta melakukan pembayaran tol secara real-time yang terintegrasi langsung dengan pencatatan riwayat transaksi (history).

Transparansi & Pelaporan: Menyediakan fitur cetak struk pembayaran (invoice) otomatis dan laporan ringkas pendapatan bagi Administrator untuk memantau arus transaksi di dalam sistem.

# Flowchart
<img width="2797" height="2032" alt="Flowchart Kelompok 4 pa drawio" src="https://github.com/user-attachments/assets/68364535-0db9-4305-9bb2-9d945a46a93a" />

Flowchart ini menggambarkan alur kerja sistem tol berbasis CLI dari awal program dibuka hingga selesai:   

- Menu Utama & Autentikasi: Pengguna dapat memilih menu Registrasi akun baru, Login, atau Keluar. Sistem akan memvalidasi data dan memisahkan hak akses berdasarkan role (Admin atau User).   Menu 
- Admin: Mengelola data rute & tarif tol (CRUD), melihat daftar user, memantau seluruh riwayat transaksi, hingga melihat laporan ringkas pendapatan.   
- Menu User: Mengelola akun pribadi seperti cek saldo, top-up saldo, membayar tol dengan pilihan golongan kendaraan (otomatis mengalikan tarif dasar), serta melihat riwayat transaksi pribadi.

# Fitur setiap role serta output dan penjelasannya
- Admin:
Fitur:
<img width="183" height="95" alt="image" src="https://github.com/user-attachments/assets/8061b74d-b353-4e3d-92db-a516af248098" />

Menu ini merupakan halaman utama yang akan diakses setelah administrator berhasil melakukan login ke dalam sistem. Menu ini menyediakan berbagai fitur administratif untuk mengelola keseluruhan data dan sistem operasional jalan tol:   

1.Menu pengelolaan tarif: Berfungsi untuk mengelola data rute jalan tol secara menyeluruh melalui fitur CRUD, yang mencakup melihat daftar tarif, menambah tarif baru dengan validasi format ID dan pencegahan data duplikat, mengubah data tarif yang sudah ada, serta menghapus data rute.   
2.Daftar user: Berfungsi untuk menampilkan tabel rekapitulasi seluruh akun pengguna yang terdaftar di dalam sistem beserta informasi hak akses role dan sisa saldo masing-masing.   
3.Riwayat tranksaksi: Berfungsi untuk merekam dan menampilkan daftar seluruh rekam jejak aktivitas finansial dari semua pengguna yang mencakup transaksi pembayaran tol maupun pengisian saldo.   
4.Laporan ringkas: Berfungsi untuk menyajikan rekapitulasi data finansial secara makro yang mencakup total pendapatan dari transaksi pembayaran tol, jumlah frekuensi transaksi bayar, serta akumulasi total dana top-up yang masuk ke dalam sistem.   
5.Logout: Berfungsi untuk mengakhiri sesi login akun admin saat ini dan mengembalikan tampilan layar utama ke menu awal aplikasi.   

- Menu pengelolaan tarif
Menu ini digunakan oleh Admin untuk mengelola data rute dan tarif dasar jalan tol secara keseluruhan. Berdasarkan tangkapan layar di atas, menu ini memiliki 5 pilihan utama:

1. Tampilkan data tarif
<img width="292" height="247" alt="Cuplikan layar 2026-11-03 000924" src="https://github.com/user-attachments/assets/5cde6ed5-6a71-4753-85be-cbcbfa96e1f0" />

Berfungsi untuk menampilkan seluruh daftar rute jalan tol yang tersedia di dalam sistem. Data disajikan dalam bentuk tabel rapi (PrettyTable) yang memuat informasi ID Rute, Kota/Gerbang Asal, Kota/Gerbang Tujuan, dan Tarif Dasar (Golongan I).

2. Tambah Tarif 
<img width="382" height="411" alt="Cuplikan layar 2026-11-03 001803" src="https://github.com/user-attachments/assets/c89132c9-3b58-484f-a01f-d790a7696fe5" />

Berfungsi untuk memasukkan data rute tol baru ke dalam database JSON. Validasi Sistem: Admin diwajibkan memasukkan ID rute dengan format yang benar (diawali huruf 'R' diikuti 3 digit angka, contoh: R500), serta dilengkapi pengecekan agar ID yang sama tidak bisa didaftarkan dua kali (duplikat). Admin juga menginput kota asal, tujuan, dan nominal tarif dasar.   

3. Ubah Tarif
<img width="373" height="392" alt="Cuplikan layar 2026-11-03 001846" src="https://github.com/user-attachments/assets/98847cd0-268d-42fa-9586-19dd9e44a4b3" />

Berfungsi untuk memperbarui informasi rute atau tarif dasar yang sudah ada berdasarkan ID rute yang dicari. Sistem akan menampilkan data lama, dan admin dapat memasukkan data pembaruan (asal, tujuan, atau tarif dasar baru) yang otomatis langsung tersimpan ke dalam file JSON.

4. Hapus Tarif
<img width="372" height="368" alt="Cuplikan layar 2026-11-03 001913" src="https://github.com/user-attachments/assets/bfa88e6d-ccdf-4fd1-9eb5-c4fd0e146d29" />

Berfungsi untuk menghapus data rute tol tertentu dari sistem. Sebelum data dihapus secara permanen, sistem akan menampilkan detail rute yang ingin dihapus dan meminta konfirmasi ulang (y/n) kepada admin untuk mencegah kesalahan penghapusan data.

5. Kembali ke menu admin
Berfungsi untuk keluar dari sub-menu pengelolaan tarif dan mengarahkan kembali tampilan ke halaman utama Admin.

- Daftar user:
<img width="195" height="117" alt="image" src="https://github.com/user-attachments/assets/84f63983-3abf-490e-a6fa-3cf582ae1ae2" />

Menu user ini berfungsi untuk menampilkan seluruh data dari user

- Riwayat Tranksaksi:
<img width="532" height="226" alt="image" src="https://github.com/user-attachments/assets/afc8f3d1-1da9-4aac-bfe4-6acf6c6a34f7" />

Fitur Riwayat Transaksi berfungsi untuk merekam dan menampilkan seluruh rekam jejak aktivitas finansial yang terjadi di dalam sistem secara transparan dan terstruktur.

- Laporan Ringkas:
<img width="401" height="256" alt="image" src="https://github.com/user-attachments/assets/d3a7ea32-9cea-4814-9c2b-82e33db75732" />

Fitur Riwayat Transaksi berfungsi untuk merekam dan menampilkan seluruh rekam jejak aktivitas finansial yang terjadi di dalam sistem secara transparan dan terstruktur.

- Log Out
<img width="373" height="228" alt="image" src="https://github.com/user-attachments/assets/0a57b8d7-c1d6-4d43-842d-e8d1f2115788" />

Fitur log out berfungsi untuk keluar dan kembali ke menu utama

- User:
Fitur:
<img width="313" height="203" alt="image" src="https://github.com/user-attachments/assets/11285b15-dceb-4d97-9788-13abd0f92436" />

Menu ini merupakan halaman utama yang akan diakses setelah pengguna (User) berhasil melakukan login ke dalam sistem (pada contoh di atas, akun yang sedang aktif bernama “Dhika”). Menu ini menyediakan berbagai fitur interaktif untuk kebutuhan transaksi perjalanan tol harian:   

1. Cek Saldo:Berfungsi untuk memeriksa ketersediaan saldo digital yang dimiliki oleh akun pengguna saat ini secara real-time.   
2. Top Up Saldo:Berfungsi untuk melakukan penambahan (pengisian ulang) saldo akun. Fitur ini dilengkapi dengan validasi nominal minimum serta batasan saldo maksimal yang diizinkan oleh sistem agar transaksi tetap aman.  
3. Bayar Tol:Menu utama untuk melakukan simulasi atau pembayaran transaksi perjalanan jalan tol.   Pengguna dapat memilih rute yang diinginkan, memilih golongan kendaraan (Golongan I hingga V) yang secara otomatis menghitung tarif menggunakan faktor pengali (multiplier), melakukan pengecekan saldo, hingga pemotongan saldo dan pencetakan struk invoice otomatis.
4. Riwayat Transaksi Saya:Berfungsi untuk menampilkan rekam jejak aktivitas finansial pribadi milik pengguna yang sedang login saja (baik itu transaksi top-up maupun pembayaran tol).   
5. Logout:Berfungsi untuk keluar dari sesi akun pengguna saat ini dan mengembalikan tampilan layar ke menu utama aplikasi. 

- Cek Saldo
<img width="371" height="146" alt="image" src="https://github.com/user-attachments/assets/b18f08df-e699-4614-9c90-71e6e51c910f" />

Fitur Cek Saldo merupakan salah satu menu fungsional di sisi User yang digunakan untuk melihat jumlah saldo digital yang tersedia pada akun yang sedang aktif saat itu.

- Top Up Saldo
<img width="558" height="448" alt="image" src="https://github.com/user-attachments/assets/74185357-f977-4753-af95-58247193f523" />

Fitur Top Up Saldo digunakan oleh pengguna untuk melakukan pengisian ulang saldo digital akun mereka sebelum melakukan transaksi pembayaran tol.

- Bayar Tol
<img width="701" height="547" alt="image" src="https://github.com/user-attachments/assets/d9418afb-1b87-4a66-aaac-f8042b192731" />

<img width="457" height="386" alt="image" src="https://github.com/user-attachments/assets/8800e42e-94a5-4622-8031-c4ef710fdc6d" />

Pada menu bayar tol, sistem menampilkan daftar rute dan pilihan golongan kendaraan beserta pengali tarifnya. Setelah pengguna memilih rute R039 dari Myanmar ke Kamboja dan golongan I, sistem otomatis menghitung total biaya sebesar Rp 1.000. Jika saldo mencukupi dan pembayaran dikonfirmasi, saldo pengguna akan terpotong secara otomatis, dan sistem langsung menerbitkan struk invoice resmi yang merinci kode transaksi TRX0006, waktu, jenis pembayaran, rincian rute, nominal biaya, serta sisa saldo akhir.

- Log Out
























