# Proyek Akhir Algoritma dan Pemrograman II

### Data Kelompok
* **Nomor Kelompok:(4)**
1. Muhammad Aziz Susilo Purnomo - 2530801095
2. Diandra Enka Nugraha - 2530801104
3. Fadhila Itmamul Fiqri - 2530801083

### Tema & Deskripsi Program
Program ini bertema Sistem Manajemen Inventaris dan Keuangan (UMKM) yang dirancang untuk membantu pemilik toko kecil dalam mengelola operasional harian secara digital.Aplikasi ini berfungsi untuk mencatat stok barang secara otomatis, mendeteksi barang yang hampir habis, serta menghitung laporan laba rugi secara real-time berdasarkan data penjualan dan pengeluaran operasional yang di masukan.

### Cara Menjalankan Program
1. Pastikan sudah menginstal Python (Versi 3.10).
2. Jalankan program dengan perintah: python aplikasi_umkm_toko.py

### Tabel Pembagian Fungsi
| Nama Fungsi | Deskripsi Singkat | Penanggung Jawab |
| :--- | :--- | :--- |
| tambah_barang() | Menambahkan barang baru ke sistem atau menambah jumlah stok (restok) yang sudah ada | Aziz |
| lihat_stok_barang() | Menampilkan seluruh daftar barang di gudang dalam bentuk tabel (List 2D) | Aziz |
| filter_stok_menipis() | Memberikan peringatan otomatis jika jumlah stok barang berada di bawah batas minimum | Aziz |
| catat_penjualan() | Mencatat transaksi keluar, mengurangi stok, dan menghitung omset serta modal terjual | Andra |
| catat_pengeluaran() | Mencatat biaya operasional toko lainnya ke dalam histori transaksi | Andra |
| laporan_laba_rugi() | Menghitung laba bersih dari selisih omset, modal, dan beban operasional | Andra |
| cari_barang() | Mencari data barang spesifik menggunakan algoritma rekursi berdasarkan kode atau nama | Fadil |
| edit_barang() | Mengubah informasi nama atau harga barang yang sudah terdaftar di sistem | Fadil |
| hapus_barang() | Menghapus data barang tertentu secara permanen dari database toko | Fadil |
| simpan_dan_muat() | Menangani penyimpanan data ke file JSON agar data tidak hilang saat program ditutup | Bersama |
