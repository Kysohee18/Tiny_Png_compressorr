import os
import sys
from PIL import Image
from tqdm import tqdm
import time

# Konfigurasi Code
INPUT_FOLDER = 'input_images'
OUTPUT_FOLDER = 'output_images'
QUALITY = 60  # Kualitas output (0-100). 60 mirip dengan kompresi TinyPNG.
MAX_WIDTH = 2048 # Opsional: Resize jika foto terlalu besar (HD)

def compress_images(max_size_kb):
    # Cek folder input
    if not os.path.exists(INPUT_FOLDER):
        print(f"Error: Folder '{INPUT_FOLDER}' tidak ditemukan.")
        print(f"Silakan buat folder '{INPUT_FOLDER}' dan masukkan foto-foto anda ke dalamnya.")
        os.makedirs(INPUT_FOLDER)
        return

    # Buat folder output jika belum ada
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # Ambil list file gambar secara rekursif (termasuk subfolder)
    files_to_process = []
    for root, dirs, files in os.walk(INPUT_FOLDER):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                full_path = os.path.join(root, file)
                files_to_process.append(full_path)

    total_files = len(files_to_process)

    if total_files == 0:
        print(f"Tidak ada foto ditemukan di folder '{INPUT_FOLDER}' dan subfoldernya.")
        return

    print(f"Ditemukan {total_files} foto. Memulai kompresi (Target: {max_size_kb}KB)...")
    print("-" * 50)

    # Mulai proses dengan Progress Bar (tqdm)
    start_time = time.time()
    
    for input_path in tqdm(files_to_process, desc="Proses", unit="foto"):
        # Hitung path relatif untuk mempertahankan struktur folder
        rel_path = os.path.relpath(input_path, INPUT_FOLDER)
        final_output_path = os.path.join(OUTPUT_FOLDER, rel_path)
        
        # Buat folder tujuan jika belum ada
        os.makedirs(os.path.dirname(final_output_path), exist_ok=True)

        try:
            with Image.open(input_path) as img:
                # Dapatkan format asli agar output sesuai input
                original_format = img.format if img.format else "JPEG"
                target_size_bytes = max_size_kb * 1024  # Target max based on input

                # --- 1. RESIZE LOGIC (Universal) ---
                if img.width > MAX_WIDTH:
                   ratio = MAX_WIDTH / float(img.width)
                   new_height = int((float(img.height) * float(ratio)))
                   img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
                
                # --- 2. JPEG PROCESSING ---
                if original_format == "JPEG":
                    # JPEG wajib RGB
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                        
                    # Mulai dari kualitas SANGAT TINGGI (95) agar ukuran maksimal
                    current_quality = 95
                    while True:
                        img.save(final_output_path, "JPEG", optimize=True, quality=current_quality)
                        if os.path.getsize(final_output_path) <= target_size_bytes or current_quality <= 15:
                            break
                        current_quality -= 5
                
                # --- 3. PNG PROCESSING (Preserve Transparency) ---
                elif original_format == "PNG":
                    # Coba simpan langsung dengan optimasi
                    img.save(final_output_path, "PNG", optimize=True)
                    
                    # Jika masih terlalu besar, baru kita lakukan kuantisasi
                    if os.path.getsize(final_output_path) > target_size_bytes:
                        colors = 256
                        while True:
                            try:
                                q_img = img.quantize(colors=colors, method=2)
                            except:
                                q_img = img.quantize(colors=colors)

                            q_img.save(final_output_path, "PNG", optimize=True)
                            
                            if os.path.getsize(final_output_path) <= target_size_bytes or colors <= 32:
                                break
                            colors = int(colors * 0.8) # Kurangi warna bertahap
                            
                # --- 4. OTHER FORMATS ---
                else:
                    img.save(final_output_path, original_format)
                
        except Exception as e:
            print(f"\nGagal memproses {rel_path}: {e}")

    end_time = time.time()
    duration = end_time - start_time
    
    print("-" * 50)
    print(f"Selesai! {total_files} foto telah dikompres.")
    print(f"Waktu proses: {duration:.2f} detik")
    print(f"Cek hasil di folder '{OUTPUT_FOLDER}'.")

if __name__ == "__main__":
    print("=== TinyPNG Local Compressor ===")
    print("Pilih Model Kompresi:")
    print("1. Standard (Max 600KB) - Kualitas Tinggi")
    print("2. Lite (Max 300KB) - Ukuran Kecil")
    
    while True:
        try:
            choice = input("Masukkan pilihan (1/2) [Default: 1]: ").strip()
            if choice == '1' or choice == '':
                limit = 600
                break
            elif choice == '2':
                limit = 300
                break
            else:
                print("Pilihan tidak valid. Silakan ketik 1 atau 2.")
        except KeyboardInterrupt:
            print("\nProgram dibatalkan.")
            sys.exit()

    compress_images(limit)
