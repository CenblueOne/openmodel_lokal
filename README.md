# OpenModel.ai Chat

Aplikasi chat berbasis Gradio yang memanfaatkan API OpenModel.ai untuk mengakses berbagai model AI (DeepSeek, Claude, Qwen, Gemini, dan lain-lain) secara gratis. Mendukung streaming respons, pemilihan model dinamis, preset system prompt, serta penyimpanan riwayat chat.

## ✨ Fitur

- **Streaming real-time** – Respons model ditampilkan langsung saat dihasilkan.
- **Pilihan model fleksibel** – Dropdown dengan daftar model populer, bisa juga input manual.
- **Preset system prompt** – 5 preset siap pakai (Asisten Umum, Coding, Analis Saham, AHSP Konstruksi, Penulis Kreatif).
- **Pengaturan parameter** – Max tokens (256–8192) dan temperature (0.0–1.0) dapat diubah.
- **Riwayat chat** – Simpan sebagai JSON atau ekspor sebagai file teks.
- **Tema kustom** – Tampilan modern dengan warna biru (primary) dan slate (neutral).

## 📋 Daftar Model Tersedia

| Model ID | Deskripsi |
|----------|-----------|
| `deepseek-v4-flash` | DeepSeek V4 Flash (cepat) |
| `deepseek-v4-pro` | DeepSeek V4 Pro (akurat) |
| `claude-haiku-4-5-20251001` | Claude Haiku 4.5 |
| `claude-sonnet-4-6` | Claude Sonnet 4.6 |
| `qwen3.6-flash` | Qwen 3.6 Flash |
| `qwen3.5-plus` | Qwen 3.5 Plus |
| `glm-5.2` | GLM 5.2 |
| `gemini-3.1-flash-lite-preview` | Gemini 3.1 Flash Lite (pratinjau) |
| `mimo-v2-flash` | Mimo V2 Flash |
| `kimi-k2.5` | Kimi K2.5 |

> **Catatan:** Daftar model dapat berubah. Lihat [halaman pricing OpenModel.ai](https://openmodel.ai/model-pricing) untuk model terbaru.

## 🔧 Prasyarat

- Python 3.10+
- Akun OpenModel.ai (gratis) dan API key

## 📦 Instalasi

1. **Clone repositori** (atau salin file `app.py` ke direktori proyek).

2. **Buat virtual environment** (disarankan):
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Install dependensi**:
   ```bash
   pip install -r requirements.txt
   ```

   Atau install manual:
   ```bash
   pip install gradio anthropic python-dotenv
   ```

4. **Buat file `.env`** di direktori yang sama dengan script, isi:
   ```
   OPENMODEL_API_KEY=your_api_key_here
   ```
   Ganti `your_api_key_here` dengan API key dari [OpenModel.ai](https://openmodel.ai).

## 🚀 Penggunaan

Jalankan script:
```bash
python openmodel_lokal.py
```

Aplikasi akan terbuka di browser secara otomatis pada `http://127.0.0.1:7860`.

### Cara menggunakan antarmuka:

1. **Panel kiri – Pengaturan**
   - Pilih **Model** dari dropdown, atau ketik manual.
   - Atur **Max Tokens** (panjang respons maksimal) dan **Temperature** (kreativitas).
   - Pilih **Preset** untuk mengisi system prompt secara otomatis.
   - Edit **System Prompt** secara manual jika perlu.

2. **Panel kanan – Chat**
   - Ketik pesan di kotak input lalu tekan Enter.
   - Respons akan muncul secara streaming.
   - Tombol **🗑️ Clear Chat** untuk menghapus percakapan.

3. **Tombol History**
   - **💾 Save JSON** – menyimpan riwayat chat ke file `.json`.
   - **📤 Export .txt** – mengekspor chat ke file teks biasa.

## ⚙️ Konfigurasi Lanjutan

### Mengubah port atau host

Di bagian bawah script, Anda bisa mengganti parameter `server_name` dan `server_port`:
```python
demo.launch(
    server_name="0.0.0.0",   # agar bisa diakses dari jaringan lain
    server_port=7860,
    inbrowser=False,
    theme=custom_theme
)
```

### Menambahkan preset sendiri

Edit dictionary `PRESETS` di dalam script:
```python
PRESETS = {
    "Nama Preset": "System prompt yang diinginkan",
    ...
}
```

### Mengubah tema

`custom_theme` menggunakan `gr.themes.Soft`. Anda bisa mengganti warna primer, sekunder, atau properti lainnya. Lihat [dokumentasi Gradio Themes](https://www.gradio.app/guides/theming-guide).

## 🧾 Struktur File

```
openmodel-chat/
├── app.py              # Script utama aplikasi
├── .env                # API key (jangan di-commit)
├── requirements.txt    # Daftar dependensi
└── README.md
```

## 🐛 Troubleshooting

- **Error `OPENMODEL_API_KEY not set`** – Pastikan file `.env` ada dan berisi API key yang benar.
- **Model tidak muncul di dropdown** – Model mungkin sudah tidak tersedia. Coba input manual dengan ID model yang valid.
- **Streaming lambat** – Coba ganti model ke `deepseek-v4-flash` (lebih cepat).

## 📄 Lisensi

Proyek ini bersifat open-source di bawah [MIT License](LICENSE).

---

> **Powered by OpenModel.ai • Anthropic SDK • Gradio 6**
