# Music Playlist

**Tagline:** Playlist yang pas dengan durasi kegiatanmu.

Aplikasi web berbasis Python dan Streamlit untuk menyusun playlist berdasarkan durasi kegiatan. Data lagu diambil dari iTunes Search API. Gemini AI digunakan untuk memberi nama playlist, menyusun urutan lagu, dan menjelaskan alasan penyusunannya.

## 1. Fitur

- Input durasi kegiatan (10–360 menit).
- Pilihan kegiatan, genre, dan artis.
- Mengambil data lagu dari iTunes Search API.
- Memilih lagu dengan algoritma greedy agar total durasi mendekati target.
- Menggunakan List dan Dictionary untuk menyimpan data lagu.
- Menggunakan Pandas DataFrame untuk mengolah dan mengurutkan data.
- Gemini AI untuk nama, urutan, dan alasan playlist.
- Dua visualisasi Matplotlib: durasi setiap lagu dan akumulasi durasi.
- Ekspor CSV, Excel, dan JSON.

## 2. Persiapan

Pastikan Python sudah terpasang. Buka terminal di folder project, lalu jalankan:

```bash
python -m venv .venv
```

Aktifkan virtual environment:

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows CMD**
```cmd
.venv\Scripts\activate
```

Install library:

```bash
pip install -r requirements.txt
```

## 3. Menjalankan aplikasi

```bash
streamlit run app.py
```

Aplikasi akan terbuka di browser pada alamat:

```text
http://localhost:8501
```

## 4. Mengaktifkan Gemini AI

Buat API key Gemini melalui Google AI Studio. Simpan key di file:

`.streamlit/secrets.toml`

Isi file:

```toml
GEMINI_API_KEY = "MASUKKAN_API_KEY_KAMU"
```

Jangan mengunggah `secrets.toml` ke GitHub. File ini sudah masuk daftar `.gitignore`.

Alternatif melalui environment variable di PowerShell:

```powershell
$env:GEMINI_API_KEY="MASUKKAN_API_KEY_KAMU"
streamlit run app.py
```

Tanpa API key, fitur pencarian lagu, pemilihan durasi, visualisasi, dan ekspor tetap berjalan. Nama dan alasan playlist menggunakan rekomendasi dasar, bukan hasil Gemini.

## 5. Struktur folder

```text
music_playlist_project/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── secrets.toml.example
```

## 6. Struktur data dan algoritma

### Struktur data
- **List:** menyimpan kumpulan lagu hasil pencarian dan playlist terpilih.
- **Dictionary:** menyimpan atribut setiap lagu seperti judul, artis, genre, durasi, tautan, dan preview.
- **Pandas DataFrame:** mengubah kumpulan lagu menjadi tabel agar dapat difilter, diurutkan, ditampilkan, dan diekspor.

### Algoritma greedy
1. Data lagu diurutkan berdasarkan durasi dari yang terpanjang.
2. Program menghitung sisa waktu dari target pengguna.
3. Lagu dimasukkan jika durasinya tidak melebihi sisa waktu.
4. Proses berlanjut sampai tidak ada lagu yang dapat ditambahkan atau target tercapai.
5. Jika tersisa waktu, program memeriksa satu lagu yang paling mendekati sisa waktu dan menambahkannya jika membuat total lebih dekat ke target.

Algoritma ini merupakan pendekatan greedy, sehingga hasilnya mendekati target tetapi tidak selalu merupakan kombinasi matematis yang paling optimal.

## 7. Alur kerja aplikasi

1. Pengguna mengisi durasi, kegiatan, genre, dan artis.
2. Program mengirim HTTP GET request ke iTunes Search API.
3. Response JSON diubah menjadi List dan Dictionary.
4. Data lagu diolah dengan Pandas.
5. Algoritma greedy memilih lagu sesuai target durasi.
6. Data playlist dikirim ke Gemini AI.
7. Gemini mengembalikan nama playlist, urutan ID lagu, dan alasan.
8. Program memvalidasi ID dari AI agar hanya lagu hasil iTunes yang digunakan.
9. Streamlit menampilkan daftar lagu, metrik, dan dua grafik.
10. Pengguna mengunduh hasil dalam CSV, Excel, atau JSON.

## 8. Kesesuaian dengan persyaratan Project Besar

| Persyaratan | Penerapan |
|---|---|
| Data input | Durasi, kegiatan, genre, artis |
| Data eksternal | iTunes Search API |
| Struktur data | List dan Dictionary |
| Algoritma | Greedy selection dan sorting |
| Pengolahan tabular | Pandas DataFrame |
| Visualisasi minimal 2 | Bar chart dan line chart |
| Ekspor | CSV, Excel, JSON |
| AI API | Gemini generateContent |
| Aplikasi web | Streamlit |

## 9. Catatan pengembangan

- iTunes menyediakan data lagu, metadata, tautan, dan preview jika tersedia. Aplikasi ini tidak mengunduh file musik penuh.
- Hasil pencarian bergantung pada ketersediaan katalog iTunes.
- Gemini memerlukan API key dan koneksi internet.
- Jangan memasukkan API key langsung ke dalam `app.py` atau repository publik.
- Untuk presentasi, jelaskan bahwa greedy memilih lagu yang paling panjang tetapi masih muat pada sisa waktu. Karena itu hasilnya bisa mendekati, bukan selalu tepat sama dengan durasi target.


## Struktur File

- `app.py` — halaman utama dan tampilan Streamlit.
- `style.css` — pengaturan desain dan warna aplikasi.
- `itunes_api.py` — mengambil data lagu dari iTunes Search API.
- `playlist.py` — algoritma pemilihan lagu berdasarkan durasi.
- `gemini_ai.py` — integrasi Gemini untuk nama, urutan, dan alasan playlist.
- `exports.py` — membuat DataFrame serta ekspor CSV, Excel, dan JSON.
- `.streamlit/secrets.toml` — tempat menyimpan API key Gemini (opsional).

Pastikan semua file Python dan `style.css` berada dalam folder proyek yang sama. Jalankan aplikasi dengan `streamlit run app.py`.
