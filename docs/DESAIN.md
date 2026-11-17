# Desain Aplikasi — Pintar Matematika (Latihan Soal SD Kelas 4)

## 1. Tujuan

Aplikasi web sederhana untuk latihan soal matematika SD kelas 4 yang:

- menampilkan **20 soal berbeda** setiap kali latihan dimulai,
- membiarkan siswa **memilih topik** latihan,
- **menghitung nilai secara otomatis** begitu latihan selesai,
- **mencatat setiap hasil latihan** sehingga bisa dilihat kembali,
- berjalan di **server lokal** dan diakses lewat **browser**.

Pengguna utama: siswa kelas 4 SD (9–10 tahun), didampingi orang tua/guru yang
ingin melihat riwayat nilai.

## 2. Keputusan Desain Utama

| Keputusan | Pilihan | Alasan |
|---|---|---|
| Bahasa server | Python 3 (hanya pustaka standar) | Tanpa `pip install`; cukup `python3 app.py` |
| Penyimpanan | SQLite (`data/latihan.db`) | Satu file, tanpa instalasi database, hasil tetap ada setelah server dimatikan |
| Tampilan | HTML + CSS + JavaScript murni | Tanpa proses build, tanpa internet |
| Bentuk soal | Pilihan ganda A–D | Mudah dijawab anak, penilaian pasti (tidak ada masalah format ketikan) |
| Sumber soal | Dibangkitkan acak oleh program | Soal selalu baru; tidak akan "habis" seperti bank soal tetap |
| Penilaian | Dilakukan di server | Kunci jawaban tidak pernah dikirim ke browser sebelum latihan dikumpulkan |

## 3. Topik Latihan

Mengacu pada materi matematika kelas 4 SD:

| Kode | Topik | Contoh jenis soal |
|---|---|---|
| `tambah-kurang` | Penjumlahan & Pengurangan | bilangan ribuan–puluh ribuan, mencari bilangan yang hilang, operasi campuran |
| `perkalian` | Perkalian | 2 angka × 1 angka, 2 angka × 2 angka, kali 10/100/1.000 |
| `pembagian` | Pembagian | pembagian habis, pembagian bersisa, mencari bilangan yang hilang |
| `pecahan` | Pecahan | pecahan senilai, menyederhanakan, tambah/kurang berpenyebut sama, membandingkan, pecahan campuran, desimal |
| `kpk-fpb` | Faktor, Kelipatan, KPK & FPB | faktor, kelipatan, bilangan prima, faktorisasi prima, KPK, FPB |
| `pembulatan` | Nilai Tempat & Pembulatan | nilai tempat, nilai angka, pembulatan, penaksiran, membandingkan bilangan |
| `keliling-luas` | Keliling & Luas Bangun Datar | persegi, persegi panjang, segitiga |
| `bangun-datar` | Bangun Datar | jenis kurva (terbuka/tertutup, sederhana/tidak sederhana); segi banyak beraturan dan tidak beraturan; segitiga dan segiempat (jenis, sifat, nama); komposisi dan dekomposisi bangun datar — sebagian soal bergambar |
| `pengukuran` | Pengukuran | satuan panjang, berat, waktu, volume, kuantitas (lusin, kodi, rim) |
| `soal-cerita` | Soal Cerita | soal cerita satu dan dua langkah, termasuk uang |
| `campuran` | Campuran Semua Topik | 20 soal diambil merata dari semua topik di atas |

### Aturan pembuatan soal

- Satu latihan = **20 soal**; teks soal dalam satu latihan tidak boleh ada yang sama.
- Angka diacak setiap kali, sehingga latihan berikutnya hampir pasti berbeda.
- Setiap soal punya **4 pilihan yang berbeda**, tepat satu yang benar. Pilihan
  pengecoh dibuat dari kesalahan yang umum (mis. luas tertukar dengan keliling).
- Soal boleh disertai **gambar** (SVG yang digambar oleh server, mis. kurva, segi banyak,
  bangun yang diuraikan dengan garis putus-putus). Gambar yang sama tidak muncul dua kali
  dalam satu latihan.
- Setiap soal punya **pembahasan singkat** yang ditampilkan setelah dinilai.
- Bilangan ditulis dengan gaya Indonesia: `12.500`, desimal `0,25`.

### Mata pelajaran Bahasa Inggris

Mata pelajaran kedua memakai alur, penilaian, dan pencatatan yang sama. Siswa memilih mata
pelajaran di Beranda, lalu memilih topiknya. Soal ditulis dalam bahasa Inggris; pembahasan
ditulis dalam bahasa Indonesia agar mudah dipahami.

Pembagian topik mengikuti buku siswa Kemendikbudristek **My Next Words Grade 4** (2021):
satu topik per unit, dikelompokkan per semester di Beranda.

| Kode | Unit buku | Isi soal |
|---|---|---|
| `en-unit-1` | Unit 1 · What Are You Doing? | am/is/are + kata kerja-ing, ejaan -ing, kegiatan di sekolah |
| `en-unit-2` | Unit 2 · There Are 67 English Books | bilangan 1–100 dalam kata, plus/minus, how many |
| `en-unit-3` | Unit 3 · My Living Room is Beside Kitchen | nama ruangan, beside/between (denah bergambar), clean/dirty/tidy/empty |
| `en-unit-4` | Unit 4 · Cici Cooks in The Kitchen | kalimat positif/negatif/tanya (do/does), respon Yes/No, kegiatan di tiap ruangan |
| `en-unit-5` | Unit 5 · Where Is My Pencil? | benda di ruang tamu dan kamar tidur, there is/are, how many, a/an, jamak, kata depan tempat |
| `en-unit-6` | Unit 6 · The Stove is in The Kitchen | benda di kamar mandi dan dapur, kegunaan benda, do not/does not, bacaan tentang ruangan |
| `en-unit-7` | Unit 7 · I Can Make Fried Egg in The Kitchen | can/can't, kata kerja memasak |
| `en-unit-8` | Unit 8 · Be On Time! | membaca jam (gambar jam): o'clock, half past, quarter past/to |
| `en-unit-9` | Unit 9 · I Go to School after Having Breakfast | kegiatan sehari-hari, before/after, morning/afternoon/evening/night |
| `en-unit-10` | Unit 10 · He Always Gets Up at 5 O'clock | always/usually/sometimes/never, bacaan kegiatan harian |
| `en-unit-11` | Unit 11 · How Do You Go to School? | nama kendaraan, by …/on foot |
| `en-unit-12` | Unit 12 · He Goes to School by Bike | kalimat go/goes to … at … by … |
| `en-semester-1` | Semester 1 Review | gabungan Unit 1–7 |
| `en-semester-2` | Semester 2 Review | gabungan Unit 8–12 |
| `en-ts3` | Latihan Tes Sumatif 3 | paket sesuai kisi-kisi sekolah (lihat di bawah) |

**Kisi-kisi Tes Sumatif 3.** Kisi-kisi sekolah memakai penomoran *Lesson 5* dan *Lesson 6*
yang tidak sama dengan nomor unit buku. Isinya dipetakan sebagai berikut, dan kosakatanya
(termasuk terjemahan versi kisi-kisi) dimasukkan ke unit terkait:

| Materi kisi-kisi | Unit |
|---|---|
| Benda di bathroom, living room, kitchen, bedroom | Unit 5 dan Unit 6 |
| There is / There are, a/an, benda jamak | Unit 5 |
| How many … are there? | Unit 5 (dan Unit 2) |
| Alat dapur (kitchenware) | Unit 6 |
| Kata kerja kegiatan memasak | Unit 7 |
| Kalimat positif, negatif, tanya; respon Yes/No | Unit 4 |

Paket `en-ts3` mengambil soal hanya dari materi di tabel ini.

Kode topik Bahasa Inggris diawali `en-` sehingga tidak bertabrakan dengan topik Matematika;
mata pelajaran sebuah latihan diturunkan dari kode topiknya, jadi skema database tidak berubah.

### Mata pelajaran Bahasa Sunda (kelas 1)

Mata pelajaran ketiga, untuk kelas 1, memakai alur yang sama. Pembagian topik mengikuti buku
**Pamekar Diajar Basa Sunda Pikeun Murid SD/MI Kelas I** (Dinas Pendidikan Provinsi Jawa Barat,
2014): satu topik per *pangajaran*. Soal ditulis dalam bahasa Sunda; pembahasan dalam bahasa
Indonesia.

| Kode | Pangajaran | Isi soal |
|---|---|---|
| `su-pangajaran-1` | 1 · Ngurus Diri Sorangan | bacaan Aa budak apik, ngariksa badan, huruf awal/akhir kata, mengeja suku kata |
| `su-pangajaran-2` | 2 · Pangaresep | bacaan karesep, kata kerja (pacul → macul, dikonci), mengeja |
| `su-pangajaran-3` | 3 · Kagiatan | bacaan berangkat sekolah dan olahraga, percakapan, kata yang mirip (bener/beuneur) |
| `su-pangajaran-4` | 4 · Kulawarga | bacaan keluarga, sebutan kekerabatan, percakapan, kata ber-"ny" |
| `su-pangajaran-5` | 5 · Pangalaman | bacaan nyaba ka Panyirapan, kata tanya, menyusun kalimat, istilah tempat, pupuh magatru |
| `su-pangajaran-6` | 6 · Lingkungan Sabudeureun | bacaan musim hujan dan kerja bakti, mengeja, tiruan bunyi, perkakas |
| `su-pangajaran-7` | 7 · Miara Barang, Sasatoan jeung Tatangkalan | merawat barang, nama hewan dan kandangnya, tanaman, menyusun kalimat |
| `su-pangajaran-8` | 8 · Kajadian Alam | bacaan katumbiri dan kejadian alam, percakapan, ucapan, keadaan alam |
| `su-semester-1` | Gabungan Semester 1 | campuran Pangajaran 1–4 |
| `su-semester-2` | Gabungan Semester 2 | campuran Pangajaran 5–8 |

Berbeda dari Matematika, sebagian besar soal Bahasa Sunda berasal dari kumpulan butir tetap yang
disusun dari bacaan, kalimat, dan latihan di buku; yang diacak adalah pilihan butir, urutannya,
dan pengecohnya. Bacaan dipotong per paragraf pendek agar sesuai untuk pembaca pemula.

Karena aplikasi kini memuat lebih dari satu kelas, tiap mata pelajaran membawa keterangan
kelasnya (Matematika dan Bahasa Inggris kelas 4, Bahasa Sunda kelas 1) yang ditampilkan pada
pilihan mata pelajaran.

## 4. Penilaian

```
nilai = (jumlah benar ÷ 20) × 100        → setiap soal bernilai 5
```

| Nilai | Predikat |
|---|---|
| 90 – 100 | Luar biasa! ⭐⭐⭐ |
| 75 – 89 | Bagus sekali! ⭐⭐ |
| 60 – 74 | Cukup baik ⭐ |
| < 60 | Ayo coba lagi! |

Soal yang tidak dijawab dihitung salah. Lama pengerjaan dihitung server
(waktu dikumpulkan − waktu dimulai).

## 5. Alur Pengguna

```
 ┌─────────┐  pilih topik   ┌──────────┐  kumpulkan  ┌────────┐
 │ Beranda │ ─────────────▶ │ Latihan  │ ──────────▶ │ Hasil  │
 │         │ ◀───────────── │ 20 soal  │             │ nilai  │
 └────┬────┘  latihan baru  └──────────┘             └───┬────┘
      │                                                  │
      │            ┌──────────┐      lihat detail        │
      └──────────▶ │ Riwayat  │ ◀────────────────────────┘
                   └──────────┘
```

## 6. Rancangan Layar

### 6.1 Beranda

```
┌──────────────────────────────────────────────────────┐
│ 🧮 Pintar Matematika            [Beranda] [Riwayat]  │
├──────────────────────────────────────────────────────┤
│  Halo! Siap latihan matematika kelas 4?              │
│                                                      │
│  Nama kamu*: [______________]   (wajib diisi)        │
│                                                      │
│  Pelajaran: (Matematika) (Bahasa Inggris)            │
│                                                      │
│  Pilih topik:                                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐              │
│  │ ➕ Tambah │ │ ✖️ Kali  │ │ ➗ Bagi   │   ...        │
│  │ & Kurang │ │          │ │          │              │
│  └──────────┘ └──────────┘ └──────────┘              │
│                                                      │
│               [  Mulai Latihan  ]                    │
└──────────────────────────────────────────────────────┘
```

### 6.2 Latihan (satu soal per layar)

```
┌──────────────────────────────────────────────────────┐
│ Perkalian                   Soal 7 dari 20   ⏱ 03:12 │
│ ▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░  (terjawab 6)              │
├──────────────────────────────────────────────────────┤
│  36 × 7 = …                                          │
│                                                      │
│  ( A ) 242        ( B ) 252                          │
│  ( C ) 262        ( D ) 259                          │
│                                                      │
│  [◀ Sebelumnya]                    [Berikutnya ▶]    │
│                                                      │
│  1 2 3 4 5 6 [7] 8 9 10 ... 20   ← lompat ke nomor   │
│                      [ Selesai & Lihat Nilai ]       │
└──────────────────────────────────────────────────────┘
```

- Jawaban boleh diubah sebelum dikumpulkan.
- Kotak nomor berwarna bila sudah dijawab.
- Bila masih ada soal kosong saat dikumpulkan, muncul konfirmasi.
- Bila halaman tidak sengaja dimuat ulang, latihan yang sedang berjalan dilanjutkan.
- Latihan bisa **dibatalkan** (tombol "Batalkan latihan" di layar Latihan, atau "Batalkan" pada
  pengingat di Beranda). Setelah dikonfirmasi, latihan dihapus dan tidak dicatat di Riwayat.
  Latihan yang sudah dikumpulkan tidak bisa dibatalkan. Memulai latihan baru saat masih ada
  latihan berjalan juga membatalkan yang lama.

### 6.3 Hasil

```
┌──────────────────────────────────────────────────────┐
│                 ⭐⭐  Bagus sekali!                    │
│                      ( 85 )                          │
│        Benar 17 · Salah 3 · Waktu 06:41              │
│        [ Latihan Baru ]   [ Lihat Riwayat ]          │
├──────────────────────────────────────────────────────┤
│ Pembahasan                                           │
│ 1. ✅ 36 × 7 = …        Jawabanmu: 252               │
│ 2. ❌ 48 × 6 = …        Jawabanmu: 278 · Benar: 288  │
│      Pembahasan: 48 × 6 = 288                        │
│ ...                                                  │
└──────────────────────────────────────────────────────┘
```

### 6.4 Riwayat

```
┌──────────────────────────────────────────────────────┐
│ Jumlah latihan: 12   Rata-rata: 78   Terbaik: 100    │
├───────────────┬───────┬────────────┬───────┬───────┬─┤
│ Tanggal       │ Nama  │ Topik      │ Benar │ Nilai │ │
│ 12 Nov 10.15  │ Budi  │ Perkalian  │ 17/20 │  85   │▶│
│ 11 Nov 16.02  │ Budi  │ Pecahan    │ 14/20 │  70   │▶│
└───────────────┴───────┴────────────┴───────┴───────┴─┘
```

Baris bisa diklik untuk membuka kembali halaman Hasil lengkap dengan pembahasan.

## 7. Arsitektur

```
 Browser (static/index.html, style.css, app.js)
        │  HTTP + JSON
        ▼
 app.py  ── server HTTP + API + penilaian
   ├── bank.py   ── daftar mata pelajaran → soal.py (Matematika), soal_inggris.py (Bahasa Inggris)
   └── SQLite    ── data/latihan.db
```

### Struktur berkas

```
app.py              server & API
soal.py             pembangkit soal Matematika
soal_inggris.py     pembangkit soal Bahasa Inggris
soal_sunda.py       pembangkit soal Bahasa Sunda (kelas 1)
bank.py             daftar mata pelajaran; penghubung app.py ke pembangkit soal
static/index.html   kerangka halaman
static/style.css    tampilan
static/app.js       logika layar
tests/              uji otomatis (unittest)
data/latihan.db     dibuat otomatis saat pertama dijalankan
```

### API

| Metode | Alamat | Fungsi |
|---|---|---|
| GET | `/api/topik` | daftar mata pelajaran beserta topiknya |
| POST | `/api/latihan` | mulai latihan baru `{nama, topik}` → 20 soal **tanpa kunci** |
| GET | `/api/latihan/{id}` | latihan berjalan (soal saja) atau latihan selesai (lengkap dengan kunci & pembahasan) |
| POST | `/api/latihan/{id}/batal` | batalkan latihan yang belum dikumpulkan; datanya dihapus dan tidak masuk Riwayat |
| POST | `/api/latihan/{id}/jawab` | kumpulkan `{jawaban: [0-3 atau null] × 20}` → dinilai & disimpan |
| GET | `/api/riwayat` | daftar latihan yang sudah selesai + ringkasan |

Latihan yang sudah dikumpulkan tidak bisa dikumpulkan ulang (nilai tidak bisa diubah).

### Model data — tabel `latihan`

| Kolom | Tipe | Keterangan |
|---|---|---|
| `id` | INTEGER PK | nomor latihan |
| `nama` | TEXT | nama siswa |
| `topik` | TEXT | kode topik |
| `dibuat` | TEXT | waktu mulai (ISO) |
| `selesai` | TEXT, boleh kosong | waktu dikumpulkan; kosong = belum selesai |
| `soal` | TEXT (JSON) | 20 soal lengkap dengan pilihan, kunci, pembahasan, dan gambar (bila ada) |
| `jawaban` | TEXT (JSON) | jawaban siswa |
| `benar` | INTEGER | jumlah benar |
| `nilai` | INTEGER | 0–100 |
| `durasi` | INTEGER | lama pengerjaan (detik) |

## 8. Menjalankan

```bash
python3 app.py              # buka http://localhost:8000
python3 app.py --port 9000  # port lain
python3 app.py --host 0.0.0.0   # agar bisa diakses perangkat lain di jaringan yang sama
```
