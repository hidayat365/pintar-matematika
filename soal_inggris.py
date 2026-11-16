"""Pembangkit soal Bahasa Inggris SD kelas 4.

Bentuk soal sama dengan ``soal.py``: dict berisi "teks", "pilihan", "benar",
"pembahasan", ditambah "gambar" (SVG) atau "bacaan" (teks bacaan) bila ada.
Soal ditulis dalam bahasa Inggris, pembahasan dalam bahasa Indonesia.
"""

import random

from soal import JUMLAH_SOAL, _svg, rakit, teks_pilihan

TOPIK = [
    {"kode": "en-vocabulary", "nama": "Vocabulary", "ikon": "🔤",
     "ket": "Kosakata: hewan, buah, tubuh, keluarga, lawan kata"},
    {"kode": "en-numbers", "nama": "Numbers, Days & Time", "ikon": "🕒",
     "ket": "Bilangan, hari, bulan, dan jam"},
    {"kode": "en-tobe", "nama": "To Be & Pronouns", "ikon": "🙋",
     "ket": "am/is/are, he/she/they, my/your/his/her, this/that"},
    {"kode": "en-present", "nama": "Simple Present", "ikon": "🌞",
     "ket": "Kegiatan sehari-hari, do/does, always/never"},
    {"kode": "en-continuous", "nama": "Present Continuous", "ikon": "🏃",
     "ket": "Kegiatan yang sedang berlangsung (is/am/are + -ing)"},
    {"kode": "en-there", "nama": "There Is/Are & Prepositions", "ikon": "📦",
     "ket": "There is/are, in/on/under/next to, nama ruangan"},
    {"kode": "en-nouns", "nama": "Nouns & Articles", "ikon": "🍎",
     "ket": "Bentuk jamak (plural) dan a/an"},
    {"kode": "en-questions", "nama": "Questions & Answers", "ikon": "❓",
     "ket": "What/where/who/when, have/has, can, percakapan"},
    {"kode": "en-places", "nama": "Places, Jobs & Transportation", "ikon": "🚌",
     "ket": "Tempat umum, pekerjaan, dan kendaraan"},
    {"kode": "en-reading", "nama": "Reading", "ikon": "📖",
     "ket": "Memahami bacaan pendek"},
    {"kode": "en-campuran", "nama": "Mixed Practice", "ikon": "🌈",
     "ket": "Gabungan semua topik"},
]


def _k(soal, *kunci):
    """Beri penanda keunikan untuk soal yang teks pertanyaannya selalu sama."""
    soal["kunci"] = kunci
    return soal


# ------------------------------------------------------------------ kosakata

HEWAN = {"cat": "kucing", "dog": "anjing", "bird": "burung", "fish": "ikan", "horse": "kuda",
         "cow": "sapi", "goat": "kambing", "chicken": "ayam", "duck": "bebek", "rabbit": "kelinci",
         "elephant": "gajah", "tiger": "harimau", "monkey": "monyet", "snake": "ular",
         "butterfly": "kupu-kupu", "frog": "katak"}
BUAH = {"apple": "apel", "banana": "pisang", "orange": "jeruk", "grape": "anggur",
        "watermelon": "semangka", "mango": "mangga", "pineapple": "nanas", "papaya": "pepaya",
        "strawberry": "stroberi", "coconut": "kelapa"}
TUBUH = {"head": "kepala", "hair": "rambut", "eye": "mata", "ear": "telinga", "nose": "hidung",
         "mouth": "mulut", "hand": "tangan", "leg": "kaki", "finger": "jari", "tooth": "gigi",
         "shoulder": "bahu", "knee": "lutut", "stomach": "perut"}
KELUARGA = {"father": "ayah", "mother": "ibu", "brother": "saudara laki-laki",
            "sister": "saudara perempuan", "grandfather": "kakek", "grandmother": "nenek",
            "uncle": "paman", "aunt": "bibi", "cousin": "sepupu"}
KELAS = {"book": "buku", "pencil": "pensil", "eraser": "penghapus", "ruler": "penggaris", "bag": "tas",
         "table": "meja", "chair": "kursi", "door": "pintu", "window": "jendela",
         "whiteboard": "papan tulis", "clock": "jam dinding"}
MAKANAN = {"rice": "nasi", "bread": "roti", "egg": "telur", "milk": "susu", "water": "air",
           "noodles": "mi", "cheese": "keju", "cake": "kue", "soup": "sup", "sugar": "gula", "salt": "garam"}
WARNA = {"red": "merah", "blue": "biru", "green": "hijau", "yellow": "kuning", "black": "hitam",
         "white": "putih", "brown": "cokelat", "purple": "ungu", "pink": "merah muda", "grey": "abu-abu"}

KELOMPOK = {  # nama: (kata, sebutan Indonesia, pertanyaan "Which one …")
    "hewan": (HEWAN, "hewan", "Which one is an animal?"),
    "buah": (BUAH, "buah", "Which one is a fruit?"),
    "tubuh": (TUBUH, "anggota tubuh", "Which one is a part of the body?"),
    "keluarga": (KELUARGA, "anggota keluarga", "Which one is a family member?"),
    "kelas": (KELAS, "benda di kelas", None),
    "makanan": (MAKANAN, "makanan atau minuman", None),
    "warna": (WARNA, "warna", "Which one is a color?"),
}

LAWAN = [("big", "small"), ("tall", "short"), ("hot", "cold"), ("fast", "slow"), ("happy", "sad"),
         ("young", "old"), ("clean", "dirty"), ("open", "closed"), ("full", "empty"), ("heavy", "light"),
         ("early", "late"), ("cheap", "expensive"), ("easy", "difficult"), ("strong", "weak"),
         ("thick", "thin"), ("rich", "poor"), ("wet", "dry"), ("long", "short"), ("new", "old"),
         ("dark", "light")]


def v_arti_inggris(r):
    kata, _, _ = KELOMPOK[r.choice(list(KELOMPOK))]
    en, idn = r.choice(list(kata.items()))
    return teks_pilihan(r, f'What is "{idn}" in English?', en, [k for k in kata if k != en],
                        f'"{idn}" dalam bahasa Inggris adalah "{en}"')


def v_arti_indonesia(r):
    kata, _, _ = KELOMPOK[r.choice(list(KELOMPOK))]
    en, idn = r.choice(list(kata.items()))
    return teks_pilihan(r, f'What is the meaning of "{en}" in Indonesian?', idn,
                        [v for v in kata.values() if v != idn],
                        f'"{en}" artinya "{idn}"')


def v_kelompok(r):
    nama = r.choice([n for n, k in KELOMPOK.items() if k[2]])
    kata, sebutan, tanya = KELOMPOK[nama]
    # "orange" bisa berarti warna, dan sebagian hewan juga makanan: hindari pengecoh yang rancu.
    lain = [n for n in ("hewan", "tubuh", "keluarga", "kelas", "warna") if n != nama]
    jawab = r.choice(list(kata))
    salah = [r.choice(list(KELOMPOK[n][0])) for n in r.sample(lain, 3)]
    return _k(teks_pilihan(r, tanya, jawab, salah,
                           f'"{jawab}" ({kata[jawab]}) termasuk {sebutan}'), "kelompok", jawab)


def v_berbeda(r):
    a, b = r.sample(["hewan", "tubuh", "keluarga", "kelas", "warna", "buah"], 2)
    if {a, b} == {"warna", "buah"}:
        b = "hewan"
    tiga = r.sample(list(KELOMPOK[a][0]), 3)
    beda = r.choice(list(KELOMPOK[b][0]))
    return _k(teks_pilihan(r, "Which word is different from the others?", beda, tiga,
                           f'"{beda}" adalah {KELOMPOK[b][1]}, sedangkan tiga kata lainnya adalah {KELOMPOK[a][1]}'),
              "berbeda", beda)


def v_lawan(r):
    kata, lawan = r.choice(LAWAN)
    lain = [x for pasangan in LAWAN for x in pasangan if x not in (kata, lawan)]
    return teks_pilihan(r, f'The opposite of "{kata}" is …', lawan, r.sample(sorted(set(lain)), 3),
                        f'Lawan kata "{kata}" adalah "{lawan}"')


# ------------------------------------------------------ bilangan, hari, waktu

SATUAN = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
          "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen",
          "nineteen"]
PULUHAN = {2: "twenty", 3: "thirty", 4: "forty", 5: "fifty", 6: "sixty", 7: "seventy", 8: "eighty",
           9: "ninety"}
URUTAN = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth",
          "tenth", "eleventh", "twelfth"]
HARI = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
BULAN = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
         "October", "November", "December"]


def kata_bilangan(n):
    if n < 20:
        return SATUAN[n]
    if n == 100:
        return "one hundred"
    return PULUHAN[n // 10] + (f"-{SATUAN[n % 10]}" if n % 10 else "")


def _mirip(r, n):
    """Bilangan lain yang mudah tertukar dengan n."""
    calon = [n % 10 * 10 + n // 10, n + 10, n - 10, n + 1, n - 1, n // 10 + 10, n % 10 + 10]
    calon = [c for c in dict.fromkeys(calon) if 1 <= c <= 100 and c != n]
    r.shuffle(calon)
    return calon[:3]


def n_kata(r):
    n = r.randint(11, 99)
    return teks_pilihan(r, f"How do we write the number {n} in words?", kata_bilangan(n),
                        [kata_bilangan(c) for c in _mirip(r, n)], f"{n} ditulis \"{kata_bilangan(n)}\"")


def n_angka(r):
    n = r.randint(11, 99)
    return teks_pilihan(r, f'The number for "{kata_bilangan(n)}" is …', n, _mirip(r, n),
                        f'"{kata_bilangan(n)}" adalah {n}')


def n_urutan(r):
    i = r.randrange(12)
    return teks_pilihan(r, f"{BULAN[i]} is the … month of the year.", URUTAN[i],
                        [u for u in URUTAN if u != URUTAN[i]],
                        f"{BULAN[i]} adalah bulan ke-{i + 1}, dalam bahasa Inggris \"{URUTAN[i]}\"")


def n_hari(r):
    i = r.randrange(7)
    bentuk = r.randrange(4)
    if bentuk == 0:
        teks, j, bahas = f"The day after {HARI[i]} is …", i + 1, "sesudah"
    elif bentuk == 1:
        teks, j, bahas = f"The day before {HARI[i]} is …", i - 1, "sebelum"
    elif bentuk == 2:
        teks, j, bahas = f"Today is {HARI[i]}. Tomorrow is …", i + 1, "sesudah"
    else:
        teks, j, bahas = f"Today is {HARI[i]}. Yesterday was …", i - 1, "sebelum"
    jawab = HARI[j % 7]
    return teks_pilihan(r, teks, jawab, [h for h in HARI if h not in (jawab, HARI[i])],
                        f"Hari {bahas} {HARI[i]} adalah {jawab}")


def n_bulan(r):
    i = r.randrange(12)
    sesudah = r.random() < 0.5
    jawab = BULAN[(i + (1 if sesudah else -1)) % 12]
    return teks_pilihan(r, f"The month {'after' if sesudah else 'before'} {BULAN[i]} is …", jawab,
                        [b for b in BULAN if b not in (jawab, BULAN[i])],
                        f"Bulan {'sesudah' if sesudah else 'sebelum'} {BULAN[i]} adalah {jawab}")


def _ucapan_jam(jam, menit):
    berikut = jam % 12 + 1
    return {0: f"{SATUAN[jam]} o'clock", 15: f"quarter past {SATUAN[jam]}",
            30: f"half past {SATUAN[jam]}", 45: f"quarter to {SATUAN[berikut]}"}[menit]


def n_jam(r):
    jam, menit = r.randint(1, 12), r.choice([0, 15, 30, 45])
    jawab = _ucapan_jam(jam, menit)
    lain = {_ucapan_jam(j, m) for j in (jam, jam % 12 + 1) for m in (0, 15, 30, 45)} - {jawab}
    aturan = {0: "tepat jam → o'clock", 15: "lewat 15 menit → quarter past",
              30: "lewat 30 menit → half past", 45: "kurang 15 menit → quarter to (jam berikutnya)"}[menit]
    return teks_pilihan(r, f"The clock shows {jam}:{menit:02d}. What time is it?", f"It is {jawab}.",
                        [f"It is {x}." for x in r.sample(sorted(lain), 3)],
                        f"{jam}:{menit:02d} dibaca \"{jawab}\" ({aturan})")


_FAKTA_WAKTU = [
    ("How many days are there in a week?", "seven", ["five", "six", "ten"], "Satu minggu ada 7 hari"),
    ("How many months are there in a year?", "twelve", ["ten", "seven", "twenty"], "Satu tahun ada 12 bulan"),
    ("How many hours are there in a day?", "twenty-four", ["twelve", "sixty", "thirty"], "Satu hari ada 24 jam"),
    ("How many minutes are there in an hour?", "sixty", ["sixteen", "thirty", "one hundred"], "Satu jam ada 60 menit"),
    ("The first day of school in a week is usually …", "Monday", ["Sunday", "Saturday", "Friday"],
     "Sekolah biasanya dimulai pada hari Senin (Monday)"),
    ("The first month of the year is …", "January", ["December", "March", "June"],
     "Bulan pertama dalam setahun adalah January"),
    ("The last month of the year is …", "December", ["January", "November", "October"],
     "Bulan terakhir dalam setahun adalah December"),
    ("We celebrate Indonesian Independence Day in …", "August", ["April", "October", "June"],
     "Hari Kemerdekaan Indonesia jatuh pada 17 Agustus (August)"),
]


def n_fakta(r):
    return teks_pilihan(r, *r.choice(_FAKTA_WAKTU))


def n_hitung(r):
    a, b = r.randint(2, 12), r.randint(2, 8)
    if r.random() < 0.5:
        teks, hasil, tanda = f"{SATUAN[a].capitalize()} plus {SATUAN[b]} is …", a + b, "+"
    else:
        a = a + b
        teks, hasil, tanda = f"{kata_bilangan(a).capitalize()} minus {SATUAN[b]} is …", a - b, "−"
    lain = [kata_bilangan(x) for x in (hasil + 1, hasil - 1, hasil + 2, hasil + 10) if x > 0]
    return teks_pilihan(r, teks, kata_bilangan(hasil), lain,
                        f"{a} {tanda} {b} = {hasil}, dalam bahasa Inggris \"{kata_bilangan(hasil)}\"")


# ------------------------------------------------------------ subjek kalimat

PEREMPUAN = ["Rina", "Sinta", "Dewi", "Maya", "Putri", "Nisa"]
LAKI = ["Budi", "Andi", "Rudi", "Joko", "Dimas", "Bayu"]

# (subjek, to be, kata ganti, bentuk di tengah kalimat)
TUNGGAL = [("He", "is", "He", "he"), ("She", "is", "She", "she"), ("My father", "is", "He", "my father"),
           ("My mother", "is", "She", "my mother"), ("My sister", "is", "She", "my sister"),
           ("My brother", "is", "He", "my brother"), ("The teacher", "is", "The teacher", "the teacher")] + \
          [(n, "is", "She", n) for n in PEREMPUAN[:3]] + [(n, "is", "He", n) for n in LAKI[:3]]
JAMAK = [("You", "are", "You", "you"), ("We", "are", "We", "we"), ("They", "are", "They", "they"),
         ("My friends", "are", "They", "my friends"), ("Budi and Rina", "are", "They", "Budi and Rina"),
         ("The students", "are", "They", "the students")]
SAYA = ("I", "am", "I", "I")


def _subjek(r, dengan_saya=True):
    return r.choice(TUNGGAL + JAMAK * 2 + ([SAYA] * 2 if dengan_saya else []))


# ------------------------------------------------------- to be dan kata ganti

def tb_tobe(r):
    s, be, _, _ = _subjek(r)
    if be == "am":
        sisa = r.choice(["a student", "ten years old", "happy today", "in the classroom", "at home"])
    elif be == "is":
        sisa = r.choice(["happy today", "in the classroom", "at home", "very kind", "in the library",
                         "very busy", "in the garden"])
    else:
        sisa = r.choice(["happy today", "in the classroom", "at home", "very busy", "in the library",
                         "ready to study", "at school"])
    return teks_pilihan(r, f"{s} ___ {sisa}.", be, [x for x in ("am", "is", "are", "be") if x != be],
                        f'Subjek "{s}" memakai "{be}": {s} {be} {sisa}.')


def tb_tanya(r):
    s, be, _, tengah = _subjek(r)
    sisa = r.choice(["at home now", "in the classroom", "happy today", "ready", "hungry", "late for school"])
    jawab = be.capitalize()
    return teks_pilihan(r, f"___ {tengah} {sisa}?", jawab,
                        [x for x in ("Am", "Is", "Are", "Do") if x != jawab],
                        f'Kalimat tanya dengan subjek "{tengah}" diawali "{jawab}": {jawab} {tengah} {sisa}?')


def tb_kata_ganti(r):
    pilih = r.randrange(5)
    umur = r.choice(["nine", "ten", "eleven"])
    if pilih == 0:
        n = r.choice(PEREMPUAN)
        teks, jawab = f"{n} is my friend. ___ is {umur} years old.", "She"
        siapa = f"{n} (perempuan)"
    elif pilih == 1:
        n = r.choice(LAKI)
        teks, jawab = f"{n} is my friend. ___ is {umur} years old.", "He"
        siapa = f"{n} (laki-laki)"
    elif pilih == 2:
        benda, warna = r.choice(["bag", "bike", "pencil case", "kite", "umbrella"]), r.choice(list(WARNA))
        teks, jawab = f"This is my {benda}. ___ is {warna}.", "It"
        siapa = f"satu benda ({benda})"
    elif pilih == 3:
        a, b = r.choice(LAKI), r.choice(PEREMPUAN)
        teks, jawab = f"{a} and {b} are my classmates. ___ are very kind.", "They"
        siapa = f"{a} dan {b} (lebih dari satu orang)"
    else:
        n = r.choice(LAKI + PEREMPUAN)
        teks, jawab = f"{n} and I are classmates. ___ are in grade four.", "We"
        siapa = f"{n} dan saya"
    return teks_pilihan(r, teks, jawab, [x for x in ("He", "She", "It", "They", "We") if x != jawab],
                        f'Kata ganti untuk {siapa} adalah "{jawab}"')


_MILIK = [("I", "have", "my"), ("You", "have", "your"), ("He", "has", "his"), ("She", "has", "her"),
          ("We", "have", "our"), ("They", "have", "their")]


def tb_milik(r):
    benda = r.choice(["book", "bike", "bag", "ball", "kite", "ruler", "hat", "pencil"])
    pilih = r.randrange(8)
    if pilih < 6:
        s, punya, milik = _MILIK[pilih]
    elif pilih == 6:
        s, punya, milik = r.choice(LAKI), "has", "his"
    else:
        s, punya, milik = r.choice(PEREMPUAN), "has", "her"
    return teks_pilihan(r, f"{s} {punya} a {benda}. It is ___ {benda}.", milik,
                        [m for m in ("my", "your", "his", "her", "our", "their") if m != milik],
                        f'Kata milik untuk "{s}" adalah "{milik}"')


def tb_penunjuk(r):
    satu, banyak = r.choice([("book", "books"), ("pencil", "pencils"), ("bag", "bags"), ("kite", "kites"),
                             ("ball", "balls"), ("ruler", "rulers"), ("hat", "hats")])
    teks, jawab, alasan = r.choice([
        (f"I am holding a {satu}. ___ is my {satu}.", "This", "satu benda yang dekat"),
        (f"I am holding two {banyak}. ___ are my {banyak}.", "These", "beberapa benda yang dekat"),
        (f"Look at the {satu} over there. ___ is my {satu}.", "That", "satu benda yang jauh"),
        (f"Look at the {banyak} over there. ___ are my {banyak}.", "Those", "beberapa benda yang jauh"),
    ])
    return teks_pilihan(r, teks, jawab, [x for x in ("This", "That", "These", "Those") if x != jawab],
                        f'Untuk {alasan} dipakai "{jawab}"')


# ------------------------------------------------------------ simple present

# (kata kerja dasar, bentuk -s, bentuk -ing, lanjutan kalimat)
KERJA = [("go", "goes", "going", "to school"), ("play", "plays", "playing", "football"),
         ("read", "reads", "reading", "a book"), ("watch", "watches", "watching", "TV"),
         ("study", "studies", "studying", "English"), ("eat", "eats", "eating", "breakfast"),
         ("drink", "drinks", "drinking", "milk"), ("wash", "washes", "washing", "the dishes"),
         ("sweep", "sweeps", "sweeping", "the floor"), ("walk", "walks", "walking", "to the park"),
         ("ride", "rides", "riding", "a bike"), ("cook", "cooks", "cooking", "dinner"),
         ("write", "writes", "writing", "a letter"), ("sing", "sings", "singing", "a song"),
         ("swim", "swims", "swimming", "in the pool"), ("draw", "draws", "drawing", "a picture")]
KAPAN = ["every day", "every week", "on Sundays"]


def sp_kata_kerja(r):
    s, be, _, _ = _subjek(r)
    dasar, es, ing, sisa = r.choice(KERJA)
    kapan = r.choice(KAPAN)
    jawab = es if be == "is" else dasar
    alasan = ("subjek orang ketiga tunggal, kata kerjanya ditambah -s/-es" if be == "is"
              else "kata kerjanya tetap bentuk dasar")
    return teks_pilihan(r, f"{s} ___ {sisa} {kapan}.", jawab,
                        [x for x in (dasar, es, ing, f"{be} {dasar}") if x != jawab],
                        f'Untuk "{s}", {alasan}: {s} {jawab} {sisa} {kapan}.')


def sp_negatif(r):
    s, be, _, _ = _subjek(r)
    dasar, _, _, sisa = r.choice(KERJA)
    jawab = "doesn't" if be == "is" else "don't"
    return teks_pilihan(r, f"{s} ___ {dasar} {sisa} {r.choice(KAPAN)}.", jawab,
                        [x for x in ("don't", "doesn't", "isn't", "aren't") if x != jawab],
                        f'Kalimat negatif simple present untuk "{s}" memakai "{jawab}" + kata kerja dasar')


def sp_tanya(r):
    _, be, _, tengah = _subjek(r, dengan_saya=False)
    dasar, _, _, sisa = r.choice(KERJA)
    jawab = "Does" if be == "is" else "Do"
    return teks_pilihan(r, f"___ {tengah} {dasar} {sisa} {r.choice(KAPAN)}?", jawab,
                        [x for x in ("Do", "Does", "Is", "Are") if x != jawab],
                        f'Kalimat tanya simple present untuk "{tengah}" diawali "{jawab}"')


def sp_jawab_singkat(r):
    tanya, ganti, bantu = r.choice([("he", "he", "does"), ("she", "she", "does"), ("they", "they", "do"),
                                    ("you", "I", "do"), ("your friends", "they", "do"),
                                    ("your father", "he", "does"), ("your sister", "she", "does")])
    dasar, _, _, sisa = r.choice(KERJA)
    ya = r.random() < 0.5
    jawab = bantu if ya else bantu + "n't"
    return teks_pilihan(r, f"{bantu.capitalize()} {tanya} {dasar} {sisa}? {'Yes' if ya else 'No'}, {ganti} ___.",
                        jawab, [x for x in ("do", "does", "don't", "doesn't", "is", "isn't") if x != jawab],
                        f'Pertanyaan diawali "{bantu.capitalize()}", jadi jawaban singkatnya memakai "{jawab}"')


_FREKUENSI = [
    ('What is the meaning of "always"?', "selalu", ["kadang-kadang", "tidak pernah", "jarang"]),
    ('What is the meaning of "usually"?', "biasanya", ["tidak pernah", "selalu", "jarang"]),
    ('What is the meaning of "sometimes"?', "kadang-kadang", ["selalu", "tidak pernah", "setiap hari"]),
    ('What is the meaning of "never"?', "tidak pernah", ["selalu", "kadang-kadang", "biasanya"]),
    ('What is the meaning of "often"?', "sering", ["tidak pernah", "jarang", "kemarin"]),
    ('What is the meaning of "every day"?', "setiap hari", ["kemarin", "besok", "tidak pernah"]),
    ("School is closed on Sunday. We ___ go to school on Sunday.", "never", ["always", "usually", "often"]),
    ("Rina brushes her teeth every morning and every night. She ___ brushes her teeth.", "always",
     ["never", "rarely", "sometimes"]),
    ("Fish cannot live on land. Fish ___ live in the water.", "always", ["never", "sometimes", "rarely"]),
    ("The sun ___ rises in the west.", "never", ["always", "usually", "often"]),
]


def sp_frekuensi(r):
    teks, jawab, salah = r.choice(_FREKUENSI)
    return teks_pilihan(r, teks, jawab, salah,
                        "always = selalu, usually = biasanya, often = sering, "
                        "sometimes = kadang-kadang, never = tidak pernah")


# -------------------------------------------------------- present continuous

SEKARANG = ["now", "right now", "at the moment"]


def pc_tobe(r):
    s, be, _, _ = _subjek(r)
    _, _, ing, sisa = r.choice(KERJA)
    return teks_pilihan(r, f"{s} ___ {ing} {sisa} {r.choice(SEKARANG)}.", be,
                        [x for x in ("am", "is", "are", "do") if x != be],
                        f'Present continuous: subjek + am/is/are + kata kerja-ing. Untuk "{s}" dipakai "{be}"')


def pc_ing(r):
    s, be, _, _ = _subjek(r)
    dasar, es, ing, sisa = r.choice(KERJA)
    return teks_pilihan(r, f"{s} {be} ___ {sisa} {r.choice(SEKARANG)}.", ing, [dasar, es, f"to {dasar}"],
                        f'Setelah "{be}" pada kegiatan yang sedang berlangsung, kata kerja diberi -ing: {ing}')


def pc_ejaan(r):
    jenis = r.randrange(3)
    if jenis == 0:
        d = r.choice(["run", "swim", "sit", "cut", "hop", "stop", "clap", "skip"])
        jawab, salah = d + d[-1] + "ing", [d + "ing", d + "eing", d + d[-1] + "eing"]
        aturan = "konsonan terakhir digandakan lalu ditambah -ing"
    elif jenis == 1:
        d = r.choice(["write", "dance", "ride", "make", "bake", "come", "take", "smile"])
        jawab, salah = d[:-1] + "ing", [d + "ing", d[:-1] + d[-2] + "ing", d[:-1] + "ng"]
        aturan = "huruf e di akhir dihilangkan lalu ditambah -ing"
    else:
        d = r.choice(["play", "read", "eat", "sleep", "cook", "jump", "drink", "walk", "sing"])
        jawab, salah = d + "ing", [d + d[-1] + "ing", d + "eing", d[:-1] + "ing"]
        aturan = "cukup ditambah -ing"
    return teks_pilihan(r, f'The -ing form of "{d}" is …', jawab, salah, f'"{d}" → "{jawab}": {aturan}')


def pc_tanya(r):
    dasar, es, ing, sisa = r.choice(KERJA)
    tanya, ganti, be = r.choice([("is he", "He", "is"), ("is she", "She", "is"), ("are they", "They", "are"),
                                 ("are you", "I", "am"), ("are the children", "They", "are")])
    lain = "are" if be != "are" else "is"
    return teks_pilihan(r, f"What {tanya} doing? {ganti} ___ {sisa}.", f"{be} {ing}",
                        [es, dasar, f"{lain} {ing}", ing],
                        f'Pertanyaan "What … doing?" dijawab dengan {be} + kata kerja-ing: {ganti} {be} {ing} {sisa}.')


def pc_negatif(r):
    ganti, be, tidak = r.choice([("He", "is", "isn't"), ("She", "is", "isn't"), ("They", "are", "aren't"),
                                 ("We", "are", "aren't"), ("I", "am", "am not")])
    (_, _, ing1, sisa1), (_, _, ing2, sisa2) = r.sample(KERJA, 2)
    return teks_pilihan(r, f"{ganti} ___ {ing1} {sisa1}. {ganti} {be} {ing2} {sisa2}.", tidak,
                        [x for x in ("isn't", "aren't", "am not", "don't", "doesn't") if x != tidak],
                        f'Bentuk negatif present continuous untuk "{ganti}" adalah "{tidak}" + kata kerja-ing')


# ------------------------------------------- there is/are dan kata depan tempat

BENDA = [("a", "book", "books"), ("a", "pencil", "pencils"), ("an", "eraser", "erasers"),
         ("a", "clock", "clocks"), ("an", "apple", "apples"), ("a", "bag", "bags"), ("a", "lamp", "lamps"),
         ("an", "umbrella", "umbrellas"), ("a", "ball", "balls"), ("a", "picture", "pictures")]
LETAK = ["on the table", "in the room", "in the classroom", "under the chair", "in the living room",
         "on the floor", "in the cupboard"]


def ta_tobe(r):
    art, satu, banyak = r.choice(BENDA)
    letak = r.choice(LETAK)
    if r.random() < 0.5:
        isi, jawab, alasan = f"{art} {satu}", "is", "satu benda"
    else:
        isi, jawab, alasan = f"{r.choice(['two', 'three', 'four', 'five', 'some', 'many'])} {banyak}", "are", "lebih dari satu benda"
    return teks_pilihan(r, f"There ___ {isi} {letak}.", jawab, [x for x in ("is", "are", "am", "be") if x != jawab],
                        f'Untuk {alasan} dipakai "There {jawab}": There {jawab} {isi} {letak}.')


def ta_jawab(r):
    art, satu, banyak = r.choice(BENDA)
    letak, ya = r.choice(LETAK), r.random() < 0.5
    if r.random() < 0.5:
        tanya, jawab = f"Is there {art} {satu} {letak}?", "is" if ya else "isn't"
    else:
        tanya, jawab = f"Are there any {banyak} {letak}?", "are" if ya else "aren't"
    return teks_pilihan(r, f"{tanya} {'Yes' if ya else 'No'}, there ___.", jawab,
                        [x for x in ("is", "are", "isn't", "aren't") if x != jawab],
                        f'Pertanyaan "{tanya.split()[0]} there …?" dijawab dengan "there {jawab}"')


_BOLA = '<circle cx="{x}" cy="{y}" r="14" fill="#ffb703" stroke="#b97f00"/>'
_KOTAK = '<rect x="{x}" y="62" width="70" height="70" fill="#e3e9ff"/>'
_MEJA = ('<rect x="40" y="70" width="140" height="12" fill="#e3e9ff"/>'
         '<line x1="56" y1="82" x2="56" y2="138"/><line x1="164" y1="82" x2="164" y2="138"/>')
_LANTAI = '<line x1="10" y1="140" x2="210" y2="140" stroke="#9aa3c2" stroke-width="2"/>'

_GAMBAR_LETAK = {  # kata depan: (gambar, benda acuan, pengecoh yang dihindari, arti)
    "on": (_MEJA + _BOLA.format(x=110, y=54), "table", [], "di atas"),
    "under": (_MEJA + _BOLA.format(x=110, y=124), "table", [], "di bawah"),
    "in": ('<path d="M75 62 V132 H145 V62" fill="#e3e9ff"/>' + _BOLA.format(x=110, y=112) + _LANTAI,
           "box", ["in front of"], "di dalam"),
    "next to": (_KOTAK.format(x=45) + _BOLA.format(x=150, y=124) + _LANTAI, "box", [], "di samping"),
    "behind": (_BOLA.format(x=140, y=56) + _KOTAK.format(x=75) + _LANTAI, "box", ["on"], "di belakang"),
    "between": (_KOTAK.format(x=15) + _KOTAK.format(x=135) + _BOLA.format(x=110, y=124) + _LANTAI,
                "boxes", [], "di antara"),
}


def ta_letak_gambar(r):
    depan = r.choice(list(_GAMBAR_LETAK))
    gambar, acuan, hindari, arti = _GAMBAR_LETAK[depan]
    lain = [d for d in ("in", "on", "under", "next to", "behind", "between") if d != depan and d not in hindari]
    soal = teks_pilihan(r, f"Look at the picture. The ball is ___ the {acuan}.", depan, lain,
                        f'Bola berada {arti} {"kotak-kotak" if acuan == "boxes" else "meja" if acuan == "table" else "kotak"}: '
                        f'"{depan}" = {arti}')
    soal["gambar"] = _svg(gambar)
    return _k(soal, "letak", depan)


_LETAK_KALIMAT = [
    ("The fish is ___ the aquarium.", "in"), ("The picture is ___ the wall.", "on"),
    ("The milk is ___ the fridge.", "in"), ("The books are ___ the bag.", "in"),
    ("The plate is ___ the table.", "on"), ("The carpet is ___ the floor.", "on"),
    ("The roots of a tree are ___ the ground.", "under"),
    ("The letter B is ___ the letters A and C.", "between"),
    ("Tuesday is ___ Monday and Wednesday.", "between"),
    ("The number 5 is ___ the numbers 4 and 6.", "between"),
    ("My shoes are ___ my feet.", "on"), ("The clothes are ___ the cupboard.", "in"),
]


def ta_letak_kalimat(r):
    teks, jawab = r.choice(_LETAK_KALIMAT)
    return teks_pilihan(r, teks, jawab, [d for d in ("in", "on", "under", "between") if d != jawab],
                        "in = di dalam, on = di atas (menempel), under = di bawah, between = di antara")


_RUANG = [("cook our food", "kitchen", "dapur"), ("sleep at night", "bedroom", "kamar tidur"),
          ("take a bath", "bathroom", "kamar mandi"), ("sit and watch TV with the family", "living room", "ruang keluarga"),
          ("eat together at the table", "dining room", "ruang makan"), ("park the car", "garage", "garasi"),
          ("plant flowers", "garden", "taman")]


def ta_ruang(r):
    kegiatan, ruang, arti = r.choice(_RUANG)
    return teks_pilihan(r, f"We {kegiatan} in the ___.", ruang, [x[1] for x in _RUANG if x[1] != ruang],
                        f'"{ruang}" artinya {arti}')


# ----------------------------------------------------- kata benda dan artikel

_JAMAK_S = ["book", "pen", "chair", "cat", "apple", "bag", "door", "car", "bird", "table"]
_JAMAK_ES = ["box", "bus", "glass", "watch", "dish", "brush", "class", "fox", "bench", "dress"]
_JAMAK_IES = ["baby", "city", "story", "candy", "butterfly", "family", "strawberry", "puppy"]
_JAMAK_LAIN = {"man": "men", "woman": "women", "child": "children", "foot": "feet", "tooth": "teeth",
               "mouse": "mice", "goose": "geese"}


def _jamak(r):
    """Pilih satu kata benda: (tunggal, jamak, bentuk salah, aturan)."""
    jenis = r.randrange(4)
    if jenis == 0:
        k = r.choice(_JAMAK_S)
        return k, k + "s", [k + "es", k + "ies", k], "cukup ditambah -s"
    if jenis == 1:
        k = r.choice(_JAMAK_ES)
        return k, k + "es", [k + "s", k + "ies", k], "kata berakhiran s, x, ch, sh ditambah -es"
    if jenis == 2:
        k = r.choice(_JAMAK_IES)
        return k, k[:-1] + "ies", [k + "s", k + "es", k + "ies"], "akhiran y diganti -ies"
    k, j = r.choice(list(_JAMAK_LAIN.items()))
    return k, j, [k + "s", k + "es", j + "s"], "bentuk jamaknya tidak beraturan dan perlu dihafal"


def na_jamak(r):
    k, j, salah, aturan = _jamak(r)
    return teks_pilihan(r, f'The plural form of "{k}" is …', j, salah, f'"{k}" → "{j}": {aturan}')


def na_jumlah(r):
    k, j, salah, aturan = _jamak(r)
    n = r.choice(["two", "three", "four", "five", "many"])
    return teks_pilihan(r, f"I see one {k}. You see {n} ___.", j, salah,
                        f'Lebih dari satu memakai bentuk jamak. "{k}" → "{j}": {aturan}')


_AN = ["apple", "orange", "egg", "umbrella", "eraser", "elephant", "ant", "onion", "ice cream", "owl",
       "old book", "empty box"]
_A = ["book", "banana", "cat", "pencil", "ruler", "dog", "table", "yellow bag", "big house", "kite",
      "red apple", "small egg"]


def na_artikel(r):
    pakai_an = r.random() < 0.5
    kata = r.choice(_AN if pakai_an else _A)
    jawab = "an" if pakai_an else "a"
    kalimat = r.choice(["This is ___ {}.", "I see ___ {}.", "There is ___ {} in the picture."]).format(kata)
    alasan = "diawali bunyi vokal (a, i, u, e, o)" if pakai_an else "diawali bunyi konsonan"
    return teks_pilihan(r, kalimat, jawab, [x for x in ("a", "an", "any", "many") if x != jawab],
                        f'"{kata}" {alasan}, jadi memakai "{jawab}"')


def na_tunggal_jamak(r):
    k, j, _, _ = _jamak(r)
    if r.random() < 0.5:
        return teks_pilihan(r, f"There are three ___ in the picture.", j,
                            [k, f"a {k}", f"one {k}"],
                            f'"three" berarti lebih dari satu, jadi memakai bentuk jamak "{j}"')
    art = "an" if k[0] in "aeiou" else "a"
    return teks_pilihan(r, f"There is ___ in the picture.", f"{art} {k}",
                        [j, f"two {j}", f"many {j}"],
                        f'"There is" dipakai untuk satu benda, jadi jawabannya "{art} {k}"')


# ------------------------------------------------------- pertanyaan & jawaban

def qw_kata_tanya(r):
    nama = r.choice(LAKI + PEREMPUAN)
    benda = r.choice(["bag", "pencil", "book", "ruler", "hat"])
    kota = r.choice(["Bandung", "Jakarta", "Surabaya", "Medan", "Makassar", "Yogyakarta"])
    teks, jawab, arti = r.choice([
        (f"___ is your name? My name is {nama}.", "What", "apa"),
        (f"___ do you live? I live in {kota}.", "Where", "di mana"),
        (f"___ is that woman? She is my {r.choice(['aunt', 'teacher', 'mother', 'grandmother'])}.", "Who", "siapa"),
        (f"___ is your birthday? It is in {r.choice(BULAN)}.", "When", "kapan"),
        (f"___ old are you? I am {r.choice(['nine', 'ten', 'eleven'])} years old.", "How", "berapa (umur)"),
        (f"___ many {benda}s do you have? I have {r.choice(['two', 'three', 'four'])}.", "How", "berapa banyak"),
        (f"___ are you crying? Because I lost my {benda}.", "Why", "mengapa"),
        (f"___ color is your {benda}? It is {r.choice(list(WARNA))}.", "What", "apa (warna apa)"),
        (f"___ is my {benda}? It is {r.choice(['on the table', 'under the chair', 'in the bag'])}.", "Where", "di mana"),
        (f"___ do you go to school? I go to school by {r.choice(['bike', 'bus', 'car'])}.", "How", "bagaimana / naik apa"),
        (f"___ is your teacher? {r.choice(['Mrs. Ani', 'Mr. Hadi', 'Mrs. Sari'])} is my teacher.", "Who", "siapa"),
        (f"___ do you go to bed? I go to bed at nine o'clock.", "When", "kapan"),
        (f"___ is {nama} absent today? Because {nama} is sick.", "Why", "mengapa"),
    ])
    return teks_pilihan(r, teks, jawab, [x for x in ("What", "Where", "Who", "When", "Why", "How") if x != jawab],
                        f'Jawabannya menunjukkan yang ditanyakan adalah "{arti}", jadi memakai "{jawab}"')


def qw_have(r):
    s, be, _, _ = _subjek(r)
    benda = r.choice(["a new bag", "two brothers", "a pet cat", "many books", "a red bike", "long hair",
                      "a big house", "three pencils"])
    jawab = "has" if be == "is" else "have"
    return teks_pilihan(r, f"{s} ___ {benda}.", jawab, [x for x in ("have", "has", "having", "haves") if x != jawab],
                        f'Subjek "{s}" memakai "{jawab}"')


_BISA = [("bird", "fly", True), ("fish", "swim", True), ("fish", "walk", False), ("cat", "fly", False),
         ("horse", "run", True), ("snake", "run", False), ("monkey", "climb", True), ("duck", "swim", True),
         ("cow", "fly", False), ("rabbit", "jump", True), ("tiger", "run", True), ("elephant", "fly", False)]


def qw_can(r):
    hewan, kerja, bisa = r.choice(_BISA)
    if r.random() < 0.5:
        tanya, ganti = f"Can a {hewan} {kerja}?", "it"
    else:
        tanya, ganti = f"Can {hewan if hewan == 'fish' else hewan + 's'} {kerja}?", "they"
    jawab = f"Yes, {ganti} can." if bisa else f"No, {ganti} can't."
    return teks_pilihan(r, tanya, jawab,
                        [x for x in (f"Yes, {ganti} can.", f"No, {ganti} can't.",
                                     f"Yes, {ganti} {'is' if ganti == 'it' else 'are'}.",
                                     f"No, {ganti} {'does' if ganti == 'it' else 'do'}n't.") if x != jawab],
                        f'Pertanyaan "Can …?" dijawab dengan "can" atau "can\'t": {jawab}')


_PERCAKAPAN = [
    ("How are you?", "I am fine, thank you."), ("What is your name?", "My name is Sinta."),
    ("Where do you live?", "I live in Jakarta."), ("How old are you?", "I am ten years old."),
    ("Thank you very much.", "You are welcome."), ("Good morning, students.", "Good morning, teacher."),
    ("What is your hobby?", "My hobby is reading."), ("Nice to meet you.", "Nice to meet you, too."),
    ("What time do you go to school?", "At half past six."), ("See you tomorrow.", "See you. Goodbye."),
    ("I am sorry. I broke your pencil.", "It is okay. Don't worry."),
    ("How do you go to school?", "By bike."), ("What day is it today?", "It is Monday."),
]
_RANCU = {"Thank you very much.": ["It is okay. Don't worry."],
          "I am sorry. I broke your pencil.": ["You are welcome."]}


def qw_percakapan(r):
    tanya, jawab = r.choice(_PERCAKAPAN)
    a, b = r.sample(LAKI + PEREMPUAN, 2)
    lain = [j for _, j in _PERCAKAPAN if j != jawab and j not in _RANCU.get(tanya, [])]
    return teks_pilihan(r, f'{a}: "{tanya}"   {b}: "…"', jawab, r.sample(lain, 3),
                        f'Jawaban yang sesuai untuk "{tanya}" adalah "{jawab}"')


# ------------------------------------------- tempat, pekerjaan, dan kendaraan

# (pekerjaan, kegiatan, tempat kerja, arti)
PEKERJAAN = [
    ("teacher", "teaches students", "at a school", "guru"),
    ("doctor", "examines sick people and gives them medicine", "in a hospital", "dokter"),
    ("farmer", "plants rice in the field", "in a rice field", "petani"),
    ("pilot", "flies an airplane", None, "pilot"),
    ("chef", "cooks food in a restaurant", "in a restaurant", "koki"),
    ("police officer", "catches thieves and keeps us safe", "at a police station", "polisi"),
    ("fisherman", "catches fish in the sea", None, "nelayan"),
    ("postman", "delivers letters to our houses", None, "tukang pos"),
    ("tailor", "makes and sews clothes", None, "penjahit"),
    ("firefighter", "puts out fires", None, "pemadam kebakaran"),
    ("dentist", "takes care of our teeth", None, "dokter gigi"),
    ("driver", "drives a bus or a car", None, "sopir"),
    ("singer", "sings songs on the stage", None, "penyanyi"),
    ("librarian", "takes care of the books in a library", "in a library", "pustakawan"),
    ("nurse", "helps the doctor take care of patients", None, "perawat"),
]
_KESEHATAN = {"doctor", "nurse", "dentist"}

# (tempat, kegiatan di sana, arti)
TEMPAT = [
    ("library", "we can borrow and read books", "perpustakaan"),
    ("hospital", "sick people see a doctor", "rumah sakit"),
    ("market", "people buy vegetables, fruit and fish", "pasar"),
    ("zoo", "we can see lions, elephants and giraffes", "kebun binatang"),
    ("post office", "we send letters and packages", "kantor pos"),
    ("bank", "people save their money", "bank"),
    ("airport", "planes take off and land", "bandara"),
    ("train station", "we wait for a train", "stasiun kereta api"),
    ("school", "students study with their teachers", "sekolah"),
    ("cinema", "we watch movies on a big screen", "bioskop"),
    ("restaurant", "we order food and eat it there", "restoran"),
    ("swimming pool", "we swim", "kolam renang"),
]

# (kendaraan, ciri, arti)
KENDARAAN = [
    ("bike", "It has two wheels and no engine. We pedal it.", "sepeda"),
    ("motorcycle", "It has two wheels and an engine.", "sepeda motor"),
    ("car", "It has four wheels. A small family can ride in it.", "mobil"),
    ("bus", "It is a big vehicle on the road. It carries many passengers.", "bus"),
    ("train", "It is very long and runs on rails.", "kereta api"),
    ("plane", "It has two wings and takes off from an airport.", "pesawat terbang"),
    ("ship", "It is very big and sails on the sea.", "kapal laut"),
    ("helicopter", "It flies with a big propeller on its top.", "helikopter"),
    ("truck", "It is a big vehicle that carries sand, boxes or other goods.", "truk"),
]


def pj_pekerjaan(r):
    kerja, kegiatan, _, arti = r.choice(PEKERJAAN)
    lain = [p[0] for p in PEKERJAAN if p[0] != kerja and not (kerja in _KESEHATAN and p[0] in _KESEHATAN)]
    return teks_pilihan(r, f"A ___ {kegiatan}.", kerja, r.sample(lain, 3), f'"{kerja}" artinya {arti}')


def pj_tempat_kerja(r):
    kerja, _, tempat, arti = r.choice([p for p in PEKERJAAN if p[2]])
    lain = [p[2] for p in PEKERJAAN if p[2] and p[2] != tempat] + ["at an airport", "at a market"]
    return teks_pilihan(r, f"Where does a {kerja} work?", tempat, r.sample(lain, 3),
                        f'A {kerja} ({arti}) works {tempat}.')


def pj_tempat(r):
    tempat, kegiatan, arti = r.choice(TEMPAT)
    return teks_pilihan(r, f"The ___ is a place where {kegiatan}.", tempat,
                        r.sample([t[0] for t in TEMPAT if t[0] != tempat], 3), f'"{tempat}" artinya {arti}')


def pj_kendaraan(r):
    nama, ciri, arti = r.choice(KENDARAAN)
    return teks_pilihan(r, f"{ciri} What is it?", nama,
                        r.sample([k[0] for k in KENDARAAN if k[0] != nama], 3), f'"{nama}" artinya {arti}')


def pj_arti(r):
    daftar = r.choice([[(p[0], p[3]) for p in PEKERJAAN], [(t[0], t[2]) for t in TEMPAT],
                       [(k[0], k[2]) for k in KENDARAAN]])
    daftar = [(en, idn) for en, idn in daftar if en != idn]
    en, idn = r.choice(daftar)
    return teks_pilihan(r, f'What is "{idn}" in English?', en, r.sample([e for e, _ in daftar if e != en], 3),
                        f'"{idn}" dalam bahasa Inggris adalah "{en}"')


# -------------------------------------------------------------------- bacaan

def _bacaan_baru(r):
    """Empat bacaan pendek beserta pertanyaannya; dipakai bersama dalam satu latihan."""
    kota = ["Bandung", "Jakarta", "Surabaya", "Medan", "Makassar", "Yogyakarta", "Semarang"]
    jam = ["five o'clock", "half past five", "six o'clock", "half past four"]
    nama = r.sample(PEREMPUAN + LAKI, 5)
    hasil = []

    def ganti(n):
        return ("She", "she", "her") if n in PEREMPUAN else ("He", "he", "his")

    def tambah(bacaan, daftar):
        for tanya, jawab, salah, kalimat in daftar:
            hasil.append((bacaan, tanya, jawab, salah, kalimat))

    # 1. Perkenalan diri
    n = nama[0]
    umur, tinggal = r.choice(["nine", "ten", "eleven"]), r.choice(kota)
    hobi = r.choice(["reading", "swimming", "drawing", "singing", "playing football", "cycling"])
    makan = r.choice(["fried rice", "chicken soup", "noodles", "fried chicken", "meatballs"])
    warna = r.choice(["red", "blue", "green", "yellow", "purple"])
    hewan = r.choice(["cat", "rabbit", "bird", "dog", "hamster", "turtle"])
    piara = r.choice(["Milo", "Coco", "Luna", "Kiki", "Momo", "Bobo"])
    k = [f"Hello! My name is {n}.", f"I am {umur} years old.", f"I live in {tinggal}.", "I am in grade four.",
         f"My hobby is {hobi}.", f"My favorite food is {makan}, and my favorite color is {warna}.",
         f"I have a pet {hewan}.", f"Its name is {piara}."]
    tambah(" ".join(k), [
        (f"How old is {n}?", f"{umur} years old", ["eight years old", "twelve years old", "seven years old"], k[1]),
        (f"Where does {n} live?", f"in {tinggal}", [f"in {x}" for x in kota if x != tinggal], k[2]),
        (f"What is {n}'s hobby?", hobi, ["cooking", "dancing", "fishing", "painting"], k[4]),
        (f"What is {n}'s favorite food?", makan, ["bread", "fried fish", "pizza", "salad"], k[5]),
        (f"What is {n}'s favorite color?", warna, ["black", "white", "pink", "brown"], k[5]),
        (f"What pet does {n} have?", f"a {hewan}", ["a fish", "a horse", "a duck", "a goat"], k[6]),
        (f"What is the name of {n}'s pet?", piara, ["Bella", "Rocky", "Mimi", "Toto"], k[7]),
        (f"What grade is {n} in?", "grade four", ["grade three", "grade five", "grade six"], k[3]),
    ])

    # 2. Kegiatan sehari-hari
    n = nama[1]
    S, s, milik = ganti(n)
    bangun = r.choice(jam)
    sarapan = r.choice(["fried rice", "bread and milk", "noodles", "porridge", "an omelet"])
    naik = r.choice(["bike", "bus", "car", "motorcycle"])
    sore = r.choice(["plays football", "reads books in the library", "plays badminton", "swims in the pool"])
    k = [f"{n} is a student.", f"{S} gets up at {bangun} every morning.", f"{S} has {sarapan} for breakfast.",
         f"Then {s} goes to school by {naik}.", "School starts at seven o'clock.",
         f"After school, {n} {sore}.", f"In the evening, {s} does {milik} homework.",
         f"{S} goes to bed at nine o'clock."]
    tambah(" ".join(k), [
        (f"What time does {n} get up?", f"at {bangun}", ["at seven o'clock", "at eight o'clock", "at nine o'clock"], k[1]),
        (f"What does {n} have for breakfast?", sarapan, ["fried chicken", "fruit salad", "chicken soup", "meatballs"], k[2]),
        (f"How does {n} go to school?", f"by {naik}", ["by train", "by boat", "by plane", "by taxi"], k[3]),
        ("What time does school start?", "at seven o'clock", ["at six o'clock", "at eight o'clock", "at ten o'clock"], k[4]),
        (f"What does {n} do after school?", sore, ["watches TV", "goes to the market", "cooks dinner", "plays the guitar"], k[5]),
        (f"What does {n} do in the evening?", f"does {milik} homework", ["watches TV", "plays games", "goes to school"], k[6]),
        (f"What time does {n} go to bed?", "at nine o'clock", ["at ten o'clock", "at eight o'clock", "at eleven o'clock"], k[7]),
    ])

    # 3. Ruang kelas
    n, teman = nama[2], nama[3]
    meja = r.randint(15, 19)
    kursi, murid = meja * 2, r.randint(25, 29)
    guru, G = r.choice([("Mrs. Ani", "She"), ("Mr. Hadi", "He"), ("Mrs. Sari", "She"), ("Mr. Bima", "He")])
    mapel = r.choice(["English", "Math", "Science", "Art"])
    k = [f"This is {n}'s classroom.", "It is big and clean.",
         f"There are {meja} tables and {kursi} chairs in the classroom.", "There is a whiteboard on the wall.",
         f"There are {murid} students in the class.", f"The teacher is {guru}.", f"{G} teaches {mapel}.",
         f"{n} sits next to {teman}."]
    tambah(" ".join(k), [
        ("How many tables are there in the classroom?", meja, [kursi, murid, meja + 2, meja - 3], k[2]),
        ("How many chairs are there in the classroom?", kursi, [meja, murid, kursi + 2, kursi - 4], k[2]),
        ("How many students are there in the class?", murid, [meja, kursi, murid + 3, murid - 3], k[4]),
        ("Who is the teacher?", guru, [x for x in ("Mrs. Ani", "Mr. Hadi", "Mrs. Sari", "Mr. Bima") if x != guru], k[5]),
        (f"What does {guru} teach?", mapel, [x for x in ("English", "Math", "Science", "Art") if x != mapel], k[6]),
        ("Where is the whiteboard?", "on the wall", ["on the table", "under the chair", "next to the door"], k[3]),
        (f"Who sits next to {n}?", teman, [x for x in PEREMPUAN + LAKI if x not in (n, teman)], k[7]),
        ("What is the classroom like?", "big and clean", ["small and dirty", "big and dirty", "small and clean"], k[1]),
    ])

    # 4. Keluarga
    n = nama[4]
    S, s, milik = ganti(n)
    tinggal = r.choice(kota)
    ayah, ibu = r.sample(["teacher", "doctor", "farmer", "driver", "chef", "nurse", "tailor"], 2)
    saudara = ["one brother and one sister", "two sisters", "two brothers", "one little sister"]
    punya = r.choice(saudara)
    tujuan, naik = r.choice(["park", "beach", "zoo", "market"]), r.choice(["car", "bus", "train"])
    k = [f"{n} lives with {milik} family in {tinggal}.", f"{milik.capitalize()} father is a {ayah}.",
         f"{milik.capitalize()} mother is a {ibu}.", f"{n} has {punya}.",
         f"Every Sunday, the family goes to the {tujuan}.", f"They go there by {naik}.",
         f"{n} loves {milik} family very much."]
    tambah(" ".join(k), [
        (f"What is the job of {n}'s father?", f"a {ayah}", [f"a {ibu}", "a pilot", "a singer"], k[1]),
        (f"What is the job of {n}'s mother?", f"a {ibu}", [f"a {ayah}", "a pilot", "a singer"], k[2]),
        (f"How many brothers and sisters does {n} have?", punya, [x for x in saudara if x != punya], k[3]),
        ("Where does the family go every Sunday?", f"to the {tujuan}",
         [f"to the {x}" for x in ("park", "beach", "zoo", "market", "cinema") if x != tujuan], k[4]),
        (f"How does the family go to the {tujuan}?", f"by {naik}", [f"by {x}" for x in ("car", "bus", "train", "bike") if x != naik], k[5]),
        (f"When does the family go to the {tujuan}?", "every Sunday", ["every Monday", "every Saturday", "every day"], k[4]),
        (f"Where does {n}'s family live?", f"in {tinggal}", [f"in {x}" for x in kota if x != tinggal], k[0]),
    ])
    return hasil


def rd_bacaan(r):
    if not hasattr(r, "_bacaan_inggris"):
        r._bacaan_inggris = _bacaan_baru(r)
    bacaan, tanya, jawab, salah, kalimat = r.choice(r._bacaan_inggris)
    soal = teks_pilihan(r, tanya, jawab, salah, f'Jawabannya ada pada kalimat: "{kalimat}"')
    soal["bacaan"] = bacaan
    return soal


# ------------------------------------------------------------------- perakit

PEMBANGKIT = {
    "en-vocabulary": [v_arti_inggris, v_arti_indonesia, v_kelompok, v_berbeda, v_lawan],
    "en-numbers": [n_kata, n_angka, n_urutan, n_hari, n_bulan, n_jam, n_jam, n_fakta, n_hitung],
    "en-tobe": [tb_tobe, tb_tobe, tb_tanya, tb_kata_ganti, tb_milik, tb_penunjuk],
    "en-present": [sp_kata_kerja, sp_kata_kerja, sp_negatif, sp_tanya, sp_jawab_singkat, sp_frekuensi],
    "en-continuous": [pc_tobe, pc_ing, pc_ejaan, pc_tanya, pc_negatif],
    "en-there": [ta_tobe, ta_jawab, ta_letak_gambar, ta_letak_kalimat, ta_ruang],
    "en-nouns": [na_jamak, na_jumlah, na_artikel, na_artikel, na_tunggal_jamak],
    "en-questions": [qw_kata_tanya, qw_kata_tanya, qw_have, qw_can, qw_percakapan],
    "en-places": [pj_pekerjaan, pj_tempat_kerja, pj_tempat, pj_kendaraan, pj_arti],
    "en-reading": [rd_bacaan],
}

KODE_TOPIK = [t["kode"] for t in TOPIK]


def buat_latihan(topik, jumlah=JUMLAH_SOAL, rng=None):
    """Buat ``jumlah`` soal Bahasa Inggris berbeda untuk satu topik (atau 'en-campuran')."""
    if topik not in KODE_TOPIK:
        raise ValueError(f"topik tidak dikenal: {topik}")
    return rakit(PEMBANGKIT, topik, "en-campuran", jumlah, rng or random.Random())
