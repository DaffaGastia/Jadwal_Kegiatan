class Kegiatan:
    def __init__(self, id, tanggal, waktu, nama, tempat, deskripsi):
        self.id = id
        self.tanggal = tanggal
        self.waktu = waktu
        self.nama = nama
        self.tempat = tempat
        self.deskripsi = deskripsi

    def get_key(self):
        """
        Menghasilkan key unik untuk B-Tree
        Format key: 'YYYY-MM-DD HH:MM'
        """
        return f"{self.tanggal} {self.waktu}"

    def to_dict(self):
        """
        Mengubah objek kegiatan menjadi dictionary
        untuk disimpan ke JSON
        """
        return {
            "id": self.id,
            "tanggal": self.tanggal,
            "waktu": self.waktu,
            "nama": self.nama,
            "tempat": self.tempat,
            "deskripsi": self.deskripsi
        }

    @staticmethod
    def from_dict(data):
        """
        Membuat objek Kegiatan dari dictionary JSON
        """
        return Kegiatan(
            id=data["id"],
            tanggal=data["tanggal"],
            waktu=data["waktu"],
            nama=data["nama"],
            tempat=data["tempat"],
            deskripsi=data["deskripsi"]
        )

    def __str__(self):
        """
        Format tampilan saat kegiatan dicetak
        """
        return (
            f"ID: {self.id}\n"
            f"Tanggal: {self.tanggal}\n"
            f"Waktu: {self.waktu}\n"
            f"Nama Kegiatan: {self.nama}\n"
            f"Tempat: {self.tempat}\n"
            f"Deskripsi: {self.deskripsi}\n"
        )
