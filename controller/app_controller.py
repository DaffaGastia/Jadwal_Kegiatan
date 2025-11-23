from models.kegiatan import Kegiatan
from models.btree import BTree
from models.validator import Validator
from models.serializer import Serializer
import json
from views.header_view import clear_screen, tampilkan_header, pause
from views.menu_view import tampilkan_menu
from views.kegiatan_view import tampilkan_kegiatan, format_nama_hari
from views.output_view import show_error, show_success

from datetime import datetime

DATA_FILE = "data/jadwal.json"


class AppController:
    def __init__(self):
        self.btree = BTree(t=2)

        # Load data JSON ke B-Tree
        try:
            Serializer.load_from_json(DATA_FILE, self.btree)
        except:
            Serializer.save_to_json(DATA_FILE, self.btree)

    # ===========================================================
    #  FUNGSI UTAMA APLIKASI
    # ===========================================================

    def run(self):
        while True:
            clear_screen()
            tampilkan_header()
            tampilkan_menu()

            pilihan = input("\nPilih menu (1-6): ").strip()

            if pilihan == "1":
                self.menu_tambah()
            elif pilihan == "2":
                self.menu_cari()
            elif pilihan == "3":
                self.menu_update()
            elif pilihan == "4":
                self.menu_hapus()
            elif pilihan == "5":
                self.menu_tampilkan_semua()
            elif pilihan == "6":
                Serializer.save_to_json(DATA_FILE, self.btree)
                print("\nData berhasil disimpan. Keluar aplikasi...")
                break
            else:
                show_error("Pilihan tidak valid.")
                pause()

    # ===========================================================
    #  MENU TAMBAH KEGIATAN
    # ===========================================================

    def menu_tambah(self):
        clear_screen()
        tampilkan_header()

        print("\nTAMBAH KEGIATAN BARU")
        print("-" * 50)

        try:
            id_kegiatan = int(input("ID Kegiatan         : "))
            tanggal = input("Tanggal (YYYY-MM-DD): ")
            waktu_mulai = input("Waktu Mulai (HH:MM) : ")
            waktu_selesai = input("Waktu Selesai (HH:MM): ")
            nama = input("Nama Kegiatan       : ")
            tempat = input("Tempat              : ")
            deskripsi = input("Deskripsi           : ")

            # Validasi input
            valid, pesan = Validator.validate_kegiatan(tanggal, waktu_mulai, nama, tempat)
            if not valid:
                show_error(pesan)
                pause()
                return

            # Validasi waktu mulai < selesai
            try:
                w1 = datetime.strptime(waktu_mulai, "%H:%M")
                w2 = datetime.strptime(waktu_selesai, "%H:%M")
                if w2 <= w1:
                    show_error("Waktu selesai harus lebih besar dari waktu mulai.")
                    pause()
                    return
            except:
                show_error("Format waktu tidak valid.")
                pause()
                return

            waktu_final = f"{waktu_mulai}-{waktu_selesai}"
            kegiatan = Kegiatan(id_kegiatan, tanggal, waktu_final, nama, tempat, deskripsi)

            key = kegiatan.get_key()

            # Jika sudah ada kegiatan di waktu itu
            existing = self.btree.search(self.btree.root, key)
            if existing:
                show_error("Sudah ada kegiatan pada tanggal & waktu tersebut.")
                tampilkan_kegiatan(existing)
                if input("Timpa kegiatan? (y/n): ").lower() != "y":
                    return

            # Masukkan ke B-Tree
            self.btree.insert(key, kegiatan)
            Serializer.save_to_json(DATA_FILE, self.btree)

            show_success("Kegiatan berhasil ditambahkan.")
            tampilkan_kegiatan(kegiatan)

        except:
            show_error("Input tidak valid.")

        pause()

    # ===========================================================
    #  CARI KEGIATAN
    # ===========================================================

    def cari_by_tanggal(self, tanggal):
        """Mengambil semua kegiatan pada satu tanggal"""
        semua = self.btree.traverse()

        hasil = [k for key, k in semua if k.tanggal == tanggal]

        # Sort berdasarkan waktu mulai
        def ambil_waktu(k):
            return k.waktu.split('-')[0]

        hasil.sort(key=ambil_waktu)
        return hasil

    def cari_kegiatan_range(self, tanggal, waktu_dicari):
        """
        Mengambil semua kegiatan pada tanggal tertentu
        yang rentang waktunya mencakup waktu_dicari.
        Contoh:
        kegiatan: 10:00-12:00
        waktu_dicari: 10:30  -> masuk
        """
        semua = self.btree.traverse()
        hasil = []

        for key, k in semua:
            if k.tanggal != tanggal:
                continue

            try:
                waktu_mulai, waktu_selesai = k.waktu.split('-')
            except ValueError:
                # Kalau format tidak pakai '-', lewati saja
                continue

            if waktu_mulai <= waktu_dicari <= waktu_selesai:
                hasil.append(k)

        # Urutkan juga berdasarkan waktu mulai
        hasil.sort(key=lambda keg: keg.waktu.split('-')[0])
        return hasil

    def menu_cari(self):
        while True:
            clear_screen()
            tampilkan_header()

            print("\nCARI KEGIATAN")
            print("-" * 50)
            print("1. Cari berdasarkan tanggal saja")
            print("2. Cari berdasarkan tanggal & waktu (di dalam rentang)")
            print("3. Kembali")

            mode = input("\nPilih mode (1-3): ").strip()

            if mode == "3":
                return

            if mode == "1":
                tanggal = input("Tanggal (YYYY-MM-DD): ")
                hasil = self.cari_by_tanggal(tanggal)

                clear_screen()
                tampilkan_header()

                if hasil:
                    print(f"\nKegiatan pada {tanggal} ({format_nama_hari(tanggal)}):")
                    for i, k in enumerate(hasil, 1):
                        tampilkan_kegiatan(k, i)
                else:
                    show_error("Tidak ada kegiatan pada tanggal tersebut.")

                pause()

            elif mode == "2":
                tanggal = input("Tanggal (YYYY-MM-DD): ")
                waktu = input("Waktu (HH:MM): ")

                hasil = self.cari_kegiatan_range(tanggal, waktu)

                clear_screen()
                tampilkan_header()

                if hasil:
                    print(f"\nKegiatan yang mencakup waktu {waktu}:")
                    for i, k in enumerate(hasil, 1):
                        tampilkan_kegiatan(k, i)
                else:
                    show_error("Tidak ada kegiatan dalam rentang waktu tersebut.")

                pause()

            else:
                show_error("Input tidak valid.")
                pause()

    # ===========================================================
    #  UPDATE KEGIATAN
    # ===========================================================

    def menu_update(self):
        clear_screen()
        tampilkan_header()

        print("\nUPDATE KEGIATAN")
        print("-" * 50)

        tanggal = input("Tanggal kegiatan lama: ")
        waktu = input("Waktu mulai lama     : ")

        key_lama = f"{tanggal} {waktu}"
        kegiatan_lama = self.btree.search(self.btree.root, key_lama)

        if not kegiatan_lama:
            show_error("Kegiatan tidak ditemukan.")
            pause()
            return

        print("\nData Lama:")
        tampilkan_kegiatan(kegiatan_lama)

        if input("\nLanjut update? (y/n): ").lower() != "y":
            return

        # Input baru
        id_kegiatan = int(input("\nID baru              : "))
        tanggal_baru = input("Tanggal (YYYY-MM-DD) : ")
        w1 = input("Waktu Mulai (HH:MM)  : ")
        w2 = input("Waktu Selesai (HH:MM): ")
        nama = input("Nama Kegiatan        : ")
        tempat = input("Tempat               : ")
        deskripsi = input("Deskripsi            : ")

        waktu_final = f"{w1}-{w2}"
        kegiatan_baru = Kegiatan(id_kegiatan, tanggal_baru, waktu_final, nama, tempat, deskripsi)
        key_baru = kegiatan_baru.get_key()

        self.btree.insert(key_baru, kegiatan_baru)
        Serializer.save_to_json(DATA_FILE, self.btree)

        show_success("Kegiatan berhasil di-update.")
        tampilkan_kegiatan(kegiatan_baru)

        print("\nCatatan:")
        print("- Fitur delete() belum tersedia, data lama masih ada di JSON.")
        print("- Jika ingin menghapus, lakukan manual.")

        pause()

    # ===========================================================
    #  HAPUS KEGIATAN (Masih manual)
    # ===========================================================

    def menu_hapus(self):
        while True:
            clear_screen()
            tampilkan_header()

            print("\nHAPUS KEGIATAN")
            print("-" * 50)
            print("1. Hapus berdasarkan tanggal & waktu")
            print("2. Hapus berdasarkan ID kegiatan")
            print("3. Hapus semua kegiatan pada tanggal tertentu")
            print("4. Hapus berdasarkan rentang waktu")
            print("5. Kembali")

            pilih = input("\nPilih menu (1-5): ").strip()

            if pilih == "5":
                return

            # ======= Load JSON terlebih dahulu =======
            with open(DATA_FILE, "r") as f:
                data_list = json.load(f)

            # ======================================================
            # 1) HAPUS BERDASARKAN TANGGAL & WAKTU
            # ======================================================
            if pilih == "1":
                tanggal = input("Tanggal (YYYY-MM-DD): ")
                waktu  = input("Waktu mulai (HH:MM): ")
                key_target = f"{tanggal} {waktu}"

                found = False
                new_list = []

                for item in data_list:
                    wmulai = item["waktu"].split("-")[0]
                    if f"{item['tanggal']} {wmulai}" == key_target:
                        tampilkan_kegiatan(Kegiatan.from_dict(item))
                        found = True
                    else:
                        new_list.append(item)

                if not found:
                    show_error("Kegiatan tidak ditemukan.")
                    pause()
                    continue

                if input("Hapus? (y/n): ").lower() == "y":
                    with open(DATA_FILE, "w") as f:
                        json.dump(new_list, f, indent=4)
                    self.rebuild_btree()
                    show_success("Kegiatan berhasil dihapus.")

                pause()

            # ======================================================
            # 2) HAPUS BERDASARKAN ID
            # ======================================================
            elif pilih == "2":
                id_hapus = input("Masukkan ID kegiatan: ")

                new_list = []
                target = None

                for item in data_list:
                    if str(item["id"]) == id_hapus:
                        target = item
                    else:
                        new_list.append(item)

                if not target:
                    show_error("ID tidak ditemukan.")
                    pause()
                    continue

                tampilkan_kegiatan(Kegiatan.from_dict(target))

                if input("Hapus? (y/n): ").lower() == "y":
                    with open(DATA_FILE, "w") as f:
                        json.dump(new_list, f, indent=4)
                    self.rebuild_btree()
                    show_success("Kegiatan berhasil dihapus.")

                pause()

            # ======================================================
            # 3) HAPUS SEMUA PADA TANGGAL
            # ======================================================
            elif pilih == "3":
                tanggal = input("Tanggal (YYYY-MM-DD): ")

                new_list = [item for item in data_list if item["tanggal"] != tanggal]

                if len(new_list) == len(data_list):
                    show_error("Tidak ada kegiatan pada tanggal tersebut.")
                    pause()
                    continue

                print("\nDitemukan kegiatan. Hapus semua?")
                if input("(y/n): ").lower() == "y":
                    with open(DATA_FILE, "w") as f:
                        json.dump(new_list, f, indent=4)
                    self.rebuild_btree()
                    show_success("Semua kegiatan berhasil dihapus.")

                pause()

            # ======================================================
            # 4) HAPUS BERDASARKAN RENTANG WAKTU
            # ======================================================
            elif pilih == "4":
                tanggal = input("Tanggal (YYYY-MM-DD): ")
                wmulai  = input("Dari waktu (HH:MM): ")
                wselesai = input("Sampai waktu (HH:MM): ")

                def to_int(t):
                    return int(t.replace(":", ""))

                s1 = to_int(wmulai)
                s2 = to_int(wselesai)

                new_list = []
                deleted = []

                for item in data_list:
                    if item["tanggal"] != tanggal:
                        new_list.append(item)
                        continue

                    w1, w2 = item["waktu"].split("-")
                    w1 = to_int(w1)
                    w2 = to_int(w2)

                    # overlap
                    if not (w2 <= s1 or w1 >= s2):
                        deleted.append(item)
                    else:
                        new_list.append(item)

                if not deleted:
                    show_error("Tidak ada kegiatan overlap.")
                    pause()
                    continue

                print(f"\nDitemukan {len(deleted)} kegiatan untuk dihapus.")
                if input("Hapus semua? (y/n): ").lower() == "y":
                    with open(DATA_FILE, "w") as f:
                        json.dump(new_list, f, indent=4)
                    self.rebuild_btree()
                    show_success("Berhasil dihapus.")

                pause()

            else:
                show_error("Menu tidak valid.")
                pause()



    # ===========================================================
    #  TAMPILKAN SEMUA JADWAL
    # ===========================================================

    def menu_tampilkan_semua(self):
        clear_screen()
        tampilkan_header()

        print("\nSEMUA JADWAL TERURUT")
        print("-" * 50)

        semua = self.btree.traverse()

        if not semua:
            show_error("Tidak ada jadwal.")
            pause()
            return

        tanggal_sekarang = None
        nomor = 1

        for key, k in semua:
            if k.tanggal != tanggal_sekarang:
                tanggal_sekarang = k.tanggal
                print(f"\n{tanggal_sekarang} ({format_nama_hari(tanggal_sekarang)})")
                print("-" * 40)

            tampilkan_kegiatan(k, nomor)
            nomor += 1

        pause()

    def rebuild_btree(self):
        """Membangun ulang B-Tree setelah data JSON berubah"""
        self.btree = BTree(t=2)
        Serializer.load_from_json(DATA_FILE, self.btree)
