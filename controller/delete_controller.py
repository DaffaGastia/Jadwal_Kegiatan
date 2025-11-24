import json
from models.kegiatan import Kegiatan
from models.btree import BTree
from models.serializer import Serializer
from views.header_view import clear_screen, tampilkan_header, pause
from views.kegiatan_view import tampilkan_kegiatan
from views.output_view import show_error, show_success

DATA_FILE = "data/jadwal.json"

class DeleteController:
    def __init__(self, btree):
        self.btree = btree

    def rebuild_btree(self):
        self.btree = BTree(t=2)
        Serializer.load_from_json(DATA_FILE, self.btree)

    def menu_delete(self):
        while True:
            clear_screen()
            tampilkan_header()
            print("\nHAPUS KEGIATAN")
            print("-" * 50)
            print("1. Hapus berdasarkan tanggal & waktu")
            print("2. Hapus berdasarkan ID kegiatan")
            print("3. Hapus semua kegiatan pada tanggal tertentu")
            print("4. Hapus berdasarkan rentang waktu (overlap)")
            print("5. Kembali")
            pilih = input("\nPilih menu (1-5): ").strip()
            if pilih == "5":
                return
            try:
                with open(DATA_FILE, "r") as f:
                    data_list = json.load(f)
            except:
                show_error("Gagal membaca data JSON.")
                pause()
                continue

            if pilih == "1":
                tanggal = input("Tanggal (YYYY-MM-DD): ")
                waktu   = input("Waktu mulai (HH:MM): ")
                key_target = f"{tanggal} {waktu}"
                found = None
                new_list = []
                for item in data_list:
                    waktu_mulai = item["waktu"].split("-")[0]
                    key = f"{item['tanggal']} {waktu_mulai}"
                    if key == key_target:
                        found = item
                    else:
                        new_list.append(item)
                if not found:
                    show_error("Kegiatan tidak ditemukan.")
                    pause()
                    continue
                tampilkan_kegiatan(Kegiatan.from_dict(found))
                if input("Hapus? (y/n): ").lower() == "y":
                    with open(DATA_FILE, "w") as f:
                        json.dump(new_list, f, indent=4)
                    self.rebuild_btree()
                    show_success("Kegiatan berhasil dihapus.")
                pause()

            elif pilih == "2":
                id_hapus = input("Masukkan ID kegiatan: ")
                found = None
                new_list = []
                for item in data_list:
                    if str(item["id"]) == id_hapus:
                        found = item
                    else:
                        new_list.append(item)
                if not found:
                    show_error("ID tidak ditemukan.")
                    pause()
                    continue
                tampilkan_kegiatan(Kegiatan.from_dict(found))
                if input("Hapus? (y/n): ").lower() == "y":
                    with open(DATA_FILE, "w") as f:
                        json.dump(new_list, f, indent=4)
                    self.rebuild_btree()
                    show_success("Kegiatan berhasil dihapus.")
                pause()

            elif pilih == "3":
                tanggal = input("Tanggal (YYYY-MM-DD): ")
                keys_deleted = [item for item in data_list if item["tanggal"] == tanggal]
                if not keys_deleted:
                    show_error("Tidak ada kegiatan pada tanggal tersebut.")
                    pause()
                    continue
                print(f"\nDitemukan {len(keys_deleted)} kegiatan untuk dihapus.")
                if input("Hapus semua? (y/n): ").lower() == "y":
                    new_list = [i for i in data_list if i["tanggal"] != tanggal]
                    with open(DATA_FILE, "w") as f:
                        json.dump(new_list, f, indent=4)
                    self.rebuild_btree()
                    show_success("Semua kegiatan berhasil dihapus.")
                pause()

            elif pilih == "4":
                tanggal = input("Tanggal (YYYY-MM-DD): ")
                mulai   = input("Dari waktu (HH:MM): ")
                selesai = input("Sampai waktu (HH:MM): ")
                def to_int(w):
                    return int(w.replace(":", ""))
                start = to_int(mulai)
                end   = to_int(selesai)
                new_list = []
                deleted  = []
                for item in data_list:
                    if item["tanggal"] != tanggal:
                        new_list.append(item)
                        continue
                    w1, w2 = item["waktu"].split("-")
                    w1 = to_int(w1)
                    w2 = to_int(w2)
                    if (w1 < end and w2 > start):
                        deleted.append(item)
                    else:
                        new_list.append(item)
                if not deleted:
                    show_error("Tidak ada kegiatan overlap di rentang waktu ini.")
                    pause()
                    continue
                print(f"\nDitemukan {len(deleted)} kegiatan overlap.")
                if input("Hapus semua? (y/n): ").lower() == "y":
                    with open(DATA_FILE, "w") as f:
                        json.dump(new_list, f, indent=4)
                    self.rebuild_btree()
                    show_success("Kegiatan overlap berhasil dihapus.")
                pause()
            else:
                show_error("Menu tidak valid.")
                pause()
