from views.header_view import clear_screen, tampilkan_header, pause
from views.menu_view import tampilkan_menu
from views.output_view import show_error
from controller.add_controller import AddController
from controller.search_controller import SearchController
from controller.update_controller import UpdateController
from controller.delete_controller import DeleteController
from controller.show_all_controller import ShowAllController
from models.btree import BTree
from models.serializer import Serializer

DATA_FILE = "data/jadwal.json"

class AppController:

    def __init__(self):
        self.btree = BTree(t=2)
        try:
            Serializer.load_from_json(DATA_FILE, self.btree)
        except:
            Serializer.save_to_json(DATA_FILE, self.btree)
        self.add_controller = AddController(self.btree)
        self.search_controller = SearchController(self.btree)
        self.update_controller = UpdateController(self.btree)
        self.delete_controller = DeleteController(self.btree)
        self.show_all_controller = ShowAllController(self.btree)

    def run(self):
        while True:
            clear_screen()
            tampilkan_header()
            tampilkan_menu()
            pilihan = input("\nPilih menu (1-6): ").strip()
            if pilihan == "1":
                self.add_controller.tambah_kegiatan()
            elif pilihan == "2":
                self.search_controller.menu_cari()
            elif pilihan == "3":
                self.update_controller.menu_update()
            elif pilihan == "4":
                self.delete_controller.menu_delete()
            elif pilihan == "5":
                self.show_all_controller.run()
            elif pilihan == "6":
                Serializer.save_to_json(DATA_FILE, self.btree)
                print("\nData berhasil disimpan. Keluar aplikasi...")
                break
            else:
                show_error("Pilihan tidak valid.")
                pause()
