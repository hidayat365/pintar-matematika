#!/usr/bin/env python3
"""Pintar Matematika — server latihan soal matematika SD kelas 4.

Jalankan:  python3 app.py   lalu buka http://localhost:8000
Hanya memakai pustaka standar Python. Hasil latihan disimpan di SQLite.
"""

import argparse
import json
import os
import re
import sqlite3
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import soal as bank

AKAR = Path(__file__).resolve().parent
DB_BAWAAN = Path(os.environ.get("PINTAR_DB", AKAR / "data" / "latihan.db"))
STATIS = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/index.html": ("index.html", "text/html; charset=utf-8"),
    "/style.css": ("style.css", "text/css; charset=utf-8"),
    "/app.js": ("app.js", "application/javascript; charset=utf-8"),
}
MAKS_BADAN = 64 * 1024

SKEMA = """
CREATE TABLE IF NOT EXISTS latihan (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    nama     TEXT NOT NULL,
    topik    TEXT NOT NULL,
    dibuat   TEXT NOT NULL,
    selesai  TEXT,
    soal     TEXT NOT NULL,
    jawaban  TEXT,
    benar    INTEGER,
    nilai    INTEGER,
    durasi   INTEGER
);
"""


class Galat(Exception):
    def __init__(self, status, pesan):
        super().__init__(pesan)
        self.status = status
        self.pesan = pesan


def buka_db(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.executescript(SKEMA)
    return db


def sekarang():
    return datetime.now().isoformat(timespec="seconds")


# ------------------------------------------------------------- logika aplikasi

def mulai_latihan(db, nama, topik):
    nama = " ".join(str(nama or "").split())[:40] or "Tanpa Nama"
    if topik not in bank.KODE_TOPIK:
        raise Galat(400, "Topik tidak dikenal.")
    daftar = bank.buat_latihan(topik)
    with db:
        cur = db.execute(
            "INSERT INTO latihan (nama, topik, dibuat, soal) VALUES (?, ?, ?, ?)",
            (nama, topik, sekarang(), json.dumps(daftar, ensure_ascii=False)))
    return ambil_latihan(db, cur.lastrowid)


def _baris(db, id_latihan):
    baris = db.execute("SELECT * FROM latihan WHERE id = ?", (id_latihan,)).fetchone()
    if baris is None:
        raise Galat(404, "Latihan tidak ditemukan.")
    return baris


def ambil_latihan(db, id_latihan):
    """Latihan berjalan: soal tanpa kunci. Latihan selesai: lengkap dengan kunci."""
    b = _baris(db, id_latihan)
    daftar = json.loads(b["soal"])
    data = {"id": b["id"], "nama": b["nama"], "topik": b["topik"],
            "nama_topik": bank.nama_topik(b["topik"]), "dibuat": b["dibuat"],
            "selesai": b["selesai"]}
    if b["selesai"] is None:
        data["soal"] = [{"teks": s["teks"], "pilihan": s["pilihan"]} for s in daftar]
        return data
    jawaban = json.loads(b["jawaban"])
    data.update(benar=b["benar"], nilai=b["nilai"], durasi=b["durasi"],
                jumlah=len(daftar),
                soal=[dict(s, jawaban=j) for s, j in zip(daftar, jawaban)])
    return data


def kumpulkan(db, id_latihan, jawaban):
    b = _baris(db, id_latihan)
    if b["selesai"] is not None:
        raise Galat(409, "Latihan ini sudah dikumpulkan.")
    daftar = json.loads(b["soal"])
    if not isinstance(jawaban, list) or len(jawaban) != len(daftar):
        raise Galat(400, f"Jawaban harus berupa daftar {len(daftar)} isian.")
    for j in jawaban:
        if j is not None and (type(j) is not int or not 0 <= j <= 3):
            raise Galat(400, "Setiap jawaban harus 0–3 atau kosong.")
    benar = sum(1 for s, j in zip(daftar, jawaban) if j == s["benar"])
    nilai = round(benar / len(daftar) * 100)
    selesai = sekarang()
    durasi = int((datetime.fromisoformat(selesai)
                  - datetime.fromisoformat(b["dibuat"])).total_seconds())
    with db:
        db.execute(
            "UPDATE latihan SET selesai = ?, jawaban = ?, benar = ?, nilai = ?, durasi = ? "
            "WHERE id = ? AND selesai IS NULL",
            (selesai, json.dumps(jawaban), benar, nilai, max(durasi, 0), id_latihan))
    return ambil_latihan(db, id_latihan)


def riwayat(db):
    baris = db.execute(
        "SELECT id, nama, topik, selesai, benar, nilai, durasi FROM latihan "
        "WHERE selesai IS NOT NULL ORDER BY selesai DESC, id DESC").fetchall()
    daftar = [dict(b, nama_topik=bank.nama_topik(b["topik"]), jumlah=bank.JUMLAH_SOAL)
              for b in baris]
    nilai = [d["nilai"] for d in daftar]
    ringkasan = {"jumlah": len(nilai),
                 "rata_rata": round(sum(nilai) / len(nilai)) if nilai else None,
                 "terbaik": max(nilai) if nilai else None}
    return {"ringkasan": ringkasan, "latihan": daftar}


# ---------------------------------------------------------------------- HTTP

class Penangan(BaseHTTPRequestHandler):
    server_version = "PintarMatematika/1.0"

    def log_message(self, fmt, *args):
        if not getattr(self.server, "senyap", False):
            super().log_message(fmt, *args)

    def _kirim(self, status, badan, jenis):
        self.send_response(status)
        self.send_header("Content-Type", jenis)
        self.send_header("Content-Length", str(len(badan)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(badan)

    def _json(self, status, data):
        self._kirim(status, json.dumps(data, ensure_ascii=False).encode(),
                    "application/json; charset=utf-8")

    def _badan(self):
        panjang = int(self.headers.get("Content-Length") or 0)
        if panjang > MAKS_BADAN:
            raise Galat(413, "Data terlalu besar.")
        try:
            data = json.loads(self.rfile.read(panjang) or b"{}")
        except ValueError:
            raise Galat(400, "Data bukan JSON yang sah.")
        if not isinstance(data, dict):
            raise Galat(400, "Data harus berupa objek JSON.")
        return data

    def _layani(self, metode):
        jalur = self.path.split("?", 1)[0]
        try:
            if metode == "GET" and jalur in STATIS:
                berkas, jenis = STATIS[jalur]
                return self._kirim(200, (AKAR / "static" / berkas).read_bytes(), jenis)
            if not jalur.startswith("/api/"):
                raise Galat(404, "Halaman tidak ditemukan.")
            db = buka_db(self.server.db_path)
            try:
                self._json(200, self._api(db, metode, jalur))
            finally:
                db.close()
        except Galat as g:
            self._json(g.status, {"galat": g.pesan})
        except Exception as e:  # jangan sampai server berhenti karena satu permintaan
            self.log_error("Galat tak terduga: %r", e)
            self._json(500, {"galat": "Terjadi kesalahan di server."})

    def _api(self, db, metode, jalur):
        if (metode, jalur) == ("GET", "/api/topik"):
            return {"topik": bank.TOPIK, "jumlah_soal": bank.JUMLAH_SOAL}
        if (metode, jalur) == ("GET", "/api/riwayat"):
            return riwayat(db)
        if (metode, jalur) == ("POST", "/api/latihan"):
            data = self._badan()
            return mulai_latihan(db, data.get("nama"), data.get("topik"))
        cocok = re.fullmatch(r"/api/latihan/(\d{1,12})(/jawab)?", jalur)
        if cocok:
            id_latihan = int(cocok.group(1))
            if metode == "GET" and not cocok.group(2):
                return ambil_latihan(db, id_latihan)
            if metode == "POST" and cocok.group(2):
                return kumpulkan(db, id_latihan, self._badan().get("jawaban"))
        raise Galat(404, "Alamat API tidak ditemukan.")

    def do_GET(self):
        self._layani("GET")

    def do_POST(self):
        self._layani("POST")


def buat_server(host="127.0.0.1", port=8000, db_path=DB_BAWAAN, senyap=False):
    buka_db(db_path).close()
    server = ThreadingHTTPServer((host, port), Penangan)
    server.db_path = db_path
    server.senyap = senyap
    return server


def main():
    p = argparse.ArgumentParser(description="Pintar Matematika — latihan soal SD kelas 4")
    p.add_argument("--host", default="127.0.0.1",
                   help="alamat server (pakai 0.0.0.0 agar bisa diakses perangkat lain)")
    p.add_argument("--port", type=int, default=int(os.environ.get("PORT", 8000)))
    p.add_argument("--db", default=str(DB_BAWAAN), help="lokasi berkas database")
    a = p.parse_args()
    server = buat_server(a.host, a.port, a.db)
    tampil = "localhost" if a.host in ("127.0.0.1", "0.0.0.0") else a.host
    print(f"Pintar Matematika berjalan di http://{tampil}:{server.server_port}")
    print(f"Hasil latihan disimpan di {a.db}")
    print("Tekan Ctrl+C untuk berhenti.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer dihentikan.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
