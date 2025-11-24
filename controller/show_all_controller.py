from views.header_view import clear_screen, tampilkan_header, pause
from views.kegiatan_view import tampilkan_kegiatan, format_nama_hari
from views.output_view import show_error


class ShowAllController:

    def __init__(self, btree):
        self.btree = btree

    def run(self):
        """Menampilkan seluruh jadwal secara terurut berdasarkan tanggal dan waktu"""
        clear_screen()
        tampilkan_header()
        print("\nSEMUA JADWAL TERURUT")
        print("-" * 50)
        semua = self.btree.traverse()
        if not semua:
            show_error("Tidak ada jadwal tersimpan.")
            pause()
            return
        tanggal_sekarang = None
        nomor = 1
        for key, kegiatan in semua:
            if kegiatan.tanggal != tanggal_sekarang:
                tanggal_sekarang = kegiatan.tanggal
                hari = format_nama_hari(tanggal_sekarang)
                print(f"\n{tanggal_sekarang} ({hari})")
                print("-" * 40)
            tampilkan_kegiatan(kegiatan, nomor)
            nomor += 1
        pause()
