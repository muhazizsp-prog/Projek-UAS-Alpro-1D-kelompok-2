import os

TXT_FILE = "db_toko.txt"

# ==================== INTERNAL: FILE I/O & EXCEPTION HANDLING ====================
def simpan_dan_muat(aksi="muat", data=None):
    try:
        if aksi == "simpan":
            with open(TXT_FILE, "w") as f:
                for k, v in data["stok"].items():
                    # Format teks: S|key|nama_asli|harga_beli|harga_jual|stok|batas_minimum
                    f.write(f"S|{k}|{v['nama']}|{v['h_beli']}|{v['h_jual']}|{v['stok']}|{v['min']}\n")
                for t in data["jual"]: f.write(f"J|{t[0]}|{t[1]}|{t[2]}|{t[3]}\n")
                for e in data["keluar"]: f.write(f"K|{e[0]}|{e[1]}\n")
            return True
        
        res = {"stok": {}, "jual": [], "keluar": []}
        if os.path.exists(TXT_FILE):
            with open(TXT_FILE, "r") as f:
                for b in f:
                    c = b.strip().split("|")
                    if c[0] == "S": 
                        res["stok"][c[1]] = {
                            "nama": c[2], "h_beli": float(c[3]), "h_jual": float(c[4]), 
                            "stok": int(c[5]), "min": int(c[6])
                        }
                    elif c[0] == "J": 
                        # Format transaksi penjualan: (Nama, Qty, Total Harga Jual, Total Harga Beli)
                        res["jual"].append((c[1], int(c[2]), float(c[3]), float(c[4])))
                    elif c[0] == "K": 
                        res["keluar"].append((c[1], float(c[2])))
        return res
    except Exception as e:
        print(f"║ Gagal operasi file: {e}")
        return {"stok": {}, "jual": [], "keluar": []}

db = simpan_dan_muat("muat")

# ==================== DESIGN UI: KOTAK MENU TERMINAL ====================
def cetak_menu_estetik():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("╔══════════════════════════════════════════════════════╗")
    print("║            APLIKASI PENGELOLA KEUANGAN TOKO          ║")
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
def tambah_barang():
    try:
        print("\n--- TAMBAH / RESTOK BARANG ---")
        nama = input("Nama Barang  : ").strip()
        h_beli = float(input("Harga Beli (Modal) : "))
        h_jual = float(input("Harga Jual         : "))
        stok = int(input("Jumlah Stok        : "))
        b_min = int(input("Batas Minimum      : "))
        
        if h_beli < 0 or h_jual < 0 or stok < 0 or b_min < 0: raise ValueError
        k = nama.lower()
        if k in db["stok"]: 
            db["stok"][k]["stok"] += stok
            # Mengupdate harga terbaru jika ada perubahan saat restok
            db["stok"][k]["h_beli"] = h_beli
            db["stok"][k]["h_jual"] = h_jual
        else: 
            db["stok"][k] = {"nama": nama, "h_beli": h_beli, "h_jual": h_jual, "stok": stok, "min": b_min}
        print(">> Sukses: Barang berhasil disimpan!")
    except ValueError: print(">> Gagal: Input tidak valid atau bernilai negatif!")
    input("\nTekan Enter untuk kembali...")

def lihat_stok_barang():
    print("\n--- DAFTAR STOK BARANG ---")
    if not db["stok"]: print("Gudang kosong.")
    for b in sorted([v for v in db["stok"].values()], key=lambda x: x["nama"]):
        print(f"• {b['nama']:<15} | Beli: Rp{b['h_beli']:<7,} | Jual: Rp{b['h_jual']:<7,} | Stok: {b['stok']:<3} | Min: {b['min']}")
    input("\nTekan Enter untuk kembali...")

def filter_stok_menapis():
    print("\n--- STOK YANG MENIPIS ---")
    kritis = [v for v in db["stok"].values() if v["stok"] <= v["min"]]
    if not kritis: print("Semua stok dalam kondisi aman.")
    for b in kritis: print(f"⚠️ PERINGATAN: {b['nama']:<15} sisa {b['stok']} unit (Batas min: {b['min']})")
    input("\nTekan Enter untuk kembali...")

# ==================== ANGGOTA B: KEUANGAN ====================
def catat_penjualan():
    try:
        print("\n--- CATAT PENJUALAN ---")
        k = input("Nama barang yang terjual: ").strip().lower()
        if k not in db["stok"]: return print(">> Gagal: Barang tidak ditemukan di stok!")
        qty = int(input(f"Kuantitas penjualan (Sisa {db['stok'][k]['stok']}): "))
        if qty <= 0 or db["stok"][k]["stok"] < qty: raise ValueError
        
        db["stok"][k]["stok"] -= qty
        tot_jual = qty * db["stok"][k]["h_jual"]
        tot_beli = qty * db["stok"][k]["h_beli"] # Diperlukan untuk menghitung laba bersih asli
        
        # Simpan record tuple: (Nama, Qty, Total Jual, Total Modal/Beli)
        db["jual"].append((db["stok"][k]["nama"], qty, tot_jual, tot_beli))
        print(f">> Sukses: Terjual dengan total omset Rp{tot_jual:,}")
    except ValueError: print(">> Gagal: Kuantitas tidak sah!")
    input("\nTekan Enter untuk kembali...")

def catat_pengeluaran():
    try:
        print("\n--- CATAT PENGELUARAN ---")
        ket = input("Deskripsi keperluan: ").strip()
        nom = float(input("Nominal Biaya (Rp): "))
        if nom <= 0: raise ValueError
        db["keluar"].append((ket, nom))
        print(">> Sukses: Pengeluaran operasional berhasil dicatat!")
    except ValueError: print(">> Gagal: Nominal tidak sah!")
    input("\nTekan Enter untuk kembali...")

def laporan_laba_rugi():
    print("\n--- LAPORAN LABA / RUGI ---")
    total_omset = sum([t[2] for t in db["jual"]])
    total_modal_terjual = sum([t[3] for t in db["jual"]])
    total_ops = sum([e[1] for e in db["keluar"]])
    
    # Laba kotor = Omset Penjualan - Modal Barang yang Terjual
    laba_kotor = total_omset - total_modal_terjual
    # Laba bersih = Laba kotor - Biaya operasional lain
    laba_bersih = laba_kotor - total_ops
    
    print(f" (+) Total Omset Penjualan  : Rp{total_omset:,}")
    print(f" (-) Total Modal Barang     : Rp{total_modal_terjual:,}")
    print(f" ---------------------------------------------")
    print(f" (=) Laba Kotor Toko        : Rp{laba_kotor:,}")
    print(f" (-) Beban Operasional Lain : Rp{total_ops:,}")
    print(f" =============================================")
    print(f"     NET LABA BERSIH        : Rp{laba_bersih:,}")
    input("\nTekan Enter untuk kembali...")

# ==================== ANGGOTA C: OPERASI LANJUTAN ====================
def cari_barang_rekursif(keys, dicari, idx=0):
    if idx >= len(keys): return None
    if dicari in keys[idx]: return keys[idx]
    return cari_barang_rekursif(keys, dicari, idx + 1)

def pemicu_cari():
    print("\n--- CARI BARANG (REKURSIF) ---")
    k_cari = input("Masukkan kata kunci nama: ").strip().lower()
    res = cari_barang_rekursif(list(db["stok"].keys()), k_cari)
    if res:
        b = db["stok"][res]
        print(f"\n[Data Ditemukan]\n• Nama: {b['nama']}\n• Modal Beli: Rp{b['h_beli']:,}\n• Harga Jual: Rp{b['h_jual']:,}\n• Stok: {b['stok']}\n• Batas Min: {b['min']}")
    else: print(">> Hasil: Barang tidak ditemukan.")
    input("\nTekan Enter untuk kembali...")

def edit_barang():
    print("\n--- EDIT DATA BARANG ---")
    k_lama = input("Nama barang yang ingin diubah: ").strip().lower()
    if k_lama in db["stok"]:
        try:
            n_baru = input("Nama Baru: ").strip()
            hb_baru = float(input("Harga Beli Baru: "))
            hj_baru = float(input("Harga Jual Baru: "))
            m_baru = int(input("Batas Min Baru : "))
            stk = db["stok"][k_lama]["stok"]
            
            if k_lama != n_baru.lower(): del db["stok"][k_lama]
            db["stok"][n_baru.lower()] = {"nama": n_baru, "h_beli": hb_baru, "h_jual": hj_baru, "stok": stk, "min": m_baru}
            print(">> Sukses: Data barang berhasil diperbarui!")
        except ValueError: print(">> Gagal: Format data angka salah!")
    else: print(">> Gagal: Barang tidak ditemukan.")
    input("\nTekan Enter untuk kembali...")

def hapus_barang():
    print("\n--- HAPUS BARANG PERMANEN ---")
    k = input("Nama barang yang akan dibuang: ").strip().lower()
    if k in db["stok"]:
        del db["stok"][k]
        print(">> Sukses: Produk telah dihapus dari database.")
    else: print(">> Gagal: Produk tidak ditemukan.")
    input("\nTekan Enter untuk kembali...")

# ==================== INTERFACE RUNNER ====================
def main():
    menu = {
        "1": tambah_barang, "2": lihat_stok_barang, "3": filter_stok_menapis,
        "4": catat_penjualan, "5": catat_pengeluaran, "6": laporan_laba_rugi,
        "7": pemicu_cari, "8": edit_barang, "9": hapus_barang
    }
    while True:
        cetak_menu_estetik()
        pilih = input("Pilihan menu [0-9]: ").strip()
        if pilih in menu: 
            menu[pilih]()
            simpan_dan_muat("simpan", db)
        elif pilih == "0":
            simpan_dan_muat("simpan", db)
            print("\n>> Data berhasil disimpan ke db_toko.txt. Selesai!"); break
        else:
            print("Pilihan salah! Silakan ulangi.")
            input("\nTekan Enter untuk melanjutkan...")

if __name__ == "__main__":
    main()