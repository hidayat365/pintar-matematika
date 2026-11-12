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
| `pengukuran` | Pengukuran | satuan panjang, berat, waktu, volume, kuantitas (lusin, kodi, rim) |
| `soal-cerita` | Soal Cerita | soal cerita satu dan dua langkah, termasuk uang |
| `campuran` | Campuran Semua Topik | 20 soal diambil merata dari semua topik di atas |

### Aturan pembuatan soal

- Satu latihan = **20 soal**; teks soal dalam satu latihan tidak boleh ada yang sama.
- Angka diacak setiap kali, sehingga latihan berikutnya hampir pasti berbeda.
- Setiap soal punya **4 pilihan yang berbeda**, tepat satu yang benar. Pilihan
  pengecoh dibuat dari kesalahan yang umum (mis. luas tertukar dengan keliling).
- Setiap soal punya **pembahasan singkat** yang ditampilkan setelah dinilai.
- Bilangan ditulis dengan gaya Indonesia: `12.500`, desimal `0,25`.

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
│  Nama kamu: [______________]                         │
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
   ├── soal.py   ── pembangkit soal per topik
   └── SQLite    ── data/latihan.db
```

### Struktur berkas

```
app.py              server & API
soal.py             pembangkit soal
static/index.html   kerangka halaman
static/style.css    tampilan
static/app.js       logika layar
tests/              uji otomatis (unittest)
data/latihan.db     dibuat otomatis saat pertama dijalankan
```

### API

| Metode | Alamat | Fungsi |
|---|---|---|
| GET | `/api/topik` | daftar topik |
| POST | `/api/latihan` | mulai latihan baru `{nama, topik}` → 20 soal **tanpa kunci** |
| GET | `/api/latihan/{id}` | latihan berjalan (soal saja) atau latihan selesai (lengkap dengan kunci & pembahasan) |
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
| `soal` | TEXT (JSON) | 20 soal lengkap dengan pilihan, kunci, pembahasan |
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
