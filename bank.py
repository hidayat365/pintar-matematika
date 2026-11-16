"""Daftar mata pelajaran dan topiknya; pintu tunggal bagi app.py untuk membuat soal."""

import soal
import soal_inggris
import soal_sunda

JUMLAH_SOAL = soal.JUMLAH_SOAL

_MAPEL = [
    {"kode": "matematika", "nama": "Matematika", "kelas": "Kelas 4", "ikon": "🧮", "modul": soal},
    {"kode": "inggris", "nama": "Bahasa Inggris", "kelas": "Kelas 4", "ikon": "📘", "modul": soal_inggris},
    {"kode": "sunda", "nama": "Bahasa Sunda", "kelas": "Kelas 1", "ikon": "🎋", "modul": soal_sunda},
]

# Untuk dikirim ke browser.
MAPEL = [{"kode": m["kode"], "nama": m["nama"], "kelas": m["kelas"], "ikon": m["ikon"],
          "topik": m["modul"].TOPIK}
         for m in _MAPEL]

_INDEKS = {t["kode"]: (m, t) for m in _MAPEL for t in m["modul"].TOPIK}
KODE_TOPIK = list(_INDEKS)


def nama_topik(kode):
    return _INDEKS[kode][1]["nama"] if kode in _INDEKS else kode


def nama_mapel(kode):
    return _INDEKS[kode][0]["nama"] if kode in _INDEKS else ""


def buat_latihan(topik, rng=None):
    if topik not in _INDEKS:
        raise ValueError(f"topik tidak dikenal: {topik}")
    return _INDEKS[topik][0]["modul"].buat_latihan(topik, rng=rng)
