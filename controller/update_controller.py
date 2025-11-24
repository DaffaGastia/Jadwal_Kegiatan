from models.kegiatan import Kegiatan
from models.validator import Validator
from models.serializer import Serializer
from views.header_view import clear_screen, tampilkan_header, pause
from views.kegiatan_view import tampilkan_kegiatan
from views.output_view import show_error, show_success
from datetime import datetime
import json

DATA_FILE = "data/jadwal.json"

class UpdateController:
    def __init__(self, btree):
        self.btree = btree

    # -----------------------------------------------------------
    #  CARI KEGIATAN LAMA
    # -----------------------------------------------------------
    def cari_kegiatan_lama(self, tanggal, waktu):
        key = f"{tanggal} {waktu}"
        return self.btree.search(self.btree.root, key)

    # -----------------------------------------------------------
    #  INPUT VALIDASI WAJIB TERISI
    # -----------------------------------------------------------
    def input_tidak_kosong(self, pesan):
        while True:
            val = input(pesan).strip()
            if val == "":
                show_error("Input tidak boleh kosong.")
                pause()
            else:
                return val

    # -----------------------------------------------------------
    #  INPUT JAM VALID + FORMAT BENAR
    # -----------------------------------------------------------
    def input_jam_valid(self, pesan):
        while True:
            jam = input(pesan).strip()
            if jam == "":
                show_error("Waktu tidak boleh kosong.")
                pause()
                continue

            try:
                datetime.strptime(jam, "%H:%M")
                return jam
            except:
                show_error("Format waktu salah! Gunakan HH:MM.")
                pause()


    # -----------------------------------------------------------
    #  MENU UPDATE
    # -----------------------------------------------------------
    def menu_update(self):
        clear_screen()
        tampilkan_header()

        print("\nUPDATE KEGIATAN")
        print("-" * 50)

        # Input data lama
        tanggal = self.input_tidak_kosong("Tanggal kegiatan lama (YYYY-MM-DD): ")
        waktu = self.input_jam_valid("Waktu mulai lama (HH:MM)          : ")

        kegiatan_lama = self.cari_kegiatan_lama(tanggal, waktu)

        if not kegiatan_lama:
            show_error("Kegiatan tidak ditemukan.")
            pause()
            return

        print("\nData Lama:")
        tampilkan_kegiatan(kegiatan_lama)

        if input("\nLanjut update? (y/n): ").lower() != "y":
            return

        # =====================================================
        #  INPUT DATA BARU (ID TIDAK PERLU DIUBAH)
        # =====================================================

        tanggal_baru = self.input_tidak_kosong("Tanggal baru (YYYY-MM-DD) : ")
        w1 = self.input_jam_valid("Waktu Mulai baru (HH:MM)  : ")

        while True:
            w2 = self.input_jam_valid("Waktu Selesai baru (HH:MM): ")
            t1 = datetime.strptime(w1, "%H:%M")
            t2 = datetime.strptime(w2, "%H:%M")
            if w1 == w2:
                show_error("Waktu selesai tidak boleh sama dengan waktu mulai.")
                pause()
                continue
            if t2 < t1:
                print("\nCatatan: Kegiatan melewati tengah malam.")
                pause()
                break
            break


        nama = self.input_tidak_kosong("Nama Kegiatan baru     : ")
        tempat = self.input_tidak_kosong("Tempat baru            : ")
        deskripsi = self.input_tidak_kosong("Deskripsi baru         : ")

        # validator
        valid, pesan = Validator.validate_kegiatan(tanggal_baru, w1, nama, tempat)
        if not valid:
            show_error(pesan)
            pause()
            return self.menu_update()

        waktu_final = f"{w1}-{w2}"

        kegiatan_baru = Kegiatan(
            kegiatan_lama.id,  
            tanggal_baru,
            waktu_final,
            nama,
            tempat,
            deskripsi
        )

        # =====================================================
        #  UPDATE DI FILE JSON (MENGGANTI SATU DATA SAJA)
        # =====================================================

        with open(DATA_FILE, "r") as f:
            data_list = json.load(f)

        key_lama = f"{tanggal} {waktu}"
        new_list = []

        for item in data_list:
            wmulai = item["waktu"].split("-")[0]
            key_item = f"{item['tanggal']} {wmulai}"

            if key_item == key_lama:
                new_list.append(kegiatan_baru.to_dict())  # replace
            else:
                new_list.append(item)

        with open(DATA_FILE, "w") as f:
            json.dump(new_list, f, indent=4)

        # rebuild
        self.rebuild_btree()

        show_success("Kegiatan berhasil di-update.")
        tampilkan_kegiatan(kegiatan_baru)
        pause()

    # -----------------------------------------------------------
    #  REBUILD B-TREE
    # -----------------------------------------------------------
    def rebuild_btree(self):
        from models.btree import BTree
        self.btree = BTree(t=2)
        Serializer.load_from_json(DATA_FILE, self.btree)
