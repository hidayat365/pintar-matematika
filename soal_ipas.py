"""Pembangkit soal IPAS SD kelas 4.

Materi mengikuti kisi-kisi Sumatif 2 IPAS kelas 4 dari sekolah:
- Bab 2 "Letak Wilayah pada Peta dan Pemerintahan Daerah": mengenal peta, jenis peta,
  letak astronomis dan geografis, pemerintahan daerah.
- Bab 4 "Gaya di Sekitar Kita": gaya dan pengaruhnya, macam-macam gaya, manfaat gaya,
  pengaruh gaya gesek terhadap gerak benda.

Bentuk soal sama dengan ``soal.py``: dict berisi "teks", "pilihan", "benar",
"pembahasan", ditambah "gambar" (SVG) atau "bacaan" bila ada.
"""

import random
from math import cos, radians, sin

from soal import JUMLAH_SOAL, _svg, angka, fmt, rakit, teks_pilihan

B2 = "Bab 2 · Letak Wilayah pada Peta dan Pemerintahan Daerah"
B4 = "Bab 4 · Gaya di Sekitar Kita"
GAB = "Gabungan"

TOPIK = [
    {"kode": "ipas-peta", "nama": "Mengenal Peta", "ikon": "🗺️", "kelompok": B2,
     "ket": "Pengertian peta, bagian-bagian peta, simbol, skala, mata angin"},
    {"kode": "ipas-jenis-peta", "nama": "Jenis Peta", "ikon": "📍", "kelompok": B2,
     "ket": "Peta umum dan peta khusus"},
    {"kode": "ipas-letak", "nama": "Letak Astronomis dan Geografis", "ikon": "🌐", "kelompok": B2,
     "ket": "Garis lintang dan bujur, batas-batas wilayah"},
    {"kode": "ipas-pemda", "nama": "Pemerintahan Daerah", "ikon": "🏛️", "kelompok": B2,
     "ket": "Struktur, pemimpin, dan tugas pemerintah daerah"},
    {"kode": "ipas-gaya", "nama": "Gaya dan Pengaruhnya", "ikon": "👐", "kelompok": B4,
     "ket": "Pengertian gaya, pengaruh gaya pada bentuk dan gerak benda"},
    {"kode": "ipas-macam-gaya", "nama": "Macam-Macam Gaya", "ikon": "🧲", "kelompok": B4,
     "ket": "Gaya otot, listrik, magnet, pegas, gravitasi, gesek"},
    {"kode": "ipas-manfaat-gaya", "nama": "Manfaat Gaya", "ikon": "🛠️", "kelompok": B4,
     "ket": "Pemanfaatan gaya dalam kehidupan sehari-hari"},
    {"kode": "ipas-gaya-gesek", "nama": "Gaya Gesek dan Gerak Benda", "ikon": "🛞", "kelompok": B4,
     "ket": "Permukaan kasar dan licin, gaya gesek yang menguntungkan dan merugikan"},
    {"kode": "ipas-bab-2", "nama": "Gabungan Bab 2", "ikon": "🗺️", "kelompok": GAB,
     "ket": "Peta, letak wilayah, dan pemerintahan daerah"},
    {"kode": "ipas-bab-4", "nama": "Gabungan Bab 4", "ikon": "⚙️", "kelompok": GAB,
     "ket": "Semua materi gaya"},
    {"kode": "ipas-sumatif-2", "nama": "Latihan Sumatif 2", "ikon": "📝", "kelompok": GAB,
     "ket": "Sesuai kisi-kisi: Bab 2 dan Bab 4"},
]


# ---------------------------------------------------------------- alat bantu

def _k(soal, *kunci):
    """Beri penanda keunikan untuk soal yang teks pertanyaannya bisa sama."""
    soal["kunci"] = kunci
    return soal


def _dari_butir(daftar):
    """Pembangkit dari daftar butir tetap (teks, jawaban, pengecoh, pembahasan)."""
    def buat(r):
        teks, jawab, salah, bahas = r.choice(daftar)
        return teks_pilihan(r, teks, jawab, r.sample(salah, 3), bahas)
    return buat


def _pilih_satu(kelompok, tanya, bahas, hindari=None):
    """Pembangkit "manakah yang termasuk X": satu contoh benar dari ``kelompok[X]``, tiga dari kelompok lain."""
    def buat(r):
        nama = r.choice(list(kelompok))
        benar = r.choice(kelompok[nama])
        lain = [c for n, cs in kelompok.items() if n != nama and n not in (hindari or {}).get(nama, ())
                for c in cs]
        soal = teks_pilihan(r, tanya[nama] if isinstance(tanya, dict) else tanya.format(nama=nama),
                            benar, r.sample(lain, 3), bahas(nama, benar))
        return _k(soal, id(kelompok), nama, benar)
    return buat


def _golongkan(kelompok, tanya, bahas, hindari=None):
    """Pembangkit "contoh ini termasuk apa": jawabannya nama kelompok dari contoh."""
    def buat(r):
        nama = r.choice(list(kelompok))
        contoh = r.choice(kelompok[nama])
        lain = [n for n in kelompok if n != nama and n not in (hindari or {}).get(nama, ())]
        return teks_pilihan(r, tanya.format(contoh=contoh), nama, r.sample(lain, 3), bahas(nama, contoh))
    return buat


def _teks(x, y, isi, ukuran=8, tebal=True, warna="#1d2440", jangkar="middle"):
    bobot = ' font-weight="bold"' if tebal else ""
    return (f'<text x="{x}" y="{y}" font-size="{ukuran}" font-family="sans-serif"{bobot} '
            f'text-anchor="{jangkar}" fill="{warna}" stroke="none">{isi}</text>')


def _tanda(cx, cy):
    """Lingkaran merah bertanda tanya untuk menunjuk bagian gambar."""
    return (f'<circle cx="{cx}" cy="{cy}" r="7" fill="#d6394a" stroke="none"/>'
            + _teks(cx, cy + 3.2, "?", 9, warna="#ffffff"))


# ============================================================ Bab 2 · mengenal peta

BAGIAN = {
    "judul peta": "nama peta yang menunjukkan wilayah atau isi yang digambarkan",
    "mata angin": "petunjuk arah pada peta",
    "skala": "perbandingan antara jarak pada peta dengan jarak sebenarnya",
    "simbol": "tanda atau gambar yang mewakili kenampakan di permukaan bumi",
    "legenda": "keterangan tentang arti simbol-simbol pada peta",
    "garis astronomis": "garis lintang dan garis bujur untuk menentukan letak suatu tempat",
    "inset peta": "peta kecil untuk menunjukkan letak wilayah yang dipetakan di wilayah yang lebih luas",
}


def p_bagian(r):
    nama = r.choice(list(BAGIAN))
    if r.random() < 0.5:
        return teks_pilihan(r, f"Bagian peta yang berupa {BAGIAN[nama]} disebut …", nama,
                            r.sample([n for n in BAGIAN if n != nama], 3),
                            f"{nama.capitalize()} adalah {BAGIAN[nama]}.")
    return teks_pilihan(r, f"Pada peta, {nama} adalah …", BAGIAN[nama],
                        r.sample([d for n, d in BAGIAN.items() if n != nama], 3),
                        f"{nama.capitalize()} adalah {BAGIAN[nama]}.")


_PETA_DASAR = (
    '<rect x="3" y="3" width="214" height="144" fill="none" stroke="#1d2440" stroke-width="1.2"/>'
    + _teks(96, 17, "PETA PULAU CEMARA", 9)
    + '<rect x="12" y="24" width="152" height="100" fill="#cfe8fb" stroke="#1d2440" stroke-width="1"/>'
    + "".join(f'<line x1="{x}" y1="24" x2="{x}" y2="124" stroke="#7a8bb5" stroke-width="0.8" '
              f'stroke-dasharray="3 3"/>' for x in (50, 88, 126))
    + "".join(f'<line x1="12" y1="{y}" x2="164" y2="{y}" stroke="#7a8bb5" stroke-width="0.8" '
              f'stroke-dasharray="3 3"/>' for y in (49, 74, 99))
    + "".join(_teks(x, 121, t, 5.5, False, "#4a5578") for x, t in ((50, "104°BT"), (88, "106°BT"), (126, "108°BT")))
    + "".join(_teks(14, y, t, 5.5, False, "#4a5578", "start") for y, t in ((47, "6°LS"), (72, "7°LS"), (97, "8°LS")))
    + '<path d="M46 72 C48 50 78 40 100 46 C122 52 138 62 136 84 C134 104 108 114 84 110 '
      'C60 106 44 94 46 72 Z" fill="#bfe6c3" stroke="#2f7d3a" stroke-width="1.2"/>'
    + '<polygon points="86,80 94,64 102,80" fill="#8a5a2b" stroke="none"/>'
    + '<circle cx="66" cy="94" r="3" fill="#1d2440" stroke="none"/>'
    + '<path d="M100 80 C108 90 118 96 132 100" stroke="#2f6fde" stroke-width="1.6"/>'
    + '<rect x="136" y="27" width="26" height="20" fill="#ffffff" stroke="#1d2440" stroke-width="0.8"/>'
    + '<path d="M140 40 C142 32 150 30 156 34 C160 38 156 44 148 44 C142 44 139 43 140 40 Z" '
      'fill="#bfe6c3" stroke="none"/>'
    + '<rect x="150" y="35" width="4" height="4" fill="#d6394a" stroke="none"/>'
    + '<line x1="190" y1="50" x2="190" y2="31" stroke="#1d2440" stroke-width="1.5"/>'
    + '<polygon points="186,34 190,25 194,34" fill="#1d2440" stroke="none"/>'
    + _teks(190, 22, "U", 7)
    + '<rect x="170" y="66" width="44" height="58" fill="#ffffff" stroke="#1d2440" stroke-width="0.8"/>'
    + _teks(192, 75, "LEGENDA", 6)
    + '<polygon points="174,89 178,82 182,89" fill="#8a5a2b" stroke="none"/>'
    + _teks(185, 89, "Gunung", 5.5, False, jangkar="start")
    + '<circle cx="178" cy="98" r="2.5" fill="#1d2440" stroke="none"/>'
    + _teks(185, 100, "Kota", 5.5, False, jangkar="start")
    + '<path d="M173 110 C176 107 180 113 183 110" stroke="#2f6fde" stroke-width="1.4"/>'
    + _teks(185, 112, "Sungai", 5.5, False, jangkar="start")
    + '<rect x="174" y="116" width="8" height="5" fill="#bfe6c3" stroke="none"/>'
    + _teks(185, 121, "Daratan", 5.5, False, jangkar="start")
    + '<line x1="18" y1="134" x2="68" y2="134" stroke="#1d2440" stroke-width="1.5"/>'
    + "".join(f'<line x1="{x}" y1="131" x2="{x}" y2="137" stroke="#1d2440" stroke-width="1.2"/>'
              for x in (18, 43, 68))
    + _teks(18, 144, "0", 5.5, False) + _teks(43, 144, "5", 5.5, False) + _teks(68, 144, "10 km", 5.5, False)
)

# bagian: (pusat tanda, ujung garis penunjuk)
_SOROT = {
    "judul peta": ((156, 14), (146, 14)),
    "mata angin": ((206, 42), (194, 39)),
    "skala": ((84, 136), (70, 134)),
    "simbol": ((112, 32), (97, 62)),
    "legenda": ((192, 57), (192, 66)),
    "garis astronomis": ((28, 60), (50, 60)),
    "inset peta": ((122, 31), (136, 34)),
}


def p_gambar_bagian(r):
    nama = r.choice(list(_SOROT))
    (cx, cy), (x2, y2) = _SOROT[nama]
    gambar = (_PETA_DASAR + f'<line x1="{cx}" y1="{cy}" x2="{x2}" y2="{y2}" stroke="#d6394a" '
              f'stroke-width="1.5"/>' + _tanda(cx, cy))
    soal = teks_pilihan(r, "Perhatikan gambar peta. Bagian peta yang ditunjuk tanda tanya merah adalah …",
                        nama, r.sample([n for n in _SOROT if n != nama], 3),
                        f"Bagian itu adalah {nama}, yaitu {BAGIAN[nama]}.")
    soal["gambar"] = _svg(gambar)
    return _k(soal, "bagian-peta", nama)


ARAH = ["utara", "timur laut", "timur", "tenggara", "selatan", "barat daya", "barat", "barat laut"]
_SINGKAT = {"utara": "U", "timur": "T", "selatan": "S", "barat": "B"}


def _arah_lain(r, i):
    """Tiga pengecoh arah: berlawanan dan dua yang bersebelahan."""
    calon = [ARAH[(i + 4) % 8], ARAH[(i + 1) % 8], ARAH[(i - 1) % 8], ARAH[(i + 2) % 8]]
    return r.sample(calon, 3)


def p_kompas(r):
    i = r.randrange(8)
    cx, cy = 110, 75
    isi = ""
    for j in range(8):
        sudut = radians(j * 45)
        panjang = 46 if j % 2 == 0 else 32
        isi += (f'<line x1="{cx}" y1="{cy}" x2="{cx + panjang * sin(sudut):.1f}" '
                f'y2="{cy - panjang * cos(sudut):.1f}" stroke="#1d2440" stroke-width="{2.5 if j % 2 == 0 else 1.5}"/>')
        jarak = 60 if j % 2 == 0 else 44
        x, y = cx + jarak * sin(sudut), cy - jarak * cos(sudut)
        if j == i:
            isi += _tanda(round(x, 1), round(y, 1))
        elif j % 2 == 0:
            isi += _teks(round(x, 1), round(y + 4, 1), _SINGKAT[ARAH[j]], 11)
    isi += f'<circle cx="{cx}" cy="{cy}" r="4" fill="#1d2440" stroke="none"/>'
    soal = teks_pilihan(r, "Perhatikan gambar mata angin. Arah yang ditunjuk tanda tanya adalah …",
                        ARAH[i], _arah_lain(r, i),
                        f"Mata angin delapan arah searah jarum jam: {', '.join(ARAH)}. "
                        f"Yang ditunjuk adalah {ARAH[i]}.")
    soal["gambar"] = _svg(isi)
    return _k(soal, "kompas", i)


def p_arah_teks(r):
    i = r.randrange(8)
    if i % 2 == 1 and r.random() < 0.5:
        a, b = ARAH[i - 1], ARAH[(i + 1) % 8]
        return teks_pilihan(r, f"Arah di antara {a} dan {b} disebut …", ARAH[i], _arah_lain(r, i),
                            f"Di antara {a} dan {b} terdapat arah {ARAH[i]}.")
    j = (i + 4) % 8
    return teks_pilihan(r, f"Arah yang berlawanan dengan {ARAH[i]} adalah …", ARAH[j], _arah_lain(r, j),
                        f"Lawan arah {ARAH[i]} adalah {ARAH[j]}.")


_KOTA = ["Melati", "Mawar", "Anggrek", "Kenanga", "Dahlia", "Cempaka", "Teratai", "Flamboyan"]


def p_arah_kota(r):
    xs, ys = [40, 95, 150], [32, 77, 122]
    while True:
        (a, b), (c, d) = r.sample([(x, y) for x in range(3) for y in range(3)], 2)
        dx, dy = a - c, d - b          # posisi kota pertama dilihat dari kota kedua; ke atas = utara
        if dx == 0 or dy == 0 or abs(dx) == abs(dy):
            break
    sx, sy = (dx > 0) - (dx < 0), (dy > 0) - (dy < 0)
    i = {(0, 1): 0, (1, 1): 1, (1, 0): 2, (1, -1): 3, (0, -1): 4, (-1, -1): 5, (-1, 0): 6, (-1, 1): 7}[(sx, sy)]
    satu, dua = r.sample(_KOTA, 2)
    isi = ('<rect x="10" y="8" width="172" height="134" fill="#eef6e9" stroke="#9aa3c2" stroke-width="1"/>'
           '<line x1="203" y1="50" x2="203" y2="28" stroke="#1d2440" stroke-width="1.5"/>'
           '<polygon points="199,32 203,23 207,32" fill="#1d2440" stroke="none"/>' + _teks(203, 19, "U", 8))
    for (gx, gy), nama in (((a, b), satu), ((c, d), dua)):
        x, y = xs[gx], ys[gy]
        isi += (f'<circle cx="{x}" cy="{y}" r="5" fill="#d6394a" stroke="none"/>'
                + _teks(x, y + 15, f"Kota {nama}", 8))
    soal = teks_pilihan(r, f"Perhatikan peta. Kota {satu} terletak di sebelah … Kota {dua}.", ARAH[i],
                        _arah_lain(r, i),
                        f"Lihat mata angin (U = utara, ke atas). Dari Kota {dua}, Kota {satu} ada di arah {ARAH[i]}.")
    soal["gambar"] = _svg(isi)
    return _k(soal, "arah-kota", a, b, c, d)


_SKALA = [100_000, 200_000, 500_000, 1_000_000]


def p_skala_arti(r):
    s = r.choice(_SKALA)
    km = s // 100_000
    calon = [f"{fmt(km * 10)} km", f"{fmt(km * 100)} km", f"{fmt(s)} km", f"{km} m"]
    return teks_pilihan(r, f"Skala 1 : {fmt(s)} artinya 1 cm pada peta sama dengan … pada jarak sebenarnya.",
                        f"{km} km", r.sample(calon, 3),
                        f"1 cm di peta = {fmt(s)} cm sebenarnya = {fmt(s // 100)} m = {km} km.")


def p_skala_hitung(r):
    s = r.choice(_SKALA[:3])
    per = s // 100_000
    n = r.randint(2, 9)
    hasil = n * per
    return angka(r, f"Pada peta berskala 1 : {fmt(s)}, jarak Kota A ke Kota B adalah {n} cm. "
                    f"Jarak sebenarnya kedua kota itu adalah …", hasil,
                 f"1 cm di peta = {per} km. Jadi {n} cm = {n} × {per} km = {hasil} km.",
                 salah=[hasil * 10, n + per, hasil + per, hasil * 100], satuan=" km", langkah=[1, 2, 5])


_SIMBOL = {
    "gunung": ('<polygon points="80,105 110,45 140,105" fill="#8a5a2b" stroke="none"/>',
               "Segitiga cokelat atau merah melambangkan gunung."),
    "sungai": ('<path d="M30 110 C60 50 95 125 125 70 S175 55 195 35" stroke="#2f6fde" stroke-width="5"/>',
               "Garis biru berkelok-kelok melambangkan sungai."),
    "batas wilayah": ('<line x1="25" y1="75" x2="195" y2="75" stroke="#1d2440" stroke-width="4" '
                      'stroke-dasharray="12 8"/>', "Garis putus-putus melambangkan batas wilayah."),
    "rel kereta api": ('<line x1="25" y1="75" x2="195" y2="75" stroke="#1d2440" stroke-width="4"/>'
                       + "".join(f'<line x1="{x}" y1="66" x2="{x}" y2="84" stroke="#1d2440" stroke-width="3"/>'
                                 for x in range(35, 195, 16)),
                       "Garis hitam dengan garis-garis kecil melintang melambangkan rel kereta api."),
    "danau": ('<path d="M60 75 C60 45 110 40 140 50 C170 60 165 100 130 105 C95 112 60 100 60 75 Z" '
              'fill="#8cc4f5" stroke="#2f6fde" stroke-width="2.5"/>',
              "Daerah berwarna biru yang dikelilingi daratan melambangkan danau."),
    "kota": ('<circle cx="110" cy="75" r="13" fill="#1d2440" stroke="none"/>',
             "Titik atau bulatan hitam melambangkan kota."),
}


def p_simbol(r):
    nama = r.choice(list(_SIMBOL))
    gambar, bahas = _SIMBOL[nama]
    soal = teks_pilihan(r, "Simbol pada gambar biasanya digunakan pada peta untuk menunjukkan …", nama,
                        r.sample([n for n in _SIMBOL if n != nama], 3), bahas)
    soal["gambar"] = _svg('<rect x="10" y="10" width="200" height="130" fill="#f7faf5" stroke="#9aa3c2" '
                          'stroke-width="1"/>' + gambar)
    return _k(soal, "simbol", nama)


_PETA = [
    ("Gambaran permukaan bumi pada bidang datar yang diperkecil dengan skala tertentu disebut …", "peta",
     ["globe", "atlas", "denah", "kompas"],
     "Peta adalah gambaran permukaan bumi (seluruh atau sebagian) pada bidang datar yang diperkecil dengan skala tertentu."),
    ("Tiruan bumi yang berbentuk bola disebut …", "globe", ["peta", "atlas", "kompas"],
     "Globe adalah tiruan bumi berbentuk bola yang diperkecil."),
    ("Kumpulan peta yang disusun menjadi sebuah buku disebut …", "atlas", ["globe", "denah", "kompas"],
     "Atlas adalah kumpulan peta yang dibukukan."),
    ("Orang yang ahli membuat peta disebut …", "kartografer", ["arsitek", "astronot", "petani"],
     "Pembuat peta disebut kartografer, sedangkan ilmunya disebut kartografi."),
    ("Peta digambar pada bidang yang …", "datar", ["bulat", "melengkung", "berbentuk bola"],
     "Peta digambar pada bidang datar, misalnya kertas. Tiruan bumi berbentuk bola disebut globe."),
    ("Ukuran wilayah pada peta dibuat … daripada ukuran sebenarnya.", "lebih kecil",
     ["lebih besar", "sama besar", "dua kali lebih besar"],
     "Peta adalah gambar permukaan bumi yang diperkecil dengan skala tertentu."),
    ("Pada peta, arah utara biasanya berada di bagian … peta.", "atas", ["bawah", "kiri", "kanan"],
     "Pada umumnya arah utara pada peta berada di bagian atas."),
    ("Matahari terbit dari arah …", "timur", ["barat", "utara", "selatan"],
     "Matahari terbit di timur dan terbenam di barat."),
    ("Matahari terbenam di arah …", "barat", ["timur", "utara", "selatan"],
     "Matahari terbit di timur dan terbenam di barat."),
    ("Mata angin utama ada empat, yaitu …", "utara, timur, selatan, dan barat",
     ["timur laut, tenggara, barat daya, dan barat laut", "utara, timur laut, timur, dan tenggara",
      "kiri, kanan, atas, dan bawah"],
     "Empat arah utama adalah utara, timur, selatan, dan barat. Di antaranya ada empat arah lain."),
    ("Alat yang digunakan untuk menunjukkan arah mata angin adalah …", "kompas",
     ["termometer", "jam dinding", "penggaris"], "Kompas digunakan untuk menunjukkan arah mata angin."),
    ("Warna biru pada peta menunjukkan …", "perairan, seperti laut, danau, dan sungai",
     ["dataran rendah", "dataran tinggi", "pegunungan"], "Warna biru pada peta menunjukkan perairan."),
    ("Warna hijau pada peta menunjukkan …", "dataran rendah",
     ["laut dalam", "pegunungan", "dataran tinggi"], "Warna hijau pada peta menunjukkan dataran rendah."),
    ("Warna kuning pada peta biasanya menunjukkan …", "dataran tinggi",
     ["laut dangkal", "sungai", "dataran rendah"], "Warna kuning pada peta menunjukkan dataran tinggi."),
    ("Warna cokelat pada peta menunjukkan …", "pegunungan",
     ["laut", "dataran rendah", "danau"], "Warna cokelat pada peta menunjukkan daerah pegunungan."),
    ("Pada peta, laut yang dalam digambarkan dengan warna biru …", "tua", ["muda", "kehijauan", "keputihan"],
     "Makin dalam lautnya, makin tua warna birunya. Laut dangkal berwarna biru muda."),
    ("Skala yang ditulis dengan angka, misalnya 1 : 100.000, disebut skala …", "angka",
     ["garis", "warna", "simbol"], "Skala yang ditulis dengan angka perbandingan disebut skala angka."),
    ("Skala yang digambar berupa garis yang dibagi menjadi beberapa bagian disebut skala …", "garis",
     ["angka", "warna", "titik"], "Skala yang berupa garis dengan keterangan jarak disebut skala garis."),
    ("Simbol berupa garis pada peta dapat menunjukkan …", "sungai, jalan, atau batas wilayah",
     ["puncak gunung", "letak kota", "luas danau"],
     "Simbol garis dipakai untuk sungai, jalan, rel kereta api, dan batas wilayah."),
    ("Simbol berupa titik atau bulatan kecil pada peta biasanya menunjukkan …", "kota",
     ["sungai", "jalan raya", "laut"], "Titik atau bulatan kecil pada peta biasanya menunjukkan kota."),
    ("Untuk mengetahui arti simbol-simbol pada peta, kita melihat …", "legenda",
     ["judul peta", "skala", "inset peta"], "Legenda berisi keterangan arti simbol-simbol pada peta."),
    ("Untuk mengetahui jarak sebenarnya antara dua tempat pada peta, kita memerlukan …", "skala",
     ["legenda", "judul peta", "simbol"], "Skala adalah perbandingan jarak pada peta dengan jarak sebenarnya."),
    ("Untuk mengetahui wilayah yang digambarkan pada peta, kita membaca …", "judul peta",
     ["legenda", "skala", "inset peta"], "Judul peta menunjukkan wilayah atau isi yang digambarkan."),
    ("Untuk menentukan letak astronomis suatu tempat pada peta, kita menggunakan …", "garis astronomis",
     ["legenda", "judul peta", "skala"], "Garis astronomis terdiri atas garis lintang dan garis bujur."),
    ("Untuk mengetahui arah suatu tempat pada peta, kita melihat …", "mata angin",
     ["legenda", "skala", "judul peta"], "Mata angin adalah petunjuk arah pada peta."),
    ("Judul peta biasanya diletakkan di bagian … peta.", "atas", ["bawah", "dalam legenda", "dalam inset"],
     "Judul peta biasanya berada di bagian atas tengah peta."),
    ("Judul peta biasanya ditulis dengan huruf …", "kapital (huruf besar)",
     ["miring kecil", "sambung", "kecil semua"], "Judul peta biasanya ditulis dengan huruf kapital."),
    ("Peta kecil yang terdapat di dalam peta utama disebut …", "inset peta",
     ["legenda", "skala", "judul peta"],
     "Inset peta adalah peta kecil yang menunjukkan letak wilayah yang dipetakan di wilayah yang lebih luas."),
]


# ============================================================= Bab 2 · jenis peta

PETA_JENIS = {
    "peta umum": ["peta Indonesia", "peta dunia", "peta Provinsi Jawa Barat", "peta Pulau Kalimantan",
                  "peta Asia Tenggara", "peta wilayah Kabupaten Bandung",
                  "peta yang menggambarkan gunung, sungai, jalan, dan kota", "peta wilayah sebuah kecamatan"],
    "peta khusus": ["peta persebaran flora di Indonesia", "peta persebaran fauna di Indonesia",
                    "peta curah hujan", "peta tempat wisata di Pulau Bali", "peta persebaran hasil tambang",
                    "peta persebaran penduduk", "peta jalur kereta api", "peta daerah rawan banjir",
                    "peta persebaran hasil pertanian"],
}


def p_golong_peta(r):
    nama = r.choice(list(PETA_JENIS))
    contoh = r.choice(PETA_JENIS[nama])
    lain = "peta khusus" if nama == "peta umum" else "peta umum"
    alasan = ("menampilkan informasi umum suatu wilayah" if nama == "peta umum"
              else "memberikan informasi tertentu (khusus)")
    return teks_pilihan(r, f"{contoh.capitalize()} termasuk jenis …", nama, [lain, "globe", "denah"],
                        f"{contoh.capitalize()} {alasan}, jadi termasuk {nama}.")


p_contoh_peta = _pilih_satu(
    PETA_JENIS, "Berikut ini yang merupakan contoh {nama} adalah …",
    lambda nama, benar: f"{benar.capitalize()} termasuk {nama}. "
                        + ("Peta umum menampilkan informasi umum suatu wilayah."
                           if nama == "peta umum" else "Peta khusus memberikan informasi tertentu."))

BENTANG = {
    "bentang alam": ["gunung", "sungai", "danau", "laut", "pantai", "lembah"],
    "bentang buatan": ["jalan raya", "bendungan", "pelabuhan", "bandara", "rel kereta api", "jembatan"],
}
p_bentang = _pilih_satu(
    BENTANG, {"bentang alam": "Berikut ini yang termasuk bentang alam adalah …",
              "bentang buatan": "Berikut ini yang termasuk bentang buatan (dibuat oleh manusia) adalah …"},
    lambda nama, benar: f"{benar.capitalize()} termasuk {nama}. "
                        + ("Bentang alam terbentuk secara alami." if nama == "bentang alam"
                           else "Bentang buatan dibuat oleh manusia."))

_JENIS = [
    ("Peta yang menampilkan informasi umum suatu wilayah, seperti bentang alam dan bentang buatan, disebut …",
     "peta umum", ["peta khusus", "denah", "globe"],
     "Peta umum menampilkan informasi umum suatu wilayah, misalnya gunung, sungai, jalan, kota, dan provinsi."),
    ("Peta yang memberikan informasi tertentu tentang kenampakan di permukaan bumi, misalnya persebaran "
     "flora dan fauna, disebut …", "peta khusus", ["peta umum", "atlas", "denah"],
     "Peta khusus memberikan informasi tertentu, seperti persebaran flora, fauna, curah hujan, dan tempat wisata."),
    ("Nama lain dari peta khusus adalah peta …", "tematik", ["dunia", "topografi", "provinsi"],
     "Peta khusus disebut juga peta tematik karena membahas satu tema tertentu."),
    ("Peta umum menggambarkan bentang alam dan bentang …", "buatan", ["hewan", "cuaca", "udara"],
     "Peta umum menggambarkan bentang alam (gunung, sungai) dan bentang buatan (jalan, kota)."),
    ("Peta yang menunjukkan banyaknya hujan yang turun di berbagai daerah disebut peta …", "curah hujan",
     ["persebaran flora", "wisata", "persebaran fauna"], "Peta curah hujan menunjukkan banyaknya hujan di suatu daerah."),
    ("Peta yang menunjukkan tempat hidup hewan-hewan di suatu wilayah disebut peta …", "persebaran fauna",
     ["persebaran flora", "curah hujan", "wisata"], "Fauna adalah dunia hewan."),
    ("Peta yang menunjukkan tempat tumbuh berbagai jenis tumbuhan disebut peta …", "persebaran flora",
     ["persebaran fauna", "curah hujan", "wisata"], "Flora adalah dunia tumbuhan."),
    ("Peta yang menunjukkan letak pantai, museum, dan tempat rekreasi disebut peta …", "wisata",
     ["curah hujan", "persebaran fauna", "persebaran flora"], "Peta wisata menunjukkan letak tempat-tempat wisata."),
    ("Keluarga Dina ingin berlibur dan mencari letak tempat rekreasi di Yogyakarta. Peta yang paling tepat "
     "digunakan adalah …", "peta wisata", ["peta curah hujan", "peta persebaran fauna", "peta persebaran flora"],
     "Peta wisata menunjukkan letak tempat-tempat rekreasi."),
    ("Pak Tani ingin mengetahui daerah yang paling banyak turun hujan. Peta yang tepat digunakan adalah …",
     "peta curah hujan", ["peta wisata", "peta persebaran fauna", "peta persebaran flora"],
     "Peta curah hujan menunjukkan banyaknya hujan yang turun di suatu daerah."),
    ("Siswa ingin mengetahui daerah tempat hidup orang utan dan komodo. Peta yang tepat digunakan adalah …",
     "peta persebaran fauna", ["peta persebaran flora", "peta curah hujan", "peta wisata"],
     "Orang utan dan komodo adalah hewan (fauna)."),
    ("Bunga Rafflesia arnoldii tumbuh di Bengkulu. Informasi ini dapat ditemukan pada peta …",
     "persebaran flora", ["persebaran fauna", "curah hujan", "jalur kereta api"],
     "Rafflesia adalah tumbuhan (flora)."),
    ("Peta yang menggambarkan wilayah kabupaten, kota, dan provinsi beserta gunung dan sungainya termasuk …",
     "peta umum", ["peta khusus", "peta wisata", "peta curah hujan"],
     "Peta yang menampilkan informasi umum suatu wilayah termasuk peta umum."),
    ("Peta khusus berguna untuk …", "memberikan informasi tertentu tentang suatu wilayah",
     ["menggambarkan bumi dalam bentuk bola", "menunjukkan arti simbol pada peta", "mengukur suhu udara"],
     "Peta khusus memberikan informasi tertentu, misalnya curah hujan atau persebaran hewan."),
]


# =============================================== Bab 2 · letak astronomis dan geografis

def _lintang(v):
    return "0°" if v == 0 else f"{abs(v)}° {'LU' if v > 0 else 'LS'}"


def p_grid(r):
    b0 = r.choice([96, 100, 104, 106, 110, 114, 120, 126, 130])
    bujur = [b0 + 2 * i for i in range(4)]
    awal = r.choice([6, 4, 2, 0, -2])                     # lintang baris teratas
    lintang = [awal - 2 * i for i in range(4)]
    xs, ys = [60, 100, 140, 180], [37, 67, 97, 127]
    baris = r.choice([i for i, v in enumerate(lintang) if v != 0])
    kolom = r.randrange(4)
    isi = '<rect x="40" y="22" width="170" height="120" fill="#eef6fd" stroke="#9aa3c2" stroke-width="1"/>'
    for x, b in zip(xs, bujur):
        isi += (f'<line x1="{x}" y1="22" x2="{x}" y2="142" stroke="#7a8bb5" stroke-width="1"/>'
                + _teks(x, 16, f"{b}°BT", 7, False))
    for y, v in zip(ys, lintang):
        warna = "#d6394a" if v == 0 else "#7a8bb5"
        isi += (f'<line x1="40" y1="{y}" x2="210" y2="{y}" stroke="{warna}" stroke-width="{1.6 if v == 0 else 1}"/>'
                + _teks(36, y + 3, _lintang(v).replace(" ", ""), 7, False, jangkar="end"))
    x, y = xs[kolom], ys[baris]
    isi += f'<circle cx="{x}" cy="{y}" r="5" fill="#d6394a" stroke="none"/>' + _teks(x + 10, y - 6, "A", 10)
    v, b = lintang[baris], bujur[kolom]
    jawab = f"{_lintang(v)} dan {b}° BT"
    lain = {f"{_lintang(-v)} dan {b}° BT", f"{_lintang(v)} dan {b}° BB"}
    lain |= {f"{_lintang(v)} dan {c}° BT" for c in bujur if c != b}
    lain |= {f"{_lintang(w)} dan {b}° BT" for w in lintang if w not in (v, 0)}
    soal = teks_pilihan(r, "Perhatikan gambar garis lintang dan garis bujur. Titik A terletak pada …", jawab,
                        r.sample(sorted(lain - {jawab}), 3),
                        f"Garis mendatar adalah garis lintang dan garis tegak adalah garis bujur. "
                        f"Titik A berada pada {_lintang(v)} dan {b}° BT.")
    soal["gambar"] = _svg(isi)
    return _k(soal, "grid", b0, awal, baris, kolom)


_DAERAH = ["Kabupaten Tunas Jaya", "Kota Pelita", "Kabupaten Bukit Hijau", "Kota Taman Sari"]
_TETANGGA = ["Kabupaten Sinar Harapan", "Kota Mekar Asri", "Kabupaten Lembah Damai", "Kabupaten Gunung Indah",
             "Kota Tirta Jaya", "Kabupaten Sawah Luas", "Laut Biru", "Kabupaten Padi Kuning"]


def _bacaan_batas(r):
    daerah = r.choice(_DAERAH)
    utara, timur, selatan, barat = r.sample(_TETANGGA, 4)
    a, b = r.randint(5, 8), r.randint(105, 112)
    k = [f"{daerah} terletak di antara {a}° LS – {a + 1}° LS dan {b}° BT – {b + 1}° BT.",
         f"Di sebelah utara, {daerah} berbatasan dengan {utara}.",
         f"Di sebelah timur berbatasan dengan {timur}.",
         f"Di sebelah selatan berbatasan dengan {selatan}.",
         f"Di sebelah barat berbatasan dengan {barat}."]
    bacaan = " ".join(k) + " (Daerah ini hanya contoh.)"
    batas = list(dict.fromkeys([utara, timur, selatan, barat] + _TETANGGA))
    hasil = []
    for arah, nama, kalimat in (("utara", utara, k[1]), ("timur", timur, k[2]),
                                ("selatan", selatan, k[3]), ("barat", barat, k[4])):
        hasil.append((f"Di sebelah {arah}, {daerah} berbatasan dengan …", nama,
                      [n for n in batas[:4] if n != nama] + [batas[4]], f'Lihat kalimat: "{kalimat}"'))
    hasil += [
        (f'Kalimat "{k[0][:-1]}" menunjukkan letak … {daerah}.', "astronomis",
         ["geografis", "strategis", "ekonomis"], "Letak berdasarkan garis lintang dan bujur disebut letak astronomis."),
        (f"Keterangan tentang daerah-daerah yang berbatasan dengan {daerah} menunjukkan letak …", "geografis",
         ["astronomis", "strategis", "ekonomis"],
         "Letak berdasarkan batas-batas wilayah di permukaan bumi disebut letak geografis."),
        (f"{daerah} berada di sebelah … garis khatulistiwa.", "selatan", ["utara", "timur", "barat"],
         f"{daerah} terletak pada garis lintang selatan (LS), jadi berada di selatan khatulistiwa."),
    ]
    return [(bacaan, *h) for h in hasil]


def p_batas(r):
    if not hasattr(r, "_bacaan_batas_ipas"):
        r._bacaan_batas_ipas = _bacaan_batas(r)
    bacaan, teks, jawab, salah, bahas = r.choice(r._bacaan_batas_ipas)
    soal = teks_pilihan(r, teks, jawab, r.sample(salah, 3), bahas)
    soal["bacaan"] = bacaan
    return soal


def p_pernyataan(r):
    a, b = r.randint(1, 9), r.randint(96, 139)
    astro = [f"terletak di antara {a}° LS – {a + 1}° LS", f"berada pada {a}° LU dan {b}° BT",
             f"terletak di antara {b}° BT – {b + 1}° BT", "dilalui garis khatulistiwa (garis lintang 0°)"]
    geo = ["di sebelah utara berbatasan dengan Laut Jawa", "di sebelah selatan berbatasan dengan Samudra Hindia",
           "terletak di antara Benua Asia dan Benua Australia", "di sebelah timur berbatasan dengan kabupaten tetangga",
           "terletak di antara Samudra Hindia dan Samudra Pasifik", "di sebelah barat berbatasan dengan Selat Sunda"]
    if r.random() < 0.5:
        benar = r.choice(astro)
        soal = teks_pilihan(r, "Pernyataan berikut yang menunjukkan letak astronomis suatu wilayah adalah …",
                            benar, r.sample(geo, 3), "Letak astronomis ditentukan dengan garis lintang dan bujur.")
    else:
        benar = r.choice(geo)
        soal = teks_pilihan(r, "Pernyataan berikut yang menunjukkan letak geografis suatu wilayah adalah …",
                            benar, r.sample(astro, 3),
                            "Letak geografis ditentukan oleh batas-batas wilayah di permukaan bumi.")
    return _k(soal, "pernyataan", benar[:20])


_LETAK = [
    ("Letak suatu tempat berdasarkan garis lintang dan garis bujur disebut letak …", "astronomis",
     ["geografis", "strategis", "ekonomis"], "Letak astronomis ditentukan dengan garis lintang dan garis bujur."),
    ("Letak suatu tempat berdasarkan kenyataannya di permukaan bumi, yaitu batas-batasnya dengan wilayah "
     "lain, disebut letak …", "geografis", ["astronomis", "strategis", "ekonomis"],
     "Letak geografis ditentukan oleh batas-batas wilayah di permukaan bumi."),
    ("Garis khayal yang melingkari bumi secara mendatar dan sejajar dengan khatulistiwa disebut garis …",
     "lintang", ["bujur", "tepi", "batas"], "Garis lintang adalah garis khayal mendatar yang sejajar khatulistiwa."),
    ("Garis khayal yang menghubungkan kutub utara dan kutub selatan bumi disebut garis …", "bujur",
     ["lintang", "tepi", "batas"], "Garis bujur adalah garis khayal tegak dari kutub utara ke kutub selatan."),
    ("Garis lintang 0° disebut juga garis …", "khatulistiwa (ekuator)", ["bujur", "kutub", "batas"],
     "Garis lintang 0° adalah khatulistiwa atau ekuator yang membagi bumi menjadi belahan utara dan selatan."),
    ("Garis bujur 0° melewati kota Greenwich di negara …", "Inggris", ["Indonesia", "Belanda", "Jepang"],
     "Garis bujur 0° melewati kota Greenwich di Inggris."),
    ("LS adalah singkatan dari …", "Lintang Selatan", ["Laut Selatan", "Lintang Sejajar", "Letak Samudra"],
     "LU = Lintang Utara, LS = Lintang Selatan, BT = Bujur Timur, BB = Bujur Barat."),
    ("BT adalah singkatan dari …", "Bujur Timur", ["Batas Timur", "Bujur Tengah", "Benua Timur"],
     "LU = Lintang Utara, LS = Lintang Selatan, BT = Bujur Timur, BB = Bujur Barat."),
    ("Letak astronomis Indonesia adalah …", "6° LU – 11° LS dan 95° BT – 141° BT",
     ["6° LS – 11° LU dan 95° BT – 141° BT", "6° LU – 11° LS dan 95° BB – 141° BB",
      "11° LU – 6° LS dan 95° BT – 141° BT"],
     "Indonesia terletak di antara 6° LU – 11° LS dan 95° BT – 141° BT."),
    ("Karena dilalui garis khatulistiwa, Indonesia memiliki iklim …", "tropis", ["dingin", "gurun", "kutub"],
     "Daerah di sekitar khatulistiwa beriklim tropis."),
    ("Di Indonesia yang beriklim tropis terdapat dua musim, yaitu …", "musim hujan dan musim kemarau",
     ["musim dingin dan musim panas", "musim semi dan musim gugur", "musim salju dan musim hujan"],
     "Iklim tropis memiliki musim hujan dan musim kemarau."),
    ("Secara geografis, Indonesia terletak di antara dua benua, yaitu …", "Benua Asia dan Benua Australia",
     ["Benua Asia dan Benua Afrika", "Benua Eropa dan Benua Australia", "Benua Amerika dan Benua Asia"],
     "Indonesia terletak di antara Benua Asia dan Benua Australia."),
    ("Secara geografis, Indonesia juga terletak di antara dua samudra, yaitu …",
     "Samudra Hindia dan Samudra Pasifik",
     ["Samudra Atlantik dan Samudra Pasifik", "Samudra Hindia dan Samudra Atlantik",
      "Samudra Arktik dan Samudra Hindia"], "Indonesia terletak di antara Samudra Hindia dan Samudra Pasifik."),
    ("Kota di Indonesia yang dilalui garis khatulistiwa dan memiliki Tugu Khatulistiwa adalah …", "Pontianak",
     ["Jakarta", "Surabaya", "Makassar"], "Tugu Khatulistiwa berada di Pontianak, Kalimantan Barat."),
    ("Daerah yang terletak di sebelah selatan garis khatulistiwa berada pada garis lintang …",
     "selatan (LS)", ["utara (LU)", "timur (BT)", "barat (BB)"],
     "Daerah di selatan khatulistiwa berada pada Lintang Selatan (LS)."),
    ("Pulau Jawa terletak di sebelah … garis khatulistiwa.", "selatan", ["utara", "timur", "barat"],
     "Seluruh Pulau Jawa berada pada Lintang Selatan."),
    ("Seluruh wilayah Indonesia berada di sebelah … garis bujur 0°.", "timur", ["barat", "utara", "selatan"],
     "Indonesia terletak pada 95° BT – 141° BT, yaitu di sebelah timur garis bujur 0°."),
    ("Letak geografis suatu kabupaten dapat diketahui dari …", "batas-batas wilayahnya dengan daerah lain",
     ["garis lintang dan garis bujurnya", "jumlah penduduknya", "nama bupatinya"],
     "Letak geografis dilihat dari batas-batas wilayah di permukaan bumi."),
    ("Letak astronomis suatu kota dapat diketahui dari …", "garis lintang dan garis bujurnya",
     ["batas-batas wilayahnya", "jumlah sekolahnya", "nama wali kotanya"],
     "Letak astronomis dilihat dari garis lintang dan garis bujur."),
]


# ======================================================== Bab 2 · pemerintahan daerah

PEMIMPIN = [("provinsi", "gubernur"), ("kabupaten", "bupati"), ("kota", "wali kota"), ("kecamatan", "camat"),
            ("kelurahan", "lurah"), ("desa", "kepala desa"), ("rukun warga (RW)", "ketua RW"),
            ("rukun tetangga (RT)", "ketua RT")]


def p_pemimpin(r):
    wilayah, pemimpin = r.choice(PEMIMPIN)
    if r.random() < 0.5:
        return teks_pilihan(r, f"Wilayah {wilayah} dipimpin oleh …", pemimpin,
                            r.sample([p for _, p in PEMIMPIN if p != pemimpin], 3),
                            f"Pemimpin {wilayah} adalah {pemimpin}.")
    return teks_pilihan(r, f"{pemimpin.capitalize()} adalah pemimpin wilayah …", wilayah,
                        r.sample([w for w, _ in PEMIMPIN if w != wilayah], 3),
                        f"Pemimpin {wilayah} adalah {pemimpin}.")


_TINGKAT = ["provinsi", "kabupaten/kota", "kecamatan", "desa/kelurahan", "RW", "RT"]


def p_urutan(r):
    if r.random() < 0.6:
        i = r.randint(1, 4)
        return teks_pilihan(r, f"Wilayah yang lebih kecil dari {_TINGKAT[i - 1]}, tetapi lebih luas dari "
                               f"{_TINGKAT[i + 1]} adalah …", _TINGKAT[i],
                            r.sample([t for t in _TINGKAT if t != _TINGKAT[i]], 3),
                            "Urutan wilayah dari yang terluas: " + " – ".join(_TINGKAT) + ".")
    empat = _TINGKAT[:4]
    luas = r.random() < 0.5
    benar = empat if luas else empat[::-1]
    salah = set()
    while len(salah) < 3:
        acak = r.sample(empat, 4)
        if acak != benar:
            salah.add(" – ".join(acak))
    return teks_pilihan(r, f"Urutan wilayah pemerintahan dari yang paling {'luas' if luas else 'kecil'} adalah …",
                        " – ".join(benar), sorted(salah),
                        "Urutan wilayah dari yang terluas: " + " – ".join(_TINGKAT) + ".")


_LAYANAN = [
    ("Ayah ingin membuat kartu keluarga (KK) yang baru. Ayah dapat mengurusnya di …",
     "Dinas Kependudukan dan Pencatatan Sipil"),
    ("Ibu ingin mengurus akta kelahiran adik. Ibu dapat mengurusnya di …", "Dinas Kependudukan dan Pencatatan Sipil"),
    ("Puskesmas dan rumah sakit daerah diurus oleh …", "Dinas Kesehatan"),
    ("Sekolah-sekolah negeri di kabupaten atau kota diurus oleh …", "Dinas Pendidikan"),
    ("Lampu lalu lintas dan angkutan umum di daerah diatur oleh …", "Dinas Perhubungan"),
    ("Sampah dan kebersihan lingkungan di daerah diurus oleh …", "Dinas Lingkungan Hidup"),
    ("Jika terjadi kebakaran, warga dapat meminta bantuan …", "Dinas Pemadam Kebakaran"),
    ("Petani yang membutuhkan bibit unggul dan penyuluhan dibantu oleh …", "Dinas Pertanian"),
    ("Pedagang yang berjualan di trotoar dan melanggar peraturan daerah ditertibkan oleh …",
     "Satuan Polisi Pamong Praja (Satpol PP)"),
]


def p_layanan(r):
    teks, jawab = r.choice(_LAYANAN)
    lain = sorted({j for _, j in _LAYANAN if j != jawab})
    return teks_pilihan(r, teks, jawab, r.sample(lain, 3), f"Urusan itu ditangani oleh {jawab}.")


TUGAS = {
    "pemerintah daerah": ["membangun dan memperbaiki jalan di daerahnya", "membangun sekolah dan puskesmas",
                          "mengurus kebersihan dan sampah", "melayani pembuatan KTP dan akta kelahiran",
                          "membangun dan merawat pasar tradisional", "menjaga ketertiban umum di daerahnya"],
    "pemerintah pusat": ["mencetak dan mengatur uang rupiah", "mengatur hubungan dengan negara lain",
                         "mengatur pertahanan negara", "mengatur urusan peradilan"],
}
p_tugas = _pilih_satu(
    TUGAS, "Berikut ini yang merupakan tugas {nama} adalah …",
    lambda nama, benar: f"{benar.capitalize()} adalah tugas {nama}. Urusan uang, hubungan luar negeri, "
                        f"pertahanan, dan peradilan diatur oleh pemerintah pusat.")

_PEMDA = [
    ("Gubernur, bupati, dan wali kota dipilih melalui …", "pemilihan kepala daerah (pilkada) oleh rakyat",
     ["penunjukan oleh kepala sekolah", "undian di kantor kecamatan", "pemilihan oleh ketua RT"],
     "Kepala daerah dipilih langsung oleh rakyat melalui pilkada."),
    ("Masa jabatan gubernur, bupati, dan wali kota adalah … tahun.", "5", ["3", "10", "2"],
     "Masa jabatan kepala daerah adalah 5 tahun."),
    ("Kepala desa dipilih oleh …", "warga desa melalui pemilihan kepala desa (pilkades)",
     ["bupati", "camat", "gubernur"], "Kepala desa dipilih langsung oleh warga desa."),
    ("Camat diangkat oleh …", "bupati atau wali kota", ["warga kecamatan", "ketua RT", "kepala desa"],
     "Camat tidak dipilih warga, tetapi diangkat oleh bupati atau wali kota."),
    ("Lurah diangkat oleh …", "bupati atau wali kota", ["warga kelurahan melalui pemilihan", "ketua RW", "kepala desa"],
     "Lurah diangkat oleh bupati atau wali kota, berbeda dengan kepala desa yang dipilih warga."),
    ("Ketua RT dipilih oleh …", "warga RT itu sendiri", ["gubernur", "bupati", "camat"],
     "Ketua RT dipilih oleh warga di lingkungan RT tersebut."),
    ("DPRD adalah singkatan dari …", "Dewan Perwakilan Rakyat Daerah",
     ["Dinas Pembangunan Rakyat Daerah", "Dewan Pemimpin Rakyat Desa", "Dinas Pelayanan Rakyat Daerah"],
     "DPRD = Dewan Perwakilan Rakyat Daerah."),
    ("Lembaga yang bersama kepala daerah membuat peraturan daerah adalah …", "DPRD",
     ["Satpol PP", "puskesmas", "Dinas Perhubungan"], "Peraturan daerah dibuat oleh DPRD bersama kepala daerah."),
    ("Peraturan yang dibuat oleh kepala daerah bersama DPRD disebut …", "peraturan daerah (perda)",
     ["undang-undang dasar", "peraturan desa", "tata tertib sekolah"],
     "Peraturan daerah (perda) dibuat oleh kepala daerah bersama DPRD."),
    ("Anggota DPRD dipilih oleh rakyat melalui …", "pemilihan umum (pemilu)",
     ["penunjukan bupati", "undian", "pemilihan kepala desa"], "Anggota DPRD dipilih oleh rakyat melalui pemilu."),
    ("Penyelenggara pemerintahan daerah adalah kepala daerah dan …", "DPRD",
     ["ketua RT", "kepala sekolah", "Satpol PP"], "Pemerintahan daerah dijalankan oleh kepala daerah bersama DPRD."),
    ("Dalam menjalankan tugasnya, gubernur dibantu oleh …", "wakil gubernur", ["wakil bupati", "camat", "lurah"],
     "Gubernur dibantu oleh wakil gubernur."),
    ("Dalam menjalankan tugasnya, bupati dibantu oleh …", "wakil bupati", ["wakil gubernur", "lurah", "ketua RW"],
     "Bupati dibantu oleh wakil bupati."),
    ("Dalam menjalankan tugasnya, wali kota dibantu oleh …", "wakil wali kota", ["wakil gubernur", "ketua RT", "kepala desa"],
     "Wali kota dibantu oleh wakil wali kota."),
    ("Lembaga desa yang bersama kepala desa membuat peraturan desa adalah …",
     "Badan Permusyawaratan Desa (BPD)", ["DPRD provinsi", "Satpol PP", "puskesmas"],
     "Peraturan desa dibuat oleh kepala desa bersama BPD."),
    ("Kabupaten dan kota merupakan bagian dari wilayah …", "provinsi", ["kecamatan", "desa", "RT"],
     "Provinsi terbagi menjadi kabupaten dan kota."),
    ("Kecamatan merupakan bagian dari wilayah …", "kabupaten atau kota", ["desa", "kelurahan", "RW"],
     "Kabupaten atau kota terbagi menjadi kecamatan."),
    ("Saat ini Indonesia terdiri atas … provinsi.", "38", ["34", "27", "45"], "Indonesia memiliki 38 provinsi."),
    ("Perbedaan desa dan kelurahan adalah …",
     "kepala desa dipilih oleh warga, sedangkan lurah diangkat oleh bupati atau wali kota",
     ["lurah dipilih oleh warga, sedangkan kepala desa diangkat oleh presiden",
      "desa dipimpin camat, sedangkan kelurahan dipimpin gubernur",
      "desa lebih luas daripada provinsi"],
     "Kepala desa dipilih warga desa, sedangkan lurah diangkat oleh bupati atau wali kota."),
    ("Tugas Satpol PP adalah …", "menegakkan peraturan daerah dan menjaga ketertiban umum",
     ["membuat undang-undang", "mengajar di sekolah", "memimpin provinsi"],
     "Satuan Polisi Pamong Praja (Satpol PP) menegakkan perda dan menjaga ketertiban umum."),
    ("Sikap yang baik terhadap peraturan daerah adalah …", "menaatinya, misalnya membuang sampah pada tempatnya",
     ["melanggarnya jika tidak ada petugas", "mengabaikannya", "merusak fasilitas umum"],
     "Sebagai warga yang baik, kita menaati peraturan daerah."),
    ("Selain memimpin provinsi, gubernur juga berperan sebagai wakil pemerintah … di daerah.", "pusat",
     ["desa", "kecamatan", "RT"], "Gubernur juga menjadi wakil pemerintah pusat di daerah."),
    ("Pemerintah daerah membangun puskesmas agar …", "warga mudah mendapatkan layanan kesehatan",
     ["warga mudah membeli mainan", "jalan menjadi lebih lebar", "sekolah libur lebih lama"],
     "Puskesmas memberikan layanan kesehatan kepada warga."),
    ("Wilayah kabupaten umumnya …", "lebih luas dan banyak daerah perdesaan",
     ["lebih sempit dan penuh gedung tinggi", "tidak memiliki kecamatan", "dipimpin oleh wali kota"],
     "Kabupaten umumnya lebih luas dengan banyak perdesaan, sedangkan kota berupa daerah perkotaan."),
]


# ======================================================== Bab 4 · gaya dan pengaruhnya

PENGARUH = {
    "benda diam menjadi bergerak": [
        "Bola yang diam di lapangan ditendang hingga menggelinding",
        "Meja yang diam didorong hingga berpindah tempat",
        "Kelereng yang diam disentil hingga bergerak",
        "Mobil mainan yang diam ditarik dengan tali hingga berjalan",
        "Ayunan yang diam didorong hingga berayun"],
    "benda bergerak menjadi diam": [
        "Kiper menangkap bola yang melaju ke arah gawang",
        "Sepeda yang melaju direm hingga berhenti",
        "Bola yang menggelinding ditahan dengan kaki",
        "Andi menahan troli belanja yang meluncur hingga berhenti"],
    "arah gerak benda berubah": [
        "Pemain tenis memukul bola yang datang kembali ke arah lawan",
        "Pemain sepak bola menyundul bola ke arah gawang",
        "Bola yang dilempar ke dinding memantul berbalik arah",
        "Pemain bulu tangkis mengembalikan kok ke daerah lawan",
        "Pengendara sepeda membelokkan setang ke kanan"],
    "gerak benda menjadi lebih cepat": [
        "Sepeda yang sedang berjalan dikayuh lebih kencang",
        "Gerobak yang sedang berjalan didorong lebih kuat",
        "Ayunan yang sedang berayun didorong lagi agar makin kencang",
        "Perahu yang sedang berlayar didayung lebih kuat"],
    "bentuk benda berubah": [
        "Tanah liat dibentuk menjadi vas bunga",
        "Plastisin ditekan hingga menjadi pipih",
        "Kaleng minuman bekas diinjak hingga penyok",
        "Adonan roti diuleni dan dibentuk bulat",
        "Kertas diremas hingga menjadi gumpalan",
        "Balon ditekan dengan kedua tangan hingga bentuknya berubah"],
}
p_pengaruh = _golongkan(
    PENGARUH, "Peristiwa: {contoh}. Pengaruh gaya pada peristiwa tersebut adalah …",
    lambda nama, contoh: f'Pada peristiwa "{contoh.lower()}", gaya membuat {nama}.',
    hindari={"benda diam menjadi bergerak": ("gerak benda menjadi lebih cepat",)})

TARIK_DORONG = {
    "tarikan": ["membuka laci meja", "menimba air dari sumur", "menarik tali layang-layang", "mencabut rumput",
                "menarik kursi untuk duduk", "menarik tali busur panah", "menarik gerobak dengan tali"],
    "dorongan": ["menendang bola", "mendorong gerobak", "menutup laci meja", "menekan tombol bel",
                 "mendorong meja", "mendorong ayunan", "memukul paku dengan palu"],
}
p_tarik_dorong = _pilih_satu(
    TARIK_DORONG, "Kegiatan berikut yang merupakan contoh gaya berupa {nama} adalah …",
    lambda nama, benar: f"{benar.capitalize()} termasuk {nama}. Gaya dapat berupa tarikan atau dorongan.")

_GAYA = [
    ("Gaya adalah … pada suatu benda.", "tarikan atau dorongan",
     ["warna atau bentuk", "panas atau dingin", "berat atau ringan"],
     "Gaya adalah tarikan atau dorongan yang diberikan pada suatu benda."),
    ("Satuan gaya adalah …", "newton (N)", ["meter (m)", "kilogram (kg)", "derajat Celsius (°C)"],
     "Besar gaya dinyatakan dalam satuan newton (N)."),
    ("Alat untuk mengukur besar gaya adalah …", "neraca pegas (dinamometer)",
     ["termometer", "penggaris", "kompas"], "Besar gaya diukur dengan neraca pegas atau dinamometer."),
    ("Satuan gaya newton diambil dari nama ilmuwan …", "Isaac Newton",
     ["Thomas Alva Edison", "Albert Einstein", "Alexander Graham Bell"],
     "Satuan gaya diambil dari nama Isaac Newton."),
    ("Gaya dapat memengaruhi benda dengan cara berikut, kecuali …", "mengubah warna benda",
     ["mengubah bentuk benda", "menggerakkan benda yang diam", "mengubah arah gerak benda"],
     "Gaya dapat mengubah bentuk, gerak, arah, dan kecepatan benda, tetapi tidak mengubah warnanya."),
    ("Semakin besar gaya dorong yang diberikan pada sebuah benda, benda itu akan bergerak semakin …", "cepat",
     ["lambat", "berat", "kecil"], "Gaya yang lebih besar membuat benda bergerak lebih cepat."),
    ("Bola A didorong pelan dan bola B didorong kuat. Bola yang bergerak lebih jauh adalah …",
     "bola B yang didorong kuat", ["bola A yang didorong pelan", "keduanya sama jauh", "tidak ada yang bergerak"],
     "Gaya yang lebih besar membuat benda bergerak lebih jauh."),
    ("Untuk memindahkan lemari yang berat, kita membutuhkan gaya yang …", "besar",
     ["kecil", "sangat lemah", "tidak ada"], "Benda yang berat membutuhkan gaya yang besar untuk dipindahkan."),
    ("Gaya tidak dapat dilihat, tetapi pengaruhnya dapat …", "dirasakan dan diamati",
     ["didengar sebagai lagu", "dicium baunya", "dihitung warnanya"],
     "Kita tidak bisa melihat gaya, tetapi bisa merasakan dan mengamati pengaruhnya."),
    ("Gaya yang bekerja karena dua benda saling bersentuhan disebut gaya …", "sentuh",
     ["tak sentuh", "udara", "cahaya"], "Gaya sentuh terjadi jika benda bersentuhan, misalnya gaya otot dan gaya gesek."),
    ("Gaya yang dapat bekerja tanpa menyentuh bendanya disebut gaya …", "tak sentuh",
     ["sentuh", "otot", "gesek"], "Gaya tak sentuh bekerja tanpa bersentuhan, misalnya gaya magnet dan gravitasi."),
    ("Berikut ini yang termasuk gaya tak sentuh adalah gaya …", "magnet", ["otot", "gesek", "pegas"],
     "Magnet dapat menarik paku tanpa menyentuhnya, jadi termasuk gaya tak sentuh."),
    ("Berikut ini yang termasuk gaya sentuh adalah gaya …", "otot", ["magnet", "gravitasi", "listrik statis"],
     "Gaya otot bekerja dengan menyentuh benda, jadi termasuk gaya sentuh."),
    ("Saat bola plastik ditekan, bola menjadi penyok. Hal ini menunjukkan bahwa gaya dapat …",
     "mengubah bentuk benda", ["mengubah warna benda", "membuat benda melayang", "menambah berat benda"],
     "Tekanan (gaya) membuat bentuk bola berubah."),
    ("Bola yang menggelinding ditendang ke arah lain. Gaya mengubah … bola.", "arah gerak",
     ["warna", "berat", "ukuran"], "Tendangan mengubah arah gerak bola."),
]


# ========================================================= Bab 4 · macam-macam gaya

JENIS_GAYA = {
    "gaya otot": ["Ibu mengangkat ember berisi air", "Andi mendorong meja ke pinggir kelas",
                  "Kuda menarik delman", "Sapi menarik bajak di sawah", "Pemain menendang bola",
                  "Ayah memeras kain cucian", "Siti menarik tali timba", "Petani mencangkul tanah",
                  "Kakak meremas adonan kue"],
    "gaya listrik": ["Penggaris plastik yang digosokkan ke rambut kering dapat menarik potongan kertas kecil",
                     "Balon yang digosokkan ke rambut dapat menempel di dinding",
                     "Rambut ikut tertarik ke atas saat disisir dengan sisir plastik",
                     "Potongan kertas kecil tertarik oleh sisir plastik yang sudah digosok",
                     "Petir menyambar di langit saat hujan"],
    "gaya magnet": ["Paku-paku menempel pada batang magnet", "Jarum kompas selalu menunjuk arah utara–selatan",
                    "Pintu kulkas dapat menutup dengan rapat", "Tempat pensil bermagnet tertutup dengan sendirinya",
                    "Derek magnet mengangkat besi bekas", "Peniti tertarik oleh magnet tanpa disentuh"],
    "gaya pegas": ["Batu melesat jauh dari ketapel yang ditarik lalu dilepas", "Anak panah melesat dari busurnya",
                   "Anak melompat tinggi di atas trampolin", "Kasur spring bed terasa empuk saat diduduki",
                   "Shockbreaker sepeda motor meredam guncangan", "Karet gelang yang ditarik kembali ke bentuk semula",
                   "Ujung pulpen cetek keluar masuk saat ditekan"],
    "gaya gravitasi": ["Buah mangga jatuh dari pohonnya", "Bola yang dilempar ke atas jatuh kembali ke tanah",
                       "Air terjun mengalir dari atas ke bawah", "Air hujan turun ke bumi",
                       "Daun kering berjatuhan ke tanah", "Pensil yang terlepas dari tangan jatuh ke lantai"],
    "gaya gesek": ["Sepeda berhenti saat direm", "Telapak tangan terasa hangat saat digosok-gosokkan",
                   "Korek api menyala saat digesekkan", "Bola yang menggelinding di rumput lama-lama berhenti",
                   "Alas sepatu yang bergerigi membuat kita tidak terpeleset",
                   "Penghapus dapat menghapus tulisan pensil", "Ban mobil menjadi halus setelah lama dipakai"],
}
# Pada contoh ini otot ikut bekerja (menarik, melempar, menggosok), jadi "gaya otot" tidak dipakai sebagai pengecoh.
_TANPA_OTOT = {n: ("gaya otot",) for n in ("gaya listrik", "gaya pegas", "gaya gravitasi", "gaya gesek")}

p_jenis_gaya = _golongkan(
    JENIS_GAYA, "Peristiwa berikut terjadi karena adanya gaya apa?\n{contoh}.",
    lambda nama, contoh: f'"{contoh}" adalah contoh {nama}.', hindari=_TANPA_OTOT)
p_contoh_gaya = _pilih_satu(
    JENIS_GAYA, "Berikut ini yang merupakan contoh {nama} adalah …",
    lambda nama, benar: f'"{benar}" adalah contoh {nama}.', hindari=_TANPA_OTOT)

MAGNETIS = {
    "benda magnetis": ["paku besi", "peniti", "jarum jahit", "klip kertas dari besi", "mur dan baut besi",
                       "gunting besi"],
    "benda nonmagnetis": ["penghapus karet", "pensil kayu", "sendok plastik", "kertas", "kain", "gelas kaca",
                          "karet gelang"],
}
p_magnetis = _pilih_satu(
    MAGNETIS, {"benda magnetis": "Benda berikut yang dapat ditarik oleh magnet adalah …",
               "benda nonmagnetis": "Benda berikut yang tidak dapat ditarik oleh magnet adalah …"},
    lambda nama, benar: f"{benar.capitalize()} termasuk {nama}. Magnet hanya menarik benda dari besi atau baja.")

_MACAM = [
    ("Gaya otot adalah gaya yang dihasilkan oleh …", "otot tubuh manusia atau hewan",
     ["tarikan bumi", "batang magnet", "benda yang lentur"], "Gaya otot berasal dari kerja otot tubuh."),
    ("Hewan yang tenaga ototnya dimanfaatkan petani untuk membajak sawah adalah …", "kerbau",
     ["kucing", "ayam", "kelinci"], "Kerbau dan sapi dimanfaatkan untuk membajak sawah."),
    ("Gaya listrik statis dapat timbul jika dua benda …", "digosokkan satu sama lain",
     ["dibiarkan diam", "direndam air", "dijemur"], "Listrik statis timbul karena dua benda saling digosokkan."),
    ("Magnet memiliki dua kutub, yaitu …", "kutub utara dan kutub selatan",
     ["kutub timur dan kutub barat", "kutub atas dan kutub bawah", "kutub kiri dan kutub kanan"],
     "Setiap magnet memiliki kutub utara dan kutub selatan."),
    ("Jika kutub utara magnet didekatkan dengan kutub utara magnet lain, keduanya akan …", "tolak-menolak",
     ["tarik-menarik", "diam saja", "menyatu"], "Kutub yang sejenis akan tolak-menolak."),
    ("Jika kutub utara magnet didekatkan dengan kutub selatan magnet lain, keduanya akan …", "tarik-menarik",
     ["tolak-menolak", "diam saja", "berputar"], "Kutub yang berbeda jenis akan tarik-menarik."),
    ("Bagian magnet yang gaya tariknya paling kuat adalah …", "kedua ujungnya (kutub magnet)",
     ["bagian tengahnya", "seluruh bagian sama kuat", "bagian yang dicat"],
     "Gaya magnet paling kuat berada di kutub-kutubnya."),
    ("Benda yang dapat ditarik oleh magnet disebut benda …", "magnetis", ["nonmagnetis", "elastis", "lentur"],
     "Benda yang dapat ditarik magnet disebut benda magnetis, contohnya paku besi."),
    ("Benda yang dapat kembali ke bentuk semula setelah ditarik atau ditekan disebut benda …", "elastis (lentur)",
     ["magnetis", "rapuh", "cair"], "Benda elastis memiliki gaya pegas, contohnya karet dan per."),
    ("Benda berikut yang tidak memiliki gaya pegas adalah …", "plastisin", ["karet gelang", "per", "trampolin"],
     "Plastisin tidak kembali ke bentuk semula setelah ditekan, jadi tidak elastis."),
    ("Gaya gravitasi adalah gaya tarik …", "bumi", ["magnet", "otot", "angin"],
     "Gaya gravitasi adalah gaya tarik bumi terhadap benda-benda."),
    ("Arah gaya gravitasi selalu menuju ke …", "bawah (pusat bumi)", ["atas", "kanan", "segala arah"],
     "Gravitasi menarik benda ke arah pusat bumi, yaitu ke bawah."),
    ("Jika tidak ada gaya gravitasi, benda-benda di bumi akan …", "melayang",
     ["jatuh lebih cepat", "menjadi lebih berat", "berubah warna"], "Tanpa gravitasi, benda tidak tertarik ke bawah."),
    ("Ilmuwan yang terkenal dengan cerita apel jatuh dan teori gravitasi adalah …", "Isaac Newton",
     ["Thomas Alva Edison", "Alexander Graham Bell", "Wright bersaudara"],
     "Isaac Newton terkenal dengan teori gravitasi."),
    ("Gaya gesek adalah gaya yang timbul karena …", "dua permukaan benda saling bersentuhan dan bergesekan",
     ["benda ditarik oleh bumi", "benda elastis kembali ke bentuk semula", "benda ditarik oleh magnet"],
     "Gaya gesek timbul antara dua permukaan yang bergesekan."),
    ("Jarum kompas selalu menunjuk arah utara–selatan karena pengaruh gaya …", "magnet bumi",
     ["otot", "pegas", "gesek"], "Bumi bersifat seperti magnet besar sehingga jarum kompas menunjuk utara–selatan."),
    ("Gaya pegas terjadi pada benda yang …", "lentur (elastis)", ["keras dan rapuh", "cair", "magnetis"],
     "Gaya pegas dimiliki benda lentur yang dapat kembali ke bentuk semula."),
]


# ============================================================ Bab 4 · manfaat gaya

ALAT_GAYA = {
    "gaya magnet": ["kompas", "pintu kulkas", "tempat pensil bermagnet", "derek magnet pengangkat besi"],
    "gaya pegas": ["kasur spring bed", "ketapel", "trampolin", "shockbreaker sepeda motor", "neraca pegas",
                   "busur panah"],
    "gaya gesek": ["rem sepeda", "alas sepatu bergerigi", "korek api", "penghapus pensil", "ban bergerigi"],
}
p_alat_gaya = _pilih_satu(
    ALAT_GAYA, "Benda berikut yang cara kerjanya memanfaatkan {nama} adalah …",
    lambda nama, benar: f"{benar.capitalize()} memanfaatkan {nama}.")

_MANFAAT = [
    ("Alat yang memanfaatkan gaya magnet untuk menunjukkan arah adalah …", "kompas",
     ["neraca pegas", "rem", "ketapel"], "Kompas memakai jarum magnet untuk menunjukkan arah."),
    ("Pintu kulkas dapat menutup rapat karena memanfaatkan gaya …", "magnet", ["pegas", "otot", "gravitasi"],
     "Karet pintu kulkas berisi magnet sehingga menempel rapat."),
    ("Di tempat pengumpulan besi bekas, besi dipisahkan dari sampah lain dengan memanfaatkan …", "magnet",
     ["pegas", "ketapel", "pelumas"], "Magnet menarik besi sehingga besi terpisah dari sampah lain."),
    ("Kasur spring bed terasa empuk karena memanfaatkan gaya …", "pegas", ["magnet", "gravitasi", "listrik"],
     "Di dalam spring bed terdapat banyak per (pegas)."),
    ("Shockbreaker pada sepeda motor memanfaatkan gaya pegas untuk …", "meredam guncangan saat melewati jalan rusak",
     ["mempercepat laju motor", "menyalakan mesin", "menyalakan lampu"],
     "Pegas pada shockbreaker meredam guncangan."),
    ("Trampolin memanfaatkan gaya … sehingga kita dapat melompat tinggi.", "pegas",
     ["magnet", "gesek", "listrik"], "Alas trampolin lentur dan memantulkan kita ke atas."),
    ("Neraca pegas dimanfaatkan untuk …", "mengukur besar gaya atau berat benda",
     ["mengukur suhu", "menentukan arah", "mengukur panjang meja"], "Neraca pegas digunakan untuk mengukur gaya."),
    ("Rem sepeda dapat menghentikan laju sepeda karena memanfaatkan gaya …", "gesek",
     ["magnet", "pegas", "listrik"], "Karet rem bergesekan dengan roda sehingga sepeda melambat dan berhenti."),
    ("Alas sepatu dibuat bergerigi agar …", "tidak mudah terpeleset",
     ["sepatu lebih ringan", "warna sepatu lebih terang", "sepatu cepat aus"],
     "Gerigi memperbesar gaya gesek sehingga kita tidak mudah terpeleset."),
    ("Air dapat mengalir dari tempat tinggi ke tempat rendah karena gaya …", "gravitasi",
     ["magnet", "pegas", "listrik"], "Gravitasi menarik air ke bawah."),
    ("Air terjun dimanfaatkan untuk menggerakkan turbin pembangkit listrik. Air terjun jatuh ke bawah karena gaya …",
     "gravitasi", ["magnet", "pegas", "otot"], "Air terjun jatuh karena tarikan gravitasi bumi."),
    ("Karena ada gaya gravitasi, benda-benda di bumi …", "tidak melayang dan tetap berada di tempatnya",
     ["melayang di udara", "terbang ke angkasa", "bergerak sendiri ke atas"],
     "Gravitasi menarik benda ke bumi sehingga benda tidak melayang."),
    ("Petani memanfaatkan gaya otot kerbau untuk …", "membajak sawah",
     ["menyiram tanaman", "menentukan arah", "mengukur hujan"], "Kerbau membantu petani membajak sawah."),
    ("Contoh pemanfaatan gaya otot dalam kegiatan sehari-hari adalah …", "mengangkat ember berisi air",
     ["jarum kompas menunjuk utara", "buah jatuh dari pohon", "kasur terasa empuk"],
     "Mengangkat ember memakai tenaga otot."),
    ("Perajin gerabah memanfaatkan gaya untuk …", "mengubah bentuk tanah liat menjadi pot atau vas",
     ["mengubah warna tanah liat", "membuat tanah liat melayang", "menarik tanah liat dengan magnet"],
     "Gaya dapat mengubah bentuk benda, misalnya tanah liat."),
    ("Ibu menguleni adonan menjadi roti. Gaya dimanfaatkan untuk …", "mengubah bentuk adonan",
     ["mengubah warna adonan", "membuat adonan melayang", "menarik adonan dengan magnet"],
     "Saat diuleni, bentuk adonan berubah karena gaya."),
    ("Ketapel dan busur panah memanfaatkan gaya … untuk melontarkan benda.", "pegas",
     ["magnet", "gravitasi", "gesek"], "Karet ketapel dan tali busur yang lentur melontarkan benda."),
    ("Korek api dapat menyala karena memanfaatkan gaya …", "gesek", ["magnet", "pegas", "gravitasi"],
     "Batang korek api digesekkan pada bidang kasar kotaknya."),
    ("Ban kendaraan dibuat beralur (bergerigi) agar …", "tidak mudah tergelincir di jalan",
     ["lebih cepat aus", "lebih licin", "lebih ringan"],
     "Alur pada ban memperbesar gaya gesek dengan jalan."),
    ("Penghapus dapat menghapus tulisan pensil karena gaya …", "gesek", ["magnet", "pegas", "gravitasi"],
     "Penghapus bergesekan dengan kertas sehingga tulisan pensil terhapus."),
    ("Paku yang tercecer di lantai dapat dikumpulkan dengan cepat menggunakan …", "magnet",
     ["sapu lidi basah", "karet gelang", "kain lap"], "Magnet menarik paku besi."),
    ("Kita dapat berjalan tanpa tergelincir karena ada gaya … antara telapak kaki dan tanah.", "gesek",
     ["magnet", "pegas", "listrik"], "Gaya gesek menahan kaki agar tidak tergelincir."),
    ("Air hujan turun ke bumi dan menyirami tanaman. Air hujan turun karena gaya …", "gravitasi",
     ["magnet", "pegas", "gesek"], "Gravitasi menarik air hujan ke bawah."),
    ("Pegas pada pulpen cetek bermanfaat untuk …", "mengeluarkan dan memasukkan kembali ujung pulpen",
     ["menghapus tulisan", "menentukan arah", "mengukur suhu"],
     "Pegas di dalam pulpen membuat ujungnya kembali masuk."),
    ("Kuda menarik delman. Manfaat gaya otot hewan bagi manusia adalah …", "membantu mengangkut orang atau barang",
     ["menentukan arah mata angin", "membuat air mengalir", "meredam guncangan"],
     "Hewan seperti kuda membantu mengangkut orang atau barang."),
]


# ======================================================== Bab 4 · gaya gesek dan gerak

_LICIN = ["lantai keramik", "kaca", "lantai marmer", "papan kayu yang halus"]
_KASAR = ["karpet", "rumput", "pasir", "jalan berkerikil", "handuk"]
_BENDA = ["Mobil mainan", "Bola", "Kelereng", "Balok kayu"]


def p_permukaan(r):
    licin, kasar, benda = r.choice(_LICIN), r.choice(_KASAR), r.choice(_BENDA)
    awal = f"{benda} didorong dengan kekuatan yang sama di atas {licin} dan di atas {kasar}."
    bentuk = r.randrange(3)
    if bentuk == 0:
        soal = teks_pilihan(r, f"{awal} {benda} akan bergerak lebih jauh di atas …", licin,
                            [kasar, "keduanya sama jauh", "tidak bergerak di keduanya"],
                            f"Permukaan {licin} licin sehingga gaya geseknya kecil. Benda bergerak lebih jauh.")
    elif bentuk == 1:
        soal = teks_pilihan(r, f"{awal} {benda} akan lebih cepat berhenti di atas …", kasar,
                            [licin, "keduanya sama cepat berhenti", "tidak berhenti di keduanya"],
                            f"Permukaan {kasar} kasar sehingga gaya geseknya besar. Benda lebih cepat berhenti.")
    else:
        soal = teks_pilihan(r, f"{awal} Gaya gesek di atas {kasar} lebih … daripada di atas {licin}.", "besar",
                            ["kecil", "sama besar", "tidak ada"],
                            "Permukaan kasar menimbulkan gaya gesek yang lebih besar daripada permukaan licin.")
    return _k(soal, "permukaan", licin, kasar, bentuk)


GESEK = {
    "menguntungkan": ["rem sepeda dapat menghentikan laju sepeda", "alas sepatu bergerigi membuat kita tidak terpeleset",
                      "korek api dapat menyala saat digesekkan", "kita dapat menulis di kertas dengan pensil",
                      "ban beralur membuat mobil tidak tergelincir", "penghapus dapat menghapus tulisan pensil",
                      "kita dapat berjalan tanpa tergelincir"],
    "merugikan": ["ban kendaraan menjadi gundul karena lama dipakai", "alas sepatu menjadi tipis dan aus",
                  "mesin kendaraan cepat panas dan aus", "lemari berat sulit didorong di lantai yang kasar",
                  "engsel pintu berbunyi dan sulit dibuka", "rantai sepeda yang kering menjadi berat dikayuh"],
}
p_untung_rugi = _pilih_satu(
    GESEK, "Berikut ini yang merupakan contoh gaya gesek yang {nama} adalah …",
    lambda nama, benar: f'"{benar.capitalize()}" adalah contoh gaya gesek yang {nama}.')

_GESEK = [
    ("Arah gaya gesek selalu … arah gerak benda.", "berlawanan dengan",
     ["searah dengan", "tegak lurus ke atas dari", "sama dengan"],
     "Gaya gesek arahnya berlawanan dengan arah gerak benda sehingga memperlambat gerak."),
    ("Gaya gesek membuat gerak benda menjadi …", "lebih lambat hingga akhirnya berhenti",
     ["lebih cepat", "selalu tetap", "naik ke atas"], "Gaya gesek menghambat gerak benda."),
    ("Permukaan yang kasar menimbulkan gaya gesek yang …", "besar",
     ["kecil", "tidak ada", "sama dengan permukaan licin"], "Makin kasar permukaan, makin besar gaya geseknya."),
    ("Permukaan yang licin menimbulkan gaya gesek yang …", "kecil",
     ["besar", "sangat besar", "sama dengan permukaan kasar"], "Makin licin permukaan, makin kecil gaya geseknya."),
    ("Lantai kamar mandi yang basah dan licin membuat kita mudah terpeleset karena gaya geseknya …", "kecil",
     ["besar", "sangat kuat", "berubah menjadi magnet"], "Permukaan licin memiliki gaya gesek kecil."),
    ("Agar tidak terpeleset di lantai kamar mandi yang licin, sebaiknya kita …",
     "memakai sandal beralas kasar atau menaruh keset", ["berlari di lantai", "menuang sabun di lantai",
                                                         "memakai kaus kaki licin"],
     "Alas yang kasar memperbesar gaya gesek sehingga kita tidak mudah terpeleset."),
    ("Mesin kendaraan diberi oli (pelumas) agar …", "gaya geseknya berkurang sehingga mesin tidak cepat aus",
     ["gaya geseknya bertambah", "mesin menjadi kotor", "kendaraan lebih berat"],
     "Pelumas memperkecil gaya gesek antarbagian mesin."),
    ("Lemari yang berat diberi roda agar …", "mudah dipindahkan karena gaya geseknya kecil",
     ["sulit dipindahkan", "gaya geseknya bertambah besar", "tidak bisa bergerak"],
     "Roda memperkecil gaya gesek dengan lantai."),
    ("Engsel pintu yang berbunyi dan sulit dibuka sebaiknya diberi …", "pelumas atau oli",
     ["pasir", "lem", "tanah"], "Pelumas memperkecil gaya gesek pada engsel."),
    ("Ban sepeda yang sudah lama dipakai menjadi gundul (halus). Ini contoh gaya gesek yang …", "merugikan",
     ["menguntungkan", "tidak berpengaruh", "mempercepat sepeda"],
     "Gesekan yang terus-menerus membuat ban aus, jadi merugikan."),
    ("Cara memperbesar gaya gesek adalah …", "membuat permukaan benda menjadi kasar atau bergerigi",
     ["memberi oli", "memasang roda", "menghaluskan permukaan"],
     "Permukaan kasar atau bergerigi memperbesar gaya gesek."),
    ("Cara memperkecil gaya gesek adalah …", "memberi pelumas pada benda yang bergesekan",
     ["membuat permukaan bergerigi", "menaburkan pasir", "memakai alas karet yang kasar"],
     "Pelumas, roda, dan permukaan halus memperkecil gaya gesek."),
    ("Saat kedua telapak tangan digosok-gosokkan, tangan terasa …", "hangat", ["dingin", "basah", "lengket"],
     "Gesekan menimbulkan panas."),
    ("Bola yang ditendang di lapangan rumput lama-kelamaan berhenti karena …",
     "ada gaya gesek antara bola dan rumput", ["ada gaya magnet", "bola ditarik pegas", "bola berubah warna"],
     "Gaya gesek memperlambat bola hingga berhenti."),
    ("Kendaraan dapat berhenti saat direm karena rem memperbesar …", "gaya gesek",
     ["gaya magnet", "gaya pegas", "gaya listrik"], "Rem bergesekan dengan roda sehingga laju kendaraan berkurang."),
    ("Gaya gesek terjadi antara …", "dua permukaan benda yang saling bersentuhan",
     ["dua magnet yang berjauhan", "bumi dan bulan", "dua benda yang tidak bersentuhan"],
     "Gaya gesek termasuk gaya sentuh."),
]


# ------------------------------------------------------------------- perakit

PEMBANGKIT = {
    "ipas-peta": [p_bagian, p_bagian, p_gambar_bagian, p_kompas, p_arah_teks, p_arah_kota, p_skala_arti,
                  p_skala_hitung, p_simbol, _dari_butir(_PETA), _dari_butir(_PETA), _dari_butir(_PETA)],
    "ipas-jenis-peta": [_dari_butir(_JENIS), _dari_butir(_JENIS), p_golong_peta, p_contoh_peta, p_bentang],
    "ipas-letak": [_dari_butir(_LETAK), _dari_butir(_LETAK), _dari_butir(_LETAK), p_grid, p_grid, p_batas,
                   p_batas, p_pernyataan],
    "ipas-pemda": [_dari_butir(_PEMDA), _dari_butir(_PEMDA), _dari_butir(_PEMDA), p_pemimpin, p_pemimpin,
                   p_urutan, p_layanan, p_tugas],
    "ipas-gaya": [_dari_butir(_GAYA), _dari_butir(_GAYA), p_pengaruh, p_pengaruh, p_tarik_dorong],
    "ipas-macam-gaya": [p_jenis_gaya, p_jenis_gaya, p_contoh_gaya, _dari_butir(_MACAM), _dari_butir(_MACAM),
                        p_magnetis],
    "ipas-manfaat-gaya": [_dari_butir(_MANFAAT), _dari_butir(_MANFAAT), _dari_butir(_MANFAAT), p_alat_gaya],
    "ipas-gaya-gesek": [_dari_butir(_GESEK), _dari_butir(_GESEK), p_permukaan, p_permukaan, p_untung_rugi,
                        p_untung_rugi],
}

GABUNGAN = {
    "ipas-bab-2": ["ipas-peta", "ipas-jenis-peta", "ipas-letak", "ipas-pemda"],
    "ipas-bab-4": ["ipas-gaya", "ipas-macam-gaya", "ipas-manfaat-gaya", "ipas-gaya-gesek"],
    "ipas-sumatif-2": ["ipas-peta", "ipas-jenis-peta", "ipas-letak", "ipas-pemda",
                       "ipas-gaya", "ipas-macam-gaya", "ipas-manfaat-gaya", "ipas-gaya-gesek"],
}

KODE_TOPIK = [t["kode"] for t in TOPIK]


def buat_latihan(topik, jumlah=JUMLAH_SOAL, rng=None):
    """Buat ``jumlah`` soal IPAS berbeda untuk satu subtopik atau satu paket gabungan."""
    if topik not in KODE_TOPIK:
        raise ValueError(f"topik tidak dikenal: {topik}")
    r = rng or random.Random()
    if topik in GABUNGAN:
        return rakit({k: PEMBANGKIT[k] for k in GABUNGAN[topik]}, topik, topik, jumlah, r)
    return rakit(PEMBANGKIT, topik, None, jumlah, r)
