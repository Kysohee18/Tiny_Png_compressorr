# TinyPNG Local Compressor

Aplikasi Python sederhana untuk mengompres foto secara lokal mirip dengan TinyPNG, namun dengan kontrol lebih fleksibel. Program ini sekarang mendukung dua mode kompresi untuk menyesuaikan kebutuhan ukuran file anda.

## Fitur

*   **Offline & Lokal**: Tidak perlu upload ke internet, privasi aman.
*   **Dua Model Kompresi**:
    1.  **Standard (Max 600KB)**: Menjaga kualitas visual setinggi mungkin dengan batas 600KB. Cocok untuk website portfolio atau galeri berkualitas tinggi.
    2.  **Lite (Max 300KB)**: Kompresi lebih agresif untuk ukuran file yang sangat kecil. Cocok untuk thumbnail, aplikasi mobile, atau website dengan traffic tinggi.
*   **Resize Otomatis**: Foto yang lebarnya lebih dari 2048px akan di-resize otomatis untuk menghemat size.
*   **Dukungan Format**: Mendukung JPG, JPEG, dan PNG (transparansi dijaga).
*   **Struktur Folder**: Mempertahankan struktur folder asli dari folder `input_images`.

## Cara Instalasi

1.  Pastikan anda sudah menginstal **Python 3**.
2.  Install library yang dibutuhkan dengan menjalankan perintah berikut di terminal/command prompt:

    ```bash
    pip install -r requirements.txt
    ```

    *Jika belum ada file requirements.txt, anda bisa install manual:*
    ```bash
    pip install Pillow tqdm
    ```

## Cara Penggunaan

1.  **Siapkan Foto**: Buat folder bernama `input_images` (jika belum ada) dan masukkan semua foto yang ingin dikompres ke dalamnya. Anda bisa menaruh foto di dalam subfolder juga.
2.  **Jalankan Script**: Buka terminal di lokasi folder ini, lalu jalankan:

    ```bash
    python compressor.py
    ```
3.  **Pilih Mode**: Program akan meminta anda memilih model kompresi:
    *   Ketik `1` atau tekan Enter untuk mode **Standard (600KB)**.
    *   Ketik `2` untuk mode **Lite (300KB)**.
4.  **Tunggu Proses**: Proses kompresi akan berjalan dengan progress bar.
5.  **Cek Hasil**: Foto yang sudah dikompres akan muncul di folder `output_images`.

## Troubleshooting

*   Jika foto tidak terkompresi sesuai target (masih di atas 300KB/600KB), itu berarti foto tersebut memiliki detail yang sangat kompleks. Script sudah berusaha menurunkan kualitas hingga batas minimal (Quality 15) atau mengurangi warna (untuk PNG).
*   Pastikan nama file foto tidak menggunakan karakter khusus yang aneh jika mengalami error path.
