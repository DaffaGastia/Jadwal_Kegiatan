from datetime import datetime

def format_nama_hari(tanggal_str):
    """Konversi tanggal YYYY-MM-DD menjadi nama hari."""
    try:
        tanggal = datetime.strptime(tanggal_str, "%Y-%m-%d")
        hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
        return hari[tanggal.weekday()]
    except:
        return ""


def format_waktu(waktu):
    """Format waktu menjadi lebih rapi."""
    if "-" in waktu:
        w1, w2 = waktu.split("-")
        return f"{w1} - {w2}"
    return waktu


def tampilkan_kegiatan(kegiatan, nomor=None):
    """Menampilkan kegiatan dengan layout rapi."""
    prefix = f"[{nomor}] " if nomor else ""
    waktu_display = format_waktu(kegiatan.waktu)
    nama_hari = format_nama_hari(kegiatan.tanggal)

    print(f"\n{prefix}{'='*45}")
    print(f"Tanggal  : {kegiatan.tanggal} ({nama_hari})")
    print(f"Waktu    : {waktu_display}")
    print(f"Kegiatan : {kegiatan.nama}")
    print(f"Tempat   : {kegiatan.tempat}")
    print(f"Deskripsi: {kegiatan.deskripsi}")
    print("="*45)
