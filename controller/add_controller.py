from models.kegiatan import Kegiatan
from models.validator import Validator
from models.serializer import Serializer
from views.header_view import clear_screen, tampilkan_header, pause
from views.kegiatan_view import tampilkan_kegiatan
from views.output_view import show_error, show_success
from datetime import datetime

DATA_FILE = "data/jadwal.json"

class AddController:
    def __init__(self, btree):
        self.btree = btree

    def tambah_kegiatan(self):
        clear_screen()
        tampilkan_header()
        print("\nTAMBAH KEGIATAN BARU")
        print("-" * 50)

        try:
            id_kegiatan = int(input("ID Kegiatan         : "))
            tanggal = input("Tanggal (YYYY-MM-DD): ")
            waktu_mulai = input("Waktu Mulai (HH:MM) : ")
            waktu_selesai = input("Waktu Selesai(HH:MM): ")
            nama = input("Nama Kegiatan       : ")
            tempat = input("Tempat              : ")
            deskripsi = input("Deskripsi           : ")
            valid, pesan = Validator.validate_kegiatan(tanggal, waktu_mulai, nama, tempat)
            if not valid:
                show_error(pesan)
                pause()
                return
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
            existing = self.btree.search(self.btree.root, key)
            if existing:
                show_error("Sudah ada kegiatan pada tanggal & waktu tersebut.")
                tampilkan_kegiatan(existing)
                if input("Timpa kegiatan? (y/n): ").lower() != "y":
                    return
            self.btree.insert(key, kegiatan)
            Serializer.save_to_json(DATA_FILE, self.btree)
            show_success("Kegiatan berhasil ditambahkan.")
            tampilkan_kegiatan(kegiatan)
        except Exception:
            show_error("Input tidak valid.")
        pause()
