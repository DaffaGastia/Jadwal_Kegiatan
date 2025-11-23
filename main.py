from btree.btree import BTree
from models.kegiatan import Kegiatan
from utils.serializer import Serializer
from utils.validator import Validator
import os
from datetime import datetime

DATA_FILE = "data/jadwal.json"

def clear_screen():
    """Clear console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    """Pause dan tunggu user input"""
    input("\nTekan ENTER untuk melanjutkan...")

def tampilkan_header():
    """Tampilkan header aplikasi"""
    print("\n" + "="*50)
    print("   APLIKASI PENJADWALAN KEGIATAN HARIAN")
    print("          MENGGUNAKAN B-TREE")
    print("="*50)

def tampilkan_menu():
    """Tampilkan menu utama"""
    print("\n" + "-"*50)
    print("MENU UTAMA:")
    print("-"*50)
    print("1. Tambah Kegiatan")
    print("2. Cari Kegiatan")
    print("3. Update Kegiatan")
    print("4. Hapus Kegiatan")
    print("5. Tampilkan Semua Jadwal")
    print("6. Keluar")
    print("-"*50)

def format_nama_hari(tanggal_str):
    """Konversi tanggal ke nama hari dalam Bahasa Indonesia"""
    try:
        tanggal = datetime.strptime(tanggal_str, "%Y-%m-%d")
        hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
        return hari[tanggal.weekday()]
    except:
        return ""

def input_kegiatan():
    """Input data kegiatan baru"""
    try:
        id_kegiatan = int(input("ID Kegiatan           : "))
        tanggal = input("Tanggal (YYYY-MM-DD)  : ")
        waktu_mulai = input("Waktu Mulai (HH:MM)   : ")
        waktu_selesai = input("Waktu Selesai (HH:MM) : ")
        nama = input("Nama Kegiatan         : ")
        tempat = input("Tempat                : ")
        deskripsi = input("Deskripsi             : ")

        valid, pesan = Validator.validate_kegiatan(tanggal, waktu_mulai, nama, tempat)
        if not valid:
            print(f"\nError: {pesan}")
            return None
        try:
            mulai = datetime.strptime(waktu_mulai, "%H:%M")
            selesai = datetime.strptime(waktu_selesai, "%H:%M")
            if selesai <= mulai:
                print("\nError: Waktu selesai harus lebih besar dari waktu mulai!")
                return None
        except ValueError:
            print("\nError: Format waktu tidak valid!")
            return None
        waktu = f"{waktu_mulai}-{waktu_selesai}"
        return Kegiatan(id_kegiatan, tanggal, waktu, nama, tempat, deskripsi)
    except ValueError:
        print("\nError: ID Kegiatan harus berupa angka!")
        return None
    except KeyboardInterrupt:
        print("\n\nInput dibatalkan.")
        return None

def tampilkan_kegiatan(kegiatan, nomor=None):
    """Tampilkan detail kegiatan dengan format rapi"""
    prefix = f"[{nomor}] " if nomor else ""
    if '-' in kegiatan.waktu:
        waktu_mulai, waktu_selesai = kegiatan.waktu.split('-')
        waktu_display = f"{waktu_mulai} - {waktu_selesai}"
    else:
        waktu_display = kegiatan.waktu
    nama_hari = format_nama_hari(kegiatan.tanggal)
    print(f"\n{prefix}{'='*45}")
    print(f"Tanggal  : {kegiatan.tanggal} ({nama_hari})")
    print(f"Waktu    : {waktu_display}")
    print(f"Kegiatan : {kegiatan.nama}")
    print(f"Tempat   : {kegiatan.tempat}")
    print(f"Deskripsi: {kegiatan.deskripsi}")
    print("="*45)

def cari_kegiatan_by_tanggal(btree, tanggal):
    """Cari semua kegiatan pada tanggal tertentu"""
    semua = btree.traverse()
    kegiatan_hari = [k for key, k in semua if k.tanggal == tanggal]
    kegiatan_hari.sort(key=lambda k: k.waktu.split('-')[0] if '-' in k.waktu else k.waktu)
    return kegiatan_hari

def menu_tambah_kegiatan(btree):
    """Menu untuk menambah kegiatan"""
    while True:
        clear_screen()
        tampilkan_header()
        print("\nTAMBAH KEGIATAN BARU")
        print("-"*50)
        
        kegiatan = input_kegiatan()
        
        if kegiatan:
            key = kegiatan.get_key()
            existing = btree.search(btree.root, key)
            if existing:
                print("\nSudah ada kegiatan pada tanggal dan waktu tersebut!")
                print("Kegiatan yang ada:")
                tampilkan_kegiatan(existing)
                overwrite = input("\nApakah ingin menimpa kegiatan tersebut? (y/n): ").lower()
                if overwrite != 'y':
                    print("\nPenambahan dibatalkan.")
                    pause()
                    continue
            
            btree.insert(key, kegiatan)
            Serializer.save_to_json(DATA_FILE, btree)
            print("\nKegiatan berhasil ditambahkan!")
            tampilkan_kegiatan(kegiatan)
        
        print("\n" + "-"*50)
        lagi = input("Tambah kegiatan lagi? (y/n): ").lower()
        if lagi != 'y':
            break

def menu_cari_kegiatan(btree):
    """Menu untuk mencari kegiatan"""
    while True:
        clear_screen()
        tampilkan_header()
        print("\nCARI KEGIATAN")
        print("-"*50)
        print("\nPilih mode pencarian:")
        print("1. Cari berdasarkan tanggal saja")
        print("2. Cari berdasarkan tanggal dan waktu spesifik")
        print("3. Kembali")
        
        mode = input("\nPilih mode (1-3): ").strip()
        if mode == "3":
            break
        try:
            if mode == "1":
                print("\n" + "-"*50)
                tanggal = input("Tanggal (YYYY-MM-DD): ")
                
                kegiatan_hari = cari_kegiatan_by_tanggal(btree, tanggal)
                
                if kegiatan_hari:
                    nama_hari = format_nama_hari(tanggal)
                    print(f"\nDitemukan {len(kegiatan_hari)} kegiatan pada {tanggal} ({nama_hari}):")
                    print("="*50)
                    for idx, k in enumerate(kegiatan_hari, 1):
                        tampilkan_kegiatan(k, idx)
                else:
                    print(f"\nTidak ada kegiatan pada tanggal {tanggal}.")
                    
                pause()
                
            elif mode == "2":
                print("\n" + "-"*50)
                tanggal = input("Tanggal (YYYY-MM-DD): ")
                waktu = input("Waktu Mulai (HH:MM) : ")
                key = f"{tanggal} {waktu}"
                hasil = btree.search(btree.root, key)
                if hasil:
                    print("\nData Ditemukan!")
                    tampilkan_kegiatan(hasil)
                else:
                    print("\nKegiatan tidak ditemukan pada waktu tersebut.")
                    lihat_semua = input(f"\nLihat semua kegiatan di tanggal {tanggal}? (y/n): ").lower()
                    if lihat_semua == 'y':
                        kegiatan_hari = cari_kegiatan_by_tanggal(btree, tanggal)
                        if kegiatan_hari:
                            nama_hari = format_nama_hari(tanggal)
                            print(f"\nKegiatan di tanggal {tanggal} ({nama_hari}):")
                            for idx, k in enumerate(kegiatan_hari, 1):
                                tampilkan_kegiatan(k, idx)
                        else:
                            print(f"\nTidak ada kegiatan di tanggal {tanggal}.")
                
                pause()
            else:
                print("\nPilihan tidak valid!")
                pause()
        
        except KeyboardInterrupt:
            print("\n\nPencarian dibatalkan.")
            break
        
        print("\n" + "-"*50)
        lagi = input("Cari kegiatan lagi? (y/n): ").lower()
        if lagi != 'y':
            break

def menu_update_kegiatan(btree):
    """Menu untuk update kegiatan"""
    while True:
        clear_screen()
        tampilkan_header()
        print("\nUPDATE KEGIATAN")
        print("-"*50)
        
        try:
            print("\nCari kegiatan yang ingin diupdate:")
            print("1. Cari berdasarkan tanggal (pilih dari daftar)")
            print("2. Cari berdasarkan tanggal dan waktu spesifik")
            
            mode = input("\nPilih mode (1-2): ").strip()
            hasil = None
            key_lama = None
            
            if mode == "1":
                tanggal = input("\nTanggal (YYYY-MM-DD): ")
                kegiatan_hari = cari_kegiatan_by_tanggal(btree, tanggal)
                
                if not kegiatan_hari:
                    print(f"\nTidak ada kegiatan pada tanggal {tanggal}.")
                    lagi = input("\nCoba cari lagi? (y/n): ").lower()
                    if lagi != 'y':
                        break
                    continue
                
                print(f"\nKegiatan pada {tanggal}:")
                for idx, k in enumerate(kegiatan_hari, 1):
                    waktu_display = k.waktu.split('-')[0] if '-' in k.waktu else k.waktu
                    print(f"{idx}. [{waktu_display}] {k.nama}")
                pilih = input("\nPilih nomor kegiatan yang ingin diupdate: ").strip()
                try:
                    idx = int(pilih) - 1
                    if 0 <= idx < len(kegiatan_hari):
                        hasil = kegiatan_hari[idx]
                        waktu_key = hasil.waktu.split('-')[0] if '-' in hasil.waktu else hasil.waktu
                        key_lama = f"{hasil.tanggal} {waktu_key}"
                    else:
                        print("\nNomor tidak valid!")
                        pause()
                        continue
                except ValueError:
                    print("\nInput tidak valid!")
                    pause()
                    continue
                    
            elif mode == "2":
                tanggal = input("\nTanggal lama (YYYY-MM-DD): ")
                waktu = input("Waktu mulai lama (HH:MM) : ")
                key_lama = f"{tanggal} {waktu}"
                hasil = btree.search(btree.root, key_lama)
            else:
                print("\nPilihan tidak valid!")
                pause()
                continue
            
            if not hasil:
                print("\nKegiatan tidak ditemukan.")
                lagi = input("\nCoba cari lagi? (y/n): ").lower()
                if lagi != 'y':
                    break
                continue
            print("\nData Lama:")
            tampilkan_kegiatan(hasil)
            
            konfirmasi = input("\nLanjutkan update? (y/n): ").lower()
            if konfirmasi != 'y':
                print("\nUpdate dibatalkan.")
                pause()
                break
            print("\n" + "-"*50)
            print("Masukkan data baru:")
            print("-"*50)
            
            kegiatan_baru = input_kegiatan()
            
            if kegiatan_baru:
                key_baru = kegiatan_baru.get_key()
                btree.insert(key_baru, kegiatan_baru)
                Serializer.save_to_json(DATA_FILE, btree)
                print("\nKegiatan berhasil di-update!")
                print("\nData Baru:")
                tampilkan_kegiatan(kegiatan_baru)
                if key_lama != key_baru:
                    print("\nCatatan: B-Tree delete belum diimplementasi.")
                    print("Data lama masih tersimpan. Silakan hapus manual dari JSON jika perlu.")
        
        except KeyboardInterrupt:
            print("\n\nUpdate dibatalkan.")
            break
        
        print("\n" + "-"*50)
        lagi = input("Update kegiatan lain? (y/n): ").lower()
        if lagi != 'y':
            break

def menu_hapus_kegiatan(btree):
    """Menu untuk hapus kegiatan"""
    clear_screen()
    tampilkan_header()
    print("\nHAPUS KEGIATAN")
    print("-"*50)
    print("\nFitur delete() belum tersedia pada B-Tree.")
    print("\nCara manual:")
    print("1. Buka file: data/jadwal.json")
    print("2. Hapus kegiatan yang diinginkan")
    print("3. Restart aplikasi")
    pause()

def menu_tampilkan_semua(btree):
    """Menu untuk menampilkan semua jadwal"""
    clear_screen()
    tampilkan_header()
    print("\nSEMUA JADWAL TERURUT")
    print("-"*50)

    semua = btree.traverse()
    
    if not semua:
        print("\nBelum ada kegiatan terdaftar.")
    else:
        print(f"\nTotal: {len(semua)} kegiatan\n")
        tanggal_sekarang = None
        nomor = 1
        for key, kegiatan in semua:
            if kegiatan.tanggal != tanggal_sekarang:
                if tanggal_sekarang is not None:
                    print("\n" + "="*50)
                tanggal_sekarang = kegiatan.tanggal
                nama_hari = format_nama_hari(tanggal_sekarang)
                print(f"\n{tanggal_sekarang} ({nama_hari})")
                print("-"*50)
            if '-' in kegiatan.waktu:
                waktu_display = kegiatan.waktu.replace('-', ' - ')
            else:
                waktu_display = kegiatan.waktu
            print(f"\n[{nomor}] {waktu_display}")
            print(f"    {kegiatan.nama}")
            print(f"    {kegiatan.tempat}")
            print(f"    {kegiatan.deskripsi}")
            nomor += 1
        print("\n" + "="*50)
    pause()

def main():
    """Fungsi utama aplikasi"""
    btree = BTree(t=2)
    clear_screen()
    tampilkan_header()
    print("\nMemuat data dari JSON...")
    try:
        Serializer.load_from_json(DATA_FILE, btree)
        print("Data berhasil dimuat!")
        pause()
    except FileNotFoundError:
        print("File data tidak ditemukan. Membuat file baru...")
        Serializer.save_to_json(DATA_FILE, btree)
        print("File data berhasil dibuat!")
        pause()
    except Exception as e:
        print(f"Error saat memuat data: {e}")
        pause()

    while True:
        try:
            clear_screen()
            tampilkan_header()
            tampilkan_menu()
            pilihan = input("\nPilih menu (1-6): ").strip()
            if pilihan == "1":
                menu_tambah_kegiatan(btree)
            elif pilihan == "2":
                menu_cari_kegiatan(btree)
            elif pilihan == "3":
                menu_update_kegiatan(btree)
            elif pilihan == "4":
                menu_hapus_kegiatan(btree)
            elif pilihan == "5":
                menu_tampilkan_semua(btree)
            elif pilihan == "6":
                clear_screen()
                tampilkan_header()
                print("\nMenyimpan data...")
                Serializer.save_to_json(DATA_FILE, btree)
                print("Data berhasil disimpan!")
                print("\nTerima kasih telah menggunakan aplikasi!")
                print("="*50 + "\n")
                break
            else:
                print("\nPilihan tidak valid. Silakan pilih 1-6.")
                pause()
        except KeyboardInterrupt:
            print("\n\nProgram dihentikan oleh user.")
            print("Menyimpan data...")
            Serializer.save_to_json(DATA_FILE, btree)
            print("Data berhasil disimpan!")
            print("\nTerima kasih!\n")
            break
        except Exception as e:
            print(f"\nTerjadi error: {e}")
            pause()

if __name__ == "__main__":
    main()