"""Pembangkit soal Bahasa Sunda SD kelas 1.

Materi mengikuti buku "Pamekar Diajar Basa Sunda Pikeun Murid SD/MI Kelas I"
(Dinas Pendidikan Provinsi Jawa Barat, 2014), Pangajaran 1 sampai 8. Bacaan,
kalimat, dan kosakata diambil dari buku itu; soal ditulis dalam bahasa Sunda,
pembahasan dalam bahasa Indonesia.

Bentuk soal sama dengan ``soal.py``: dict berisi "teks", "pilihan", "benar",
"pembahasan", ditambah "bacaan" bila soalnya memakai bacaan.
"""

import random

from soal import JUMLAH_SOAL, rakit, teks_pilihan

S1, S2, GAB = "Semester 1", "Semester 2", "Gabungan"

TOPIK = [
    {"kode": "su-pangajaran-1", "nama": "Pangajaran 1 · Ngurus Diri Sorangan", "ikon": "🧼", "kelompok": S1,
     "ket": "Ngariksa badan, mikawanoh aksara, ngéjah kecap"},
    {"kode": "su-pangajaran-2", "nama": "Pangajaran 2 · Pangaresep", "ikon": "🪁", "kelompok": S1,
     "ket": "Karesep, miara sato, kecap pagawéan (macul, dikonci)"},
    {"kode": "su-pangajaran-3", "nama": "Pangajaran 3 · Kagiatan", "ikon": "🏫", "kelompok": S1,
     "ket": "Indit ka sakola, olahraga, kecap anu méh sarua"},
    {"kode": "su-pangajaran-4", "nama": "Pangajaran 4 · Kulawarga", "ikon": "👨‍👩‍👧", "kelompok": S1,
     "ket": "Lanceuk-adi, sesebutan kulawarga, paguneman"},
    {"kode": "su-pangajaran-5", "nama": "Pangajaran 5 · Pangalaman", "ikon": "🏞️", "kelompok": S2,
     "ket": "Bacaan nyaba ka lembur, kecap pananya, istilah tempat"},
    {"kode": "su-pangajaran-6", "nama": "Pangajaran 6 · Lingkungan Sabudeureun", "ikon": "🌧️", "kelompok": S2,
     "ket": "Usum hujan, miara lingkungan, kerja bakti, pakakas"},
    {"kode": "su-pangajaran-7", "nama": "Pangajaran 7 · Miara Barang, Sasatoan jeung Tatangkalan",
     "ikon": "🐯", "kelompok": S2, "ket": "Apik kana barang, ngaran sasatoan, kandang, tatangkalan"},
    {"kode": "su-pangajaran-8", "nama": "Pangajaran 8 · Kajadian Alam", "ikon": "🌈", "kelompok": S2,
     "ket": "Katumbiri, usum, hujan, lini, samagaha"},
    {"kode": "su-semester-1", "nama": "Gabungan Semester 1", "ikon": "⭐", "kelompok": GAB,
     "ket": "Campuran Pangajaran 1–4"},
    {"kode": "su-semester-2", "nama": "Gabungan Semester 2", "ikon": "🌟", "kelompok": GAB,
     "ket": "Campuran Pangajaran 5–8"},
]


# ---------------------------------------------------------------- alat bantu

def _butir(r, daftar, bacaan=None):
    """Buat soal dari satu butir (teks, jawaban, pengecoh, catatan)."""
    teks, jawab, salah, catatan = r.choice(daftar)
    bahas = f'Jawabannya "{jawab}".' + (f" {catatan}" if catatan else "")
    soal = teks_pilihan(r, teks, jawab, r.sample(salah, 3), bahas)
    if bacaan:
        soal["bacaan"] = bacaan
    return soal


def _dari_bacaan(kumpulan):
    """Pembangkit: pilih satu paragraf bacaan lalu satu pertanyaannya."""
    def buat(r):
        bacaan, butir = r.choice(kumpulan)
        return _butir(r, [b if len(b) == 4 else (*b, "Jawabannya ada di dalam bacaan.") for b in butir], bacaan)
    return buat


def _dari_butir(daftar):
    return lambda r: _butir(r, daftar)


def _arti(kamus):
    """Pembangkit soal arti kata Sunda -> Indonesia dan sebaliknya."""
    def buat(r):
        su, idn = r.choice(list(kamus.items()))
        if r.random() < 0.5:
            return teks_pilihan(r, f'Naon hartina kecap "{su}" dina basa Indonésia?', idn,
                                r.sample(sorted({v for v in kamus.values() if v != idn}), 3),
                                f'"{su}" artinya "{idn}".')
        return teks_pilihan(r, f'Naon basa Sundana "{idn}"?', su, r.sample([k for k in kamus if k != su], 3),
                            f'"{idn}" dalam bahasa Sunda adalah "{su}".')
    return buat


def _susun(daftar):
    """Pembangkit soal menyusun kata menjadi kalimat; ``daftar`` berisi (kata acak, kalimat benar)."""
    def buat(r):
        acak, benar = r.choice(daftar)
        kata = benar.split()
        tengah = len(kata) // 2
        calon = [kata[::-1], kata[tengah:] + kata[:tengah], kata[1::2] + kata[::2][::-1]]
        tulis = lambda k: " ".join(k)[0].upper() + " ".join(k)[1:] + "."
        salah = [tulis(k) for k in calon if k != kata]
        return teks_pilihan(r, f"Susun jadi kalimah anu bener: {acak}", tulis(kata), salah,
                            f"Susunan yang benar: {tulis(kata)}")
    return buat


def _geser(ejaan):
    """Pemenggalan suku kata yang keliru: satu batas digeser satu atau dua huruf."""
    kata = ejaan.replace("-", "")
    batas, pos = [], 0
    for bagian in ejaan.split("-")[:-1]:
        pos += len(bagian)
        batas.append(pos)
    hasil = []
    for d in (-1, 1, 2, -2):
        for i in range(len(batas)):
            baru = batas[:i] + [batas[i] + d] + batas[i + 1:]
            if all(0 < b < len(kata) for b in baru) and baru == sorted(set(baru)):
                potong = "-".join(kata[a:b] for a, b in zip([0] + baru, baru + [len(kata)]))
                if potong != ejaan and potong not in hasil:
                    hasil.append(potong)
    for tambahan in range(1, len(kata)):          # kata pendek: tambah satu batas yang keliru
        if len(hasil) >= 3:
            break
        if tambahan not in batas:
            baru = sorted(batas + [tambahan])
            potong = "-".join(kata[a:b] for a, b in zip([0] + baru, baru + [len(kata)]))
            if potong not in hasil:
                hasil.append(potong)
    if len(hasil) < 3:
        hasil.append(kata)
    return hasil


_BILANGAN = ["", "hiji", "dua", "tilu", "opat", "lima"]


def _engang(daftar):
    """Pembangkit soal mengeja (memenggal suku kata) dan menghitung suku kata."""
    def buat(r):
        ejaan = r.choice(daftar)
        kata, banyak = ejaan.replace("-", ""), ejaan.count("-") + 1
        if r.random() < 0.6:
            return teks_pilihan(r, f'Kecap "{kata}" diéjahna …', ejaan, _geser(ejaan)[:3],
                                f'"{kata}" dieja per suku kata: {ejaan}.')
        return teks_pilihan(r, f'Kecap "{kata}" diwangun ku sabaraha engang?', _BILANGAN[banyak],
                            [b for b in _BILANGAN[1:] if b != _BILANGAN[banyak]],
                            f'{ejaan}: ada {banyak} suku kata ("engang"), dalam bahasa Sunda "{_BILANGAN[banyak]}".')
    return buat


# ======================================================= alat bantu semester 1

def _aksara(daftar):
    """Pembangkit soal mengenal huruf awal dan akhir kata (untuk pembaca pemula)."""
    def buat(r):
        kata = r.choice(daftar)
        bentuk = r.randrange(3)
        if bentuk == 2:
            awal = kata[0]
            lain = r.sample([k for k in daftar if k[0] != awal], 3)
            return teks_pilihan(r, f'Kecap mana anu dimimitian ku aksara "{awal}"?', kata, lain,
                                f'"{kata}" diawali huruf "{awal}".')
        huruf = kata[0] if bentuk == 0 else kata[-1]
        calon = [h for h in dict.fromkeys(kata + "abdkmnpstu") if h != huruf]
        tanya = "dimimitian" if bentuk == 0 else "ditungtungan"
        arti = "diawali" if bentuk == 0 else "diakhiri"
        return teks_pilihan(r, f'Kecap "{kata}" {tanya} ku aksara …', huruf, calon[:3],
                            f'"{kata}" {arti} huruf "{huruf}".')
    return buat


def _nasal(daftar, awalan):
    """Pembangkit soal kata kerja berawalan nasal; ``daftar`` berisi (kata dasar, bentukan, kalimat)."""
    def buat(r):
        dasar, jadi, kalimat = r.choice(daftar)
        salah = [dasar] + [a + dasar[1:] for a in awalan if a + dasar[1:] != jadi][:2]
        return teks_pilihan(r, kalimat, jadi, salah,
                            f'Kata dasar "{dasar}" menjadi kata kerja "{jadi}": {kalimat.replace("___", jadi)}')
    return buat


# ================================================ Pangajaran 1 · ngurus diri sorangan

_BACAAN_1 = [
    ("Aa budak apik. Tara poho mandi. Sok maké sabun. Mandi isuk soré. Sasarap saban isuk. "
     "Lamun arék sakola, Aa pasti pamitan ka ibu katut ka apa.", [
        ("Budak nu kumaha ari Aa téh?", "budak apik", ["budak bangor", "budak kedul", "budak jorok"]),
        ("Iraha Aa mandina?", "isuk jeung soré", ["peuting wungkul", "saminggu sakali", "tara mandi"]),
        ("Aa mandi maké naon?", "sabun", ["lém", "gula", "kapur"]),
        ("Sok kumaha Aa méméh ka sakola?", "pamitan ka ibu jeung apa", ["terus lumpat", "saré deui", "ulin heula"]),
        ("Iraha Aa sasarap?", "saban isuk", ["saban peuting", "saminggu sakali", "tara sasarap"]),
     ]),
    ("Aa téh ngaran sabenerna mah Tisna. Disebut Aa sotéh ku adina. Ari adi Aa ngaranna Jayadi. "
     "Sok disebut Ii.", [
        ("Saha ngaran sabenerna Aa?", "Tisna", ["Jayadi", "Oki", "Komar"]),
        ("Saha ngaran adi Aa?", "Jayadi", ["Oki", "Komar", "Koswara"]),
        ("Jayadi sok disebut naon?", "Ii", ["Aa", "Uu", "Nyai"]),
        ("Saha anu nyebut Aa ka Tisna?", "adina", ["guruna", "akina", "sobatna"]),
     ]),
]

_NGARIKSA = [
    ("Huntu kudu …", "dikosok", ["diantep", "dicét", "dikonci"], "Gigi harus disikat (dikosok)."),
    ("Mandi sapoé … kali.", "dua", ["hiji", "lima", "sapuluh"], "Mandi sehari dua kali."),
    ("Kuku ulah sina …", "kalotor", ["beresih", "séhat", "rapih"], "Kuku jangan dibiarkan kotor."),
    ("Kadé, ulah sok dahar …", "lada", ["sangu", "buah", "sayur"], '"Lada" = pedas.'),
    ("Jandéla kamar kudu …", "dibuka", ["dipiceun", "didahar", "diseuseuh"], "Jendela kamar harus dibuka."),
    ("Dibaju kudu …", "rapih", ["kotor", "baseuh", "soéh"], "Berpakaian harus rapi."),
    ("Hirup kudu …", "apik", ["jorok", "kedul", "bangor"], '"Apik" = rapi dan bersih.'),
    ("Ulah loba …", "jajan", ["diajar", "maca", "mandi"], "Jangan banyak jajan."),
    ("Apik pasti …", "séhat", ["gering", "kotor", "lapar"], "Kalau rapi dan bersih pasti sehat."),
    ("Kadé poho …", "sasarap", ["jajan", "heureuy", "ribut"], "Jangan lupa sarapan."),
    ("Urang kudu ngariksa badan supaya hirup …", "séhat", ["gering", "jorok", "kedul"],
     "Menjaga badan agar hidup sehat."),
]

_EJAAN_1 = ["bi-ma", "mé-ja", "pa-lu", "da-si", "ku-pa", "na-ko", "ha-lu", "ro-ti", "sa-té",
            "to-pi", "a-bon", "a-rit", "i-mah", "a-sin", "o-pat", "u-bar", "ji-dar", "ka-pur", "kor-si",
            "lam-pu", "jal-ma", "man-di", "ka-la-pa", "lo-ma-ri", "sa-pa-tu", "sa-ko-la", "ja-pa-ti",
            "so-ra-bi", "jan-dé-la", "lan-té-ra", "ko-ro-pak", "ti-ku-kur", "ku-lam-bu", "ta-ra-jé"]
_KECAP_1 = ["méja", "palu", "dasi", "kupa", "nako", "halu", "roti", "saté", "topi", "bima", "jidar", "kapur",
            "korsi", "lampu", "sapatu", "kalapa", "lomari", "tikukur", "kulambu", "jandéla"]

_KAMUS_1 = {"huntu": "gigi", "dahar": "makan", "lada": "pedas", "imah": "rumah", "korsi": "kursi",
            "lomari": "lemari", "sakola": "sekolah", "jandéla": "jendela", "ubar": "obat", "opat": "empat",
            "jalma": "orang", "tarajé": "tangga", "isuk": "pagi", "kalapa": "kelapa", "apa": "ayah",
            "jidar": "penggaris"}


# ========================================================== Pangajaran 2 · pangaresep

_BACAAN_2 = [
    ("Tisna boga japati sajodo. Dikukut ti anakna kénéh. Asalna mah tacan bisa hiber. "
     "Anak japati disebut piyik.", [
        ("Tisna boga sato naon?", "japati sajodo", ["hayam sajodo", "domba hiji", "lauk emas"]),
        ("Anak japati disebut naon?", "piyik", ["ciak", "belo", "pedét"]),
        ("Japati dikukut ti iraha?", "ti anakna kénéh", ["ti geus kolot", "ti kamari", "ti peuting tadi"]),
     ]),
    ("Sato séjénna ogé dikukut. Kelenci paméré ti Komar. Sarua éta ogé aya sajodo. "
     "Ari warna buluna barodas.", [
        ("Kelenci Tisna téh paméré ti saha?", "ti Komar", ["ti Oki", "ti Jayadi", "ti Koswara"]),
        ("Kumaha warna bulu kelencina?", "bodas", ["hideung", "beureum", "belang"]),
        ("Sabaraha kelenci Tisna?", "sajodo", ["hiji", "lima", "sapuluh"]),
     ]),
    ("Karesep Tisna miara sato. Diurus mani tulatén pisan. Tara tepi ka elat maraban, "
     "sabab bisi matak jadi dosa.", [
        ("Naon karesep Tisna?", "miara sato", ["ngagambar", "langlayangan", "ngurus taman"]),
        ("Kumaha Tisna ngurus satona?", "tulatén pisan", ["kedul", "sangeunahna", "tara diurus"]),
        ("Naon sababna Tisna tara elat maraban?", "bisi matak jadi dosa", ["bisi hujan", "bisi kabeurangan", "bisi leungit"]),
     ]),
    ("Nastiti karesepna ngurus taman hareupeun imahna. Di taman loba tangkal kembang. Saban poé ku Nastiti "
     "sok dicebor. Ari Koswara mah karesepna langlayangan. Sok nyieun sorangan, tara meuli. "
     "Koswara sok ngapungkeun langlayangan di lapang.", [
        ("Naon karesep Nastiti?", "ngurus taman", ["langlayangan", "ngagambar", "miara japati"]),
        ("Naon karesep Koswara?", "langlayangan", ["ngurus taman", "ngagambar", "paparahuan"]),
        ("Di mana Koswara ngapungkeun langlayangan?", "di lapang", ["di balong", "di jero kelas", "di dapur"]),
        ("Kembang di taman saban poé sok …", "dicebor", ["diduruk", "dipiceun", "dijual"]),
        ("Langlayangan Koswara téh meunang …", "nyieun sorangan", ["meuli", "nginjeum", "manggih"]),
     ]),
    ("Soléh karesepna ulin paparahuan di sisi balong. Soléh ogé sok nyieun sorangan. Ari Yanti karesepna "
     "kana ngagambar. Gambar meunang Yanti sok ditémpélkeun dina majalah dinding di sakola.", [
        ("Naon karesep Soléh?", "ulin paparahuan", ["ngagambar", "langlayangan", "ngurus taman"]),
        ("Di mana Soléh ulin paparahuan?", "di sisi balong", ["di lapang", "di jero kelas", "di jalan"]),
        ("Naon karesep Yanti?", "ngagambar", ["ulin paparahuan", "langlayangan", "miara sato"]),
        ("Gambar Yanti ditémpélkeun di mana?", "dina majalah dinding di sakola",
         ["dina panto imah", "dina tangkal", "dina mobil"]),
     ]),
]

_GAWE_M = [("pacul", "macul", "Patani ___ di sawah."), ("poé", "moé", "Wanti ___ anduk."),
           ("paku", "maku", "Bapa keur ___ panto lomari."), ("poé", "moé", "Dadan ___ sapatu."),
           ("pacul", "macul", "Toha dititah ___.")]
_GAWE_N = [("témbok", "némbok", "Semén dipaké ___.")]

# (kalimat, jawaban, bentuk lain yang tidak boleh jadi pengecoh)
_DI = [("Ato ___ seragam.", "dibaju", ["ditopi"]), ("Kacambah sok ___.", "diloték", ["diliwet"]),
       ("Béas arék ___.", "diliwet", ["diloték"]), ("Panto garasi ___.", "dikonci", ["digambar"]),
       ("Ban kempés rék ___.", "dikompa", []), ("Laut ___ ku Yati.", "digambar", []),
       ("Maman ___ biru.", "ditopi", ["dibaju"])]


def p2_di(r):
    kalimat, jawab, hindari = r.choice(_DI)
    lain = [d[1] for d in _DI if d[1] != jawab and d[1] not in hindari]
    return teks_pilihan(r, kalimat, jawab, r.sample(lain, 3),
                        f'Kalimat yang tepat: {kalimat.replace("___", jawab)}')


_BARANG_2 = [
    ("Calik dina ___.", "témbok", ["paku", "palu", "pacul"], "Duduk di atas tembok."),
    ("Digawé di ___ roti.", "pabrik", ["témbok", "palu", "paku"], "Bekerja di pabrik roti."),
    ("Suku kacugak ___.", "paku", ["témbok", "pabrik", "liwet"], "Kaki tertusuk paku."),
    ("___ motor ragrag.", "Konci", ["Liwet", "Loték", "Témbok"], "Kunci motor jatuh."),
    ("___ asak sapanci.", "Liwet", ["Konci", "Paku", "Pacul"], "Nasi liwet matang sepanci."),
    ("Sudaryat dahar ___.", "loték", ["konci", "paku", "pacul"], "Loték adalah makanan (sejenis pecel)."),
    ("Isukan ___ Kemis.", "poé", ["paku", "baju", "konci"], '"Poé" = hari.'),
    ("Maké ___ lebaran.", "baju", ["paku", "pacul", "témbok"], "Memakai baju lebaran."),
]

_EJAAN_2 = ["e-mur", "pe-ti", "su-gu", "sa-wah", "ku-ya", "sen-dal", "lan-cah", "ku-éh", "ka-os",
            "am-bu", "én-tog", "un-cal", "pi-a-la", "ra-di-o", "ak-sa-ra", "ki-lo-an", "ka-ram-ba",
            "ta-rum-pah", "kom-pu-ter", "ke-len-ci", "ja-pa-ti"]
_KECAP_2 = ["peti", "sugu", "cau", "sawah", "kuya", "sendal", "lancah", "kaos", "piala", "radio", "karamba",
            "gula", "cuka", "wani", "layar", "pacul", "lawon"]

_KAMUS_2 = {"cau": "pisang", "kuya": "kura-kura", "lancah": "laba-laba", "kuéh": "kue", "ambu": "ibu",
            "uncal": "rusa", "pacul": "cangkul", "lawon": "kain", "karesep": "kegemaran", "kelenci": "kelinci",
            "japati": "merpati", "langlayangan": "layang-layang", "balong": "kolam", "kembang": "bunga",
            "hiber": "terbang", "bodas": "putih", "béas": "beras", "panto": "pintu", "anduk": "handuk"}


# ============================================================ Pangajaran 3 · kagiatan

_BACAAN_3 = [
    ("Saban isuk Oki disampeur ku Tisna. Terus indit ka sakola. Sok laleumpang lantaran deukeut. "
     "Teu kungsi sapuluh menit ogé nepi. Tara kabeurangan.", [
        ("Saha nu disampeur ku Tisna?", "Oki", ["Jayadi", "Komar", "Ratna"]),
        ("Naha inditna sok laleumpang?", "lantaran deukeut", ["lantaran jauh", "lantaran hujan", "lantaran peré"]),
        ("Sabaraha lila leumpang ka sakola téh?", "teu kungsi sapuluh menit", ["sajam", "dua jam", "sapoé"]),
        ("Iraha Tisna nyampeur Oki?", "saban isuk", ["saban peuting", "poé Ahad wungkul", "sabulan sakali"]),
     ]),
    ("Lamun keur giliran pikét, kudu sasapu meresihan heula kelas. Kabéh kagiliran saminggu séwang. "
     "Diajar kudu saregep, ulah bari heureuy. Di jero kelas teu meunang ribut jeung lulumpatan. "
     "Komo silih balédog mah bisi matak cilaka.", [
        ("Kudu kumaha lamun keur giliran pikét?", "sasapu meresihan kelas",
         ["ulin di lapang", "saré di kelas", "balik ka imah"]),
        ("Kumaha ngabagi giliran pikét téh?", "saminggu séwang", ["sataun séwang", "tara dibagi", "sapoé kabéh"]),
        ("Diajar kudu kumaha?", "saregep", ["bari heureuy", "bari ribut", "bari lulumpatan"]),
        ("Naha di kelas ulah silih balédog?", "bisi matak cilaka", ["bisi lapar", "bisi tunduh", "bisi hujan"]),
     ]),
    ("Poé Ahad di lapang balédésa aya senam. Saméméh tabuh tujuh ogé geus karumpul. Maraké baju jeung sapatu "
     "paranti olahraga. Barudak loba nu miluan. Olahraga téh penting pikeun kaséhatan. "
     "Urang matak jadi gumbira deuih.", [
        ("Di mana senam poé Ahad téh?", "di lapang balédésa", ["di jero kelas", "di sisi balong", "di pasar"]),
        ("Poé naon aya senam téh?", "poé Ahad", ["poé Senén", "poé Kemis", "poé Jumaah"]),
        ("Tabuh sabaraha nu rék senam karumpulna?", "saméméh tabuh tujuh",
         ["tabuh dua belas", "sanggeus asar", "tengah peuting"]),
        ("Nu miluan senam maraké naon?", "baju jeung sapatu olahraga",
         ["baju seragam sakola", "baju lebaran", "jas hujan"]),
        ("Olahraga téh penting pikeun naon?", "kaséhatan", ["kasakit", "runtah", "jajan"]),
        ("Olahraga matak urang jadi …", "gumbira", ["gering", "sedih", "ambek"]),
     ]),
    ("Yanti: Hayu ah urang miluan senam.\nSinta: Di mana ari tempat senamna?\n"
     "Yanti: Di buruan kantor kacamatan.\nSinta: Ari budak meunang miluan kitu?\n"
     "Yanti: Atuh puguh waé meunang mah.\nYanti: Tapi kudu bébéja heula ka Ema.", [
        ("Yanti ngajak Sinta naon?", "miluan senam", ["piknik", "maénbal", "ngagambar"]),
        ("Di mana tempat senamna?", "di buruan kantor kacamatan", ["di lapang balédésa", "di sakola", "di sisi balong"]),
        ("Kudu bébéja heula ka saha?", "ka Ema", ["ka sobat", "ka dokter", "ka Pa Udi"]),
        ("Naha budak meunang miluan senam?", "meunang", ["teu meunang", "kudu mayar", "ngan kolot wungkul"]),
     ]),
    ("Pandu: Ari poé Ahad kamari ka mana?\nIrman: Apan ku Uwa diajak ka Ciwidéy.\n"
     "Pandu: Leuh, jauh atuh ka Ciwidéy mah.\nIrman: Tapi matak resep. Loba pamandangan éndah, hawana seger.\n"
     "Pandu: Tangtu, sabab daérah pagunungan.\nIrman: Hanjakal teu kaburu ka Kawah Putih.", [
        ("Ka mana Irman poé Ahad kamari?", "ka Ciwidéy", ["ka Ciater", "ka Panyirapan", "ka Pangandaran"]),
        ("Ku saha Irman diajakna?", "ku Uwa", ["ku Bibi", "ku Aki", "ku Guru"]),
        ("Kumaha hawa di Ciwidéy?", "seger", ["panas", "bau", "bayeungyang"]),
        ("Naha hawa di Ciwidéy seger?", "sabab daérah pagunungan",
         ["sabab deukeut laut", "sabab loba mobil", "sabab di tengah kota"]),
        ("Tempat naon anu teu kaburu didatangan ku Irman?", "Kawah Putih", ["Ciater", "Pangandaran", "Lémbang"]),
     ]),
]

_MIRIP = [
    ("Jalma ___ bakal dipercaya.", "bener", ["beuneur", "bébér", "beubeur"], '"Bener" = benar/jujur.'),
    ("Ulah sok ___ sorangan atuh.", "seuri", ["séri", "leutak", "beubeur"], '"Seuri" = tertawa.'),
    ("Paré di sawah mimiti ___.", "beuneur", ["bener", "hideng", "séri"], '"Beuneur" = berisi/bernas.'),
    ("Kapal ___ layar di tengah laut.", "bébér", ["beubeur", "bener", "leutak"], '"Bébér" = membentangkan.'),
    ("Murid kudu ___ kana tugas.", "hideng", ["hideung", "eunteung", "leutak"],
     '"Hideng" = tahu sendiri tanpa disuruh.'),
    ("Maké ___ ngarah pageuh.", "beubeur", ["bébér", "bener", "séri"], '"Beubeur" = ikat pinggang.'),
    ("Irman maké kacapanon ___.", "hideung", ["hideng", "énténg", "seuri"], '"Hideung" = hitam.'),
    ("Pék ___ uyah téh, rasana asin.", "létak", ["leutak", "bébér", "beubeur"], '"Létak" = jilat.'),
    ("Pérsib lawan Pérsija hasilna ___.", "séri", ["seuri", "leutak", "eunteung"], '"Séri" = seri/imbang.'),
    ("Sapatu kotor ku ___ balong.", "leutak", ["létak", "bébér", "séri"], '"Leutak" = lumpur.'),
    ("Tamu piwarang ka ___.", "lebet", ["leubeut", "leutak", "beubeur"], '"Lebet" = dalam/masuk (bahasa halus).'),
    ("Balingbing mani ___.", "leubeut", ["lebet", "létak", "hideng"], '"Leubeut" = berbuah lebat.'),
    ("___ ditunda dina méja.", "Eunteung", ["Énténg", "Hideung", "Seuri"], '"Eunteung" = cermin.'),
    ("Ah, geuning ___ tugas téh.", "énténg", ["eunteung", "leutak", "beubeur"], '"Énténg" = ringan/mudah.'),
    ("Areng warnana tangtu ___.", "hideung", ["hideng", "bener", "séri"], "Arang berwarna hitam."),
]

_EJAAN_3 = ["eu-rih", "ca-reuh", "sam-peu", "si-reum", "beu-si", "ngo-ra", "ba-ngo", "a-ngin", "la-ngit",
            "eu-weuh", "leu-eur", "beu-reum", "seu-keut", "keu-yeup", "peun-teun", "su-ung", "reu-ngit",
            "ka-wung", "mun-ding", "bén-téng", "é-ngang", "bang-kong", "ka-lang-kang", "ba-ling-bing",
            "cang-ka-léng"]

_KAMUS_3 = {"sampeu": "singkong", "sireum": "semut", "beusi": "besi", "ngora": "muda", "beureum": "merah",
            "seukeut": "tajam", "keuyeup": "kepiting", "reungit": "nyamuk", "munding": "kerbau",
            "bangkong": "katak", "kalangkang": "bayangan", "suung": "jamur", "euweuh": "tidak ada",
            "leueur": "licin", "seueur": "banyak", "peunteun": "nilai", "hideung": "hitam",
            "eunteung": "cermin", "leutak": "lumpur", "seuri": "tertawa"}


# =========================================================== Pangajaran 4 · kulawarga

_BACAAN_4 = [
    ("Tisna téh budak panengah ti tilu sadulur. Boga lanceuk ngaranna Ratna, jeung boga adi ngaranna Jayadi. "
     "Éta tilu sadulur téh putrana Ibu Néngsih jeung Bapa Rusmana.", [
        ("Sabaraha urang Tisna sadulur?", "tilu", ["dua", "opat", "lima"]),
        ("Saha ngaran lanceuk Tisna?", "Ratna", ["Jayadi", "Manik", "Wulan"]),
        ("Saha ngaran adi Tisna?", "Jayadi", ["Ratna", "Ikbal", "Oki"]),
        ("Saha ngaran indung Tisna?", "Ibu Néngsih", ["Ibu Ati", "Bibi Éla", "Ibu Déwi"]),
        ("Saha ngaran bapa Tisna?", "Bapa Rusmana", ["Bapa Dayat", "Pa Udi", "Aki Suganda"]),
        ("Tisna téh budak …", "panengah", ["cikal", "bungsu", "tunggal"]),
     ]),
    ("Ratna téh disebutna anak cikal, nyaéta budak panggedéna. Jayadi disebutna anak bungsu, nyaéta budak "
     "pangleutikna. Ratna sakolana geus kelas genep. Ari Jayadi mah tacan sakola. Karesep Ratna kana nyanyi.", [
        ("Anak cikal nyaéta budak …", "panggedéna", ["pangleutikna", "panengah", "pangpinterna"]),
        ("Anak bungsu nyaéta budak …", "pangleutikna", ["panggedéna", "panengah", "pangjangkungna"]),
        ("Ratna sakolana kelas sabaraha?", "kelas genep", ["kelas hiji", "kelas tilu", "tacan sakola"]),
        ("Saha anu tacan sakola?", "Jayadi", ["Ratna", "Tisna", "Oki"]),
        ("Naon karesep Ratna?", "nyanyi", ["ngagambar", "langlayangan", "maénbal"]),
        ("Saha anu disebut anak cikal?", "Ratna", ["Tisna", "Jayadi", "Komar"]),
     ]),
    ("Bapa Dayat jeung Ibu Ati boga budak tilu. Anu cikal ngaranna Manik. Anu panengah ngaranna Ikbal. "
     "Ari anu bungsu ngaranna Wulan. Ikbal jeung Wulan ka Manik nyebutna Ceuceu atawa Tétéh. "
     "Ari Wulan ka Ikbal nyebutna Aa atawa Akang.", [
        ("Saha anak cikal Bapa Dayat?", "Manik", ["Ikbal", "Wulan", "Tisna"]),
        ("Saha anu panengah?", "Ikbal", ["Manik", "Wulan", "Ratna"]),
        ("Saha anu bungsu?", "Wulan", ["Manik", "Ikbal", "Jayadi"]),
        ("Wulan ka Manik nyebutna naon?", "Ceuceu atawa Tétéh", ["Aa atawa Akang", "Emang", "Bibi"]),
        ("Wulan ka Ikbal nyebutna naon?", "Aa atawa Akang", ["Ceuceu atawa Tétéh", "Uwa", "Nini"]),
        ("Sabaraha budak Bapa Dayat jeung Ibu Ati?", "tilu", ["hiji", "dua", "opat"]),
     ]),
    ("Tisna: Ceuceu, abdi badé nambut jidar.\nRatna: Candak waé, itu dina luhur méja tulis.\n"
     "Tisna: Sakantenan deuih sareng patlot gambarna.\nRatna: Patlot gambar mah disimpen dina laci.\n"
     "Tisna: Hatur nuhun.", [
        ("Tisna badé nambut naon ka Ratna?", "jidar jeung patlot gambar", ["buku jeung kantong", "sapatu", "bal"]),
        ("Di mana jidarna?", "dina luhur méja tulis", ["dina laci", "dina lomari", "di buruan"]),
        ("Di mana patlot gambar disimpenna?", "dina laci", ["dina luhur méja tulis", "dina kantong", "di dapur"]),
        ("Naon anu diucapkeun ku Tisna sanggeus dibéré nambut?", "hatur nuhun", ["punten", "mangga", "embung"]),
     ]),
    ("Bibi Éla: Énjing urang piknik ka Ciater, yu.\nNugraha: Abdi mah di ditu téh hoyong ngojay.\n"
     "Pertiwi: Tapi ngojayna ulah di balong nu jero.\nNugraha: Badé ngojay di balong nu déét waé.\n"
     "Pertiwi: Abdi mah badé tumpak kuda.", [
        ("Ka mana piknikna?", "ka Ciater", ["ka Ciwidéy", "ka Pangandaran", "ka Panyirapan"]),
        ("Saha anu ngajak piknik?", "Bibi Éla", ["Ibu Ati", "Pa Udi", "Aki Suganda"]),
        ("Nugraha hoyong naon di Ciater?", "ngojay", ["tumpak kuda", "ngagambar", "langlayangan"]),
        ("Pertiwi badé naon di Ciater?", "tumpak kuda", ["ngojay", "saré", "balanja"]),
        ("Nugraha badé ngojay di balong nu kumaha?", "nu déét", ["nu jero", "nu kotor", "nu saat"]),
     ]),
    ("Aisah: Abdi badé ngabantun pesenan Ibu.\nPa Udi: Oh muhun, kamari Ibu pesen lauk emas.\n"
     "Aisah: Sakantenan mésér bawang daun deuih.\nPa Udi: Rupina Ibu téh badé mais lauk.", [
        ("Ibu pesen naon ka Pa Udi?", "lauk emas", ["hayam", "endog", "daging"]),
        ("Aisah mésér naon deui?", "bawang daun", ["cabé", "tomat", "uyah"]),
        ("Ibu badé masak naon?", "pais lauk", ["angeun lodéh", "loték", "saté"]),
     ]),
]

_KULAWARGA = [
    ("Kolotna indung atawa bapa urang disebutna …", "nini jeung aki", ["emang jeung bibi", "lanceuk jeung adi", "uwa"],
     "Nini dan aki = nenek dan kakek."),
    ("Adina indung atawa bapa urang anu lalaki disebutna …", "emang", ["bibi", "uwa", "aki"], '"Emang" = paman.'),
    ("Adina indung atawa bapa urang anu awéwé disebutna …", "bibi", ["emang", "uwa", "nini"], '"Bibi" = bibi/tante.'),
    ("Lanceukna indung atawa bapa urang disebutna …", "uwa", ["emang", "bibi", "adi"],
     '"Uwa" = kakak dari ayah atau ibu.'),
    ("Ka indung, urang nyebut …", "ema atawa ibu", ["apa atawa bapa", "aki", "emang"], "Panggilan untuk ibu."),
    ("Ka bapa, urang nyebut …", "apa atawa bapa", ["ema atawa ibu", "nini", "bibi"], "Panggilan untuk ayah."),
    ("Ka lanceuk awéwé, urang nyebut …", "ceuceu atawa tétéh", ["aa atawa akang", "bibi", "nini"],
     "Panggilan untuk kakak perempuan."),
    ("Ka lanceuk lalaki, urang nyebut …", "aa atawa akang", ["ceuceu atawa tétéh", "emang", "aki"],
     "Panggilan untuk kakak laki-laki."),
    ("Henteu sopan mun ka lanceuk nyebut …", "ngaranna wungkul", ["tétéh", "akang", "ceuceu"],
     "Tidak sopan memanggil kakak hanya dengan namanya."),
    ("Ari jeung dulur teu meunang …", "paséa", ["akur", "silih bantuan", "ulin bareng"], '"Paséa" = bertengkar.'),
    ("Mun urang dibantuan, kudu nyebut …", "nuhun", ["mangga", "embung", "héhé"], '"Nuhun" = terima kasih.'),
    ("Urang ulah ulin anu matak jadi …", "cilaka", ["séhat", "pinter", "gumbira"], '"Cilaka" = celaka.'),
    ("Lanceuk kudu bisa méré conto ka …", "adi", ["aki", "guru", "nini"], "Kakak memberi contoh kepada adik."),
    ("Mun lanceuk keur digawé, kudu …", "dibantuan", ["diganggu", "ditinggalkeun", "diheureuyan"],
     "Kalau kakak sedang bekerja, harus dibantu."),
    ("Kanyaah indung bapa urang taya …", "watesna", ["gunana", "hartina", "ngaranna"],
     "Kasih sayang orang tua tidak ada batasnya."),
    ("Lanceuk kudu … ka adi.", "ngéléhan", ["ngaheureuyan", "nyarékan", "ngalawan"], '"Ngéléhan" = mengalah.'),
    ("Naséhat saha anu wajib diturut?", "indung bapa", ["babaturan", "adi", "budak leutik"],
     "Nasihat orang tua wajib dituruti."),
]

_NY = [
    ("Murid ___ ngaranna Wéni.", "anyar", ["nyiru", "nyéré", "rinyuh"], '"Anyar" = baru.'),
    ("Ranginang dipoé dina ___.", "nyiru", ["penyu", "konyal", "sinyal"], '"Nyiru" = tampah.'),
    ("Liang sireum dicolok ku ___.", "nyéré", ["nyiru", "penyu", "konyal"], '"Nyéré" = lidi.'),
    ("Dina tangkal aya sayang ___.", "manyar", ["penyu", "nyiru", "sinyal"], "Manyar adalah nama burung."),
    ("Buah ___ rasana amis haseum.", "konyal", ["manyar", "nyiru", "rinyuh"], "Konyal adalah nama buah (markisa)."),
    ("Anu sok ngaruksak kai téh ___.", "rinyuh", ["penyu", "manyar", "konyal"], '"Rinyuh" = rayap.'),
    ("Bapa Juhana ngala madu ___.", "nyiruan", ["penyu", "rinyuh", "manyar"], '"Nyiruan" = lebah.'),
    ("Kudu ___ ka jalma sangsara.", "karunya", ["banyol", "nyanyi", "ambek"], '"Karunya" = kasihan.'),
    ("Di basisir aya ___ keur ngendog.", "penyu", ["rinyuh", "nyiruan", "manyar"], "Penyu bertelur di pantai."),
    ("Tong ambek, da ieu mah ___.", "banyol", ["karunya", "nyanyi", "anyar"], '"Banyol" = bercanda.'),
    ("Hérman ___ hareupeun sobatna.", "nyanyi", ["karunya", "anyar", "rinyuh"], "Herman bernyanyi di depan temannya."),
]

_GAWE_NY = [("sangu", "nyangu", "Ema ___ di dapur."), ("sépak", "nyépak", "Ido ___ bal ka tengah lapang."),
            ("sugu", "nyugu", "Ahmad keur ___ papan jati."), ("conto", "nyonto", "Entong ___ jalma teu bener."),
            ("susun", "nyusun", "Tugas ___ kalimah teu hésé."), ("seupan", "nyeupan", "Wati ___ taleus keur susuguh."),
            ("surung", "nyurung", "Jayadi keur ___ momobilan."), ("carék", "nyarék", "Dokter ___ dahar lada ka pasén."),
            ("sobat", "nyobat", "Milati jeung Kartini mani ___.")]

_EJAAN_4 = ["nya-nyi", "nya-i", "nyep-lés", "nyen-tak", "du-nya", "nyi-ru", "pe-nyu", "ri-nyuh", "ko-nyal",
            "ma-nyar", "si-nyal", "nyi-ru-an", "a-nyar", "ba-nyol", "ka-ru-nya", "lan-ceuk", "bung-su",
            "ci-kal", "ku-la-war-ga"]

_KAMUS_4 = {"lanceuk": "kakak", "adi": "adik", "cikal": "anak sulung", "panengah": "anak tengah",
            "indung": "ibu", "nini": "nenek", "aki": "kakek", "emang": "paman", "dulur": "saudara",
            "kulawarga": "keluarga", "nyiruan": "lebah", "rinyuh": "rayap", "nyiru": "tampah",
            "paséa": "bertengkar", "nuhun": "terima kasih", "karunya": "kasihan", "anyar": "baru",
            "sangu": "nasi", "ngojay": "berenang", "kolot": "orang tua"}


# =========================================================== Pangajaran 5 · pangalaman

_BACAAN_5 = [
    ("Tisna ku uwana diajakan nyaba ka Panyirapan. Lembur di suku gunung anu anggang ti kota. "
     "Di dinya téh aya nini jeung akina Tisna. Nini Rahmi jeung Aki Suganda téh urang Panyirapan.", [
        ("Ka mana Tisna diajakan nyaba?", "ka Panyirapan", ["ka kebon binatang", "ka basisir", "ka pasar"]),
        ("Saha anu ngajak Tisna nyaba?", "uwana", ["bapana", "lanceukna", "guruna"]),
        ("Saha ngaran akina Tisna?", "Aki Suganda", ["Aki Karyana", "Aki Solihin", "Aki Lukman"]),
        ("Saha ngaran nini Tisna?", "Nini Rahmi", ["Nini Kartini", "Nini Sumarni", "Nini Déwi"]),
        ("Di mana ayana lembur Panyirapan?", "di suku gunung", ["di sisi laut", "di tengah kota", "di sisi talaga"]),
     ]),
    ("Aki Suganda ngebon palawija. Kayaning jagong, waluh, jeung paria. Paré ogé sarua deuih melak, "
     "disebutna ngahuma. Melak paréna lain di sawah, tapi di kebon darat.", [
        ("Naon anu dipigawé ku Aki Suganda?", "ngebon palawija",
         ["dagang di pasar", "ngala lauk di laut", "ngoméan radio"]),
        ("Palawija naon anu dipelak ku Aki Suganda?", "jagong, waluh, jeung paria",
         ["alpuket, nangka, jeung limus", "jati, mahoni, jeung surén", "bawang, cabé, jeung tomat"]),
        ("Melak paré di kebon darat disebutna …", "ngahuma", ["ngebon", "nyawah", "ngarit"]),
        ("Di mana Aki Suganda melak paréna?", "di kebon darat", ["di sawah", "di balong", "di buruan"]),
     ]),
    ("Di kebon Aki Suganda loba tangkal galedé jeung jarangkung. Anu diarah buahna nyaéta alpuket, nangka, "
     "peuteuy, jeung limus. Ari anu diarah kaina nyaéta jati, mahoni, jeung surén.", [
        ("Tangkal anu diarah buahna nyaéta …", "nangka", ["jati", "mahoni", "surén"]),
        ("Tangkal anu diarah kaina nyaéta …", "jati", ["alpuket", "nangka", "limus"]),
        ("Kumaha tangkal di kebon Aki Suganda?", "galedé jeung jarangkung",
         ["laleutik kabéh", "garing jeung layu", "saeutik pisan"]),
     ]),
    ("Tatangkalan téh nyuburkeun lahan jeung jadi sumber cai. Hawa ogé jadi beresih jeung seger. "
     "Béda jeung lahan anu euweuh tatangkalan. Hawana panas, taneuhna gampang urug. "
     "Lamun usum hujan sok ngadatangkeun caah.", [
        ("Naon gunana tatangkalan?", "nyuburkeun lahan jeung jadi sumber cai",
         ["ngadatangkeun caah", "nyieun hawa jadi panas", "ngaruksak taneuh"]),
        ("Kumaha hawa di tempat anu loba tatangkalan?", "beresih jeung seger", ["panas", "bau", "kotor"]),
        ("Kumaha taneuh di lahan anu euweuh tatangkalan?", "gampang urug", ["subur", "loba caina", "seger"]),
        ("Lahan anu euweuh tatangkalan, dina usum hujan sok ngadatangkeun …", "caah", ["buah", "kai", "palawija"]),
     ]),
    ("Tisna betah pisan cicing di Panyirapan. Saban poé sok milu ka kebon. Tisna di lembur akina ukur "
     "opat poé. Tisna kudu mulang deui ka kota sabab kudu asup deui sakola.", [
        ("Sabaraha poé Tisna di lembur akina?", "opat poé", ["dua poé", "tujuh poé", "sapoé"]),
        ("Naon sababna Tisna kudu mulang deui ka kota?", "kudu asup deui sakola",
         ["teu betah di lembur", "keur gering", "dicarékan ku akina"]),
        ("Saban poé Tisna sok milu ka mana?", "ka kebon", ["ka pasar", "ka laut", "ka sakola"]),
        ("Kumaha rarasaan Tisna di Panyirapan?", "betah pisan", ["sieun", "bosen", "ambek"]),
     ]),
    ("Wéndi diajakan piknik ka kebon binatang ku lanceukna. Di kebon binatang téh aya maung, gajah, banténg, "
     "biruang, jeung uncal. Ari Yunita mah diajakan ka basisir. Yunita tumpak parahu. Saméméh balik, "
     "Yunita meuli barang karajinan tina kerang keur oléh-oléh.", [
        ("Ka mana Wéndi piknikna?", "ka kebon binatang", ["ka basisir", "ka Panyirapan", "ka gunung"]),
        ("Jeung saha Wéndi ka kebon binatang?", "jeung lanceukna", ["jeung akina", "jeung guruna", "sorangan"]),
        ("Ka mana Yunita diajakan?", "ka basisir", ["ka kebon binatang", "ka sawah", "ka pasar"]),
        ("Yunita tumpak naon di basisir?", "parahu", ["sapéda", "kuda", "mobil"]),
        ("Naon oléh-oléh anu dibeuli ku Yunita?", "barang karajinan tina kerang",
         ["gula beureum", "jagong jeung waluh", "baju anyar"]),
     ]),
]

_PANANYA = [
    ("___ anu kamari nyébor taman?", "Saha", ["Iraha", "Kumaha", "Sabaraha"], '"Saha" menanyakan orang (siapa).'),
    ("___ anu rék miluan kémping?", "Saha", ["Iraha", "Di mana", "Sabaraha"], '"Saha" menanyakan orang (siapa).'),
    ("___ gunana miara lingkungan?", "Naon", ["Saha", "Iraha", "Sabaraha"], '"Naon" menanyakan benda atau hal (apa).'),
    ("___ mimiti datang usum hujan?", "Iraha", ["Saha", "Naon", "Sabaraha"], '"Iraha" menanyakan waktu (kapan).'),
    ("___ mimitina puasa Romadon téh?", "Iraha", ["Saha", "Sabaraha", "Kumaha"], '"Iraha" menanyakan waktu (kapan).'),
    ("___ leuweung entong diruksak?", "Naha", ["Saha", "Sabaraha", "Di mana"], '"Naha" menanyakan sebab (mengapa).'),
    ("___ carana ari melak kalapa?", "Kumaha", ["Saha", "Sabaraha", "Iraha"], '"Kumaha" menanyakan cara (bagaimana).'),
    ("___ urang anu milu wisata?", "Sabaraha", ["Naon", "Kumaha", "Naha"], '"Sabaraha" menanyakan jumlah (berapa).'),
    ("___ ari tempat upacara bandéra?", "Di mana", ["Saha", "Sabaraha", "Naha"], '"Di mana" menanyakan tempat.'),
    ('Kecap pananya "saha" dipaké pikeun nanyakeun …', "jalma", ["waktu", "tempat", "jumlah"],
     '"Saha" = siapa, untuk menanyakan orang ("jalma").'),
    ('Kecap pananya "iraha" dipaké pikeun nanyakeun …', "waktu", ["jalma", "tempat", "jumlah"],
     '"Iraha" = kapan, untuk menanyakan waktu.'),
    ('Kecap pananya "di mana" dipaké pikeun nanyakeun …', "tempat", ["jalma", "waktu", "jumlah"],
     '"Di mana" untuk menanyakan tempat.'),
    ('Kecap pananya "sabaraha" dipaké pikeun nanyakeun …', "jumlah", ["jalma", "waktu", "tempat"],
     '"Sabaraha" = berapa, untuk menanyakan jumlah.'),
]

# (kalimat, pelaku) dan (kalimat, benda) dari buku
_PALAKU = [("rék ngagoréng ulén", "Yulia"), ("diajar tumpak sapéda", "Galih"), ("keur ngarang dongéng", "Wahyu"),
           ("bisaeun ngoméan radio", "Solihin"), ("pinter ngawihkeun lagu", "Kartini"),
           ("nyépak bal tarik pisan", "Gumilang"), ("ngaraut awi keur karajinan", "Yusup"),
           ("ngadorong mobil lebah tanjakan", "Ujé")]
_BARANG_DIPIGAWE = [("anduk", "keur diseuseuh ku Nita"), ("suluh", "rék dibeulahan ku Ahmad"),
                    ("papan", "rék dihampelas ku Karyana"), ("balong", "keur dibedahkeun ku Pa Haji"),
                    ("kompor", "rék dihurungkeun ku Ibu Déwi"), ("hayam katé", "keur diparaban ku Mang Didi"),
                    ("angeun lodéh", "keur dihaneutkeun ku Sartika"),
                    ("panto gerbang", "geus dikonci ku Bapa Satpam")]


def p5_saha_naon(r):
    bentuk = r.randrange(4)
    if bentuk < 2:
        kegiatan, nama = r.choice(_PALAKU)
        if bentuk == 0:
            return teks_pilihan(r, f"{nama} {kegiatan}. ___ anu {kegiatan} téh?", "Saha",
                                ["Naon", "Iraha", "Di mana"],
                                f'Yang ditanyakan orangnya ({nama}), jadi memakai "Saha" (siapa).')
        return teks_pilihan(r, f"{nama} {kegiatan}. Saha anu {kegiatan} téh?", nama,
                            r.sample([n for _, n in _PALAKU if n != nama], 3),
                            f'Dalam kalimatnya: "{nama} {kegiatan}."')
    benda, kegiatan = r.choice(_BARANG_DIPIGAWE)
    kalimat = f"{benda.capitalize()} {kegiatan}."
    if bentuk == 2:
        return teks_pilihan(r, f"{kalimat} ___ anu {kegiatan} téh?", "Naon", ["Saha", "Iraha", "Di mana"],
                            f'Yang ditanyakan bendanya ({benda}), jadi memakai "Naon" (apa).')
    return teks_pilihan(r, f"{kalimat} Naon anu {kegiatan} téh?", benda,
                        r.sample([b for b, _ in _BARANG_DIPIGAWE if b != benda], 3),
                        f'Dalam kalimatnya: "{kalimat}"')


_SUSUN_5 = [
    ("sapéda – Mardani – boga – mini", "Mardani boga sapéda mini"),
    ("juara – jadi – penca – Ibrahim", "Ibrahim jadi juara penca"),
    ("ngaji – keur – Nurjanah – diajar", "Nurjanah keur diajar ngaji"),
    ("balik – Déwi – olahraga – kakara", "Déwi kakara balik olahraga"),
    ("rék – Kostaman – maénbal – latihan", "Kostaman rék latihan maénbal"),
    ("sedepmalem – melak – tangkal – Ria", "Ria melak tangkal sedepmalem"),
    ("bénsin – Iskandar – dititah – dagang", "Iskandar dititah dagang bénsin"),
    ("kuda – balap – resep – Héryanti – lalajo", "Héryanti resep lalajo balap kuda"),
    ("getol – sunat – puasa – Jamaludin – pisan", "Jamaludin getol pisan puasa sunat"),
]

_TEMPAT = [
    ("Paré di ___ téréh dipanén.", "sawah", ["jurang", "laut", "jalan"], "Padi ditanam di sawah."),
    ("Sakitu halodo gé ___ teu saat.", "sumur", ["gunung", "jalan", "lapang"],
     "Walau kemarau, sumur tidak kering (saat = kering)."),
    ("Cai di ___ palidna ka hilir.", "walungan", ["lapang", "gunung", "jalan"],
     '"Walungan" = sungai; airnya mengalir ke hilir.'),
    ("Hawa di luhur ___ tiris pisan.", "gunung", ["sumur", "walungan", "jalan"],
     "Udara di atas gunung dingin sekali (tiris = dingin)."),
    ("Di ___ Ciburuy loba wisatawan.", "talaga", ["jurang", "jalan", "sumur"], '"Talaga" = danau.'),
    ("Barudak latihan maénbal di ___.", "lapang", ["sumur", "jurang", "laut"], '"Lapang" = lapangan.'),
    ("Kamari aya mobil tigebrus ka ___.", "jurang", ["lapang", "gunung", "kampung"],
     '"Tigebrus" = terperosok; mobil terperosok ke jurang.'),
    ("Kendaraan di ___ raya mani tararik.", "jalan", ["sawah", "sumur", "talaga"], '"Jalan raya" = jalan besar.'),
    ("Pamayang ngala lauk di tengah ___.", "laut", ["sawah", "lapang", "jurang"],
     '"Pamayang" = nelayan; menangkap ikan di laut.'),
    ("Teu kudu éra najan imah di ___.", "kampung", ["sumur", "walungan", "laut"],
     "Tidak perlu malu walau rumah di kampung."),
    ("Di ___ ramé, loba ku kendaraan.", "kota", ["sawah", "jurang", "sumur"], "Kota ramai, banyak kendaraan."),
    ("Murid kumpul di ___ upacara.", "lapang", ["sumur", "walungan", "jurang"], '"Lapang upacara" = lapangan upacara.'),
    ("Leumpang dina sisi ___ matak paur.", "jurang", ["lapang", "taman", "kampung"],
     "Berjalan di tepi jurang menakutkan (paur = ngeri)."),
]

_MAGATRU = [
    ("Sato galak anu belang coréléng nyaéta …", "maung", ["lutung", "bajing", "domba"], '"Maung" = harimau.'),
    ("Maung kabeukina dahar …", "daging", ["jukut", "bungbuahan", "daun"], "Harimau suka makan daging."),
    ("Maung cicingna di …", "leuweung ganggong", ["sawah", "balong", "pagupon"],
     '"Leuweung ganggong" = hutan lebat.'),
    ("Sato hideung anu resep cicing dina tangkal katelahna …", "lutung", ["maung", "bajing", "munding"],
     "Lutung berbulu hitam dan suka tinggal di pohon."),
    ("Sato leutik tapi lucu anu beuki kana bungbuahan nyaéta …", "bajing", ["maung", "lutung", "banténg"],
     '"Bajing" = tupai; suka buah-buahan.'),
    ("Bajing beuki pisan kana kalapa …", "ngora", ["garing", "kolot", "buruk"], "Tupai suka kelapa muda (ngora = muda)."),
    ("Tembang anu nyaritakeun maung, lutung, jeung bajing téh pupuh …", "magatru", ["kinanti", "pucung", "maskumambang"],
     "Di buku, tembang tentang hewan itu memakai pupuh magatru."),
]

_KAMUS_5 = {"walungan": "sungai", "talaga": "danau", "lapang": "lapangan", "kebon": "kebun", "lembur": "kampung",
            "dayeuh": "kota", "basisir": "pantai", "leuweung": "hutan", "pangalaman": "pengalaman",
            "aki": "kakek", "nini": "nenek", "lanceuk": "kakak", "tangkal": "pohon", "sato": "hewan",
            "parahu": "perahu", "taneuh": "tanah"}


# ============================================== Pangajaran 6 · lingkungan sabudeureun

_BACAAN_6 = [
    ("Ayeuna geus mimiti usum hujan. Langit mindeng ceudeum. Turunna hujan téh matak atoh. Buruan moal ngebul, "
     "da taneuhna henteu garing. Sumur ogé bakal pinuh deui caina. Dina usum halodo mah sumur téh loba nu saat.", [
        ("Ayeuna geus mimiti usum naon?", "usum hujan", ["usum halodo", "usum panén", "usum peré"]),
        ("Kumaha langit dina usum hujan?", "mindeng ceudeum", ["béngras", "panas", "loba béntang"]),
        ("Dina usum hujan sumur bakal …", "pinuh deui caina", ["saat", "ngebul", "garing"]),
        ("Dina usum halodo sumur téh loba nu …", "saat", ["pinuh", "limpas", "caah"]),
     ]),
    ("Hujan téh rahmat pikeun kahirupan. Lahan jadi subur, pepelakan henteu layu. Sawah jeung kebon bisa "
     "dipelakan deui ku patani.", [
        ("Hujan téh rahmat pikeun …", "kahirupan", ["runtah", "laleur", "kasakit"]),
        ("Lamun aya hujan, lahan jadi …", "subur", ["garing", "ngebul", "saat"]),
        ("Saha anu melakan sawah jeung kebon?", "patani", ["pamayang", "guru", "dokter"]),
     ]),
    ("Urang kudu waspada. Hujan téh bisa nyababkeun caah. Solokan jeung walungan limpas. Imah kakeueum. "
     "Tangkal kai ogé sok aya nu rungkad. Éta téh matak bahaya mun ninggang ka urang.", [
        ("Hujan gedé bisa nyababkeun …", "caah", ["halodo", "kahuruan", "lini"]),
        ("Lamun caah, solokan jeung walungan …", "limpas", ["saat", "garing", "ngebul"]),
        ("Tangkal kai anu rungkad matak bahaya mun …", "ninggang ka urang", ["dipelak deui", "disiram", "dibeuli"]),
     ]),
    ("Datangna caah téh lantaran salah urang kénéh. Solokan teu ngalir, kapengpet ku runtah anu ngahunyud. "
     "Urang teu meunang miceun runtah ka solokan. Runtah kudu dipiceun kana tempatna.", [
        ("Solokan teu ngalir lantaran kapengpet ku …", "runtah", ["cai", "lauk", "kembang"]),
        ("Runtah kudu dipiceun kana …", "tempatna", ["solokan", "walungan", "jalan"]),
        ("Datangna caah téh lantaran salah …", "urang kénéh", ["hujan", "patani", "tatangkalan"]),
     ]),
    ("Lobana runtah téh bakal nimbulkeun rupa-rupa kasakit. Matak rujit jeung bau. Loba laleur anu sok "
     "nyebarkeun bibit kasakit. Lingkungan anu beresih nyababkeun urang jadi séhat.", [
        ("Lobana runtah bakal nimbulkeun …", "kasakit", ["rahmat", "kaséhatan", "katumbiri"]),
        ("Sato naon anu sok nyebarkeun bibit kasakit?", "laleur", ["japati", "domba", "kelenci"]),
        ("Lingkungan anu beresih nyababkeun urang jadi …", "séhat", ["gering", "rujit", "ripuh"]),
     ]),
    ("Urang lembur Jadaria sabulan sakali sok ngayakeun kerja bakti. Biasana dina poé Ahad. Jalan jeung gang "
     "dibébérés. Runtah dikumpulkeun terus dipiceun kana tempatna. Solokan diberesihan sangkan caina lancar.", [
        ("Iraha urang Jadaria ngayakeun kerja bakti?", "sabulan sakali dina poé Ahad",
         ["unggal poé", "sataun sakali", "unggal peuting"]),
        ("Solokan diberesihan sangkan …", "caina lancar", ["caina saat", "loba runtah", "jadi caah"]),
        ("Naon ngaran lembur anu ngayakeun kerja bakti?", "Jadaria", ["Panyirapan", "Ciburuy", "Lembang"]),
     ]),
    ("Anu miluan kerja bakti téh lain kolot wungkul. Para rumaja jeung barudak ogé milu. Aya anu mawa pacul "
     "atawa singkup. Aya nu mawa parang atawa arit pikeun ngababad jukut. Barudak lolobana mawa sapu nyéré.", [
        ("Saha waé anu miluan kerja bakti?", "kolot, rumaja, jeung barudak",
         ["kolot wungkul", "barudak wungkul", "guru wungkul"]),
        ("Pakakas naon anu dibawa ku barudak?", "sapu nyéré", ["pacul", "parang", "singkup"]),
        ("Arit dipaké pikeun naon?", "ngababad jukut", ["nyiksikan bawang", "nulis", "meresihan kaca"]),
     ]),
    ("Kerja bakti dimimitian ti isuk-isuk. Digarawé bari suka seuri. Biasana kerja bakti téh tepi ka wanci "
     "lohor. Loba nu mawa lalawuh. Aya leupeut, goréngan, jeung bandrék.", [
        ("Kerja bakti biasana tepi ka wanci …", "lohor", ["magrib", "isa", "subuh"]),
        ("Lalawuh naon anu dibawa dina kerja bakti?", "leupeut jeung goréngan",
         ["baso jeung mi", "roti jeung susu", "és jeung permén"]),
        ("Kumaha digarawéna dina kerja bakti?", "bari suka seuri", ["bari ambek", "bari ceurik", "kapaksa"]),
     ]),
]

_EJAAN_6 = ["ha-lo-do", "hu-jan", "la-ngit", "wa-lu-ngan", "so-lo-kan", "ta-neuh", "run-tah", "ling-kung-an",
            "su-mur", "bu-ru-an", "sa-wah", "ke-bon", "tang-kal", "ba-ha-ya", "jang-krik", "ang-klung",
            "sem-prong", "cong-krang", "su-bur", "rah-mat", "was-pa-da", "ka-hi-rup-an", "pe-pe-lak-an"]

_SORA = [
    ("Ulah ___ miceun runtah di mana waé.", "bra-bru", ["krang-kring", "bruy-bray", "pras-pris"],
     "Jangan sembarangan membuang sampah di mana saja."),
    ("Jambu aér nu geus asak ___ ragragan.", "plak-pluk", ["krang-kring", "bruy-bray", "blung-blong"],
     "Jambu air yang sudah matang berjatuhan."),
    ("Lampu di luhur panggung ___ caraang.", "bruy-bray", ["plak-pluk", "trong-trang", "plus-plos"],
     "Lampu di atas panggung terang benderang."),
    ("Dagang téh geuning ___ euweuh batian.", "plus-plos", ["krang-kring", "bruy-bray", "jlung-jleng"],
     "Berdagang ternyata tidak ada untungnya."),
    ("Hujan geus mimiti ___, hawa karasa tiris.", "pras-pris", ["krang-kring", "blung-blong", "crung-créng"],
     "Hujan mulai rintik-rintik, udara terasa dingin."),
    ("Asa ti tatadi telepon kadéngé ___ waé.", "krang-kring", ["bruy-bray", "pras-pris", "jlung-jleng"],
     "Dari tadi telepon terdengar berdering terus."),
    ("Tutupkeun panto dapur téh, ulah ___ kitu.", "blung-blong", ["pras-pris", "krang-kring", "plak-pluk"],
     "Tutup pintu dapurnya, jangan dibiarkan terbuka begitu."),
    ("Barudak nguah angeun di dapur kadéngé ___.", "trong-trang", ["bruy-bray", "pras-pris", "jlung-jleng"],
     "Bunyi alat dapur beradu saat anak-anak mengambil sayur."),
    ("Anu ngibing bénjang ___ ka jero kalang.", "jlung-jleng", ["krang-kring", "pras-pris", "trong-trang"],
     "Penari benjang berlompatan masuk ke arena."),
]

# (kalimat, pakakas, kelompok alat pemotong atau bukan)
_PAKAKAS = [
    ("Héni nyiksikan bawang maké …", "péso", True, '"Péso" = pisau.'),
    ("Ani motongan lawon bahan baju maké …", "gunting", True, "Memotong kain memakai gunting."),
    ("Mang Dadan ngababad jukut maké …", "arit", True, '"Arit" = sabit, untuk membabat rumput.'),
    ("Néngsih ngaréndos bungbu maké …", "coét", False, '"Coét" = cobek, untuk mengulek bumbu.'),
    ("Dudi ngarapet langlayangan maké …", "lém", False, "Merekatkan layang-layang memakai lem."),
    ("Édi ngajulan jambu tina tangkal maké …", "gantar", False, '"Gantar" = galah, untuk menjolok buah.'),
    ("Karmila meresihan kaca jandéla maké …", "lap", False, "Membersihkan kaca jendela memakai lap."),
    ("Barudak sasapu di buruan maké …", "sapu nyéré", False, '"Sapu nyéré" = sapu lidi.'),
    ("Aki macul taneuh di kebon maké …", "pacul", False, '"Pacul" = cangkul.'),
]


def p6_pakakas(r):
    teks, jawab, pemotong, catatan = r.choice(_PAKAKAS)
    lain = [p[1] for p in _PAKAKAS if p[1] != jawab and not (pemotong and p[2])]
    return teks_pilihan(r, teks, jawab, r.sample(lain, 3), f'Jawabannya "{jawab}". {catatan}')


_KAMUS_6 = {"halodo": "kemarau", "runtah": "sampah", "caah": "banjir", "solokan": "selokan",
            "buruan": "halaman rumah", "beresih": "bersih", "kasakit": "penyakit", "laleur": "lalat",
            "pakakas": "perkakas", "jukut": "rumput", "ceudeum": "mendung", "patani": "petani",
            "gering": "sakit", "peuting": "malam", "isuk-isuk": "pagi-pagi"}


# ================ Pangajaran 7 · miara barang, mikanyaah sasatoan jeung tatangkalan

_BARANG = [
    ("Barang anu sok digunakeun dina kagiatan sakola nyaéta …", "patlot", ["bal", "rékét", "langlayangan"],
     '"Patlot" = pensil.'),
    ("Barang anu sok dipaké dina kaulinan nyaéta …", "bal", ["jidar", "patlot", "buku"], "Bola dipakai untuk bermain."),
    ("Patlot gunana pikeun …", "nulis", ["ulin", "dahar", "sasapu"], "Pensil gunanya untuk menulis."),
    ("Baju anu geus kotor kudu gancang …", "diseuseuh", ["disemir", "dipaké deui", "dipiceun"],
     '"Diseuseuh" = dicuci (untuk pakaian).'),
    ("Sapatu anu geus kotor kudu gancang …", "dikumbah", ["ditunda di mana waé", "dipaké saré", "dipiceun"],
     '"Dikumbah" = dicuci.'),
    ("Sapatu kulit sangkan awét kudu …", "disemir", ["diseuseuh", "dibeulahan", "diraut"],
     "Sepatu kulit disemir agar awet."),
    ("Barang kudu ditunda dina …", "tempatna", ["mana waé", "jalan", "solokan"],
     "Barang harus disimpan di tempatnya."),
    ("Lamun nginjeum barang batur, kudu gancang …", "dipulangkeun", ["dijual", "dipiceun", "diruksak"],
     '"Dipulangkeun" = dikembalikan.'),
    ("Dina mulangkeun barang batur, urang kudu nyebut …", "nuhun", ["punten", "mangga", "héhé"],
     '"Nuhun" = terima kasih.'),
    ("Lamun barang batur leungit ku urang, kudu …", "digantian", ["diantep", "disumputkeun", "dipoékeun"],
     '"Digantian" = diganti.'),
    ("Barang bakal awét lamun urangna …", "apik", ["jabrah", "kedul", "poho"],
     '"Apik" = rapi dan hati-hati dalam merawat.'),
    ("Barang anu geus ruksak moal payu kana …", "duit", ["cai", "sakola", "tangkal"],
     "Barang rusak tidak laku dijual (payu = laku)."),
    ("Lamun apik ngurusna, umur barang bisa …", "panjang", ["pondok", "leungit", "ruksak"],
     "Kalau dirawat dengan baik, barang awet."),
    ("Baju paranti sakola dipakéna mun urang …", "sakola", ["ulin", "saré", "mandi"],
     "Baju sekolah dipakai untuk sekolah."),
    ('Tembang "Apik kana Barang" téh dina pupuh …', "kinanti", ["magatru", "pucung", "asmarandana"],
     "Di buku, tembang itu memakai pupuh kinanti."),
    ("Kudu leuwih apik mun nginjeum barang ti …", "batur", ["toko", "pasar", "sakola"],
     "Barang pinjaman dari orang lain harus dijaga lebih hati-hati."),
]

_SASATOAN = [
    ("Maung anu buluna belang coréléng disebutna maung …", "lodya", ["tutul", "kumbang", "bodas"],
     "Harimau loreng disebut maung lodya."),
    ("Maung anu buluna totol-totol disebutna maung …", "tutul", ["lodya", "kumbang", "bodas"],
     "Macan tutul berbulu totol-totol."),
    ("Maung anu warna buluna hideung disebutna maung …", "kumbang", ["lodya", "tutul", "bodas"],
     "Macan kumbang berbulu hitam."),
    ("Hayam jago disadana …", "kongkorongok", ["ngagerem", "ngagaur", "ngéong"], "Ayam jago berkokok."),
    ("Sato anu sok digawékeun di sawah nyaéta …", "munding", ["maung", "bajing", "japati"], '"Munding" = kerbau.'),
    ("Sato anu sok narik délman nyaéta …", "kuda", ["domba", "hayam", "kelenci"], "Delman ditarik kuda."),
    ("Sato anu ngahasilkeun madu nyaéta …", "nyiruan", ["laleur", "jangkrik", "hileud"], '"Nyiruan" = lebah.'),
    ("Sato anu buluna rancung sareukeut nyaéta …", "landak", ["kelenci", "domba", "bajing"],
     "Landak berbulu runcing dan tajam."),
    ("Sato anu ceulina rarancung jeung kabeukina jukut nyaéta …", "kelenci", ["landak", "maung", "nyiruan"],
     '"Kelenci" = kelinci.'),
    ("Sato anu hirupna di cai nyaéta …", "lauk", ["hayam", "domba", "japati"], '"Lauk" = ikan.'),
    ("Sato anu sok hiber nyaéta …", "japati", ["domba", "munding", "lauk"], '"Japati" = merpati; bisa terbang.'),
    ("Sato anu tandukan nyaéta …", "banténg", ["hayam", "japati", "lauk"], "Banteng bertanduk."),
    ("Sato anu kabeukina jukut nyaéta …", "domba", ["maung", "lauk", "nyiruan"], "Domba makan rumput."),
    ("Lutung buluna hideung lestreng, buntutna …", "panjang", ["pondok", "euweuh", "bodas"],
     "Lutung berbulu hitam legam dan berekor panjang."),
    ("Keuyeup ngaliang dina galeng …", "sawah", ["jalan", "imah", "langit"],
     '"Keuyeup" = kepiting sawah; bersarang di pematang sawah.'),
    ("Ka sasatoan urang kudu …", "welas asih", ["nyiksa", "ambek", "hiri dengki"],
     "Kita harus menyayangi hewan."),
    ("Urang ulah nyiksa sasatoan sabab sato ogé miboga rasa …", "nyeri", ["amis", "pait", "asin"],
     "Hewan juga bisa merasa sakit."),
    ("Lamun nyiruan nyeureud kana kulit, matak …", "bareuh", ["séhat", "atoh", "seger"],
     "Sengatan lebah membuat kulit bengkak (bareuh)."),
]

_KANDANG = [
    ("Pagupon nyaéta kandang …", "japati", ["maung", "lauk", "munding"], "Pagupon adalah kandang merpati."),
    ("Korang nyaéta paranti ngawadahan …", "lauk", ["japati", "hayam", "maung"],
     "Korang adalah wadah ikan hasil tangkapan."),
    ("Sato galak saperti maung ditunda dina …", "karangkéng", ["pagupon", "korang", "kurung"],
     "Karangkéng adalah kerangkeng untuk hewan buas."),
    ("Manuk dikukutna dina …", "kurung", ["korang", "karangkéng", "balong"], "Burung dipelihara di dalam sangkar (kurung)."),
    ("Lauk kancra hirupna di …", "balong", ["pagupon", "kurung", "karangkéng"], '"Balong" = kolam ikan.'),
]

_TATANGKALAN = [
    ("Tatangkalan butuh …", "cai", ["runtah", "hama", "seuneu"], "Tanaman membutuhkan air."),
    ("Tatangkalan kudu digemuk jeung …", "disiram", ["dituar", "diduruk", "diantep"],
     "Tanaman harus dipupuk dan disiram."),
    ("Hama anu sok aya dina daun nyaéta …", "hileud", ["lauk", "japati", "domba"], '"Hileud" = ulat.'),
    ("Dina lahan anu subur, tatangkalan gampang …", "jadi", ["layu", "garing", "paéh"],
     "Di lahan subur tanaman mudah tumbuh."),
    ("Anu jarangkung nyaéta tangkal …", "kai", ["kembang", "jukut", "bawang"], "Pohon kayu tumbuh tinggi."),
    ("Sangu asalna tina tangkal …", "paré", ["jagong", "kalapa", "jati"], "Nasi berasal dari padi."),
    ("Lamun daunna layu terus garing, bisi eukeur loba …", "hama", ["cai", "kembang", "buah"],
     "Daun layu dan kering bisa karena banyak hama."),
]

_SUSUN_7 = [
    ("entong – kahadé – baju – kotor – maké", "kahadé entong maké baju kotor"),
    ("séhat – maké – henteu – kotor – baju", "maké baju kotor henteu séhat"),
    ("tacan – awét – tangtu – mahal – barang", "barang mahal tacan tangtu awét"),
    ("hartina – barang – kana – hémat – apik", "apik kana barang hartina hémat"),
    ("batur – bébéja – kudu – maké – barang", "maké barang batur kudu bébéja"),
    ("henteu – ngaku – batur – hadé – barang", "ngaku barang batur henteu hadé"),
    ("kawajiban – kana – apik – jadi – barang", "apik kana barang jadi kawajiban"),
    ("kudu – sangkan – sapatu – awét – disemir", "sangkan awét sapatu kudu disemir"),
    ("baju – maksakeun – ulah – maké – baseuh", "ulah maksakeun maké baju baseuh"),
    ("dipakéna – beresih – baju – genah – matak", "baju beresih matak genah dipakéna"),
]

_KAMUS_7 = {"maung": "harimau", "munding": "kerbau", "hayam": "ayam", "japati": "merpati", "manuk": "burung",
            "lauk": "ikan", "nyiruan": "lebah", "kelenci": "kelinci", "bajing": "tupai", "hileud": "ulat",
            "patlot": "pensil", "jidar": "penggaris", "kantong": "tas", "kembang": "bunga",
            "nginjeum": "meminjam", "nuhun": "terima kasih", "paré": "padi", "sangu": "nasi"}


# ======================================================= Pangajaran 8 · kajadian alam

_BACAAN_8 = [
    ("Soré-soré aya hujan poyan sakeudeung. Barudak nuluykeun deui arulin. Aya nu maénbal jeung aya nu ulin "
     "ucing sumput. Henteu lila ti harita di langit aya katumbiri. Melengkung warna-warni matak resep nempona.", [
        ("Barudak arulin naon?", "maénbal jeung ucing sumput", ["langlayangan jeung kaléci", "ngojay", "sapédahan"]),
        ("Naon anu katempo di langit sanggeus hujan poyan?", "katumbiri", ["béntang", "bulan", "kilat"]),
        ("Kumaha rupana katumbiri?", "melengkung warna-warni", ["buleud hideung", "pasagi bodas", "lempeng beureum"]),
     ]),
    ("Warna katumbiri téh aya tujuh rupa, nyaéta beureum, oranyeu, konéng, héjo, biru, nila, jeung wungu. "
     "Katumbiri témbong di langit lamun aya hujan poyan. Hujan poyan téh nyaéta hujan, tapi aya cahaya "
     "panonpoé. Lamun hujanna geus euweuh, katumbirina ogé leungit.", [
        ("Warna katumbiri aya sabaraha rupa?", "tujuh", ["tilu", "lima", "salapan"]),
        ("Anu lain warna katumbiri nyaéta …", "hideung", ["beureum", "héjo", "wungu"]),
        ("Iraha katumbiri témbong di langit?", "lamun aya hujan poyan",
         ["lamun peuting", "lamun aya lini", "lamun usum halodo"]),
        ("Hujan poyan téh nyaéta …", "hujan tapi aya cahaya panonpoé",
         ["hujan bari aya angin tarik", "hujan dina wanci peuting", "hujan anu gedé pisan"]),
        ("Lamun hujanna geus euweuh, katumbiri bakal …", "leungit", ["beuki gedé", "ragrag", "jadi béntang"]),
     ]),
    ("Isuk-isuk panonpoé mucunghul ti beulah wétan, dunya jadi caang. Panonpoé tilem di beulah kulon, dunya "
     "jadi poék. Éta nu disebut datangna peuting. Dina wanci peuting urang sok reureuh, sangkan isukna "
     "karasa seger.", [
        ("Panonpoé mucunghul ti beulah …", "wétan", ["kulon", "kalér", "kidul"]),
        ("Panonpoé tilem di beulah …", "kulon", ["wétan", "kalér", "kidul"]),
        ("Lamun panonpoé geus tilem, dunya jadi …", "poék", ["caang", "panas", "bayeungyang"]),
        ("Dina wanci peuting urang sok …", "reureuh", ["sakola", "upacara", "kerja bakti"]),
     ]),
    ("Dina usum halodo loba tempat anu hésé cai. Sumur, balong, jeung walungan loba nu saat. Dina usum hujan "
     "mah sumur, balong, jeung walungan téh pinuh deui ku cai. Tapi usum hujan bisa nyababkeun caah.", [
        ("Dina usum halodo loba tempat anu hésé …", "cai", ["runtah", "hawa", "taneuh"]),
        ("Dina usum hujan, sumur jeung walungan …", "pinuh deui ku cai", ["saat", "ngebul", "kahuruan"]),
        ("Usum hujan bisa nyababkeun …", "caah", ["kahuruan", "halodo", "samagaha"]),
     ]),
    ("Turunna hujan téh rupa-rupa. Hujan anu dibarung ku angin tarik disebutna hujan angin. Hujan anu henteu "
     "gedé disebut girimis. Lamun taneuh karasa ngarieg, éta téh aya lini. Lamun beurang ngadadak jadi poék, "
     "éta téh aya samagaha.", [
        ("Hujan anu dibarung ku angin tarik disebutna …", "hujan angin", ["hujan poyan", "girimis", "lini"]),
        ("Hujan anu henteu gedé disebut …", "girimis", ["hujan angin", "caah", "samagaha"]),
        ("Lamun taneuh karasa ngarieg, éta téh aya …", "lini", ["katumbiri", "girimis", "halodo"]),
        ("Lamun beurang ngadadak jadi poék, éta téh aya …", "samagaha", ["lini", "katumbiri", "caah"]),
     ]),
    ("Isuk-isuk panonpoé mucunghul tina sela gunung. Manuk ramé disarada dina dahan. Hawa karasa seger. "
     "Hanjakal jaman kiwari mah geus loba nu robah. Cai di walungan geus henteu hérang. Runtah ngahunyud "
     "ditapuk laleur, jadi sumber kasakit. Mémérés lingkungan jadi tanggung jawab urang saréréa.", [
        ("Panonpoé mucunghul dipapag ku sora …", "manuk", ["mobil", "gelap", "telepon"]),
        ("Kumaha cai walungan jaman kiwari?", "geus henteu hérang", ["hérang ngagenyas", "amis", "haneut"]),
        ("Runtah anu ngahunyud jadi sumber …", "kasakit", ["cai", "kahirupan", "kabungah"]),
        ("Mémérés lingkungan jadi tanggung jawab …", "urang saréréa",
         ["patani wungkul", "guru wungkul", "barudak wungkul"]),
     ]),
    ("Ahmad: Kamari teu tulus latihan pramuka téh.\nGalih: Enya, apan hujan sakitu gedéna.\n"
     "Hérlin: Lapangna gé tangtu kakeueum atuh.\nGalih: Biasana mah lantaran solokan sok limpas.\n"
     "Galih: Latihan pramuka téh di hareupeun kantor kacamatan nu genah mah.\n"
     "Hérlin: Ih, jauh atuh di dinya mah.", [
        ("Naon sababna latihan pramuka teu tulus?", "hujan gedé",
         ["euweuh guruna", "lapangna dipaké maénbal", "peré sakola"]),
        ("Lapang kakeueum lantaran solokan sok …", "limpas", ["saat", "garing", "beresih"]),
        ("Ceuk Galih, latihan pramuka téh genahna di mana?", "di hareupeun kantor kacamatan",
         ["di lapang nu kakeueum", "di sisi walungan", "di jero kelas"]),
        ("Saha anu nyebutkeun tempatna jauh?", "Hérlin", ["Ahmad", "Galih", "Wening"]),
     ]),
]

_ALAM = [
    ("Lamun langit ceudeum, biasana bakal aya …", "hujan", ["lini", "samagaha", "halodo"],
     "Langit mendung biasanya tanda akan hujan."),
    ("Lamun peuting, anu sok caang di langit nyaéta …", "bulan jeung béntang", ["panonpoé", "katumbiri", "méga"],
     "Pada malam hari yang bersinar adalah bulan dan bintang."),
    ("Ombak biasana aya di …", "laut", ["sumur", "sawah", "jalan"], "Ombak ada di laut."),
    ("Cai laut rasana …", "asin", ["amis", "pait", "haseum"], "Air laut rasanya asin."),
    ("Langlayangan bisa ngapung lantaran aya …", "angin", ["hujan", "lini", "gelap"],
     "Layang-layang terbang karena ada angin."),
    ("Ari keur hujan, sakapeung sok kadéngé sora …", "gelap", ["jangkrik", "angklung", "manuk"],
     '"Gelap" dalam bahasa Sunda berarti petir.'),
    ("Di langit melengkung warna-warni disebutna …", "katumbiri", ["samagaha", "kilat", "méga"],
     '"Katumbiri" = pelangi.'),
    ("Lini sakapeung datangna lantaran aya gunung …", "bitu", ["urug", "caah", "saat"],
     '"Gunung bitu" = gunung meletus.'),
    ("Dina usum halodo sok aya kahuruan, anu matak urang ulah nyoo …", "seuneu", ["cai", "taneuh", "bal"],
     "Jangan bermain api pada musim kemarau."),
]

_UCAPAN = [
    ("Mun manggih kabungah, urang kudu nyebut …", "alhamdulillah", "Saat mendapat kebahagiaan."),
    ("Sémah keketrok panto terus ngucapkeun …", "assalamualaikum", "Tamu mengetuk pintu lalu mengucap salam."),
    ("Mun ngadéngé sora gelap, pék ucapkeun …", "subhanalloh", "Saat mendengar suara petir."),
    ("Lamun urang jangji, kudu ditungtungan ku …", "insa alloh", "Saat berjanji."),
    ("Mun urang manggih kareuwas, ucapkeun …", "astagpirulloh", "Saat terkejut."),
    ("Takbir dina solat téh nyaéta ngucapkeun …", "allohu akbar", "Takbir dalam salat."),
    ("Saméméh ngamimitian gawé, urang ngucap …", "bismillah", "Sebelum memulai pekerjaan."),
]


def p8_ucapan(r):
    teks, jawab, catatan = r.choice(_UCAPAN)
    return teks_pilihan(r, teks, jawab, r.sample([u[1] for u in _UCAPAN if u[1] != jawab], 3),
                        f'Jawabannya "{jawab}". {catatan}')


# (benda alam, keadaannya, kelompok bunyi keras?, arti)
_KAAYAAN = [
    ("imah", "ngagebru", True, "rumah roboh berdebum"), ("hujan", "ngagebrét", False, "hujan turun sangat deras"),
    ("seuneu", "ngabebela", False, "api berkobar-kobar"), ("angin", "ngagelebug", False, "angin bertiup kencang"),
    ("cai", "ngagulidag", False, "air mengalir deras"), ("ombak", "ngajelegur", True, "ombak berdebur"),
    ("taneuh", "ngarieg", False, "tanah bergetar"), ("curug", "ngaguruh", True, "air terjun bergemuruh"),
    ("gelap", "ngajelegér", True, "petir menggelegar"), ("kilat", "ngabaranyay", False, "kilat menyambar terang"),
]
_KALIMAH_KAAYAAN = {
    "imah": "Waktu lahan urug, loba imah ___.", "hujan": "Ari keur hujan ___, ulah bijil ti imah.",
    "seuneu": "Seuneu ___ katémbongna matak paur.", "angin": "Di tengah pasawahan karasa angin ___.",
    "cai": "Cai ___ kénéh sanajan usum halodo.", "ombak": "Ombak ___ terus muncrat ka sisi basisir.",
    "taneuh": "Tangtuna aya lini, da karasa taneuh ___.", "curug": "Ti kajauhan geus kadéngé sora curug ___.",
    "gelap": "Gelap ___ tarik pisan, matak katorékan.", "kilat": "Kilat ___ nyaangan poékna langit.",
}


def p8_kaayaan(r):
    benda, keadaan, keras, arti = r.choice(_KAAYAAN)
    lain = [k for k in _KAAYAAN if k[0] != benda and not (keras and k[2])
            and {k[0], benda} != {"cai", "hujan"} and {k[0], benda} != {"kilat", "seuneu"}]
    if r.random() < 0.6:
        return teks_pilihan(r, _KALIMAH_KAAYAAN[benda], keadaan, [k[1] for k in r.sample(lain, 3)],
                            f'"{benda.capitalize()} {keadaan}" artinya {arti}.')
    return teks_pilihan(r, f"Anu sok disebut {keadaan} nyaéta …", benda, [k[0] for k in r.sample(lain, 3)],
                        f'"{benda.capitalize()} {keadaan}" artinya {arti}.')


_SUSUN_8 = [
    ("jareblog – dina – buruan – hujan – usum", "dina usum hujan buruan jareblog"),
    ("hujan – bayeungyang – arék – hawa – lantaran", "hawa bayeungyang lantaran arék hujan"),
    ("rubuh – puyuh – anténeu – angin – nyababkeun", "angin puyuh nyababkeun anténeu rubuh"),
    ("karang – laut – neumbagan – ngajelegur – ombak", "ombak laut ngajelegur neumbagan karang"),
    ("matak – sora – katorékan – tingjelegér – gelap", "sora gelap tingjelegér matak katorékan"),
]

_KAMUS_8 = {"katumbiri": "pelangi", "panonpoé": "matahari", "lini": "gempa bumi", "gelap": "petir",
            "samagaha": "gerhana", "wétan": "timur", "kulon": "barat", "kalér": "utara", "kidul": "selatan",
            "beurang": "siang", "méga": "awan", "béntang": "bintang", "caang": "terang", "girimis": "gerimis",
            "usum": "musim"}


# ------------------------------------------------------------------- perakit

PEMBANGKIT = {
    "su-pangajaran-1": [_dari_bacaan(_BACAAN_1), _dari_butir(_NGARIKSA), _dari_butir(_NGARIKSA),
                        _engang(_EJAAN_1), _engang(_EJAAN_1), _aksara(_KECAP_1), _aksara(_KECAP_1),
                        _arti(_KAMUS_1)],
    "su-pangajaran-2": [_dari_bacaan(_BACAAN_2), _dari_bacaan(_BACAAN_2), _dari_bacaan(_BACAAN_2),
                        _nasal(_GAWE_M, ["n", "ng", "ny"]), _nasal(_GAWE_N, ["m", "ng", "ny"]), p2_di,
                        _dari_butir(_BARANG_2), _engang(_EJAAN_2), _aksara(_KECAP_2), _arti(_KAMUS_2)],
    "su-pangajaran-3": [_dari_bacaan(_BACAAN_3), _dari_bacaan(_BACAAN_3), _dari_bacaan(_BACAAN_3),
                        _dari_butir(_MIRIP), _dari_butir(_MIRIP), _engang(_EJAAN_3), _arti(_KAMUS_3)],
    "su-pangajaran-4": [_dari_bacaan(_BACAAN_4), _dari_bacaan(_BACAAN_4), _dari_bacaan(_BACAAN_4),
                        _dari_butir(_KULAWARGA), _dari_butir(_KULAWARGA), _dari_butir(_NY),
                        _nasal(_GAWE_NY, ["m", "ng", "n"]), _engang(_EJAAN_4), _arti(_KAMUS_4)],
    "su-pangajaran-5": [_dari_bacaan(_BACAAN_5), _dari_bacaan(_BACAAN_5), _dari_butir(_PANANYA), p5_saha_naon,
                        _susun(_SUSUN_5), _dari_butir(_TEMPAT), _dari_butir(_MAGATRU), _arti(_KAMUS_5)],
    "su-pangajaran-6": [_dari_bacaan(_BACAAN_6), _dari_bacaan(_BACAAN_6), _dari_bacaan(_BACAAN_6),
                        _engang(_EJAAN_6), _engang(_EJAAN_6), _dari_butir(_SORA), p6_pakakas, _arti(_KAMUS_6)],
    "su-pangajaran-7": [_dari_butir(_BARANG), _dari_butir(_BARANG), _dari_butir(_SASATOAN), _dari_butir(_SASATOAN),
                        _dari_butir(_KANDANG), _dari_butir(_TATANGKALAN), _susun(_SUSUN_7), _arti(_KAMUS_7)],
    "su-pangajaran-8": [_dari_bacaan(_BACAAN_8), _dari_bacaan(_BACAAN_8), _dari_bacaan(_BACAAN_8),
                        _dari_butir(_ALAM), p8_ucapan, p8_kaayaan, _susun(_SUSUN_8), _arti(_KAMUS_8)],
}

GABUNGAN = {
    "su-semester-1": [f"su-pangajaran-{i}" for i in range(1, 5)],
    "su-semester-2": [f"su-pangajaran-{i}" for i in range(5, 9)],
}

KODE_TOPIK = [t["kode"] for t in TOPIK]


def buat_latihan(topik, jumlah=JUMLAH_SOAL, rng=None):
    """Buat ``jumlah`` soal Bahasa Sunda berbeda untuk satu pangajaran atau satu paket gabungan."""
    if topik not in KODE_TOPIK:
        raise ValueError(f"topik tidak dikenal: {topik}")
    r = rng or random.Random()
    if topik in GABUNGAN:
        return rakit({k: PEMBANGKIT[k] for k in GABUNGAN[topik]}, topik, topik, jumlah, r)
    return rakit(PEMBANGKIT, topik, None, jumlah, r)
