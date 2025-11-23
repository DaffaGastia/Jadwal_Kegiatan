import os

def clear_screen():
    """Membersihkan tampilan terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    """Memberhentikan layar sampai user menekan ENTER."""
    input("\nTekan ENTER untuk melanjutkan...")


def tampilkan_header():
    """Menampilkan header utama aplikasi."""
    print("\n" + "=" * 50)
    print("   APLIKASI PENJADWALAN KEGIATAN HARIAN")
    print("          MENGGUNAKAN B-TREE (MVC)")
    print("=" * 50)
