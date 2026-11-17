# Havist Traveller — Dashboard Management

Web resmi Havist Traveller: satu halaman aplikasi (single-page app) yang menghasilkan dashboard manajemen tour & travel, dengan 4 area akses:

- **Umum** — halaman publik (profil perusahaan, destinasi, testimoni)
- **Sales** — pencatatan prospek, ACC klien, pembayaran DP/pelunasan
- **Tour Leader & Media** — jadwal trip, crew, dokumentasi
- **Management** — Dashboard, Harga & Katalog, Keuangan (laba, arus kas, piutang, DP vendor), Jadwal Trip, Crew, Laporan

## Struktur project

| File / folder       | Isi |
|----------------------|-----|
| `app.py`             | **Sumber kebenaran (source of truth).** Script Python yang men-generate `index.html` dari template + data. |
| `data.json`          | Data master trip, klien, vendor, crew, pembayaran, dsb. |
| `catalog.json`       | Katalog harga & destinasi. |
| `logo_b64.txt`       | Logo Havist Traveller dalam base64, disisipkan langsung ke `index.html`. |
| `index.html`         | **Build output.** Hasil generate dari `app.py` — inilah yang dipublikasikan sebagai halaman web (satu file HTML mandiri, tanpa dependency CDN untuk fitur export). |
| `tests/`             | Suite regresi (Node.js + jsdom) yang memvalidasi logika kalkulasi, export, dan setiap modul sebelum publish. |

## Build ulang

```bash
python3 app.py
```

Ini membaca `data.json`, `catalog.json`, dan `logo_b64.txt`, lalu menulis ulang `index.html`.

## Menjalankan test

```bash
node tests/tfull.js
node tests/tcalc.js
# dst — setiap file tests/t*.js adalah suite independen
```

## Fitur export

Export Excel (`.xlsx`) dibuat sendiri tanpa library eksternal (writer OOXML/zip minimal, murni JavaScript) dan diunduh lewat kanal `downloads` resmi milik runtime artifact Claude (`claude.use('downloads').save(...)`) — bukan trik `<a download>`, karena halaman berjalan di sandbox yang mengabaikan unduhan lewat script biasa.

## Catatan

Halaman `index.html` ini juga dipublikasikan sebagai Claude Artifact (publik) untuk dipakai tim sehari-hari. Repo ini adalah salinan/arsip kode sumbernya.
