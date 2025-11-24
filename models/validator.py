import datetime

class Validator:
    @staticmethod
    def valid_tanggal(tanggal):
        """
        Format tanggal wajib: YYYY-MM-DD
        """
        try:
            datetime.datetime.strptime(tanggal, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def valid_waktu(waktu):
        """
        Format waktu wajib: HH:MM (24 jam)
        """
        try:
            datetime.datetime.strptime(waktu, "%H:%M")
            return True
        except ValueError:
            return False

    @staticmethod
    def not_empty(value):
        """
        Mengecek input tidak boleh kosong
        """
        return value is not None and value.strip() != ""

    @staticmethod
    def validate_kegiatan(tanggal, waktu, nama, tempat):
        """
        Validasi lengkap untuk input kegiatan
        """
        if not Validator.valid_tanggal(tanggal):
            return False, "Format tanggal harus YYYY-MM-DD"
        if not Validator.valid_waktu(waktu):
            return False, "Format waktu harus HH:MM"
        if not Validator.not_empty(nama):
            return False, "Nama kegiatan tidak boleh kosong"
        if not Validator.not_empty(tempat):
            return False, "Tempat tidak boleh kosong"
        return True, "Valid"
