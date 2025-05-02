from datetime import datetime

def format_tanggal(tanggal) -> str:
    try:
        # Jika input string, ubah ke datetime
        if isinstance(tanggal, str):
            tanggal_obj = datetime.strptime(tanggal, "%Y-%m-%d")
        elif isinstance(tanggal, datetime):
            tanggal_obj = tanggal
        else:
            return "Input tidak valid. Harus string atau datetime."

        # Mapping nama bulan ke bahasa Indonesia
        bulan_indo = [
            "Januari", "Februari", "Maret", "April", "Mei", "Juni",
            "Juli", "Agustus", "September", "Oktober", "November", "Desember"
        ]

        tanggal_format = f"{tanggal_obj.day:02d} {bulan_indo[tanggal_obj.month - 1]} {tanggal_obj.year}"
        return tanggal_format

    except Exception as e:
        return f"Format tanggal tidak valid: {e}"