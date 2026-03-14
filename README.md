# Sistem Pelacakan Alumni

## Daily Project 3 – Rekayasa Kebutuhan

Aplikasi ini merupakan implementasi dari desain sistem pada **Daily Project 2**.
Sistem digunakan untuk melakukan **pelacakan perkembangan karier alumni** secara sederhana.

---

# Deskripsi Sistem

Sistem Pelacakan Alumni adalah aplikasi web yang membantu pihak kampus dalam memantau perkembangan karier alumni melalui simulasi pencarian data dari berbagai sumber publik seperti:

* LinkedIn
* Google Scholar
* Website perusahaan

Sistem ini dibuat untuk memenuhi tugas **Daily Project 3 mata kuliah Rekayasa Kebutuhan**.

---

# Fitur Aplikasi

* Login Admin
* Dashboard Statistik
* CRUD Data Alumni
* Pelacakan Alumni
* Riwayat Pelacakan
* Pencarian Alumni

---

# Teknologi yang Digunakan

| Komponen     | Teknologi    |
| ------------ | ------------ |
| Backend      | Python Flask |
| ORM          | SQLAlchemy   |
| Database     | SQLite       |
| Frontend     | HTML         |
| UI Framework | Bootstrap 5  |
| Icon         | FontAwesome  |

---

# Struktur Folder

```
sistem-pelacakan-alumni
│
├── app.py
├── database.db
│
├── templates
│   ├── layout.html
│   ├── login.html
│   ├── dashboard.html
│   ├── alumni.html
│   ├── tambah_alumni.html
│   ├── edit_alumni.html
│   ├── hasil_pelacakan.html
│   └── riwayat_pelacakan.html
│
└── README.md
```

---

# Cara Menjalankan Aplikasi

### Install Dependencies

```
pip install flask flask-sqlalchemy werkzeug
```

### Jalankan Server

```
python app.py
```

### Akses Web

```
http://127.0.0.1:5000
```

### Login Admin

```
Email    : admin@kampus.ac.id
Password : admin123
```

---

# Tabel Pengujian Sistem

Pengujian dilakukan berdasarkan kebutuhan sistem pada Daily Project 2.

| No | Fitur             | Skenario Pengujian            | Hasil                  | Status |
| -- | ----------------- | ----------------------------- | ---------------------- | ------ |
| 1  | Login             | Admin login dengan data benar | Login berhasil         | PASS   |
| 2  | Login             | Password salah                | Sistem menolak login   | PASS   |
| 3  | Tambah Alumni     | Mengisi data alumni           | Data tersimpan         | PASS   |
| 4  | Edit Alumni       | Mengubah data alumni          | Data berhasil diupdate | PASS   |
| 5  | Hapus Alumni      | Menghapus data alumni         | Data terhapus          | PASS   |
| 6  | Lacak Alumni      | Klik tombol lacak             | Hasil pelacakan muncul | PASS   |
| 7  | Simpan Pelacakan  | Menyimpan hasil pelacakan     | Data tersimpan         | PASS   |
| 8  | Pencarian Alumni  | Mencari berdasarkan nama      | Data difilter          | PASS   |
| 9  | Riwayat Pelacakan | Melihat data pelacakan        | Data tampil            | PASS   |

---

# Kesimpulan

Sistem Pelacakan Alumni berhasil diimplementasikan sesuai dengan desain pada **Daily Project 2**.
Semua fitur utama sistem telah diuji dan berjalan dengan baik.

Aplikasi ini dapat digunakan sebagai **prototype sistem tracer study alumni**.

---

# Author

Akhsan Makki
NIM : 202210370311241
Universitas Muhammadiyah Malang
