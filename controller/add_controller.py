from models.kegiatan import Kegiatan
from models.validator import Validator
from models.serializer import Serializer
from models.btree import BTree
from views.header_view import clear_screen, tampilkan_header, pause
from views.kegiatan_view import tampilkan_kegiatan
from views.output_view import show_error, show_success
from datetime import datetime
import json

DATA_FILE = "data/jadwal.json"

class AddController:
    def __init__(self, btree):
        self.btree = btree

    def generate_id(self):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
            if not data:
                return 1
            last_id = max(item["id"] for item in data)
            return last_id + 1
        except:
            return 1

    def input_tidak_kosong(self, pesan):
        while True:
            val = input(pesan).strip()
            if val == "":
                show_error("Input tidak boleh kosong.")
                pause()
            else:
                return val

    def input_tanggal(self):
        while True:
            tanggal = input("Tanggal (YYYY-MM-DD): ").strip()
            if tanggal == "":
                show_error("Tanggal tidak boleh kosong.")
                pause()
                continue
            try:
                datetime.strptime(tanggal, "%Y-%m-%d")
                return tanggal
            except:
                show_error("Format tanggal salah! Gunakan YYYY-MM-DD.")
                pause()

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

    def tambah_kegiatan(self):
        clear_screen()
        tampilkan_header()
        print("\nTAMBAH KEGIATAN BARU")
        print("-" * 50)
        id_kegiatan = self.generate_id()
        tanggal = self.input_tanggal()
        waktu_mulai = self.input_jam_valid("Waktu Mulai (HH:MM) : ")
        while True:
            waktu_selesai = self.input_jam_valid("Waktu Selesai(HH:MM): ")
            w1 = datetime.strptime(waktu_mulai, "%H:%M")
            w2 = datetime.strptime(waktu_selesai, "%H:%M")
            if w2 <= w1:
                show_error("Waktu selesai harus lebih besar dari waktu mulai.")
                pause()
                continue
            break  
        
        nama = self.input_tidak_kosong("Nama Kegiatan       : ")
        tempat = self.input_tidak_kosong("Tempat              : ")
        deskripsi = self.input_tidak_kosong("Deskripsi           : ")
        valid, pesan = Validator.validate_kegiatan(tanggal, waktu_mulai, nama, tempat)
        if not valid:
            show_error(pesan)
            pause()
            return self.tambah_kegiatan()
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
        pause()
