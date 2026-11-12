# 🧮 Pintar Matematika

Repositori ini berisi dua program belajar matematika:

1. **Pintar Matematika** — aplikasi web latihan soal matematika SD kelas 4 (di bawah ini).
2. **Math Guru AI** — asisten tanya-jawab matematika di terminal ([lihat di bawah](#-math-guru-ai)).

## Aplikasi Latihan Soal SD Kelas 4

- 20 soal pilihan ganda yang selalu baru setiap kali latihan
- 11 pilihan topik: penjumlahan & pengurangan, perkalian, pembagian, pecahan, KPK & FPB,
  nilai tempat & pembulatan, keliling & luas, bangun datar, pengukuran, soal cerita, dan campuran
- Nilai langsung dihitung, lengkap dengan pembahasan tiap soal
- Semua hasil latihan tercatat dan bisa dilihat di halaman Riwayat

### Menjalankan

Hanya butuh Python 3.9+ — tidak ada yang perlu di-`pip install`.

```bash
python3 app.py
```

Lalu buka <http://localhost:8000> di browser.

| Pilihan | Kegunaan |
|---|---|
| `--port 9000` | memakai port lain |
| `--host 0.0.0.0` | agar bisa dibuka dari HP/komputer lain di jaringan yang sama |
| `--db lokasi/berkas.db` | lokasi penyimpanan hasil latihan (bawaan: `data/latihan.db`) |

### Uji otomatis

```bash
python3 -m unittest discover -s tests
```

Rancangan lengkap (layar, API, model data) ada di [docs/DESAIN.md](docs/DESAIN.md).

---

# 🎯 Math Guru AI

Asisten pembelajaran matematika pintar yang ditenagai oleh Google Gemini AI. Dirancang untuk membantu siswa memahami konsep matematika dengan cara yang interaktif dan menyenangkan.

## ✨ Fitur Utama
- 🤖 Berbasis Google Gemini AI (upgrade dari Ollama + Qwen)
- 🎓 Penjelasan step-by-step yang mudah dipahami
- 📝 Contoh soal yang relevan
- 💡 Pendekatan pembelajaran yang adaptif
- 🌐 Dukungan Bahasa Indonesia
- ⚡ Respons cepat dan akurat
- 🔄 Fitur retry otomatis untuk koneksi yang stabil
- 🧹 Fitur clear screen untuk antarmuka yang bersih

## 🚀 Perbandingan dengan Versi Sebelumnya

Sebelumnya:
- Menggunakan Ollama + Qwen
- Memerlukan server lokal
- Setup yang lebih kompleks

Sekarang:
- Menggunakan Google Gemini
- Cloud-based, tanpa perlu server lokal
- Setup lebih sederhana
- Performa lebih stabil

## 🛠️ Cara Menggunakan

### Prasyarat
```bash
pip install google-generativeai
pip install langchain-core
pip install tenacity
```

### Konfigurasi
1. Dapatkan API key dari [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Ganti `YOUR_API_KEY` dengan API key Anda di file `math_guru.py`:
```python
GOOGLE_API_KEY = "YOUR_API_KEY"
```

### Menjalankan Aplikasi
1. Download atau clone repository ini
```bash
git clone https://github.com/username/math-guru-ai.git
cd math-guru-ai
```

2. Jalankan aplikasi
```bash
python3 math_guru.py
```

## 📖 Penggunaan

Setelah aplikasi berjalan:
1. Ketik pertanyaan matematika Anda dalam Bahasa Indonesia
2. Tunggu respons dari AI
3. Gunakan perintah khusus:
   - Ketik `clear` untuk membersihkan layar
   - Ketik `keluar` untuk mengakhiri sesi

## 🤝 Kontribusi

Kontribusi selalu diterima! Cara berkontribusi:
1. Fork repository ini
2. Buat branch baru (`git checkout -b fitur-baru`)
3. Commit perubahan Anda (`git commit -m 'Menambahkan fitur baru'`)
4. Push ke branch tersebut (`git push origin fitur-baru`)
5. Buat Pull Request

## 📝 Lisensi

Proyek ini dilisensikan di bawah MIT License - lihat file [LICENSE](LICENSE) untuk detail.

## 🙏 Kredit

- [Google Generative AI](https://ai.google.dev/)
- [LangChain](https://www.langchain.com/)
- [Tenacity](https://tenacity.readthedocs.io/)

## 📞 Dukungan

Jika Anda menemukan masalah atau memiliki pertanyaan:
1. Buat issue di repository ini
2. Hubungi kami melalui email di: kontak@classy.id
```
