import os
import json

# ============================================================
# PEMBAGIAN FUNGSI
# Anggota 1 - Muhammad Aziz Susilo Purnomo (2530801095) : tambah_barang(), lihat_stok_barang(), filter_stok_menipis()
# Anggota 2 - Diandra Enka Nugraha (2530801104) : catat_penjualan(), catat_pengeluaran(), laporan_laba_rugi()
# Anggota 3 - Fadhillah Itmamul Fiqri (2530801083) : cari_barang(), edit_barang(), hapus_barang()
# Internal   : SEMUA ANGGOTA KELOMPOK: simpan_dan_muat() — dipanggil otomatis oleh program
# ============================================================

JSON_FILE = "db_toko.json"

# KONSEP TUPLE: Data tetap/read-only yang tidak boleh diubah saat runtime
PROFIL_TOKO = ("UMKM Jaya", "Jl. Perjuangan, No. 8", "021-112233") 

# ==================== INTERNAL: FILE I/O & EXCEPTION HANDLING ====================
def simpan_dan_muat(mode="muat", data=None):
    if mode == "simpan":
        try:
            with open(JSON_FILE, "w") as f:
                json.dump(data, f, indent=2)
            return True
        except IOError as e:
            print(f"║ Gagal menyimpan file: {e}")
            return False
    
    # Mode "muat"
    try:
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, "r") as f:
                data = json.load(f)
                
                if not isinstance(data, dict): raise ValueError("Struktur file tidak sesuai")
                if not isinstance(data.get("stok"), dict): data["stok"] = {}
                if not isinstance(data.get("jual"), list): data["jual"] = []
                if not isinstance(data.get("keluar"), list): data["keluar"] = []
                
                # Paksa konversi List kembali jadi Tuple saat loading dari JSON
                data["jual"] = [tuple(item) for item in data["jual"] if isinstance(item, (list, tuple))]
                data["keluar"] = [tuple(item) for item in data["keluar"] if isinstance(item, (list, tuple))]
                
                return data
        return {"stok": {}, "jual": [], "keluar": []}
    except (json.JSONDecodeError, ValueError, OSError):
        print("║ File data rusak/tidak valid, memulai dari data kosong.")
        return {"stok": {}, "jual": [], "keluar": []}

# ==================== DESIGN UI ====================
def cetak_menu_estetik():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("╔══════════════════════════════════════════════════════╗")
    print(f"║            APLIKASI TOKO {PROFIL_TOKO[0]:<22}      ║") 
    # [PERBAIKAN #2] Semua elemen Tuple PROFIL_TOKO sekarang ditampilkan bermakna
    print(f"║        {PROFIL_TOKO[1]} | {PROFIL_TOKO[2]}            ║")
    print("╠══════════════════════════════════════════════════════╣")
    print("║  [1]  Tambah / Restok Barang                         ║")
    print("║  [2]  Lihat Stok Barang                              ║")
    print("║  [3]  Filter Stok Menipis                            ║")
    print("║  [4]  Catat Penjualan                                ║")
    print("║  [5]  Catat Pengeluaran                              ║")
    print("║  [6]  Laporan Keuangan (Laba / Rugi)                 ║")
    print("║  [7]  Cari Barang                                    ║")
    print("║  [8]  Edit Barang                                    ║")
    print("║  [9]  Hapus Barang                                   ║")
    print("╠══════════════════════════════════════════════════════╣")
    print("║  [0]  Keluar & Simpan Data                           ║")
    print("╚══════════════════════════════════════════════════════╝")

# ==================== ANGGOTA A: MANAJEMEN STOK ====================
def tambah_barang(db):
    try:
        print("\n--- TAMBAH / RESTOK BARANG ---")
        kode = input("Kode Barang : ").strip().upper()
        if not kode: raise ValueError("Kode tidak boleh kosong!")
        
        if kode in db["stok"]: 
            print(f"Barang '{db['stok'][kode]['nama']}' sudah ada. Mode Restock.")
            tambahan = input(f"Jumlah stok yang ditambahkan (Saat ini: {db['stok'][kode]['stok']}): ").strip()
            try:
                tambahan = int(tambahan)
            except ValueError:
                raise ValueError("Jumlah restock harus berupa angka!")
            if tambahan <= 0: raise ValueError("Jumlah restok harus di atas 0!")
            
            db["stok"][kode]["stok"] += tambahan
            print(f">> Sukses: Stok {kode} ditambah menjadi {db['stok'][kode]['stok']}!")
        else:
            nama = input("Nama Barang : ").strip()
            if not nama: raise ValueError("Nama tidak boleh kosong!")
            try:
                h_beli = float(input("Harga Beli  : "))
                h_jual = float(input("Harga Jual  : "))
                stok = int(input("Jumlah Stok : "))
                b_min = int(input("Batas Min   : "))
            except ValueError:
                raise ValueError("Input angka tidak valid! Pastikan memasukkan angka.")
            if h_beli < 0 or h_jual < 0 or stok < 0 or b_min < 0: 
                raise ValueError("Nilai angka tidak boleh negatif!")
            if h_jual <= h_beli:
                raise ValueError("Harga jual harus lebih besar dari harga beli!")
            
            db["stok"][kode] = {"nama": nama, "h_beli": h_beli, "h_jual": h_jual, "stok": stok, "min": b_min}
            print(">> Sukses: Barang baru terdaftar!")
    except ValueError as e: 
        print(f">> Gagal: {e}")
    return db

def lihat_stok_barang(db):
    print("\n--- DAFTAR STOK BARANG ---")
    if not db["stok"]: 
        print("Gudang kosong.")
        return []
    tabel_2d = [[k, v["nama"], v["stok"], v["h_beli"], v["h_jual"]] for k, v in db["stok"].items()]
    for baris in tabel_2d:
        print(f"• [{baris[0]}] {baris[1]:<15} | Beli: Rp{baris[3]:<7,.0f} | Jual: Rp{baris[4]:<7,.0f} | Stok: {baris[2]:<3}")
    return tabel_2d

def filter_stok_menipis(db):
    print("\n--- STOK YANG MENIPIS ---")
    kritis = [(k, v) for k, v in db["stok"].items() if v["stok"] <= v["min"]]
    if not kritis: print("Semua stok aman.")
    for k, b in kritis: print(f"⚠️ PERINGATAN: [{k}] {b['nama']:<15} sisa {b['stok']} unit")
    return db

# ==================== ANGGOTA B: KEUANGAN ====================
def catat_penjualan(db):
    try:
        print("\n--- CATAT PENJUALAN ---")
        kode = input("Kode Barang: ").strip().upper()
        if kode not in db["stok"]: raise KeyError("Kode barang tidak ada!")
        try:
            qty = int(input(f"Kuantitas (Sisa {db['stok'][kode]['stok']}): "))
        except ValueError:
            raise ValueError("Kuantitas harus berupa angka!")
        if qty <= 0: raise ValueError("Kuantitas harus di atas 0!")
        if db["stok"][kode]['stok'] < qty: raise ValueError("Stok tidak cukup!")
        
        db["stok"][kode]["stok"] -= qty
        tot_jual = qty * db["stok"][kode]["h_jual"]
        tot_beli = qty * db["stok"][kode]["h_beli"]
        
        # [PERBAIKAN #3] Riwayat jual kini menggunakan Tuple (immutable/read-only)
        db["jual"].append((kode, db["stok"][kode]["nama"], qty, tot_jual, tot_beli))
        print(f">> Sukses: Terjual! Omset Rp{tot_jual:,}")
    except (ValueError, KeyError) as e: 
        print(f">> Gagal: {e}")
    return db

def catat_pengeluaran(db):
    try:
        print("\n--- CATAT PENGELUARAN ---")
        ket = input("Deskripsi : ").strip()
        # [PERBAIKAN #6] Validasi deskripsi kosong dipindahkan SEBELUM input nominal
        if not ket: raise ValueError("Deskripsi tidak boleh kosong!")
        
        try:
            nom = float(input("Nominal   : Rp "))
        except ValueError:
            raise ValueError("Nominal harus berupa angka!")
        if nom <= 0: raise ValueError("Nominal harus lebih dari 0!")
        
        db["keluar"].append((ket, nom)) 
        print(">> Sukses: Pengeluaran dicatat!")
    except ValueError as e: 
        print(f">> Gagal: {e}")
    return db

def laporan_laba_rugi(db):
    print("\n--- LAPORAN LABA / RUGI ---")
    total_omset = sum(baris[3] for baris in db["jual"])
    total_modal = sum(baris[4] for baris in db["jual"])
    total_ops = sum(e[1] for e in db["keluar"])
    laba_bersih = total_omset - total_modal - total_ops
    
    print(f" (+) Omset Penjualan  : Rp{total_omset:,}")
    print(f" (-) Modal Terjual    : Rp{total_modal:,}")
    print(f" (-) Beban Operasional: Rp{total_ops:,}")
    print(f" =============================================")
    print(f"     NET LABA BERSIH  : Rp{laba_bersih:,}")
    return db

# ==================== ANGGOTA C: OPERASI LANJUTAN ====================
# [PERBAIKAN #1 & #7] Rekursif Head-Tail yang bermakna & digabung menjadi 1 fungsi saja
def cari_barang(db, dicari=None, tabel_2d=None):
    # --- MODE REKURSIF (dipanggil saat tabel_2d sudah ada) ---
    if tabel_2d is not None:
        if not tabel_2d: 
            return [] # Base case: list sudah habis/kosong
        # Head-Tail Recursion: Cek elemen pertama (Head), lalu rekursi sisa list (Tail)
        ditemukan = []
        if dicari in tabel_2d[0][0].lower() or dicari in tabel_2d[0][1].lower():
            ditemukan.append(tabel_2d[0])
        return ditemukan + cari_barang(db, dicari, tabel_2d[1:])
    
    # --- MODE INTERFACE (dipanggil dari menu utama) ---
    print("\n--- CARI BARANG (REKURSIF) ---")
    k_cari = input("Masukkan Kode/Nama: ").strip().lower()
    
    # [PERBAIKAN #4] Menangani bug pencarian kosong
    if not k_cari:
        print(">> Kata kunci pencarian tidak boleh kosong!")
        return db
    
    # [PERBAIKAN #5] Membuat List 2D secara diam-diam tanpa mencetak ke layar
    tabel = [[k, v["nama"], v["stok"], v["h_beli"], v["h_jual"]] for k, v in db["stok"].items()]
    hasil = cari_barang(db, k_cari, tabel) # Memanggil dirinya sendiri dengan data lengkap
    
    if hasil:
        print(f"\nDitemukan {len(hasil)} hasil:")
        for res in hasil:
            print(f"• [{res[0]}] {res[1]:<15} | Stok: {res[2]} | Jual: Rp{res[4]:,}")
    else: 
        print(">> Barang tidak ditemukan.")
    return db

def edit_barang(db):
    print("\n--- EDIT DATA BARANG ---")
    kode = input("Kode Barang yang diubah: ").strip().upper()
    if kode in db["stok"]:
        try:
            print("(Kosongkan & Enter jika tidak ingin mengubah)")
            n_baru = input(f"Nama Baru [{db['stok'][kode]['nama']}]: ").strip()
            hb_baru = input(f"Harga Beli [{db['stok'][kode]['h_beli']}]: ").strip()
            hj_baru = input(f"Harga Jual [{db['stok'][kode]['h_jual']}]: ").strip()
            
            val_h_beli = db["stok"][kode]["h_beli"]
            if hb_baru:
                try: val_h_beli = float(hb_baru)
                except ValueError: raise ValueError("Harga beli harus berupa angka!")
                if val_h_beli < 0: raise ValueError("Harga beli tidak boleh negatif!")
                
            val_h_jual = db["stok"][kode]["h_jual"]
            if hj_baru:
                try: val_h_jual = float(hj_baru)
                except ValueError: raise ValueError("Harga jual harus berupa angka!")
                if val_h_jual < 0: raise ValueError("Harga jual tidak boleh negatif!")
            
            if val_h_jual <= val_h_beli:
                raise ValueError("Harga jual harus > harga beli!")
                
            if n_baru: db["stok"][kode]["nama"] = n_baru
            db["stok"][kode]["h_beli"] = val_h_beli
            db["stok"][kode]["h_jual"] = val_h_jual
                
            print(">> Sukses: Data diperbarui!")
        except ValueError as e: 
            print(f">> Gagal: {e}")
    else: 
        print(">> Gagal: Kode tidak ditemukan.")
    return db

def hapus_barang(db):
    print("\n--- HAPUS BARANG ---")
    kode = input("Kode Barang yang dihapus: ").strip().upper()
    if kode in db["stok"]:
        del db["stok"][kode]
        print(f">> Sukses: Kode {kode} dihapus.")
    else: print(">> Gagal: Kode tidak ditemukan.")
    return db

# ==================== INTERFACE RUNNER ====================
def main():
    db = simpan_dan_muat("muat")
    while True:
        cetak_menu_estetik()
        pilih = input("Pilihan menu [0-9]: ").strip()
        
        if pilih == "1": db = tambah_barang(db)
        elif pilih == "2": lihat_stok_barang(db)
        elif pilih == "3": filter_stok_menipis(db)
        elif pilih == "4": db = catat_penjualan(db)
        elif pilih == "5": db = catat_pengeluaran(db)
        elif pilih == "6": laporan_laba_rugi(db)
        elif pilih == "7": db = cari_barang(db) # Cukup 1 fungsi pemanggil
        elif pilih == "8": db = edit_barang(db)
        elif pilih == "9": db = hapus_barang(db)
        elif pilih == "0":
            simpan_dan_muat("simpan", db)
            print("\n>> Data tersimpan. Terima kasih!\n"); break
        else:
            print("Pilihan salah!")
        
        if pilih != "0": input("\nTekan Enter...")

if __name__ == "__main__":
    main()