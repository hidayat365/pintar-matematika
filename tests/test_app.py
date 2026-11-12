import json
import random
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import app  # noqa: E402
import soal  # noqa: E402


class UjiSoal(unittest.TestCase):
    def test_setiap_topik_menghasilkan_20_soal_unik_dan_sah(self):
        for kode in soal.KODE_TOPIK:
            for benih in range(150):
                daftar = soal.buat_latihan(kode, rng=random.Random(benih))
                self.assertEqual(len(daftar), 20, kode)
                self.assertEqual(len({(s["teks"], s.get("gambar")) for s in daftar}), 20, kode)
                for s in daftar:
                    self.assertEqual(len(s["pilihan"]), 4, s)
                    self.assertEqual(len(set(s["pilihan"])), 4, s)
                    self.assertIn(s["benar"], range(4), s)
                    self.assertTrue(s["pembahasan"], s)
                    self.assertNotIn("kunci", s)

    def test_setiap_pembangkit_berjalan(self):
        r = random.Random(7)
        for kode, daftar in soal.PEMBANGKIT.items():
            for buat in daftar:
                for _ in range(300):
                    s = buat(r)
                    self.assertEqual(len(set(s["pilihan"])), 4, (buat.__name__, s))

    def test_soal_bergambar_sah_dan_tidak_berulang(self):
        from xml.dom.minidom import parseString
        ada = 0
        for benih in range(60):
            daftar = soal.buat_latihan("bangun-datar", rng=random.Random(benih))
            gambar = [s["gambar"] for s in daftar if "gambar" in s]
            ada += len(gambar)
            self.assertEqual(len(gambar), len(set(gambar)))
            for g in gambar:
                parseString(g)                      # SVG harus XML yang sah
            self.assertTrue(all("kunci" not in s for s in daftar))
        self.assertGreater(ada, 0)

    def test_bangun_datar_mencakup_semua_subtopik(self):
        nama = {f.__name__ for f in soal.PEMBANGKIT["bangun-datar"]}
        for wajib in ("bd_kurva_gambar", "bd_segi_banyak_gambar", "bd_segi_banyak_teori",
                      "bd_jenis_segitiga", "bd_segiempat_gambar", "bd_dekomposisi_segitiga",
                      "bd_komposisi_persegi", "bd_susun_gambar"):
            self.assertIn(wajib, nama)

    def test_latihan_berikutnya_berbeda(self):
        a = [s["teks"] for s in soal.buat_latihan("perkalian")]
        b = [s["teks"] for s in soal.buat_latihan("perkalian")]
        self.assertNotEqual(a, b)

    def test_kunci_hitungan_benar(self):
        r = random.Random(1)
        for _ in range(200):
            s = soal.kali_1(r)
            a, b = s["teks"].replace(" = …", "").split(" × ")
            self.assertEqual(s["pilihan"][s["benar"]], str(int(a) * int(b)))

    def test_campuran_memuat_semua_topik(self):
        daftar = soal.buat_latihan("campuran", rng=random.Random(3))
        self.assertEqual(len(daftar), 20)


class UjiApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.db = Path(cls.tmp.name) / "uji.db"
        cls.server = app.buat_server("127.0.0.1", 0, cls.db, senyap=True)
        cls.alamat = f"http://127.0.0.1:{cls.server.server_port}"
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.tmp.cleanup()

    def minta(self, jalur, data=None):
        badan = json.dumps(data).encode() if data is not None else None
        req = urllib.request.Request(self.alamat + jalur, data=badan,
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req) as res:
                return res.status, json.loads(res.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read())

    def kunci(self, id_latihan):
        db = app.buka_db(self.db)
        try:
            baris = db.execute("SELECT soal FROM latihan WHERE id = ?", (id_latihan,)).fetchone()
        finally:
            db.close()
        return [s["benar"] for s in json.loads(baris["soal"])]

    def test_halaman_utama(self):
        with urllib.request.urlopen(self.alamat + "/") as res:
            self.assertIn(b"Pintar Matematika", res.read())

    def test_alur_lengkap(self):
        status, topik = self.minta("/api/topik")
        self.assertEqual(status, 200)
        self.assertEqual(len(topik["topik"]), 11)

        status, latihan = self.minta("/api/latihan", {"nama": "Budi", "topik": "pecahan"})
        self.assertEqual(status, 200)
        self.assertEqual(len(latihan["soal"]), 20)
        self.assertNotIn("benar", latihan["soal"][0])       # kunci tidak bocor
        self.assertNotIn("pembahasan", latihan["soal"][0])

        status, jalan = self.minta(f"/api/latihan/{latihan['id']}")
        self.assertNotIn("benar", jalan["soal"][0])

        kunci = self.kunci(latihan["id"])
        jawaban = list(kunci)
        jawaban[0] = (kunci[0] + 1) % 4   # satu salah
        jawaban[1] = None                 # satu kosong
        status, hasil = self.minta(f"/api/latihan/{latihan['id']}/jawab", {"jawaban": jawaban})
        self.assertEqual(status, 200)
        self.assertEqual(hasil["benar"], 18)
        self.assertEqual(hasil["nilai"], 90)
        self.assertEqual(hasil["soal"][0]["benar"], kunci[0])

        status, _ = self.minta(f"/api/latihan/{latihan['id']}/jawab", {"jawaban": kunci})
        self.assertEqual(status, 409)                       # tidak bisa dikumpulkan ulang

        status, catatan = self.minta("/api/riwayat")
        self.assertIn(latihan["id"], [x["id"] for x in catatan["latihan"]])
        self.assertGreaterEqual(catatan["ringkasan"]["jumlah"], 1)

    def test_masukan_tidak_sah(self):
        self.assertEqual(self.minta("/api/latihan", {"topik": "kalkulus"})[0], 400)
        self.assertEqual(self.minta("/api/latihan/99999")[0], 404)
        _, latihan = self.minta("/api/latihan", {"nama": "", "topik": "campuran"})
        self.assertEqual(latihan["nama"], "Tanpa Nama")
        self.assertEqual(self.minta(f"/api/latihan/{latihan['id']}/jawab", {"jawaban": [0]})[0], 400)
        self.assertEqual(self.minta(f"/api/latihan/{latihan['id']}/jawab", {"jawaban": [9] * 20})[0], 400)
        # latihan yang belum selesai tidak masuk riwayat
        _, catatan = self.minta("/api/riwayat")
        self.assertNotIn(latihan["id"], [x["id"] for x in catatan["latihan"]])
        self.assertEqual(self.minta("/../app.py")[0], 404)


if __name__ == "__main__":
    unittest.main()
