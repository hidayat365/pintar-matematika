"""Pembangkit soal Bahasa Inggris SD kelas 4.

Pembagian topik mengikuti buku siswa Kemendikbudristek "My Next Words Grade 4"
(Unit 1-7 semester 1, Unit 8-12 semester 2). Kosakata dan pola kalimat dari
kisi-kisi Tes Sumatif 3 dimasukkan ke unit yang sesuai dan juga tersedia sebagai
paket latihan tersendiri.

Bentuk soal sama dengan ``soal.py``: dict berisi "teks", "pilihan", "benar",
"pembahasan", ditambah "gambar" (SVG) atau "bacaan" (teks bacaan) bila ada.
Soal ditulis dalam bahasa Inggris, pembahasan dalam bahasa Indonesia.
"""

import random
from math import cos, radians, sin

from soal import JUMLAH_SOAL, _svg, rakit, teks_pilihan

S1, S2, GAB = "Semester 1", "Semester 2", "Gabungan"

TOPIK = [
    {"kode": "en-unit-1", "nama": "Unit 1 · What Are You Doing?", "ikon": "🏃", "kelompok": S1,
     "ket": "Kegiatan yang sedang dilakukan (is/am/are + -ing)"},
    {"kode": "en-unit-2", "nama": "Unit 2 · There Are 67 English Books", "ikon": "🔢", "kelompok": S1,
     "ket": "Bilangan 1–100, plus/minus, how many"},
    {"kode": "en-unit-3", "nama": "Unit 3 · My Living Room is Beside Kitchen", "ikon": "🏠", "kelompok": S1,
     "ket": "Nama ruangan, beside/between, clean/dirty/tidy"},
    {"kode": "en-unit-4", "nama": "Unit 4 · Cici Cooks in The Kitchen", "ikon": "🍳", "kelompok": S1,
     "ket": "Kegiatan di rumah: cooks, don't/doesn't, do/does"},
    {"kode": "en-unit-5", "nama": "Unit 5 · Where Is My Pencil?", "ikon": "🛋️", "kelompok": S1,
     "ket": "Benda di ruang tamu & kamar tidur, there is/are, in/on/under"},
    {"kode": "en-unit-6", "nama": "Unit 6 · The Stove is in The Kitchen", "ikon": "🧼", "kelompok": S1,
     "ket": "Benda di kamar mandi & dapur, do not/does not"},
    {"kode": "en-unit-7", "nama": "Unit 7 · I Can Make Fried Egg in The Kitchen", "ikon": "🍲", "kelompok": S1,
     "ket": "Can/can't dan kata kerja memasak"},
    {"kode": "en-unit-8", "nama": "Unit 8 · Be On Time!", "ikon": "🕒", "kelompok": S2,
     "ket": "Membaca jam: o'clock, half past, quarter past/to"},
    {"kode": "en-unit-9", "nama": "Unit 9 · I Go to School after Having Breakfast", "ikon": "🌅", "kelompok": S2,
     "ket": "Kegiatan sehari-hari, before/after"},
    {"kode": "en-unit-10", "nama": "Unit 10 · He Always Gets Up at 5 O'clock", "ikon": "⏰", "kelompok": S2,
     "ket": "Always, usually, sometimes, never; bacaan"},
    {"kode": "en-unit-11", "nama": "Unit 11 · How Do You Go to School?", "ikon": "🚌", "kelompok": S2,
     "ket": "Nama kendaraan, by … dan on foot"},
    {"kode": "en-unit-12", "nama": "Unit 12 · He Goes to School by Bike", "ikon": "🚲", "kelompok": S2,
     "ket": "Kalimat go/goes to … at … by …"},
    {"kode": "en-semester-1", "nama": "Semester 1 Review", "ikon": "🌈", "kelompok": GAB,
     "ket": "Gabungan Unit 1–7"},
    {"kode": "en-semester-2", "nama": "Semester 2 Review", "ikon": "🌟", "kelompok": GAB,
     "ket": "Gabungan Unit 8–12"},
    {"kode": "en-ts3", "nama": "Latihan Tes Sumatif 3", "ikon": "📝", "kelompok": GAB,
     "ket": "Sesuai kisi-kisi: benda di rumah, there is/are, alat dapur, do/does"},
]


# ---------------------------------------------------------------- alat bantu

def _k(soal, *kunci):
    """Beri penanda keunikan untuk soal yang teks pertanyaannya selalu sama."""
    soal["kunci"] = kunci
    return soal


def _arti(r, kamus, ke_inggris):
    """Soal arti kata dari ``kamus`` {inggris: indonesia}; pengecoh dari kamus yang sama."""
    en, idn = r.choice(list(kamus.items()))
    if ke_inggris:
        return teks_pilihan(r, f'What is "{idn}" in English?', en,
                            r.sample([k for k in kamus if k != en], 3),
                            f'"{idn}" dalam bahasa Inggris adalah "{en}"')
    return teks_pilihan(r, f'What is the meaning of "{en}" in Indonesian?', idn,
                        r.sample(sorted({v for v in kamus.values() if v != idn}), 3),
                        f'"{en}" artinya "{idn}"')


def _teks_svg(x, y, isi, ukuran=13):
    return (f'<text x="{x}" y="{y}" font-size="{ukuran}" font-family="sans-serif" font-weight="bold" '
            f'text-anchor="middle" fill="#1d2440" stroke="none">{isi}</text>')


def _dari_bacaan(r, atribut, pembuat):
    """Ambil satu pertanyaan dari kumpulan bacaan yang dipakai bersama dalam satu latihan."""
    if not hasattr(r, atribut):
        setattr(r, atribut, pembuat(r))
    bacaan, tanya, jawab, salah, kalimat = r.choice(getattr(r, atribut))
    soal = teks_pilihan(r, tanya, jawab, salah, f'Jawabannya ada pada kalimat: "{kalimat}"')
    soal["bacaan"] = bacaan
    return soal


def _ing(dasar):
    if dasar in ("get", "swim", "run", "sit", "cut"):
        return dasar + dasar[-1] + "ing"
    return (dasar[:-1] if dasar.endswith("e") else dasar) + "ing"


def _frasa(kata, objek):
    return f"{kata} {objek}".strip()


PEREMPUAN = ["Aisyah", "Cici", "Lili", "Gita"]
LAKI = ["Joshua", "Made", "Ujang", "Bagas", "Fahri", "Budi"]

# (subjek, to be, kata ganti, bentuk di tengah kalimat)
TUNGGAL = [("He", "is", "He", "he"), ("She", "is", "She", "she"), ("My father", "is", "He", "my father"),
           ("My mother", "is", "She", "my mother"), ("Mr. Ilham", "is", "He", "Mr. Ilham"),
           ("Mrs. Neneng", "is", "She", "Mrs. Neneng")] + \
          [(n, "is", "She", n) for n in PEREMPUAN] + [(n, "is", "He", n) for n in LAKI]
JAMAK = [("You", "are", "You", "you"), ("We", "are", "We", "we"), ("They", "are", "They", "they"),
         ("Aisyah and Cici", "are", "They", "Aisyah and Cici"),
         ("Joshua and Made", "are", "They", "Joshua and Made"),
         ("The students", "are", "They", "the students")]
SAYA = ("I", "am", "I", "I")


def _subjek(r, dengan_saya=True):
    return r.choice(TUNGGAL + JAMAK * 3 + ([SAYA] * 4 if dengan_saya else []))


# ====================================================== Unit 1 · present continuous

# (kata kerja dasar, bentuk -s, bentuk -ing, lanjutan kalimat, arti bentuk -ing)
KERJA_1 = [
    ("read", "reads", "reading", "a book in the library", "membaca"),
    ("write", "writes", "writing", "in the classroom", "menulis"),
    ("discuss", "discusses", "discussing", "in the classroom", "berdiskusi"),
    ("dance", "dances", "dancing", "in the classroom", "menari"),
    ("watch", "watches", "watching", "TV in the living room", "menonton"),
    ("borrow", "borrows", "borrowing", "books in the library", "meminjam"),
    ("buy", "buys", "buying", "snacks in the canteen", "membeli"),
    ("play", "plays", "playing", "marbles in the schoolyard", "bermain"),
    ("drink", "drinks", "drinking", "water in the canteen", "minum"),
    ("eat", "eats", "eating", "in the canteen", "makan"),
    ("clean", "cleans", "cleaning", "the classroom", "membersihkan"),
    ("swim", "swims", "swimming", "in the swimming pool", "berenang"),
    ("draw", "draws", "drawing", "a picture", "menggambar"),
    ("go", "goes", "going", "to school by bike", "pergi"),
]
SEKARANG = ["now", "right now"]


def u1_tobe(r):
    s, be, _, _ = _subjek(r)
    _, _, ing, sisa, _ = r.choice(KERJA_1)
    return teks_pilihan(r, f"{s} ___ {ing} {sisa} {r.choice(SEKARANG)}.", be,
                        [x for x in ("am", "is", "are", "do") if x != be],
                        f'Kegiatan yang sedang berlangsung: subjek + am/is/are + kata kerja-ing. Untuk "{s}" dipakai "{be}"')


def u1_ing(r):
    s, be, _, _ = _subjek(r)
    dasar, es, ing, sisa, _ = r.choice(KERJA_1)
    return teks_pilihan(r, f"{s} {be} ___ {sisa} {r.choice(SEKARANG)}.", ing, [dasar, es, f"to {dasar}"],
                        f'Setelah "{be}" pada kegiatan yang sedang berlangsung, kata kerja diberi -ing: {ing}')


def u1_ejaan(r):
    jenis = r.randrange(3)
    if jenis == 0:
        d = r.choice(["swim", "run", "sit", "cut", "clap", "stop"])
        jawab, salah = d + d[-1] + "ing", [d + "ing", d + "eing", d + d[-1] + "eing"]
        aturan = "konsonan terakhir digandakan lalu ditambah -ing"
    elif jenis == 1:
        d = r.choice(["write", "dance", "have", "make", "ride", "take", "come"])
        jawab, salah = d[:-1] + "ing", [d + "ing", d[:-1] + d[-2] + "ing", d[:-1] + "ng"]
        aturan = "huruf e di akhir dihilangkan lalu ditambah -ing"
    else:
        d = r.choice(["read", "play", "eat", "drink", "clean", "borrow", "buy", "draw", "discuss", "go"])
        jawab, salah = d + "ing", [d + d[-1] + "ing", d + "eing", d[:-1] + "ing"]
        aturan = "cukup ditambah -ing"
    return teks_pilihan(r, f'The -ing form of "{d}" is …', jawab, salah, f'"{d}" → "{jawab}": {aturan}')


def u1_tanya(r):
    dasar, es, ing, sisa, _ = r.choice(KERJA_1)
    pilih = r.randrange(5)
    if pilih == 0:
        tanya, ganti, be = f"is {r.choice(PEREMPUAN)}", "She", "is"
    elif pilih == 1:
        tanya, ganti, be = f"is {r.choice(LAKI)}", "He", "is"
    elif pilih == 2:
        tanya, ganti, be = "are you", "I", "am"
    elif pilih == 3:
        tanya, ganti, be = "are the students", "They", "are"
    else:
        tanya, ganti, be = f"are {r.choice(LAKI)} and {r.choice(PEREMPUAN)}", "They", "are"
    lain = "are" if be != "are" else "is"
    return teks_pilihan(r, f"What {tanya} doing? {ganti} ___ {sisa}.", f"{be} {ing}",
                        [es, dasar, f"{lain} {ing}", ing],
                        f'"What … doing?" dijawab dengan {be} + kata kerja-ing: {ganti} {be} {ing} {sisa}.')


_ARTI_1 = {k[2]: k[4] for k in KERJA_1}


def u1_arti(r):
    return _arti(r, _ARTI_1, r.random() < 0.5)


def u1_kalimat(r):
    s, be, _, _ = _subjek(r)
    dasar, _, ing, sisa, _ = r.choice(KERJA_1)
    lain = "are" if be != "are" else "is"
    benar = f"{s} {be} {ing} {sisa}."
    return _k(teks_pilihan(r, "Which sentence is correct?", benar,
                           [f"{s} {lain} {ing} {sisa}.", f"{s} {be} {dasar} {sisa}.", f"{s} {ing} {sisa}."],
                           f"Polanya subjek + am/is/are + kata kerja-ing: {benar}"), "u1-kalimat", benar)


_TEMPAT_1 = [("borrowing books", "library"), ("reading books", "library"), ("having lunch", "canteen"),
             ("buying snacks", "canteen"), ("playing marbles", "schoolyard"),
             ("playing football", "schoolyard"), ("swimming", "swimming pool")]


def u1_tempat(r):
    kegiatan, tempat = r.choice(_TEMPAT_1)
    s, be, _, _ = r.choice(TUNGGAL + JAMAK)
    return teks_pilihan(r, f"{s} {be} {kegiatan} in the ___.", tempat,
                        [t for t in ("library", "canteen", "schoolyard", "swimming pool", "bathroom")
                         if t != tempat],
                        f'Kegiatan "{kegiatan}" dilakukan di "{tempat}"')


# ============================================================ Unit 2 · bilangan

SATUAN = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
          "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen",
          "nineteen"]
PULUHAN = {2: "twenty", 3: "thirty", 4: "forty", 5: "fifty", 6: "sixty", 7: "seventy", 8: "eighty",
           9: "ninety"}


def kata_bilangan(n):
    if n < 20:
        return SATUAN[n]
    if n == 100:
        return "one hundred"
    return PULUHAN[n // 10] + (f"-{SATUAN[n % 10]}" if n % 10 else "")


def _mirip(r, n):
    """Tiga bilangan lain yang mudah tertukar dengan n."""
    calon = [n % 10 * 10 + n // 10, n + 10, n - 10, n + 1, n - 1, n // 10 + 10, n % 10 + 10, n + 2, n - 2]
    calon = [c for c in dict.fromkeys(calon) if 1 <= c <= 100 and c != n]
    r.shuffle(calon)
    return calon[:3]


def u2_kata(r):
    n = r.randint(21, 100)
    return teks_pilihan(r, f"How do we write the number {n} in words?", kata_bilangan(n),
                        [kata_bilangan(c) for c in _mirip(r, n)], f'{n} ditulis "{kata_bilangan(n)}"')


def u2_angka(r):
    n = r.randint(21, 99)
    return teks_pilihan(r, f'The number for "{kata_bilangan(n)}" is …', n, _mirip(r, n),
                        f'"{kata_bilangan(n)}" adalah {n}')


def u2_hitung(r):
    if r.random() < 0.5:
        a = r.randint(10, 80)
        b = r.randint(2, 100 - a)
        hasil, tanda, baca = a + b, "+", "plus"
    else:
        a = r.randint(20, 100)
        b = r.randint(2, a - 5)
        hasil, tanda, baca = a - b, "−", "minus"
    teks = (f"{a} {tanda} {b} = …" if r.random() < 0.5
            else f"{kata_bilangan(a).capitalize()} {baca} {kata_bilangan(b)} is …")
    return teks_pilihan(r, teks, kata_bilangan(hasil), [kata_bilangan(x) for x in _mirip(r, hasil)],
                        f'{a} {tanda} {b} = {hasil}, dalam bahasa Inggris "{kata_bilangan(hasil)}"')


def u2_simbol(r):
    teks, jawab, arti = r.choice([
        ('In "25 + 15", we read the symbol "+" as …', "plus", "tambah"),
        ('In "75 − 3", we read the symbol "−" as …', "minus", "kurang"),
        ('In "40 − 2 = 38", we read the symbol "=" as …', "is", "sama dengan"),
    ])
    return teks_pilihan(r, teks, jawab, [x for x in ("plus", "minus", "is", "many") if x != jawab],
                        f'Tanda itu dibaca "{jawab}" ({arti})')


def u2_antara(r):
    n = r.randint(22, 98)
    return teks_pilihan(r, f"My number is between {n - 1} and {n + 1}. What is my number?",
                        kata_bilangan(n), [kata_bilangan(c) for c in _mirip(r, n)],
                        f'Bilangan di antara {n - 1} dan {n + 1} adalah {n}, yaitu "{kata_bilangan(n)}"')


def u2_urutan(r):
    if r.random() < 0.4:
        n, langkah = r.choice([30, 40, 50, 60, 70, 80, 90]), 10
        lain = [n + 10, n + 20 if n < 90 else n - 30, n // 10 + 10]
    else:
        n, langkah = r.randint(23, 99), 1
        lain = _mirip(r, n)
    deret = ", ".join(kata_bilangan(x) for x in (n - 2 * langkah, n - langkah)) + ", ___"
    return teks_pilihan(r, f"What comes next? {deret.capitalize()}", kata_bilangan(n),
                        [kata_bilangan(x) for x in lain],
                        f'Bilangannya bertambah {langkah}, jadi berikutnya {n}: "{kata_bilangan(n)}"')


def u2_how_many(r):
    n = r.randint(21, 99)
    benda = r.choice(["English books", "pencils", "chairs", "marbles", "students", "flowers", "notebooks"])
    a, b = _mirip(r, n)[:2]
    return teks_pilihan(r, f"There are {n} {benda}. How many {benda} are there?",
                        f"There are {kata_bilangan(n)}.",
                        [f"There are {kata_bilangan(a)}.", f"There are {kata_bilangan(b)}.",
                         f"There is {kata_bilangan(n)}."],
                        f'{n} = "{kata_bilangan(n)}", dan untuk benda lebih dari satu dipakai "There are"')


# ================================================ Unit 3 · ruangan dan keadaannya

RUANGAN = {"living room": "ruang tamu", "bedroom": "kamar tidur", "bathroom": "kamar mandi",
           "dining room": "ruang makan", "kitchen": "dapur", "garage": "garasi"}
SIFAT = {"clean": "bersih", "dirty": "kotor", "big": "besar", "large": "luas", "tidy": "rapi",
         "empty": "kosong", "small": "kecil", "messy": "berantakan"}
_KEGIATAN_RUANG = [("cook our food", "kitchen"), ("sleep at night", "bedroom"), ("take a bath", "bathroom"),
                   ("sit and watch TV with the family", "living room"),
                   ("eat together at the table", "dining room"), ("park the car", "garage")]


def u3_arti_ruang(r):
    return _arti(r, RUANGAN, r.random() < 0.5)


def u3_kegiatan(r):
    kegiatan, ruang = r.choice(_KEGIATAN_RUANG)
    return teks_pilihan(r, f"We {kegiatan} in the ___.", ruang,
                        r.sample([x for x in RUANGAN if x != ruang], 3), f'"{ruang}" artinya {RUANGAN[ruang]}')


def u3_arti_sifat(r):
    return _arti(r, SIFAT, r.random() < 0.5)


def u3_lawan(r):
    kata, lawan = r.choice([("clean", "dirty"), ("dirty", "clean"), ("tidy", "messy"), ("messy", "tidy"),
                            ("big", "small"), ("small", "big"), ("empty", "full")])
    lain = [x for x in ("clean", "dirty", "tidy", "messy", "big", "small", "empty", "full")
            if x not in (kata, lawan)]
    return teks_pilihan(r, f'The opposite of "{kata}" is …', lawan, r.sample(lain, 3),
                        f'Lawan kata "{kata}" adalah "{lawan}"')


def u3_keadaan(r):
    ruang = r.choice(list(RUANGAN))
    teks, jawab, salah = r.choice([
        (f"The {ruang} is not dirty. It is ___.", "clean", ["empty", "messy", "small"]),
        (f"Nobody cleans the {ruang}. It is very ___.", "dirty", ["clean", "tidy", "empty"]),
        (f"There is nothing in the {ruang}. It is ___.", "empty", ["dirty", "tidy", "full"]),
        (f"Everything in the {ruang} is in the right place. The {ruang} is ___.", "tidy",
         ["messy", "dirty", "empty"]),
        (f"Many people can sit in the {ruang}. It is ___.", "large", ["small", "empty", "dirty"]),
    ])
    return teks_pilihan(r, teks, jawab, salah, f'"{jawab}" artinya {SIFAT[jawab]}')


def u3_how_where(r):
    ruang, nama = r.choice(list(RUANGAN)), r.choice(PEREMPUAN + LAKI)
    a, b = r.choice([("large", "clean"), ("big", "tidy"), ("small", "dirty"), ("clean", "tidy")])
    teks, jawab, pilihan, bahas = r.choice([
        (f"How is the {ruang}? It ___ {a} and {b}.", "is", ("is", "are", "am", "be"),
         f'Satu ruangan memakai "is": It is {a} and {b}.'),
        (f"___ is the {ruang}? It is {a} and {b}.", "How", ("How", "Where", "Who", "When"),
         '"How" menanyakan keadaan (bagaimana)'),
        (f"___ is {nama}? {nama} is in the {ruang}.", "Where", ("How", "Where", "What", "When"),
         '"Where" menanyakan tempat (di mana)'),
        (f"Where is {nama}? {nama} is ___ the {ruang}.", "in", ("in", "on", "under", "between"),
         f'Berada di dalam ruangan memakai "in": in the {ruang}'),
    ])
    return teks_pilihan(r, teks, jawab, [x for x in pilihan if x != jawab], bahas)


def _denah(ruang):
    isi = ""
    for i, nama in enumerate(ruang):
        x = 8 + i * 69
        isi += f'<rect x="{x}" y="40" width="66" height="70" fill="#e3e9ff"/>'
        kata = nama.split()
        if len(kata) == 1:
            isi += _teks_svg(x + 33, 80, nama, 11)
        else:
            isi += _teks_svg(x + 33, 72, kata[0], 11) + _teks_svg(x + 33, 88, kata[1], 11)
    return _svg(isi)


def u3_denah(r):
    a, b, c, lain = r.sample(list(RUANGAN), 4)
    if r.random() < 0.5:
        soal = teks_pilihan(r, f"Look at the picture. Which room is between the {a} and the {c}?",
                            f"the {b}", [f"the {a}", f"the {c}", f"the {lain}"],
                            f'"between" = di antara. Ruangan di antara {a} dan {c} adalah {b}')
    else:
        benar = r.choice([f"The {b} is between the {a} and the {c}.", f"The {a} is beside the {b}.",
                          f"The {c} is beside the {b}."])
        soal = teks_pilihan(r, "Look at the picture. Which sentence is correct?", benar,
                            [f"The {a} is beside the {c}.", f"The {a} is between the {b} and the {c}.",
                             f"The {c} is between the {a} and the {b}.", f"The {b} is beside the {lain}."],
                            '"beside" = di samping (bersebelahan), "between" = di antara dua ruangan')
    soal["gambar"] = _denah([a, b, c])
    return _k(soal, "denah", a, b, c, soal["teks"])


# ================================================= Unit 4 · simple present di rumah

# (kata kerja dasar, bentuk -s, objek, ruangan)
KERJA_4 = [("sleep", "sleeps", "", "bedroom"), ("study", "studies", "", "bedroom"),
           ("have", "has", "breakfast", "dining room"), ("play", "plays", "", "yard"),
           ("cook", "cooks", "", "kitchen"), ("watch", "watches", "TV", "living room"),
           ("read", "reads", "a book", "living room"), ("take", "takes", "a bath", "bathroom"),
           ("eat", "eats", "", "dining room"), ("wash", "washes", "the dishes", "kitchen")]


def u4_positif(r):
    s, be, _, _ = _subjek(r)
    dasar, es, objek, ruang = r.choice(KERJA_4)
    jawab = es if be == "is" else dasar
    alasan = ("He/She/nama satu orang: kata kerja ditambah -s/-es" if be == "is"
              else "I/You/We/They: kata kerja tetap bentuk dasar")
    return teks_pilihan(r, f"{s} {_frasa('___', objek)} in the {ruang}.", jawab,
                        [x for x in (dasar, es, _ing(dasar), f"{be} {dasar}") if x != jawab],
                        f"{alasan}: {s} {_frasa(jawab, objek)} in the {ruang}.")


def u4_negatif(r, lengkap=False):
    s, be, _, _ = _subjek(r)
    dasar, _, objek, ruang = r.choice(KERJA_4)
    if lengkap:
        jawab, pilihan = ("does not" if be == "is" else "do not"), ("do not", "does not", "is not", "are not")
    else:
        jawab, pilihan = ("doesn't" if be == "is" else "don't"), ("don't", "doesn't", "isn't", "aren't")
    return teks_pilihan(r, f"{s} ___ {_frasa(dasar, objek)} in the {ruang}.", jawab,
                        [x for x in pilihan if x != jawab],
                        f'Kalimat negatif untuk "{s}" memakai "{jawab}" + kata kerja dasar')


def u4_tanya(r):
    _, be, _, tengah = _subjek(r, dengan_saya=False)
    dasar, _, objek, ruang = r.choice(KERJA_4)
    jawab = "Does" if be == "is" else "Do"
    return teks_pilihan(r, f"___ {tengah} {_frasa(dasar, objek)} in the {ruang}?", jawab,
                        [x for x in ("Do", "Does", "Is", "Are") if x != jawab],
                        f'Kalimat tanya untuk "{tengah}" diawali "{jawab}" + kata kerja dasar')


_PENANYA = [("they", "they", "do"), ("you", "I", "do"), ("Budi", "he", "does"), ("Gita", "she", "does"),
            ("Cici", "she", "does"), ("Joshua", "he", "does"), ("Aisyah and Cici", "they", "do"),
            ("your father", "he", "does"), ("your mother", "she", "does")]
_GANTI_SALAH = {"he": "she", "she": "he", "they": "he", "I": "you"}


def u4_respon(r):
    subjek, ganti, bantu = r.choice(_PENANYA)
    dasar, _, objek, ruang = r.choice(KERJA_4)
    ya = r.random() < 0.5
    akhir = lambda b: b if ya else b + "n't"
    lain = "do" if bantu == "does" else "does"
    jawab = f"{ganti} {akhir(bantu)}"
    return teks_pilihan(
        r, f"{bantu.capitalize()} {subjek} {_frasa(dasar, objek)} in the {ruang}? {'Yes' if ya else 'No'}, ___.",
        jawab, [f"{ganti} {akhir(lain)}", f"{_GANTI_SALAH[ganti]} {akhir(bantu)}",
                f"{ganti} {'is' if ya else 'is not'}"],
        f'Pertanyaan diawali "{bantu.capitalize()}" dan "{subjek}" diganti "{ganti}", jadi jawabannya "{jawab}"')


def u4_what_does(r):
    s, _, ganti, _ = r.choice([t for t in TUNGGAL if t[0] not in ("He", "She")])
    dasar, es, objek, ruang = r.choice(KERJA_4)
    lawan = "He" if ganti == "She" else "She"
    return teks_pilihan(r, f"What does {s} do in the {ruang}?", f"{ganti} {_frasa(es, objek)}.",
                        [f"{ganti} {_frasa(dasar, objek)}.", f"{lawan} {_frasa(es, objek)}.",
                         f"{ganti} {_frasa(_ing(dasar), objek)}."],
                        f'"{s}" diganti "{ganti}", dan kata kerjanya ditambah -s/-es: {ganti} {_frasa(es, objek)}.')


def u4_bentuk_s(r):
    dasar, es = r.choice([(k[0], k[1]) for k in KERJA_4] + [("go", "goes"), ("drink", "drinks"),
                                                            ("brush", "brushes"), ("help", "helps")])
    calon = {dasar, dasar + "s", dasar + "es", _ing(dasar),
             dasar[:-1] + "ies" if dasar.endswith("y") else dasar + "ies"} - {es}
    return teks_pilihan(r, f'With "he" or "she", the verb "{dasar}" becomes …', es, r.sample(sorted(calon), 3),
                        f'He/She {es}: kata kerja "{dasar}" berubah menjadi "{es}"')


def u4_kegiatan_ruang(r):
    kegiatan, ruang = r.choice([("take a bath", "bathroom"), ("cook", "kitchen"), ("sleep", "bedroom"),
                                ("have dinner", "dining room"), ("watch TV", "living room")])
    lain = [k for k in ("take a bath", "cook", "sleep", "have dinner", "watch TV", "play football")
            if k != kegiatan]
    return teks_pilihan(r, f"What do we usually do in the {ruang}?", f"We {kegiatan}.",
                        [f"We {k}." for k in r.sample(lain, 3)],
                        f'Di {RUANGAN[ruang]} ("{ruang}") kita biasanya "{kegiatan}"')


# ==================================== Unit 5 & 6 · benda di dalam rumah (dan kisi-kisi)

RUANG_TAMU = {"clock": "jam dinding", "picture": "gambar", "painting": "lukisan", "shelf": "rak",
              "television": "televisi", "cupboard": "lemari", "lamp": "lampu", "vase": "vas bunga",
              "table": "meja", "stool": "kursi kecil", "carpet": "karpet", "side table": "meja sisi"}
KAMAR_TIDUR = {"wardrobe": "lemari pakaian", "pillow": "bantal", "blanket": "selimut", "bolster": "guling",
               "bed": "kasur", "chair": "kursi", "mirror": "cermin", "desk": "meja belajar",
               "bookshelf": "rak buku", "desk lamp": "lampu meja"}
KAMAR_MANDI = {"toothbrush": "sikat gigi", "shampoo": "sampo", "soap": "sabun", "toothpaste": "pasta gigi",
               "towel": "handuk", "dipper": "gayung", "bathtub": "bak mandi", "mirror": "cermin",
               "sink": "penampung air basuh", "tap": "keran", "toilet paper": "kertas toilet",
               "bathroom shelf": "rak di kamar mandi"}
DAPUR = {"plate": "piring", "spoon": "sendok", "fork": "garpu", "glass": "gelas", "bowl": "mangkuk",
         "pan": "wajan", "stove": "kompor", "frying pan": "penggorengan", "cooking oil": "minyak goreng",
         "spice container": "wadah bumbu", "cabinet": "tempat penyimpanan", "trash bin": "tempat sampah",
         "turner": "pembalik", "chopping board": "papan potong", "grater": "pemarut", "kettle": "teko",
         "knife": "pisau", "oven": "pemanggang", "peeler": "pengupas", "pot": "panci"}
BENDA_5 = {**RUANG_TAMU, **KAMAR_TIDUR}
BENDA_6 = {**KAMAR_MANDI, **DAPUR}

# Benda yang jelas hanya ada di satu ruangan.
KHAS = {"bedroom": ["pillow", "blanket", "bolster", "bed", "wardrobe"],
        "living room": ["sofa", "television"],
        "bathroom": ["toothbrush", "soap", "shampoo", "towel", "bathtub", "toothpaste", "dipper"],
        "kitchen": ["stove", "frying pan", "kettle", "chopping board", "grater", "cooking oil"]}
_TAK_BERBILANG = {"soap", "shampoo", "toothpaste", "cooking oil"}


def _sandang(kata):
    if kata in _TAK_BERBILANG:
        return kata
    return f"{'an' if kata[0] in 'aeiou' else 'a'} {kata}"


def _di_ruang(r, ruang_pilihan):
    ruang = r.choice(ruang_pilihan)
    benda = r.choice(KHAS[ruang])
    if r.random() < 0.5:
        return teks_pilihan(r, f"Where do we usually find {_sandang(benda)}?", f"in the {ruang}",
                            [f"in the {x}" for x in KHAS if x != ruang],
                            f'"{benda}" biasanya ada di "{ruang}" ({RUANGAN[ruang]})')
    return _k(teks_pilihan(r, f"Which thing do we usually find in the {ruang}?", benda,
                           [r.choice(KHAS[x]) for x in KHAS if x != ruang],
                           f'"{benda}" biasanya ada di "{ruang}" ({RUANGAN[ruang]})'), "di-ruang", benda)


def u5_arti(r):
    return _arti(r, BENDA_5, r.random() < 0.5)


def u5_di_ruang(r):
    return _di_ruang(r, ["bedroom", "living room"])


def u6_arti(r):
    return _arti(r, BENDA_6, r.random() < 0.5)


def u6_di_ruang(r):
    return _di_ruang(r, ["bathroom", "kitchen"])


def ts3_di_ruang(r):
    return _di_ruang(r, list(KHAS))


# (kata sandang, tunggal, jamak, ruangan)
BENDA_RUMAH = [("a", "sofa", "sofas", "living room"), ("a", "lamp", "lamps", "living room"),
               ("a", "table", "tables", "living room"), ("a", "chair", "chairs", "living room"),
               ("a", "painting", "paintings", "living room"), ("a", "clock", "clocks", "living room"),
               ("a", "bed", "beds", "bedroom"), ("a", "pillow", "pillows", "bedroom"),
               ("a", "blanket", "blankets", "bedroom"), ("a", "bolster", "bolsters", "bedroom"),
               ("a", "wardrobe", "wardrobes", "bedroom"), ("a", "mirror", "mirrors", "bathroom"),
               ("a", "toothbrush", "toothbrushes", "bathroom"), ("a", "towel", "towels", "bathroom"),
               ("a", "stove", "stoves", "kitchen"), ("a", "pan", "pans", "kitchen"),
               ("a", "plate", "plates", "kitchen"), ("a", "glass", "glasses", "kitchen"),
               ("an", "oven", "ovens", "kitchen")]
BANYAK = ["two", "three", "four", "five"]


def u5_there(r):
    art, satu, banyak, ruang = r.choice(BENDA_RUMAH)
    if r.random() < 0.5:
        isi, jawab, alasan = f"{art} {satu}", "is", "satu benda"
    else:
        isi, jawab, alasan = f"{r.choice(BANYAK)} {banyak}", "are", "lebih dari satu benda"
    return teks_pilihan(r, f"There ___ {isi} in the {ruang}.", jawab,
                        [x for x in ("is", "are", "am", "be") if x != jawab],
                        f'Untuk {alasan} dipakai "There {jawab}": There {jawab} {isi} in the {ruang}.')


def u5_there_isi(r):
    art, satu, banyak, ruang = r.choice(BENDA_RUMAH)
    n = r.choice(BANYAK)
    if r.random() < 0.5:
        return teks_pilihan(r, f"There is ___ in the {ruang}.", f"{art} {satu}",
                            [banyak, f"{n} {banyak}", f"many {banyak}"],
                            f'"There is" dipakai untuk satu benda, jadi jawabannya "{art} {satu}"')
    return teks_pilihan(r, f"There are ___ in the {ruang}.", f"{n} {banyak}",
                        [f"{art} {satu}", satu, f"{n} {satu}"],
                        f'"There are" dipakai untuk benda lebih dari satu dan kata bendanya jamak: "{n} {banyak}"')


def u5_there_jawab(r):
    art, satu, banyak, ruang = r.choice(BENDA_RUMAH)
    ya = r.random() < 0.5
    if r.random() < 0.5:
        tanya, jawab = f"Is there {art} {satu} in the {ruang}?", "is" if ya else "isn't"
    else:
        tanya, jawab = f"Are there any {banyak} in the {ruang}?", "are" if ya else "aren't"
    return teks_pilihan(r, f"{tanya} {'Yes' if ya else 'No'}, there ___.", jawab,
                        [x for x in ("is", "are", "isn't", "aren't") if x != jawab],
                        f'Pertanyaan "{tanya.split()[0]} there …?" dijawab dengan "there {jawab}"')


def u5_how_many(r):
    (_, satu1, banyak1, ruang), (_, satu2, banyak2, _) = r.sample(BENDA_RUMAH, 2)
    n = r.choice(BANYAK)
    bentuk = r.randrange(4)
    if bentuk == 0:
        return teks_pilihan(r, f"How many {banyak1} ___ there in the {ruang}?", "are", ["is", "am", "do"],
                            '"How many" selalu diikuti benda jamak dan "are there"')
    if bentuk == 1:
        return teks_pilihan(r, f"How many ___ are there in the {ruang}?", banyak1,
                            [satu1, f"a {satu1}", f"one {satu1}"],
                            f'Setelah "How many" dipakai kata benda jamak: "{banyak1}"')
    if bentuk == 2:
        lain = r.choice([b for b in BANYAK if b != n])
        return teks_pilihan(r, f"There are {n} {banyak1} and one {satu2} in the {ruang}. "
                               f"How many {banyak1} are there?", f"There are {n}.",
                            ["There is one.", f"There is {n}.", f"There are {lain}."],
                            f'Jumlah {banyak1} adalah {n}, dan lebih dari satu memakai "There are"')
    return teks_pilihan(r, f"There are {n} {banyak1} and one {satu2} in the {ruang}. "
                           f"How many {banyak2} are there?", "There is one.",
                        [f"There are {n}.", "There are one.", f"There is {n}."],
                        f'Hanya ada satu {satu2}, dan satu benda memakai "There is"')


_JAMAK_S = ["pillow", "blanket", "bolster", "sofa", "lamp", "clock", "table", "chair", "mirror", "bed",
            "stove", "spoon", "plate", "bowl", "towel", "pan"]
_JAMAK_ES = ["toothbrush", "glass", "box", "brush", "dish", "watch"]


def u5_jamak(r):
    if r.random() < 0.6:
        k = r.choice(_JAMAK_S)
        j, salah, aturan = k + "s", [k + "es", k + "ies", k], "cukup ditambah -s"
    else:
        k = r.choice(_JAMAK_ES)
        j, salah, aturan = k + "es", [k + "s", k + "ies", k], "kata berakhiran s, x, ch, sh ditambah -es"
    if r.random() < 0.5:
        return teks_pilihan(r, f'The plural form of "{k}" is …', j, salah, f'"{k}" → "{j}": {aturan}')
    return teks_pilihan(r, f"There is one {k}. There are {r.choice(BANYAK)} ___.", j, salah,
                        f'Lebih dari satu memakai bentuk jamak. "{k}" → "{j}": {aturan}')


def u5_artikel(r):
    pakai_an = r.random() < 0.4
    kata = r.choice(["oven", "umbrella", "egg", "apple", "old sofa", "empty vase"] if pakai_an else
                    ["sofa", "bed", "pillow", "lamp", "mirror", "table", "big oven", "new umbrella"])
    jawab = "an" if pakai_an else "a"
    alasan = "diawali bunyi vokal (a, i, u, e, o)" if pakai_an else "diawali bunyi konsonan"
    return teks_pilihan(r, f"There is ___ {kata} in the room.", jawab,
                        [x for x in ("a", "an", "two", "many") if x != jawab],
                        f'Satu benda memakai a/an. "{kata}" {alasan}, jadi memakai "{jawab}"')


_BOLA = '<circle cx="{x}" cy="{y}" r="14" fill="#ffb703" stroke="#b97f00"/>'
_KOTAK = '<rect x="{x}" y="62" width="70" height="70" fill="#e3e9ff"/>'
_MEJA = ('<rect x="40" y="70" width="140" height="12" fill="#e3e9ff"/>'
         '<line x1="56" y1="82" x2="56" y2="138"/><line x1="164" y1="82" x2="164" y2="138"/>')
_LANTAI = '<line x1="10" y1="140" x2="210" y2="140" stroke="#9aa3c2" stroke-width="2"/>'

_GAMBAR_LETAK = {  # kata depan: (gambar, benda acuan, pengecoh yang dihindari, arti)
    "on": (_MEJA + _BOLA.format(x=110, y=54), "table", [], "di atas"),
    "under": (_MEJA + _BOLA.format(x=110, y=124), "table", [], "di bawah"),
    "in": ('<path d="M75 62 V132 H145 V62" fill="#e3e9ff"/>' + _BOLA.format(x=110, y=112) + _LANTAI,
           "box", [], "di dalam"),
    "beside": (_KOTAK.format(x=45) + _BOLA.format(x=150, y=124) + _LANTAI, "box", [], "di samping"),
    "behind": (_BOLA.format(x=140, y=56) + _KOTAK.format(x=75) + _LANTAI, "box", ["on"], "di belakang"),
    "between": (_KOTAK.format(x=15) + _KOTAK.format(x=135) + _BOLA.format(x=110, y=124) + _LANTAI,
                "boxes", [], "di antara"),
}


def u5_letak_gambar(r):
    depan = r.choice(list(_GAMBAR_LETAK))
    gambar, acuan, hindari, arti = _GAMBAR_LETAK[depan]
    lain = [d for d in _GAMBAR_LETAK if d != depan and d not in hindari]
    tempat = {"boxes": "kotak-kotak", "table": "meja", "box": "kotak"}[acuan]
    soal = teks_pilihan(r, f"Look at the picture. Where is the ball? It is ___ the {acuan}.", depan, lain,
                        f'Bola berada {arti} {tempat}: "{depan}" = {arti}')
    soal["gambar"] = _svg(gambar)
    return _k(soal, "letak", depan)


_LETAK_KALIMAT = [
    ("The picture is ___ the wall.", "on"), ("The clothes are ___ the wardrobe.", "in"),
    ("The pillow is ___ the bed.", "on"), ("The vase is ___ the table.", "on"),
    ("The carpet is ___ the floor.", "on"), ("The books are ___ the bag.", "in"),
    ("The shirt and trousers are ___ the cupboard.", "in"),
    ("The pillow is ___ the two bolsters.", "between"),
    ("The letter B is ___ the letters A and C.", "between"),
    ("My slippers are ___ the bed, on the floor.", "under"),
    ("The cat sleeps ___ the table, on the floor.", "under"),
]


def u5_letak_kalimat(r):
    teks, jawab = r.choice(_LETAK_KALIMAT)
    return teks_pilihan(r, teks, jawab, [d for d in ("in", "on", "under", "between") if d != jawab],
                        "in = di dalam, on = di atas (menempel), under = di bawah, between = di antara")


# (kalimat, jawaban, benda yang tidak boleh jadi pengecoh)
_FUNGSI = [
    ("I use ___ to wash my hair.", "shampoo", ["soap"]),
    ("I use ___ to clean my body.", "soap", ["shampoo"]),
    ("I brush my teeth with a ___ and toothpaste.", "toothbrush", []),
    ("I dry my body with a ___.", "towel", []),
    ("I look at my face in the ___.", "mirror", []),
    ("We eat soup with a ___.", "spoon", ["fork"]),
    ("We drink water from a ___.", "glass", ["bowl"]),
    ("Mother cuts the vegetables with a ___.", "knife", ["peeler", "grater"]),
    ("Mother boils water in a ___.", "kettle", ["pot", "pan"]),
    ("Mother fries an egg in a ___.", "frying pan", ["pan", "pot"]),
    ("We put rice and fried chicken on a ___.", "plate", ["bowl"]),
    ("We grate cheese with a ___.", "grater", ["knife"]),
    ("We peel potatoes with a ___.", "peeler", ["knife"]),
    ("We throw rubbish into the ___.", "trash bin", []),
    ("Mother turns the fried egg with a ___.", "turner", ["spoon", "fork"]),
    ("Mother cuts carrots on a ___.", "chopping board", ["plate"]),
    ("We take water from the bathtub with a ___.", "dipper", ["bowl", "glass"]),
    ("Mother bakes a cake in the ___.", "oven", ["stove"]),
    ("Mother puts the pan on the ___ to cook.", "stove", ["oven"]),
]
_PENGECOH_FUNGSI = ["toothbrush", "towel", "mirror", "spoon", "fork", "glass", "bowl", "knife", "kettle",
                    "frying pan", "plate", "grater", "peeler", "trash bin", "turner", "chopping board",
                    "dipper", "stove", "pot", "pan", "soap", "shampoo"]


def u6_fungsi(r):
    teks, jawab, hindari = r.choice(_FUNGSI)
    lain = [b for b in _PENGECOH_FUNGSI if b != jawab and b not in hindari]
    return teks_pilihan(r, teks, jawab, r.sample(lain, 3), f'"{jawab}" artinya {BENDA_6[jawab]}')


def u6_negatif(r):
    return u4_negatif(r, lengkap=True)


def u6_tidak_cocok(r):
    s, be, _, _ = r.choice(TUNGGAL + JAMAK + [SAYA])
    kegiatan, ruang = r.choice([("watch TV", "bathroom"), ("sleep", "kitchen"), ("take a bath", "kitchen"),
                                ("cook", "bedroom"), ("sleep", "garage"), ("study", "bathroom"),
                                ("read newspapers", "bathroom")])
    jawab = "does not" if be == "is" else "do not"
    return teks_pilihan(r, f"{s} ___ {kegiatan} in the {ruang}.", jawab,
                        [x for x in ("do not", "does not", "is not", "are not") if x != jawab],
                        f'Subjek "{s}" memakai "{jawab}" + kata kerja dasar')


def _bacaan_ruangan(r):
    pilihan = {
        "living room": (["a sofa", "a table", "a television", "a lamp", "a clock", "a vase"], "watch TV"),
        "bedroom": (["a bed", "a wardrobe", "a mirror", "a desk", "a bookshelf", "a desk lamp"], "sleep and study"),
        "kitchen": (["a stove", "a cabinet", "a sink", "a trash bin", "an oven", "a kettle"], "help my mother cook"),
    }
    luar = ["a bathtub", "a dipper", "a pedicab", "a towel"]
    hasil = []
    for ruang in r.sample(list(pilihan), 2):
        benda, kegiatan = pilihan[ruang]
        a, b, c = r.sample(benda, 3)
        s1, s2 = r.choice([("big", "clean"), ("small", "tidy"), ("large", "clean"), ("small", "clean")])
        k = [f"This is my {ruang}.", f"My {ruang} is {s1} and {s2}.",
             f"There are {a}, {b}, and {c} in the {ruang}.", f"I {kegiatan} in it.", f"I love my {ruang}."]
        bacaan = " ".join(k)
        kegiatan_lain = [x[1] for x in pilihan.values() if x[1] != kegiatan] + ["take a bath", "play football"]
        hasil += [
            (bacaan, "What room is it?", f"the {ruang}", [f"the {x}" for x in RUANGAN if x != ruang], k[0]),
            (bacaan, f"What is the {ruang} like?", f"{s1} and {s2}",
             ["small and dirty", "big and dirty", "large and messy", "big and empty"], k[1]),
            (bacaan, f"What does the writer do in the {ruang}?", kegiatan, kegiatan_lain, k[3]),
            (bacaan, f"Which thing is in the {ruang}?", a, luar, k[2]),
            (bacaan, f"Which thing is NOT in the {ruang}?", r.choice(luar), [a, b, c], k[2]),
        ]
    return hasil


def u6_bacaan(r):
    return _dari_bacaan(r, "_bacaan_ruangan", _bacaan_ruangan)


# ================================================ Unit 7 · can / can't dan memasak

MEMASAK = {"serve": "menyajikan", "cook": "memasak", "grate": "memarut", "cut": "memotong",
           "boil": "merebus", "simmer": "menghangatkan", "turn": "membalik", "check": "memeriksa",
           "taste": "mencicipi", "peel": "mengupas", "add": "menambahkan", "mix": "mencampur",
           "fry": "menggoreng", "clean": "membersihkan"}

# (kegiatan, ruangan, bisa dilakukan di sana?)
_BISA = [("cook noodles", "kitchen", True), ("fry fish", "kitchen", True), ("boil water", "kitchen", True),
         ("take a bath", "bathroom", True), ("brush our teeth", "bathroom", True),
         ("wash our hands", "bathroom", True), ("watch TV", "living room", True),
         ("take a rest", "bedroom", True), ("sleep", "bedroom", True), ("play badminton", "bedroom", False),
         ("take a bath", "kitchen", False), ("cook noodles", "bathroom", False), ("sleep", "bathroom", False),
         ("fry fish", "bedroom", False), ("play football", "living room", False), ("swim", "kitchen", False)]


def u7_can(r):
    kegiatan, ruang, bisa = r.choice(_BISA)
    s = r.choice(["We", "I", "They", "You"])
    jawab = "can" if bisa else "can't"
    return teks_pilihan(r, f"{s} ___ {kegiatan} in the {ruang}.", jawab,
                        [x for x in ("can", "can't", "is", "are") if x != jawab],
                        f'"can" = bisa, "can\'t" = tidak bisa. {s} {jawab} {kegiatan} in the {ruang}.')


def u7_dasar(r):
    s, _, _, _ = _subjek(r)
    dasar, es, ing, objek = r.choice([("cook", "cooks", "cooking", "noodles"), ("fry", "fries", "frying", "fish"),
                                      ("boil", "boils", "boiling", "water"), ("make", "makes", "making", "a fried egg"),
                                      ("wash", "washes", "washing", "the dishes"), ("watch", "watches", "watching", "TV"),
                                      ("read", "reads", "reading", "magazines"), ("play", "plays", "playing", "a puzzle")])
    return teks_pilihan(r, f"{s} can ___ {objek}.", dasar, [es, ing, f"to {dasar}"],
                        f'Setelah "can" selalu kata kerja dasar: {s} can {dasar} {objek}.')


_KEGIATAN_7 = {"kitchen": ["cook noodles", "fry fish", "boil water"],
               "bathroom": ["take a bath", "brush my teeth", "wash my hands"],
               "living room": ["watch TV", "read magazines"],
               "bedroom": ["take a rest", "sleep"]}


def u7_kegiatan(r):
    ruang = r.choice(list(_KEGIATAN_7))
    kegiatan = r.choice(_KEGIATAN_7[ruang])
    return _k(teks_pilihan(r, f"What can you do in the {ruang}? I can ___ in the {ruang}.", kegiatan,
                           [r.choice(_KEGIATAN_7[x]) for x in _KEGIATAN_7 if x != ruang],
                           f'Di {RUANGAN[ruang]} ("{ruang}") kita bisa "{kegiatan}"'), "u7-kegiatan", kegiatan)


def u7_arti_kerja(r):
    return _arti(r, MEMASAK, r.random() < 0.5)


_BERDEKATAN = [{"boil", "simmer"}, {"cook", "fry"}, {"cut", "peel"}, {"cook", "boil"}, {"cut", "grate"},
               {"mix", "add"}, {"check", "taste"}]


def u7_alat(r):
    teks, jawab = r.choice([
        ("We use a grater to ___ the cheese.", "grate"), ("We use a peeler to ___ the potatoes.", "peel"),
        ("We use a knife to ___ the vegetables.", "cut"), ("We use a kettle to ___ the water.", "boil"),
        ("We use a frying pan to ___ an egg.", "fry"), ("We use a turner to ___ the fried egg.", "turn"),
        ("We ___ the soup to know if it is delicious.", "taste"),
        ("We ___ the food on a plate for our guests.", "serve"),
        ("We ___ the dirty table after cooking.", "clean"),
        ("We ___ sugar and flour in a bowl.", "mix"),
    ])
    lain = [k for k in MEMASAK if k != jawab and {k, jawab} not in _BERDEKATAN]
    return teks_pilihan(r, teks, jawab, r.sample(lain, 3), f'"{jawab}" artinya {MEMASAK[jawab]}')


def u7_jawab(r):
    kegiatan, ruang, bisa = r.choice(_BISA)
    kegiatan = kegiatan.replace("our ", "her ")
    nama = r.choice(PEREMPUAN)
    jawab = "can" if bisa else "can't"
    return teks_pilihan(r, f"Can {nama} {kegiatan} in the {ruang}? {'Yes' if bisa else 'No'}, she ___.", jawab,
                        [x for x in ("can", "can't", "does", "is") if x != jawab],
                        'Pertanyaan "Can …?" dijawab dengan "can" atau "can\'t"')


# ========================================================== Unit 8 · membaca jam

def _ucapan_jam(jam, menit):
    berikut = jam % 12 + 1
    return {0: f"{SATUAN[jam]} o'clock", 15: f"quarter past {SATUAN[jam]}",
            30: f"half past {SATUAN[jam]}", 45: f"quarter to {SATUAN[berikut]}"}[menit]


_ATURAN_JAM = {0: "tepat jam → o'clock", 15: "lewat 15 menit → quarter past",
               30: "lewat 30 menit → half past", 45: "kurang 15 menit → quarter to (jam berikutnya)"}


def _waktu(r):
    return r.randint(1, 12), r.choice([0, 0, 30, 30, 15, 45])


def _jam_lain(r, jam, menit, n=3):
    semua = {_ucapan_jam(j, m) for j in (jam, jam % 12 + 1, (jam - 2) % 12 + 1) for m in (0, 15, 30, 45)}
    return r.sample(sorted(semua - {_ucapan_jam(jam, menit)}), n)


def _gambar_jam(jam, menit):
    cx, cy = 110, 75
    isi = f'<circle cx="{cx}" cy="{cy}" r="62" fill="#fafbff"/>'
    for i in range(12):
        t = radians(i * 30)
        isi += (f'<line x1="{cx + 54 * sin(t):.1f}" y1="{cy - 54 * cos(t):.1f}" x2="{cx + 60 * sin(t):.1f}" '
                f'y2="{cy - 60 * cos(t):.1f}" stroke-width="2"/>')
    for angka in range(1, 13):
        t = radians(angka * 30)
        isi += _teks_svg(f"{cx + 45 * sin(t):.1f}", f"{cy - 45 * cos(t) + 4.5:.1f}", angka, 12)
    tj, tm = radians((jam % 12 + menit / 60) * 30), radians(menit * 6)
    isi += (f'<line x1="{cx}" y1="{cy}" x2="{cx + 26 * sin(tj):.1f}" y2="{cy - 26 * cos(tj):.1f}" '
            f'stroke="#1d2440" stroke-width="5"/>'
            f'<line x1="{cx}" y1="{cy}" x2="{cx + 38 * sin(tm):.1f}" y2="{cy - 38 * cos(tm):.1f}" '
            f'stroke="#d6394a" stroke-width="3"/>'
            f'<circle cx="{cx}" cy="{cy}" r="4" fill="#1d2440" stroke="none"/>')
    return _svg(isi)


def u8_gambar(r):
    jam, menit = _waktu(r)
    jawab = _ucapan_jam(jam, menit)
    soal = teks_pilihan(r, "Look at the clock. What time is it?", f"It is {jawab}.",
                        [f"It is {x}." for x in _jam_lain(r, jam, menit)],
                        f'Jarum pendek menunjuk jam, jarum panjang menunjuk menit. Dibaca "{jawab}" ({_ATURAN_JAM[menit]})')
    soal["gambar"] = _gambar_jam(jam, menit)
    return _k(soal, "jam", jam, menit)


def u8_digital(r):
    jam, menit = _waktu(r)
    jawab = _ucapan_jam(jam, menit)
    return teks_pilihan(r, f"The clock shows {jam:02d}:{menit:02d}. What time is it?", f"It is {jawab}.",
                        [f"It is {x}." for x in _jam_lain(r, jam, menit)],
                        f'{jam:02d}:{menit:02d} dibaca "{jawab}" ({_ATURAN_JAM[menit]})')


def u8_ke_angka(r):
    jam, menit = _waktu(r)
    tulis = lambda j, m: f"{(j - 1) % 12 + 1:02d}.{m:02d}"
    jawab = tulis(jam, menit)
    calon = {tulis(jam, m) for m in (0, 15, 30, 45)} | {tulis(jam + 1, menit), tulis(jam - 1, menit),
                                                        tulis(jam + 1, (menit + 30) % 60)}
    return teks_pilihan(r, f"It is {_ucapan_jam(jam, menit)}. The time is …", jawab,
                        r.sample(sorted(calon - {jawab}), 3),
                        f'"{_ucapan_jam(jam, menit)}" adalah pukul {jawab} ({_ATURAN_JAM[menit]})')


def u8_ya_tidak(r):
    jam, menit = _waktu(r)
    benar = _ucapan_jam(jam, menit)
    a, b, c = _jam_lain(r, jam, menit)
    if r.random() < 0.4:
        tanya, jawab, salah = benar, "Yes, it is.", ["No, it is not.", f"No, it is {a}.", f"No, it is {b}."]
    else:
        tanya, jawab, salah = a, f"No, it is {benar}.", ["Yes, it is.", f"No, it is {a}.", f"No, it is {b}."]
    return teks_pilihan(r, f"The clock shows {jam:02d}:{menit:02d}. Is it {tanya}?", jawab, salah,
                        f'{jam:02d}:{menit:02d} dibaca "{benar}"')


def u8_kegiatan(r):
    nama = r.choice(PEREMPUAN + LAKI)
    dasar, es, rentang = r.choice([("get up", "gets up", (4, 5)), ("take a bath", "takes a bath", (5, 6)),
                                   ("have breakfast", "has breakfast", (6, 7)),
                                   ("go to school", "goes to school", (6, 7)), ("go to bed", "goes to bed", (8, 9)),
                                   ("have dinner", "has dinner", (6, 7)), ("play football", "plays football", (3, 4))])
    jam, menit = r.choice(rentang), r.choice([0, 15, 30, 45])
    jawab = _ucapan_jam(jam, menit)
    return teks_pilihan(r, f"{nama} {es} at {jam:02d}.{menit:02d}. What time does {nama} {dasar}?",
                        f"at {jawab}", [f"at {x}" for x in _jam_lain(r, jam, menit)],
                        f'{jam:02d}.{menit:02d} dibaca "{jawab}" ({_ATURAN_JAM[menit]})')


def u8_istilah(r):
    teks, jawab, salah, bahas = r.choice([
        ('"Half past seven" means …', "30 minutes after seven o'clock",
         ["30 minutes before seven o'clock", "15 minutes after seven o'clock", "exactly seven o'clock"],
         '"half past" = lewat setengah jam (30 menit)'),
        ('"Quarter past seven" means …', "15 minutes after seven o'clock",
         ["15 minutes before seven o'clock", "30 minutes after seven o'clock", "exactly seven o'clock"],
         '"quarter past" = lewat seperempat jam (15 menit)'),
        ('"Quarter to seven" means …', "15 minutes before seven o'clock",
         ["15 minutes after seven o'clock", "30 minutes before seven o'clock", "exactly seven o'clock"],
         '"quarter to" = kurang seperempat jam (15 menit) menuju jam itu'),
        ("How many minutes are there in a quarter of an hour?", "fifteen", ["thirty", "fifty", "sixty"],
         "Seperempat jam = 15 menit"),
        ("How many minutes are there in half an hour?", "thirty", ["fifteen", "thirteen", "sixty"],
         "Setengah jam = 30 menit"),
        ("We ask about the time with the question …", "What time is it?",
         ["How are you?", "Where is it?", "How many are there?"],
         '"What time is it?" = pukul berapa sekarang?'),
    ])
    return teks_pilihan(r, teks, jawab, salah, bahas)


# ================================================== Unit 9 · kegiatan sehari-hari

KEGIATAN_9 = {"get up": "bangun tidur", "take a bath": "mandi", "brush my teeth": "menggosok gigi",
              "water the flowers": "menyiram bunga", "have breakfast": "sarapan",
              "go to school": "pergi ke sekolah", "go to work": "pergi bekerja", "study": "belajar",
              "cook": "memasak", "play": "bermain", "pray": "berdoa", "have dinner": "makan malam",
              "go to bed": "pergi tidur", "read a book": "membaca buku"}


def u9_arti(r):
    return _arti(r, KEGIATAN_9, r.random() < 0.5)


def u9_kolokasi(r):
    teks, jawab, salah = r.choice([
        ("I ___ a bath every morning.", "take", ["go", "get", "brush"]),
        ("I ___ breakfast at six o'clock.", "have", ["go", "water", "get"]),
        ("I ___ my teeth after breakfast.", "brush", ["take", "water", "go"]),
        ("I ___ to school at half past six.", "go", ["take", "have", "get"]),
        ("I ___ the flowers in the garden.", "water", ["brush", "have", "go"]),
        ("I ___ up at half past four.", "get", ["go", "have", "take"]),
        ("I ___ dinner with my family.", "have", ["go", "get", "water"]),
        ("I ___ to bed at nine o'clock.", "go", ["get", "have", "take"]),
        ("My father ___ to work by motorcycle.", "goes", ["takes", "has", "gets"]),
        ("My mother ___ a bath at five o'clock.", "takes", ["goes", "brushes", "waters"]),
    ])
    return teks_pilihan(r, teks, jawab, salah, f"Pasangan katanya: {teks.replace('___', jawab)}")


_URUTAN = ["get up", "take a bath", "have breakfast", "go to school", "study at school", "go home",
           "do my homework", "have dinner", "go to bed"]


def u9_urutan(r):
    i = r.randrange(len(_URUTAN) - 1)
    a, b = _URUTAN[i], _URUTAN[i + 1]
    if r.random() < 0.5:
        teks, jawab, arti = f"First, I {a}. Then, I {b}. I {b} ___ I {a}.", "after", "sesudah"
    else:
        teks, jawab, arti = f"First, I {a}. Then, I {b}. I {a} ___ I {b}.", "before", "sebelum"
    return teks_pilihan(r, teks, jawab, [x for x in ("before", "after", "at", "in") if x != jawab],
                        f'"{jawab}" = {arti}; "{a}" dilakukan lebih dulu daripada "{b}"')


def u9_kapan(r):
    teks, jawab = r.choice([
        ("We have breakfast in the ___.", "morning"), ("We have dinner in the ___.", "evening"),
        ("We go to bed at ___.", "night"), ("School finishes at one o'clock in the ___.", "afternoon"),
        ("The sun rises in the ___.", "morning"), ("We get up early in the ___.", "morning"),
        ("We can see the moon and stars at ___.", "night"),
        ("We have lunch at twelve o'clock, then we play in the ___.", "afternoon"),
    ])
    return teks_pilihan(r, teks, jawab, [x for x in ("morning", "afternoon", "evening", "night") if x != jawab],
                        "morning = pagi, afternoon = siang/sore, evening = petang/malam, night = malam")


def u9_dia(r):
    dasar, es, sisa = r.choice([("take", "takes", "a bath"), ("have", "has", "breakfast"),
                                ("go", "goes", "to school"), ("brush", "brushes", "his teeth"),
                                ("water", "waters", "the flowers"), ("get", "gets", "up"),
                                ("study", "studies", "Math"), ("play", "plays", "football")])
    jam = r.choice(["five o'clock", "six o'clock", "half past six", "seven o'clock", "four o'clock"])
    return teks_pilihan(r, f"What does he do at {jam}? He ___ {sisa}.", es, [dasar, _ing(dasar), f"is {dasar}"],
                        f'Untuk "he", kata kerja ditambah -s/-es: He {es} {sisa}.')


def u9_lengkapi(r):
    teks, jawab, salah = r.choice([
        ("I ___ at 04.30 in the morning.", "get up", ["go to bed", "have dinner", "go home"]),
        ("I go to the bathroom and ___.", "brush my teeth", ["have breakfast", "go to school", "water the flowers"]),
        ("I ___ in the dining room before I go to school.", "have breakfast", ["take a bath", "go to bed", "have dinner"]),
        ("I ___ by bus at half past six.", "go to school", ["get up", "take a bath", "brush my teeth"]),
        ("I ___ a kite in the field.", "play", ["study", "cook", "pray"]),
        ("I ___ Math and English at school.", "study", ["cook", "play", "water"]),
        ("I ___ in bed before sleeping.", "read a book", ["take a bath", "go to school", "water the flowers"]),
        ("I ___ at 9.30 at night.", "go to bed", ["get up", "go to school", "have breakfast"]),
        ("Mother ___ in the garden every afternoon.", "waters the flowers", ["takes a bath", "has dinner", "goes to bed"]),
        ("Father ___ at the office every day.", "works", ["sleeps", "takes a bath", "plays"]),
    ])
    return teks_pilihan(r, teks, jawab, salah, f"Kalimat yang tepat: {teks.replace('___', jawab)}")


# ================================================== Unit 10 · adverbs of frequency

FREKUENSI = {"always": "selalu", "usually": "biasanya", "sometimes": "kadang-kadang", "never": "tidak pernah"}
# (dasar, bentuk -s, lanjutan)
RUTIN = [("get", "gets", "up", ["04.00", "04.30", "05.00"]),
         ("take", "takes", "a bath", ["04.30", "05.00", "05.30"]),
         ("have", "has", "breakfast", ["06.00", "06.15", "06.30"]),
         ("go", "goes", "to school", ["06.30", "06.45", "07.00"]),
         ("study", "studies", "", ["07.30", "08.00"]),
         ("go", "goes", "to bed", ["09.00", "09.30"]),
         ("watch", "watches", "TV", ["07.00", "08.00"])]
JAM_TULIS = ["06.00", "06.30", "07.00", "07.30", "08.00", "09.00"]


def u10_arti(r):
    en, idn = r.choice(list(FREKUENSI.items()))
    if r.random() < 0.5:
        return teks_pilihan(r, f'What is the meaning of "{en}" in Indonesian?', idn,
                            [v for v in FREKUENSI.values() if v != idn], f'"{en}" artinya "{idn}"')
    return teks_pilihan(r, f'What is "{idn}" in English?', en, [k for k in FREKUENSI if k != en],
                        f'"{idn}" dalam bahasa Inggris adalah "{en}"')


def u10_konteks(r):
    nama = r.choice(LAKI)
    dasar, es, sisa, waktu = r.choice(RUTIN)
    jam = r.choice(waktu)
    kegiatan = f"{_frasa(es, sisa)} at {jam}"
    teks, jawab = r.choice([
        (f"{nama} {kegiatan} seven days a week. He ___ {kegiatan}.", "always"),
        (f"{nama} {kegiatan} five or six days a week. He ___ {kegiatan}.", "usually"),
        (f"{nama} {kegiatan} only two days a week. He ___ {kegiatan}.", "sometimes"),
        (f"{nama} does not {_frasa(dasar, sisa)} at {jam}. He ___ {kegiatan}.", "never"),
    ])
    return teks_pilihan(r, teks, jawab, [k for k in FREKUENSI if k != jawab],
                        "always = selalu, usually = biasanya, sometimes = kadang-kadang, never = tidak pernah")


def u10_posisi(r):
    nama = r.choice(LAKI + PEREMPUAN)
    dasar, es, sisa, waktu = r.choice(RUTIN)
    kata, jam = r.choice(list(FREKUENSI)), r.choice(waktu)
    benar = f"{nama} {kata} {_frasa(es, sisa)} at {jam}."
    return _k(teks_pilihan(r, "Which sentence is correct?", benar,
                           [f"{nama} {_frasa(es, sisa)} {kata} at {jam}.",
                            f"{nama} {kata} {_frasa(dasar, sisa)} at {jam}.",
                            f"{kata.capitalize()} {nama} {_frasa(dasar, sisa)} at {jam}."],
                           f'"{kata}" diletakkan sebelum kata kerja, dan kata kerjanya tetap ditambah -s/-es: {benar}'),
              "u10-posisi", benar)


def u10_kerja(r):
    nama = r.choice(LAKI + PEREMPUAN)
    dasar, es, sisa, waktu = r.choice(RUTIN)
    kata, jam = r.choice(list(FREKUENSI)), r.choice(waktu)
    return teks_pilihan(r, f"{nama} {kata} {_frasa('___', sisa)} at {jam}.", es,
                        [dasar, _ing(dasar), f"is {dasar}"],
                        f'Subjek satu orang: kata kerja ditambah -s/-es walau ada "{kata}": {nama} {kata} {_frasa(es, sisa)}.')


def u10_tanya(r):
    dasar, _, sisa, _ = r.choice(RUTIN)
    subjek, bantu = r.choice([("you", "do"), ("Fahri", "does"), ("Aisyah", "does"), ("they", "do"),
                              ("your father", "does"), ("Joshua and Made", "do")])
    return teks_pilihan(r, f"What time ___ {subjek} {_frasa(dasar, sisa)}?", bantu,
                        [x for x in ("do", "does", "is", "are") if x != bantu],
                        f'Untuk "{subjek}" dipakai "{bantu}": What time {bantu} {subjek} {_frasa(dasar, sisa)}?')


def _bacaan_rutin(r):
    hasil = []
    kota = ["Surabaya", "Malang", "Lamongan", "Sidoarjo", "Gresik"]

    # 1. Hari Minggu bersama keluarga
    n = r.choice(PEREMPUAN)
    bangun, tujuan = r.choice(["04.30", "05.00", "05.30"]), r.choice(kota)
    k = [f"Today is Sunday. {n} and her family get up at {bangun} in the morning.",
         f"{n}'s father cleans his car.", "Her mother cooks in the kitchen.",
         f"{n} helps her mother in the kitchen.", "Her brother sweeps the yard.",
         "At eight o'clock, they have breakfast.", f"At nine o'clock, they visit grandma in {tujuan}.",
         "They arrive home in the evening. Then, they go to bed."]
    bacaan = " ".join(k)
    hasil += [
        (bacaan, f"What time do {n} and her family get up?", f"at {bangun}", ["at 04.00", "at 06.00", "at 08.00"], k[0]),
        (bacaan, f"What does {n}'s father do?", "He cleans his car.",
         ["He cooks in the kitchen.", "He sweeps the yard.", "He visits grandma alone."], k[1]),
        (bacaan, "Who cooks in the kitchen?", f"{n}'s mother", [f"{n}'s father", f"{n}'s brother", "grandma"], k[2]),
        (bacaan, "Who sweeps the yard?", f"{n}'s brother", [f"{n}'s father", f"{n}'s mother", n], k[4]),
        (bacaan, "What time do they have breakfast?", "at eight o'clock",
         ["at nine o'clock", "at seven o'clock", "at half past eight"], k[5]),
        (bacaan, "Where does grandma live?", f"in {tujuan}", [f"in {x}" for x in kota if x != tujuan], k[6]),
        (bacaan, "Which statement is TRUE?", f"{n} helps her mother in the kitchen.",
         [f"{n} sweeps the yard.", "They have breakfast at nine o'clock.", f"{n}'s mother cleans the car."], k[3]),
        (bacaan, "What do they do after they arrive home?", "They go to bed.",
         ["They have breakfast.", "They visit grandma.", "They clean the car."], k[7]),
    ]

    # 2. Me and My Day
    n = r.choice(LAKI)
    bangun, mandi = r.choice([("04.00", "04.30"), ("04.30", "05.00"), ("05.00", "05.30")])
    makan = r.choice(["fried rice", "bread and milk", "porridge", "noodles"])
    k = [f"My name is {n}.", f"I always get up at {bangun}.", f"I usually take a bath at {mandi}.",
         "I have my breakfast in the dining room.", f"I eat {makan} for breakfast.", "I go to school at 06.30.",
         "I sometimes watch TV in the afternoon.", "I never go to bed late."]
    bacaan = " ".join(k)
    hasil += [
        (bacaan, f"What time does {n} get up?", f"at {bangun}", ["at 06.30", "at 07.00", "at 03.00"], k[1]),
        (bacaan, f"What time does {n} usually take a bath?", f"at {mandi}", ["at 06.30", "at 07.00", "at 03.30"], k[2]),
        (bacaan, f"Where does {n} have breakfast?", "in the dining room",
         ["in the kitchen", "in the bedroom", "in the living room"], k[3]),
        (bacaan, f"What does {n} eat for breakfast?", makan, ["fried chicken", "meatballs", "fruit salad", "soup"], k[4]),
        (bacaan, f"What time does {n} go to school?", "at 06.30", ["at 07.30", "at 06.00", "at 08.00"], k[5]),
        (bacaan, f"How often does {n} watch TV in the afternoon?", "sometimes", ["always", "usually", "never"], k[6]),
        (bacaan, f"Does {n} go to bed late?", "No, he never goes to bed late.",
         ["Yes, he always goes to bed late.", "Yes, he usually goes to bed late.",
          "Yes, he sometimes goes to bed late."], k[7]),
        (bacaan, f"How often does {n} get up at {bangun}?", "always", ["usually", "sometimes", "never"], k[1]),
    ]
    return hasil


def u10_bacaan(r):
    return _dari_bacaan(r, "_bacaan_rutin", _bacaan_rutin)


# ================================================================ Unit 11 · kendaraan

# kendaraan: (arti, ciri, jalur, banyak roda)
KENDARAAN = {
    "bike": ("sepeda", "It has two wheels and no engine. We pedal it.", "road", "two"),
    "pedicab": ("becak", "It has three wheels. The driver pedals it and the passenger sits in front.", "road", "three"),
    "motorcycle": ("sepeda motor", "It has two wheels and an engine.", "road", "two"),
    "car": ("mobil", "It has four wheels. A small family can ride in it.", "road", "four"),
    "bus": ("bus", "It is a big vehicle on the road. It carries many passengers.", "road", None),
    "truck": ("truk", "It is a big vehicle that carries sand, boxes or other goods.", "road", None),
    "train": ("kereta api", "It is very long and runs on rails.", "rails", None),
    "boat": ("perahu", "It is small and moves on a river or a lake.", "water", None),
    "ship": ("kapal laut", "It is very big and sails on the sea.", "water", None),
    "plane": ("pesawat terbang", "It has two wings and takes off from an airport.", "air", None),
    "helicopter": ("helikopter", "It flies with a big propeller on its top.", "air", None),
}
_ARTI_11 = {k: v[0] for k, v in KENDARAAN.items() if k != "bus"}
_SERUPA = [{"boat", "ship"}, {"plane", "helicopter"}, {"bus", "truck"}, {"bike", "motorcycle"}]
TUJUAN = ["school", "the market", "the office", "the book store", "the paddy field", "the supermarket"]


def u11_arti(r):
    return _arti(r, _ARTI_11, r.random() < 0.5)


def u11_ciri(r):
    nama = r.choice(list(KENDARAAN))
    lain = [k for k in KENDARAAN if k != nama and {k, nama} not in _SERUPA]
    return teks_pilihan(r, f"{KENDARAAN[nama][1]} What is it?", nama, r.sample(lain, 3),
                        f'"{nama}" artinya {KENDARAAN[nama][0]}')


def u11_by_on(r):
    s, be, _, _ = r.choice(TUNGGAL + JAMAK + [SAYA])
    pergi = "goes" if be == "is" else "go"
    tujuan = r.choice(TUJUAN)
    if r.random() < 0.3:
        return teks_pilihan(r, f"{s} {pergi} to {tujuan} ___ foot.", "on", ["by", "in", "at"],
                            'Berjalan kaki memakai "on foot", bukan "by foot"')
    kendaraan = r.choice(["bike", "pedicab", "motorcycle", "car", "bus"])
    return teks_pilihan(r, f"{s} {pergi} to {tujuan} ___ {kendaraan}.", "by", ["on", "in", "at"],
                        f'Naik kendaraan memakai "by": by {kendaraan}')


def u11_jalur(r):
    jalur, tanya = r.choice([("water", "Which vehicle moves on water?"), ("air", "Which vehicle flies in the sky?"),
                             ("rails", "Which vehicle runs on rails?"), ("road", "Which vehicle moves on the road?")])
    jawab = r.choice([k for k, v in KENDARAAN.items() if v[2] == jalur])
    lain = r.sample([k for k, v in KENDARAAN.items() if v[2] != jalur], 3)
    return _k(teks_pilihan(r, tanya, jawab, lain, f'"{jawab}" artinya {KENDARAAN[jawab][0]}'), "jalur", jawab)


def u11_how(r):
    kendaraan = r.choice(["bike", "pedicab", "motorcycle", "car", "bus", "train", "boat"])
    siapa, jawab_s, pergi = r.choice([("do you", "I", "go"), ("does Made", "He", "goes"),
                                      ("does Aisyah", "She", "goes"), ("do they", "They", "go")])
    benar = f"{jawab_s} {pergi} to school by {kendaraan}."
    salah_pergi = "go" if pergi == "goes" else "goes"
    return teks_pilihan(r, f"How {siapa} go to school? (by {kendaraan})", benar,
                        [f"{jawab_s} {salah_pergi} to school by {kendaraan}.",
                         f"{jawab_s} {pergi} to school with {kendaraan}.",
                         f"{jawab_s} {pergi} by {kendaraan} school to."],
                        f"Polanya subjek + go/goes + to school + by + kendaraan: {benar}")


def u11_roda(r):
    nama = r.choice([k for k, v in KENDARAAN.items() if v[3]])
    jawab = KENDARAAN[nama][3]
    return teks_pilihan(r, f"How many wheels does a {nama} have?", jawab,
                        [x for x in ("two", "three", "four", "six") if x != jawab],
                        f"A {nama} ({KENDARAAN[nama][0]}) has {jawab} wheels.")


def u11_tanya(r):
    nama, tujuan = r.choice(PEREMPUAN + LAKI), r.choice(TUJUAN)
    kendaraan = r.choice(["bike", "pedicab", "bus", "car", "motorcycle"])
    return teks_pilihan(r, f"___ does {nama} go to {tujuan}? {nama} goes to {tujuan} by {kendaraan}.", "How",
                        ["Where", "When", "Who"],
                        '"How" dipakai untuk menanyakan cara atau kendaraan (naik apa)')


# ================================================== Unit 12 · go/goes to … at … by …

ORANG_12 = [("Father", "goes"), ("Mother", "goes"), ("Grandfather", "goes"), ("Joshua", "goes"),
            ("Cici", "goes"), ("Mr. Surya", "goes"), ("Mrs. Maria", "goes"),
            ("Aisyah and her family", "go"), ("Joshua and Made", "go"), ("We", "go"), ("I", "go")]
TUJUAN_12 = {"the office": "kantor", "the market": "pasar", "school": "sekolah", "the book store": "toko buku",
             "the paddy field": "sawah", "the supermarket": "swalayan", "the library": "perpustakaan"}
NAIK_12 = ["by bus", "by bike", "by pedicab", "by car", "by motorcycle", "by train", "on foot"]


def _kalimat_12(r, orang_ketiga=False):
    orang, pergi = r.choice([o for o in ORANG_12 if not (orang_ketiga and o[0] in ("I", "We"))])
    return orang, pergi, r.choice(list(TUJUAN_12)), r.choice(JAM_TULIS), r.choice(NAIK_12)


def u12_go_goes(r):
    orang, pergi, tujuan, jam, naik = _kalimat_12(r)
    return teks_pilihan(r, f"{orang} ___ to {tujuan} at {jam} {naik}.", pergi,
                        [x for x in ("go", "goes", "going", "is go") if x != pergi],
                        f'Subjek "{orang}" memakai "{pergi}": {orang} {pergi} to {tujuan} at {jam} {naik}.')


def u12_pahami(r):
    orang, pergi, tujuan, jam, naik = _kalimat_12(r, orang_ketiga=True)
    kalimat = f"{orang} {pergi} to {tujuan} at {jam} {naik}."
    bantu = "does" if pergi == "goes" else "do"
    tanya, jawab, salah = r.choice([
        (f"How {bantu} {orang} go to {tujuan}?", naik, [x for x in NAIK_12 if x != naik]),
        (f"What time {bantu} {orang} go to {tujuan}?", f"at {jam}", [f"at {x}" for x in JAM_TULIS if x != jam]),
        (f"Where {bantu} {orang} go at {jam}?", f"to {tujuan}", [f"to {x}" for x in TUJUAN_12 if x != tujuan]),
    ])
    return teks_pilihan(r, f"{kalimat} {tanya}", jawab, r.sample(salah, 3), f'Lihat kalimatnya: "{kalimat}"')


def u12_susun(r):
    orang, pergi, tujuan, jam, naik = _kalimat_12(r)
    benar = f"{orang} {pergi} to {tujuan} at {jam} {naik}."
    return _k(teks_pilihan(r, "Which sentence is in the correct order?", benar,
                           [f"{orang} to {tujuan} {pergi} at {jam} {naik}.",
                            f"{orang} {pergi} at {tujuan} to {jam} {naik}.",
                            f"{orang} {naik} {pergi} {jam} at to {tujuan}."],
                           f"Urutannya: subjek + go/goes + to (tempat) + at (waktu) + by (kendaraan): {benar}"),
              "u12-susun", benar)


def u12_kata_depan(r):
    orang, pergi, tujuan, jam, _ = _kalimat_12(r)
    kendaraan = r.choice(["bus", "bike", "pedicab", "car", "motorcycle", "train"])
    teks, jawab, arti = r.choice([
        (f"{orang} {pergi} ___ {tujuan} at {jam} by {kendaraan}.", "to", '"to" menunjukkan tempat tujuan'),
        (f"{orang} {pergi} to {tujuan} ___ {jam} by {kendaraan}.", "at", '"at" dipakai untuk jam'),
        (f"{orang} {pergi} to {tujuan} at {jam} ___ {kendaraan}.", "by", '"by" dipakai untuk kendaraan'),
    ])
    return teks_pilihan(r, teks, jawab, [x for x in ("to", "at", "by", "in") if x != jawab], arti)


def u12_jam_kata(r):
    orang, pergi, tujuan, _, naik = _kalimat_12(r)
    jam, menit = r.randint(5, 9), r.choice([0, 15, 30, 45])
    jawab = _ucapan_jam(jam, menit)
    return teks_pilihan(r, f"{orang} {pergi} to {tujuan} at {jam:02d}.{menit:02d} {naik}. "
                           f"We read the time as …", f"at {jawab}", [f"at {x}" for x in _jam_lain(r, jam, menit)],
                        f'{jam:02d}.{menit:02d} dibaca "{jawab}" ({_ATURAN_JAM[menit]})')


def u12_tanya(r):
    orang, pergi, tujuan, _, naik = _kalimat_12(r, orang_ketiga=True)
    jawab = "Does" if pergi == "goes" else "Do"
    return teks_pilihan(r, f"___ {orang} go to {tujuan} {naik}?", jawab,
                        [x for x in ("Do", "Does", "Is", "Are") if x != jawab],
                        f'Kalimat tanya untuk "{orang}" diawali "{jawab}" dan kata kerjanya kembali ke "go"')


def u12_arti_tempat(r):
    return _arti(r, {k.replace("the ", ""): v for k, v in TUJUAN_12.items()}, r.random() < 0.5)


# ------------------------------------------------------------------- perakit

PEMBANGKIT = {
    "en-unit-1": [u1_tobe, u1_ing, u1_ejaan, u1_tanya, u1_arti, u1_kalimat, u1_tempat],
    "en-unit-2": [u2_kata, u2_kata, u2_angka, u2_hitung, u2_hitung, u2_simbol, u2_antara, u2_urutan, u2_how_many],
    "en-unit-3": [u3_arti_ruang, u3_kegiatan, u3_arti_sifat, u3_lawan, u3_keadaan, u3_how_where, u3_denah, u3_denah],
    "en-unit-4": [u4_positif, u4_positif, u4_negatif, u4_tanya, u4_respon, u4_what_does, u4_bentuk_s,
                  u4_kegiatan_ruang],
    "en-unit-5": [u5_arti, u5_arti, u5_di_ruang, u5_there, u5_there_isi, u5_there_jawab, u5_how_many,
                  u5_jamak, u5_artikel, u5_letak_gambar, u5_letak_kalimat],
    "en-unit-6": [u6_arti, u6_arti, u6_di_ruang, u6_fungsi, u6_fungsi, u6_negatif, u6_tidak_cocok, u6_bacaan],
    "en-unit-7": [u7_can, u7_dasar, u7_kegiatan, u7_arti_kerja, u7_arti_kerja, u7_alat, u7_jawab],
    "en-unit-8": [u8_gambar, u8_gambar, u8_digital, u8_ke_angka, u8_ya_tidak, u8_kegiatan, u8_istilah],
    "en-unit-9": [u9_arti, u9_arti, u9_kolokasi, u9_urutan, u9_kapan, u9_dia, u9_lengkapi],
    "en-unit-10": [u10_arti, u10_konteks, u10_posisi, u10_kerja, u10_tanya, u10_bacaan, u10_bacaan],
    "en-unit-11": [u11_arti, u11_arti, u11_ciri, u11_by_on, u11_jalur, u11_how, u11_roda, u11_tanya],
    "en-unit-12": [u12_go_goes, u12_pahami, u12_pahami, u12_susun, u12_kata_depan, u12_jam_kata, u12_tanya,
                   u12_arti_tempat],
    # Kisi-kisi Tes Sumatif 3: benda di ruangan rumah, there is/are, how many, alat dapur,
    # kata kerja memasak, kalimat positif/negatif/tanya, dan respon pertanyaan.
    "en-ts3": [u5_arti, u6_arti, u6_arti, ts3_di_ruang, u5_there, u5_there_isi, u5_how_many, u5_jamak,
               u5_artikel, u7_arti_kerja, u6_fungsi, u4_positif, u4_negatif, u4_tanya, u4_respon, u4_respon],
}

GABUNGAN = {
    "en-semester-1": [f"en-unit-{i}" for i in range(1, 8)],
    "en-semester-2": [f"en-unit-{i}" for i in range(8, 13)],
}

KODE_TOPIK = [t["kode"] for t in TOPIK]


def buat_latihan(topik, jumlah=JUMLAH_SOAL, rng=None):
    """Buat ``jumlah`` soal Bahasa Inggris berbeda untuk satu unit atau satu paket gabungan."""
    if topik not in KODE_TOPIK:
        raise ValueError(f"topik tidak dikenal: {topik}")
    r = rng or random.Random()
    if topik in GABUNGAN:
        return rakit({k: PEMBANGKIT[k] for k in GABUNGAN[topik]}, topik, topik, jumlah, r)
    return rakit(PEMBANGKIT, topik, None, jumlah, r)
