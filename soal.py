"""Pembangkit soal matematika SD kelas 4.

Setiap pembangkit menerima objek ``random.Random`` dan mengembalikan dict:
    {"teks": str, "pilihan": [str × 4], "benar": indeks, "pembahasan": str}
"""

import random
from math import gcd

JUMLAH_SOAL = 20

TOPIK = [
    {"kode": "tambah-kurang", "nama": "Penjumlahan & Pengurangan", "ikon": "➕",
     "ket": "Bilangan ribuan sampai puluh ribuan"},
    {"kode": "perkalian", "nama": "Perkalian", "ikon": "✖️",
     "ket": "Perkalian bersusun dan kali 10, 100, 1.000"},
    {"kode": "pembagian", "nama": "Pembagian", "ikon": "➗",
     "ket": "Pembagian habis dan bersisa"},
    {"kode": "pecahan", "nama": "Pecahan", "ikon": "🍕",
     "ket": "Senilai, menyederhanakan, tambah, kurang, desimal"},
    {"kode": "kpk-fpb", "nama": "Faktor, Kelipatan, KPK & FPB", "ikon": "🔢",
     "ket": "Faktor, kelipatan, bilangan prima, KPK, FPB"},
    {"kode": "pembulatan", "nama": "Nilai Tempat & Pembulatan", "ikon": "🎯",
     "ket": "Nilai tempat, pembulatan, penaksiran"},
    {"kode": "keliling-luas", "nama": "Keliling & Luas", "ikon": "📐",
     "ket": "Persegi, persegi panjang, segitiga"},
    {"kode": "pengukuran", "nama": "Pengukuran", "ikon": "📏",
     "ket": "Satuan panjang, berat, waktu, volume"},
    {"kode": "soal-cerita", "nama": "Soal Cerita", "ikon": "📖",
     "ket": "Soal cerita sehari-hari"},
    {"kode": "campuran", "nama": "Campuran Semua Topik", "ikon": "🌈",
     "ket": "Gabungan semua topik"},
]


# ---------------------------------------------------------------- alat bantu

def fmt(n):
    """Tulis bilangan bulat gaya Indonesia: 12500 -> '12.500'."""
    return f"{n:,}".replace(",", ".")


def kpk(a, b):
    return a * b // gcd(a, b)


def _selisih(jawab):
    if jawab < 20:
        return [1, 2, 3, 4]
    if jawab < 200:
        return [1, 2, 5, 10, 20]
    if jawab < 2000:
        return [1, 10, 20, 100, 200]
    return [10, 100, 200, 1000, 2000]


def angka(r, teks, jawab, pembahasan, salah=(), satuan="", awalan="", langkah=None):
    """Soal berjawaban bilangan bulat. ``salah`` = pengecoh dari kesalahan umum."""
    kandidat = [s for s in dict.fromkeys(salah) if s != jawab and s >= 0]
    r.shuffle(kandidat)
    kandidat = kandidat[:3]
    langkah = langkah or _selisih(jawab)
    k = 1
    while len(kandidat) < 3:
        for _ in range(40):
            v = jawab + r.choice([-1, 1]) * r.choice(langkah) * k
            if v >= 0 and v != jawab and v not in kandidat:
                kandidat.append(v)
                break
        else:
            k += 1
    tulis = lambda v: f"{awalan}{fmt(v)}{satuan}"
    return teks_pilihan(r, teks, tulis(jawab), [tulis(v) for v in kandidat], pembahasan)


def teks_pilihan(r, teks, jawab, salah, pembahasan):
    """Soal dengan pilihan berupa teks. Butuh minimal 3 pengecoh berbeda."""
    jawab = str(jawab)
    kandidat = [s for s in dict.fromkeys(map(str, salah)) if s != jawab]
    if len(kandidat) < 3:
        raise ValueError(f"pengecoh kurang untuk soal: {teks}")
    r.shuffle(kandidat)
    pilihan = kandidat[:3] + [jawab]
    r.shuffle(pilihan)
    return {"teks": teks, "pilihan": pilihan, "benar": pilihan.index(jawab),
            "pembahasan": pembahasan}


# ------------------------------------------------- penjumlahan & pengurangan

def tk_tambah(r):
    a, b = r.randint(1000, 9999), r.randint(100, 9999)
    return angka(r, f"{fmt(a)} + {fmt(b)} = …", a + b,
                 f"{fmt(a)} + {fmt(b)} = {fmt(a + b)}")


def tk_tambah_besar(r):
    a, b = r.randint(10000, 60000), r.randint(1000, 39999)
    return angka(r, f"{fmt(a)} + {fmt(b)} = …", a + b,
                 f"{fmt(a)} + {fmt(b)} = {fmt(a + b)}")


def tk_kurang(r):
    a = r.randint(2000, 99999)
    b = r.randint(100, a - 1)
    return angka(r, f"{fmt(a)} − {fmt(b)} = …", a - b,
                 f"{fmt(a)} − {fmt(b)} = {fmt(a - b)}")


def tk_hilang_tambah(r):
    a, b = r.randint(500, 9000), r.randint(500, 9000)
    return angka(r, f"… + {fmt(b)} = {fmt(a + b)}", a,
                 f"Bilangan yang hilang = {fmt(a + b)} − {fmt(b)} = {fmt(a)}",
                 salah=[a + 2 * b])


def tk_hilang_kurang(r):
    a = r.randint(2000, 9999)
    b = r.randint(500, a - 100)
    return angka(r, f"{fmt(a)} − … = {fmt(a - b)}", b,
                 f"Bilangan yang hilang = {fmt(a)} − {fmt(a - b)} = {fmt(b)}",
                 salah=[a + (a - b)])


def tk_campur(r):
    a, b = r.randint(1000, 9000), r.randint(500, 5000)
    c = r.randint(200, a + b - 100)
    return angka(r, f"{fmt(a)} + {fmt(b)} − {fmt(c)} = …", a + b - c,
                 f"{fmt(a)} + {fmt(b)} = {fmt(a + b)}, lalu {fmt(a + b)} − {fmt(c)} = {fmt(a + b - c)}",
                 salah=[a + b + c])


# ------------------------------------------------------------------ perkalian

def kali_1(r):
    a, b = r.randint(12, 99), r.randint(2, 9)
    return angka(r, f"{a} × {b} = …", a * b, f"{a} × {b} = {a * b}",
                 salah=[(a + 1) * b, a * (b + 1), (a - 1) * b])


def kali_2(r):
    a, b = r.randint(11, 49), r.randint(11, 29)
    return angka(r, f"{a} × {b} = …", a * b,
                 f"{a} × {b} = ({a} × {b // 10 * 10}) + ({a} × {b % 10}) = "
                 f"{a * (b // 10 * 10)} + {a * (b % 10)} = {fmt(a * b)}",
                 salah=[(a + 1) * b, a * (b + 1), a * b + 10, a * b - 10])


def kali_3(r):
    a, b = r.randint(101, 999), r.randint(2, 9)
    return angka(r, f"{a} × {b} = …", a * b, f"{a} × {b} = {fmt(a * b)}",
                 salah=[(a + 10) * b, a * (b + 1), (a - 10) * b, a * b + 100])


def kali_10(r):
    a, p = r.randint(2, 999), r.choice([10, 100, 1000])
    nol = len(str(p)) - 1
    return angka(r, f"{fmt(a)} × {fmt(p)} = …", a * p,
                 f"Dikali {fmt(p)} berarti menambahkan {nol} angka nol: {fmt(a * p)}",
                 salah=[a * p * 10, a * p // 10, a * p + p, a * p * 100])


def kali_hilang(r):
    a, b = r.randint(3, 25), r.randint(3, 12)
    return angka(r, f"… × {b} = {a * b}", a,
                 f"Bilangan yang hilang = {a * b} : {b} = {a}")


def kali_tiga(r):
    a, b, c = r.randint(2, 9), r.randint(2, 9), r.randint(2, 9)
    return angka(r, f"{a} × {b} × {c} = …", a * b * c,
                 f"{a} × {b} = {a * b}, lalu {a * b} × {c} = {a * b * c}",
                 salah=[a * b + c, a + b * c, a * b * (c + 1)])


# ------------------------------------------------------------------ pembagian

def bagi_1(r):
    b, q = r.randint(2, 9), r.randint(12, 150)
    return angka(r, f"{fmt(b * q)} : {b} = …", q,
                 f"{fmt(b * q)} : {b} = {q}, karena {q} × {b} = {fmt(b * q)}")


def bagi_2(r):
    b, q = r.randint(11, 25), r.randint(4, 30)
    return angka(r, f"{fmt(b * q)} : {b} = …", q,
                 f"{fmt(b * q)} : {b} = {q}, karena {q} × {b} = {fmt(b * q)}")


def bagi_sisa(r):
    b = r.randint(3, 9)
    q, s = r.randint(5, 40), r.randint(1, b - 1)
    n = b * q + s
    return angka(r, f"Sisa pembagian {n} : {b} adalah …", s,
                 f"{n} : {b} = {q} sisa {s}, karena {q} × {b} = {b * q} dan {n} − {b * q} = {s}",
                 langkah=[1, 2, 3])


def bagi_hilang(r):
    b, q = r.randint(3, 12), r.randint(6, 40)
    return angka(r, f"… : {b} = {q}", b * q,
                 f"Bilangan yang hilang = {q} × {b} = {fmt(b * q)}",
                 salah=[b * q + b, b * q - b, q + b])


def bagi_10(r):
    q, p = r.randint(3, 99), r.choice([10, 100])
    return angka(r, f"{fmt(q * p)} : {p} = …", q,
                 f"Dibagi {p} berarti menghilangkan {len(str(p)) - 1} angka nol: {q}",
                 salah=[q * 10, q * 100, q * p])


def bagi_campur(r):
    b, q, c = r.randint(2, 9), r.randint(5, 30), r.randint(2, 6)
    return angka(r, f"{b * q} : {b} × {c} = …", q * c,
                 f"Kerjakan dari kiri: {b * q} : {b} = {q}, lalu {q} × {c} = {q * c}")


# -------------------------------------------------------------------- pecahan

def _pecahan_sederhana(r, maks=9):
    while True:
        b = r.randint(2, maks)
        a = r.randint(1, b - 1)
        if gcd(a, b) == 1:
            return a, b


def pc_senilai(r):
    a, b = _pecahan_sederhana(r)
    k = r.randint(2, 6)
    return angka(r, f"{a}/{b} = …/{b * k}   Bilangan yang tepat untuk mengisi titik-titik adalah …",
                 a * k,
                 f"Penyebut dikali {k} ({b} × {k} = {b * k}), maka pembilang juga dikali {k}: {a} × {k} = {a * k}",
                 salah=[a + k, a + b * k - b, a * k + 1])


def pc_sederhana(r):
    a, b = _pecahan_sederhana(r)
    k = r.randint(2, 6)
    return teks_pilihan(
        r, f"Bentuk paling sederhana dari {a * k}/{b * k} adalah …", f"{a}/{b}",
        [f"{a + 1}/{b}", f"{a}/{b + 1}", f"{a * k}/{b}", f"{a + 1}/{b + 1}", f"{b}/{a}"],
        f"Pembilang dan penyebut sama-sama dibagi {k}: {a * k}/{b * k} = {a}/{b}")


def pc_tambah(r):
    b = r.randint(5, 15)
    a = r.randint(1, b - 3)
    c = r.randint(1, b - a - 1)
    s = a + c
    return teks_pilihan(
        r, f"{a}/{b} + {c}/{b} = …", f"{s}/{b}",
        [f"{s}/{2 * b}", f"{s + 1}/{b}", f"{s - 1}/{b}" if s > 1 else f"{s + 2}/{b}",
         f"{a * c + 1}/{b * b}", f"{s + 1}/{2 * b}"],
        f"Penyebut sama, jadi cukup jumlahkan pembilang: {a} + {c} = {s}, hasilnya {s}/{b}")


def pc_kurang(r):
    b = r.randint(5, 15)
    a = r.randint(3, b - 1)
    c = r.randint(1, a - 1)
    s = a - c
    return teks_pilihan(
        r, f"{a}/{b} − {c}/{b} = …", f"{s}/{b}",
        [f"{a + c}/{b}", f"{s + 1}/{b}", f"{s}/{2 * b}", f"{s + 2}/{b}", f"{a}/{b}"],
        f"Penyebut sama, jadi cukup kurangkan pembilang: {a} − {c} = {s}, hasilnya {s}/{b}")


def pc_banding(r):
    besar = r.random() < 0.5
    kata = "paling besar" if besar else "paling kecil"
    if r.random() < 0.5:
        b = r.randint(7, 15)
        pemb = r.sample(range(1, b), 4)
        pilih = max(pemb) if besar else min(pemb)
        opsi = [f"{p}/{b}" for p in pemb]
        jawab = f"{pilih}/{b}"
        bahas = (f"Penyebut sama, jadi bandingkan pembilangnya. "
                 f"Pembilang {kata} adalah {pilih}, jadi jawabannya {jawab}")
    else:
        a = r.randint(1, 3)
        peny = r.sample(range(a + 1, 13), 4)
        pilih = min(peny) if besar else max(peny)
        opsi = [f"{a}/{p}" for p in peny]
        jawab = f"{a}/{pilih}"
        bahas = (f"Pembilang sama. Semakin besar penyebut, semakin kecil pecahannya. "
                 f"Jadi yang {kata} adalah {jawab}")
    opsi.remove(jawab)
    return teks_pilihan(r, f"Pecahan yang {kata} di antara pilihan berikut adalah …",
                        jawab, opsi, bahas)


def pc_campuran(r):
    w, d = r.randint(1, 5), r.randint(2, 9)
    n = r.randint(1, d - 1)
    j = w * d + n
    return teks_pilihan(
        r, f"Pecahan campuran {w} {n}/{d} jika diubah menjadi pecahan biasa adalah …",
        f"{j}/{d}",
        [f"{w + n}/{d}", f"{w * n + d}/{d}", f"{j + 1}/{d}", f"{j}/{d + 1}", f"{j + d}/{d}"],
        f"({w} × {d}) + {n} = {j}, jadi {w} {n}/{d} = {j}/{d}")


_DESIMAL = {"1/2": "0,5", "1/4": "0,25", "3/4": "0,75", "1/5": "0,2", "2/5": "0,4",
            "3/5": "0,6", "4/5": "0,8", "1/10": "0,1", "3/10": "0,3", "7/10": "0,7",
            "9/10": "0,9"}


def pc_desimal(r):
    p, d = r.choice(list(_DESIMAL.items()))
    lain = [v for v in dict.fromkeys(_DESIMAL.values()) if v != d]
    a, b = p.split("/")
    palsu = f"{a},{b}"
    if palsu != d:
        lain = r.sample(lain, 3) + [palsu]
    return teks_pilihan(r, f"Bentuk desimal dari {p} adalah …", d, lain,
                        f"{p} = {a} : {b} = {d}")


def pc_dari(r):
    a, b = _pecahan_sederhana(r, 6)
    m = r.randint(2, 12)
    n = b * m
    return angka(r, f"{a}/{b} dari {n} adalah …", a * m,
                 f"{n} : {b} = {m}, lalu {m} × {a} = {a * m}",
                 salah=[m, n - a * m, a * n])


# ------------------------------------------------------------------ KPK & FPB

_PRIMA = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59]
_KOMPOSIT = [n for n in range(4, 61) if n not in _PRIMA]


def _faktor_prima(n):
    hasil, p = [], 2
    while n > 1:
        while n % p == 0:
            hasil.append(p)
            n //= p
        p += 1
    return hasil


def kf_kpk(r):
    while True:
        a, b = r.sample(range(2, 16), 2)
        if kpk(a, b) != max(a, b) or r.random() < 0.3:
            break
    k = kpk(a, b)
    return angka(r, f"KPK dari {a} dan {b} adalah …", k,
                 f"Kelipatan {a}: {', '.join(str(a * i) for i in range(1, k // a + 1)[-4:])}… "
                 f"Kelipatan {b}: {', '.join(str(b * i) for i in range(1, k // b + 1)[-4:])}… "
                 f"Kelipatan persekutuan terkecilnya {k}",
                 salah=[a * b, gcd(a, b), a + b, k * 2])


def kf_fpb(r):
    g = r.randint(2, 12)
    while True:
        m, n = r.sample(range(1, 8), 2)
        if gcd(m, n) == 1:
            break
    a, b = g * m, g * n
    return angka(r, f"FPB dari {a} dan {b} adalah …", g,
                 f"{a} = {g} × {m} dan {b} = {g} × {n}. Faktor persekutuan terbesarnya {g}",
                 salah=[kpk(a, b), g * 2, 1 if g > 2 else 3, abs(a - b) or g + 1])


def kf_faktor(r):
    n = r.choice([x for x in _KOMPOSIT if x >= 12])
    faktor = [f for f in range(2, n) if n % f == 0]
    bukan = [f for f in range(3, n) if n % f != 0]
    j = r.choice(faktor)
    return teks_pilihan(r, f"Bilangan berikut yang merupakan faktor dari {n} adalah …",
                        j, r.sample(bukan, 3),
                        f"{n} : {j} = {n // j} (habis dibagi), jadi {j} adalah faktor dari {n}")


def kf_kelipatan(r):
    n = r.randint(3, 9)
    j = n * r.randint(4, 12)
    bukan = [x for x in range(j - 15, j + 16) if x > n and x % n != 0]
    return teks_pilihan(r, f"Bilangan berikut yang merupakan kelipatan {n} adalah …",
                        j, r.sample(bukan, 3),
                        f"{j} = {n} × {j // n}, jadi {j} adalah kelipatan {n}")


def kf_prima(r):
    j = r.choice(_PRIMA[2:])
    bukan = r.sample([9, 15, 21, 25, 27, 33, 35, 39, 45, 49, 51, 57, 1], 2) + \
        [r.choice([x for x in _KOMPOSIT if x % 2 == 0])]
    return teks_pilihan(r, "Bilangan berikut yang merupakan bilangan prima adalah …",
                        j, bukan,
                        f"{j} hanya habis dibagi 1 dan {j}, jadi {j} bilangan prima")


def kf_faktorisasi(r):
    daftar = [12, 18, 20, 24, 28, 30, 36, 40, 42, 45, 48, 50, 54, 56, 60, 63, 70, 72, 75, 80, 84, 90]
    n = r.choice(daftar)
    tulis = lambda x: " × ".join(map(str, _faktor_prima(x)))
    lain = [tulis(x) for x in r.sample([d for d in daftar if d != n], 3)]
    return teks_pilihan(r, f"Faktorisasi prima dari {n} adalah …", tulis(n), lain,
                        f"{n} = {tulis(n)}")


def kf_banyak_faktor(r):
    n = r.choice([x for x in _KOMPOSIT if x >= 8])
    faktor = [f for f in range(1, n + 1) if n % f == 0]
    return angka(r, f"Banyak faktor dari {n} adalah …", len(faktor),
                 f"Faktor dari {n}: {', '.join(map(str, faktor))}. Banyaknya ada {len(faktor)}",
                 langkah=[1, 2, 3])


# -------------------------------------------------- nilai tempat & pembulatan

_TEMPAT = ["satuan", "puluhan", "ratusan", "ribuan", "puluh ribuan"]


def _digit_beda(r, banyak=5):
    d = r.sample(range(1, 10), banyak)
    return int("".join(map(str, d))), d


def nt_bulat(r):
    p, nama = r.choice([(10, "puluhan"), (100, "ratusan"), (1000, "ribuan")])
    while True:
        n = r.randint(p * 2, 99999 if p == 1000 else 9999)
        if n % p not in (0, p // 2):
            break
    bawah = n // p * p
    j = bawah + p if n % p >= p // 2 else bawah
    arah = "ke atas" if j > bawah else "ke bawah"
    lain = [bawah, bawah + p, n // (p * 10) * p * 10, n // (p * 10) * p * 10 + p * 10,
            j + p, j - p]
    if p > 10:
        lain.append(round(n / (p // 10)) * (p // 10))
    return angka(r, f"{fmt(n)} dibulatkan ke {nama} terdekat menjadi …", j,
                 f"Lihat angka di sebelah kanan {nama}. {fmt(n)} lebih dekat ke {fmt(j)}, jadi dibulatkan {arah}",
                 salah=lain)


def nt_nilai_angka(r):
    n, d = _digit_beda(r)
    i = r.randrange(5)
    nilai = d[i] * 10 ** (4 - i)
    return angka(r, f"Nilai angka {d[i]} pada bilangan {fmt(n)} adalah …", nilai,
                 f"Angka {d[i]} menempati tempat {_TEMPAT[4 - i]}, jadi nilainya {fmt(nilai)}",
                 salah=[d[i] * 10 ** k for k in range(5)])


def nt_tempat(r):
    n, d = _digit_beda(r)
    i = r.randrange(5)
    j = _TEMPAT[4 - i]
    return teks_pilihan(r, f"Angka {d[i]} pada bilangan {fmt(n)} menempati tempat …", j,
                        [t for t in _TEMPAT if t != j],
                        f"Dari kanan: satuan, puluhan, ratusan, ribuan, puluh ribuan. Angka {d[i]} ada di tempat {j}")


def nt_taksir(r):
    a, b = r.randint(110, 890), r.randint(110, 890)
    bulat = lambda x: (x + 50) // 100 * 100
    if a % 100 == 50 or b % 100 == 50:
        a, b = a + 7, b + 7
    j = bulat(a) + bulat(b)
    return angka(r, f"Taksiran hasil {a} + {b} dengan membulatkan ke ratusan terdekat adalah …", j,
                 f"{a} ≈ {bulat(a)} dan {b} ≈ {bulat(b)}, jadi {bulat(a)} + {bulat(b)} = {fmt(j)}",
                 salah=[j + 100, j - 100, j + 200, j - 200])


def nt_banding(r):
    besar = r.random() < 0.5
    kata = "terbesar" if besar else "terkecil"
    d = r.sample(range(1, 10), 4)
    semua = set()
    while len(semua) < 4:
        r.shuffle(d)
        semua.add(int("".join(map(str, d))))
    j = max(semua) if besar else min(semua)
    return teks_pilihan(r, f"Bilangan yang {kata} di antara pilihan berikut adalah …",
                        fmt(j), [fmt(x) for x in semua if x != j],
                        f"Bandingkan mulai dari angka ribuan, lalu ratusan, puluhan, satuan. Yang {kata} adalah {fmt(j)}")


def nt_panjang(r):
    n, d = _digit_beda(r)
    bagian = " + ".join(fmt(x * 10 ** (4 - i)) for i, x in enumerate(d))
    salah = [int("".join(map(str, p))) for p in
             (d[:1] + d[2:3] + d[1:2] + d[3:], d[:3] + d[4:] + d[3:4], d[1:2] + d[:1] + d[2:])]
    return angka(r, f"{bagian} = …", n,
                 f"Gabungkan sesuai nilai tempatnya: {fmt(n)}", salah=salah)


# ------------------------------------------------------------ keliling & luas

def kl_keliling_persegi(r):
    s = r.randint(5, 60)
    return angka(r, f"Sebuah persegi memiliki panjang sisi {s} cm. Kelilingnya adalah …", 4 * s,
                 f"Keliling persegi = 4 × sisi = 4 × {s} = {4 * s} cm",
                 salah=[s * s, 2 * s, 3 * s], satuan=" cm")


def kl_luas_persegi(r):
    s = r.randint(3, 25)
    return angka(r, f"Sebuah persegi memiliki panjang sisi {s} cm. Luasnya adalah …", s * s,
                 f"Luas persegi = sisi × sisi = {s} × {s} = {s * s} cm²",
                 salah=[4 * s, 2 * s, s * s + s], satuan=" cm²")


def _pp(r):
    l = r.randint(3, 20)
    return l + r.randint(2, 15), l


def kl_keliling_pp(r):
    p, l = _pp(r)
    return angka(r, f"Persegi panjang berukuran panjang {p} cm dan lebar {l} cm. Kelilingnya adalah …",
                 2 * (p + l),
                 f"Keliling = 2 × (panjang + lebar) = 2 × ({p} + {l}) = {2 * (p + l)} cm",
                 salah=[p * l, p + l, 2 * p + l], satuan=" cm")


def kl_luas_pp(r):
    p, l = _pp(r)
    return angka(r, f"Persegi panjang berukuran panjang {p} cm dan lebar {l} cm. Luasnya adalah …",
                 p * l, f"Luas = panjang × lebar = {p} × {l} = {p * l} cm²",
                 salah=[2 * (p + l), p + l, p * l + p], satuan=" cm²")


def kl_sisi_persegi(r):
    s = r.randint(4, 40)
    return angka(r, f"Keliling sebuah persegi adalah {4 * s} cm. Panjang sisinya adalah …", s,
                 f"Sisi = keliling : 4 = {4 * s} : 4 = {s} cm",
                 salah=[2 * s, 4 * s - 4], satuan=" cm")


def kl_lebar_pp(r):
    p, l = _pp(r)
    return angka(r, f"Luas sebuah persegi panjang {p * l} cm². Jika panjangnya {p} cm, lebarnya adalah …",
                 l, f"Lebar = luas : panjang = {p * l} : {p} = {l} cm",
                 salah=[p - l if p - l != l else l + 2], satuan=" cm")


def kl_keliling_segitiga(r):
    a, b = r.randint(5, 20), r.randint(5, 20)
    c = r.randint(abs(a - b) + 1, a + b - 1)
    return angka(r, f"Sebuah segitiga memiliki panjang sisi {a} cm, {b} cm, dan {c} cm. Kelilingnya adalah …",
                 a + b + c, f"Keliling segitiga = {a} + {b} + {c} = {a + b + c} cm",
                 salah=[a + b, 2 * (a + b + c)], satuan=" cm")


def kl_luas_segitiga(r):
    a, t = 2 * r.randint(2, 12), r.randint(3, 15)
    return angka(r, f"Sebuah segitiga memiliki alas {a} cm dan tinggi {t} cm. Luasnya adalah …",
                 a * t // 2,
                 f"Luas segitiga = (alas × tinggi) : 2 = ({a} × {t}) : 2 = {a * t // 2} cm²",
                 salah=[a * t, a + t, 2 * (a + t)], satuan=" cm²")


def kl_cerita(r):
    p, l = _pp(r)
    if r.random() < 0.5:
        return angka(r, f"Kebun Pak Hasan berbentuk persegi panjang dengan panjang {p} m dan lebar {l} m. "
                        f"Di sekeliling kebun akan dipasang pagar. Panjang pagar yang dibutuhkan adalah …",
                     2 * (p + l), f"Panjang pagar = keliling = 2 × ({p} + {l}) = {2 * (p + l)} m",
                     salah=[p * l, p + l], satuan=" m")
    return angka(r, f"Lantai kamar Sinta berbentuk persegi panjang dengan panjang {p} m dan lebar {l} m. "
                    f"Luas lantai kamar Sinta adalah …",
                 p * l, f"Luas = {p} × {l} = {p * l} m²",
                 salah=[2 * (p + l), p + l], satuan=" m²")


# ----------------------------------------------------------------- pengukuran

_KONVERSI = [  # (satuan besar, satuan kecil, faktor, batas atas bilangan)
    ("km", "m", 1000, 25), ("m", "cm", 100, 50), ("cm", "mm", 10, 90),
    ("kg", "gram", 1000, 20), ("kg", "ons", 10, 40), ("kuintal", "kg", 100, 30),
    ("ton", "kg", 1000, 12), ("jam", "menit", 60, 12), ("menit", "detik", 60, 15),
    ("liter", "ml", 1000, 15), ("hari", "jam", 24, 7), ("minggu", "hari", 7, 12),
    ("tahun", "bulan", 12, 9), ("lusin", "buah", 12, 12), ("kodi", "buah", 20, 9),
    ("rim", "lembar", 500, 8), ("abad", "tahun", 100, 9), ("windu", "tahun", 8, 9),
]


def uk_turun(r):
    besar, kecil, f, maks = r.choice(_KONVERSI)
    n = r.randint(2, maks)
    return angka(r, f"{n} {besar} = … {kecil}", n * f,
                 f"1 {besar} = {fmt(f)} {kecil}, jadi {n} {besar} = {n} × {fmt(f)} = {fmt(n * f)} {kecil}",
                 salah=[n * f * 10, n * f // 10 if n * f % 10 == 0 else n * f + f, n * f + f, n * f - f])


def uk_naik(r):
    besar, kecil, f, maks = r.choice(_KONVERSI)
    n = r.randint(2, maks)
    return angka(r, f"{fmt(n * f)} {kecil} = … {besar}", n,
                 f"1 {besar} = {fmt(f)} {kecil}, jadi {fmt(n * f)} {kecil} = {fmt(n * f)} : {fmt(f)} = {n} {besar}",
                 salah=[n * 10, n * f])


def uk_gabung(r):
    besar, kecil, f, maks = r.choice([k for k in _KONVERSI if k[2] >= 60])
    n = r.randint(1, min(maks, 9))
    m = r.randrange(f // 20, f, f // 20) if f % 20 == 0 else r.randint(1, f - 1)
    return angka(r, f"{n} {besar} + {fmt(m)} {kecil} = … {kecil}", n * f + m,
                 f"{n} {besar} = {fmt(n * f)} {kecil}, lalu {fmt(n * f)} + {fmt(m)} = {fmt(n * f + m)} {kecil}",
                 salah=[n + m, n * 10 + m, n * f * 10 + m, n * f - m])


def uk_waktu(r):
    jam, menit = r.randint(6, 19), r.choice(range(0, 60, 5))
    lama = r.choice([20, 25, 35, 40, 45, 50, 55, 75, 90, 105])
    tulis = lambda t: f"{t // 60 % 24:02d}.{t % 60:02d}"
    awal = jam * 60 + menit
    return teks_pilihan(
        r, f"Dina mulai belajar pukul {tulis(awal)}. Ia belajar selama {lama} menit. "
           f"Dina selesai belajar pukul …",
        tulis(awal + lama),
        [tulis(awal + lama + s) for s in (-30, -15, -10, 10, 15, 30, 60)],
        f"{tulis(awal)} ditambah {lama} menit = pukul {tulis(awal + lama)}")


def uk_banding(r):
    besar, kecil, f, maks = r.choice([k for k in _KONVERSI if k[2] in (10, 100, 1000)])
    n = r.randint(2, min(maks, 9))
    m = r.randint(1, 9) * f // 10
    return angka(r, f"{n} {besar} − {fmt(m)} {kecil} = … {kecil}", n * f - m,
                 f"{n} {besar} = {fmt(n * f)} {kecil}, lalu {fmt(n * f)} − {fmt(m)} = {fmt(n * f - m)} {kecil}",
                 salah=[n * f + m, abs(n - m), n * f])


# ---------------------------------------------------------------- soal cerita

_NAMA = ["Andi", "Budi", "Citra", "Dewi", "Eko", "Fitri", "Gilang", "Hana", "Indra",
         "Joko", "Kiki", "Lina", "Made", "Nisa", "Putu", "Rani", "Sari", "Tono", "Wayan", "Yuni"]
_BENDA = ["kelereng", "pensil", "buku tulis", "permen", "stiker", "jeruk", "kue", "manik-manik"]
_WADAH = ["kotak", "kantong", "keranjang", "dus"]
_RIBU = [1000, 2000]


def sc_tambah(r):
    a, b, c = r.randint(1200, 6000), r.randint(300, 2500), r.randint(100, 900)
    return angka(r, f"Perpustakaan sekolah memiliki {fmt(a)} buku. Tahun ini perpustakaan membeli "
                    f"{fmt(b)} buku dan menerima sumbangan {fmt(c)} buku. Jumlah buku sekarang adalah …",
                 a + b + c, f"{fmt(a)} + {fmt(b)} + {fmt(c)} = {fmt(a + b + c)} buku",
                 salah=[a + b, a + b - c], satuan=" buku")


def sc_kurang(r):
    a = r.randint(800, 5000)
    b = r.randint(150, a - 200)
    return angka(r, f"Seorang peternak mengumpulkan {fmt(a)} butir telur. Sebanyak {fmt(b)} butir "
                    f"sudah terjual. Sisa telur peternak itu adalah …",
                 a - b, f"{fmt(a)} − {fmt(b)} = {fmt(a - b)} butir",
                 salah=[a + b], satuan=" butir")


def sc_kali(r):
    n, benda, wadah = r.choice(_NAMA), r.choice(_BENDA), r.choice(_WADAH)
    k, isi = r.randint(6, 25), r.randint(8, 36)
    return angka(r, f"{n} memiliki {k} {wadah} {benda}. Setiap {wadah} berisi {isi} {benda}. "
                    f"Jumlah {benda} {n} seluruhnya adalah …",
                 k * isi, f"{k} × {isi} = {fmt(k * isi)} {benda}",
                 salah=[k + isi, k * isi + k, k * isi - isi])


def sc_bagi(r):
    n, benda = r.choice(_NAMA), r.choice(_BENDA)
    k, q = r.randint(4, 12), r.randint(6, 30)
    return angka(r, f"{n} memiliki {k * q} {benda} yang dibagikan sama banyak kepada {k} temannya. "
                    f"Setiap teman mendapat …",
                 q, f"{k * q} : {k} = {q} {benda}", salah=[k * q - k, q + k])


def sc_harga(r):
    n = r.choice(_NAMA)
    k, harga = r.randint(3, 12), r.randint(3, 15) * 500
    return angka(r, f"{n} membeli {k} buku tulis. Harga satu buku tulis Rp{fmt(harga)}. "
                    f"Uang yang harus dibayar {n} adalah …",
                 k * harga, f"{k} × Rp{fmt(harga)} = Rp{fmt(k * harga)}",
                 salah=[k * harga + harga, k * harga - harga, k * harga + 1000, harga + k * 100],
                 awalan="Rp", langkah=_RIBU)


def sc_kembalian(r):
    n = r.choice(_NAMA)
    bayar = r.choice([20000, 50000, 100000])
    harga = r.randint(5, bayar // 500 - 3) * 500
    return angka(r, f"{n} membeli alat tulis seharga Rp{fmt(harga)}. Ia membayar dengan uang "
                    f"Rp{fmt(bayar)}. Uang kembalian yang diterima {n} adalah …",
                 bayar - harga, f"Rp{fmt(bayar)} − Rp{fmt(harga)} = Rp{fmt(bayar - harga)}",
                 salah=[bayar - harga + 1000, bayar - harga - 1000, bayar - harga + 500, bayar + harga],
                 awalan="Rp", langkah=_RIBU)


def sc_dua_langkah(r):
    k, berat = r.randint(8, 30), r.choice([20, 25, 40, 50])
    jual = r.randint(5, k * berat // 10 - 2) * 5
    return angka(r, f"Pak Tani memanen {k} karung beras. Setiap karung beratnya {berat} kg. "
                    f"Sebanyak {fmt(jual)} kg beras dijual. Sisa beras Pak Tani adalah …",
                 k * berat - jual,
                 f"{k} × {berat} = {fmt(k * berat)} kg, lalu {fmt(k * berat)} − {fmt(jual)} = {fmt(k * berat - jual)} kg",
                 salah=[k * berat, k * berat + jual], satuan=" kg")


def sc_bus(r):
    k, isi, lebih = r.randint(3, 9), r.randint(28, 55), r.randint(3, 20)
    return angka(r, f"Siswa kelas 4 pergi berwisata menggunakan {k} bus. Setiap bus berisi {isi} siswa. "
                    f"Ada pula {lebih} siswa yang naik mobil. Jumlah seluruh siswa yang ikut adalah …",
                 k * isi + lebih, f"({k} × {isi}) + {lebih} = {k * isi} + {lebih} = {k * isi + lebih} siswa",
                 salah=[k * isi, k * (isi + lebih), k + isi + lebih], satuan=" siswa")


def sc_tabung(r):
    n = r.choice(_NAMA)
    hari, uang = r.randint(6, 30), r.randint(2, 10) * 500
    return angka(r, f"{n} menabung Rp{fmt(uang)} setiap hari. Jumlah tabungan {n} setelah {hari} hari adalah …",
                 hari * uang, f"{hari} × Rp{fmt(uang)} = Rp{fmt(hari * uang)}",
                 salah=[hari * uang + uang, hari * uang - uang, hari * uang + 2 * uang, hari * uang + 5000],
                 awalan="Rp", langkah=_RIBU)


def sc_rata(r):
    k, q = r.randint(4, 9), r.randint(12, 45)
    a = r.randint(q, k * q - q)
    b = k * q - a
    return angka(r, f"Bu Ani memetik {a} buah mangga pada pagi hari dan {b} buah pada sore hari. "
                    f"Semua mangga dimasukkan sama banyak ke dalam {k} keranjang. Isi setiap keranjang adalah …",
                 q, f"{a} + {b} = {k * q}, lalu {k * q} : {k} = {q} buah",
                 salah=[k * q, q + k], satuan=" buah")


def sc_lari(r):
    n = r.choice(_NAMA)
    k, m = r.randint(3, 12), r.choice([150, 200, 250, 300, 400])
    return angka(r, f"{n} berlari mengelilingi lapangan sebanyak {k} kali. Keliling lapangan {m} m. "
                    f"Jarak yang ditempuh {n} adalah …",
                 k * m, f"{k} × {m} = {fmt(k * m)} m",
                 salah=[k * m + m, k * m - m, k + m], satuan=" m")


# ------------------------------------------------------------------- perakit

PEMBANGKIT = {
    "tambah-kurang": [tk_tambah, tk_tambah_besar, tk_kurang, tk_hilang_tambah, tk_hilang_kurang, tk_campur],
    "perkalian": [kali_1, kali_2, kali_3, kali_10, kali_hilang, kali_tiga],
    "pembagian": [bagi_1, bagi_2, bagi_sisa, bagi_hilang, bagi_10, bagi_campur],
    "pecahan": [pc_senilai, pc_sederhana, pc_tambah, pc_kurang, pc_banding, pc_campuran, pc_desimal, pc_dari],
    "kpk-fpb": [kf_kpk, kf_fpb, kf_faktor, kf_kelipatan, kf_prima, kf_faktorisasi, kf_banyak_faktor],
    "pembulatan": [nt_bulat, nt_nilai_angka, nt_tempat, nt_taksir, nt_banding, nt_panjang],
    "keliling-luas": [kl_keliling_persegi, kl_luas_persegi, kl_keliling_pp, kl_luas_pp, kl_sisi_persegi,
                      kl_lebar_pp, kl_keliling_segitiga, kl_luas_segitiga, kl_cerita],
    "pengukuran": [uk_turun, uk_naik, uk_gabung, uk_waktu, uk_banding],
    "soal-cerita": [sc_tambah, sc_kurang, sc_kali, sc_bagi, sc_harga, sc_kembalian, sc_dua_langkah,
                    sc_bus, sc_tabung, sc_rata, sc_lari],
}

KODE_TOPIK = [t["kode"] for t in TOPIK]


def nama_topik(kode):
    return next((t["nama"] for t in TOPIK if t["kode"] == kode), kode)


def buat_latihan(topik, jumlah=JUMLAH_SOAL, rng=None):
    """Buat ``jumlah`` soal berbeda untuk satu topik (atau 'campuran')."""
    if topik not in KODE_TOPIK:
        raise ValueError(f"topik tidak dikenal: {topik}")
    r = rng or random.Random()
    if topik == "campuran":
        kode = list(PEMBANGKIT)
        r.shuffle(kode)
        urutan = [kode[i % len(kode)] for i in range(jumlah)]
        r.shuffle(urutan)
    else:
        urutan = [topik] * jumlah

    hasil, terpakai = [], set()
    for kode in urutan:
        for _ in range(200):
            soal = r.choice(PEMBANGKIT[kode])(r)
            if soal["teks"] not in terpakai:
                break
        else:
            raise RuntimeError(f"gagal membuat soal unik untuk topik {kode}")
        terpakai.add(soal["teks"])
        hasil.append(soal)
    return hasil
