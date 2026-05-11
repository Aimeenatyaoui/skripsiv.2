# Streamlit — Deteksi Dini DM Tipe 2 (CBR)

UI Streamlit untuk skripsi: *Sistem deteksi dini Diabetes Mellitus tipe 2 berbasis Case-Based Reasoning (CBR)*.

## Cara menjalankan (lokal)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Struktur

- `app.py`: halaman beranda
- `pages/1_🧪_Deteksi.py`: form input pasien + hasil + Revise + Retain
- `pages/2_📚_Basis_Kasus.py`: melihat & unduh basis kasus tersimpan
- `pages/3_ℹ️_Tentang.py`: ringkasan alur sistem
- `data/case_base.csv`: basis kasus hasil retain (akan dibuat otomatis setelah simpan)

## Integrasi model CBR kamu

Setelah kamu lampirkan file Python model CBR-mu, kita akan mengganti fungsi `predict_with_user_model()` di `pages/1_🧪_Deteksi.py`
agar memakai:

- normalisasi min/max training
- bobot fitur MultiSURF (pretrained)
- Weighted Euclidean Distance
- penentuan \(k\) nearest + voting `Outcome`
