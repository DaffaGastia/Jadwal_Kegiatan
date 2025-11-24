from views.header_view import clear_screen, tampilkan_header, pause
from views.kegiatan_view import tampilkan_kegiatan, format_nama_hari
from views.output_view import show_error
from datetime import datetime


class SearchController:
    def __init__(self, btree):
        self.btree = btree

    # ===========================================================
    #  CARI SEMUA KEGIATAN PADA TANGGAL
    # ===========================================================
    def cari_by_tanggal(self, tanggal):
        semua = self.btree.traverse()
        hasil = [k for key, k in semua if k.tanggal == tanggal]

        # urutkan berdasarkan waktu mulai
        hasil.sort(key=lambda k: k.waktu.split('-')[0])
        return hasil

    # ===========================================================
    #  CARI KEGIATAN DI DALAM RENTANG WAKTU
    # ===========================================================
    def cari_kegiatan_range(self, tanggal, waktu_dicari):
        semua = self.btree.traverse()
        hasil = []

        for key, k in semua:
            if k.tanggal != tanggal:
                continue

            try:
                waktu_mulai, waktu_selesai = k.waktu.split('-')
            except ValueError:
                continue

            if waktu_mulai <= waktu_dicari <= waktu_selesai:
                hasil.append(k)

        hasil.sort(key=lambda k: k.waktu.split('-')[0])
        return hasil

    # ===========================================================
    #  MENU CARI
    # ===========================================================
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

            # ==================== KEMBALI =====================
            if mode == "3":
                return

            # ==================== CARI TANGGAL =====================
            elif mode == "1":
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

            # ==================== CARI BERDASARKAN RANGE =====================
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
