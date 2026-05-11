import streamlit as st


st.title("Tentang Aplikasi")
st.markdown(
    r"""
    Aplikasi ini dirancang untuk kebutuhan skripsi:
    **Sistem deteksi dini Diabetes Mellitus Tipe 2 berbasis Case-Based Reasoning (CBR)**.

    ### Alur sistem (ringkas)
    - **Input**: petugas Faskes 1 mengisi 8 atribut (numerik).
    - **Validasi**: cek kelengkapan & tipe data.
    - **Normalisasi**: gunakan parameter min/max dari basis kasus (pretrained).
    - **Retrieve**: hitung kemiripan dengan **Weighted Euclidean Distance** berbobot (MultiSURF).
    - **Reuse**: ambil \(k\) kasus terdekat, voting mayoritas `Outcome`.
    - **Revise**: user memvalidasi hasil sesuai pertimbangan klinis.
    - **Retain**: simpan kasus + hasil validasi ke basis kasus.

    ### Catatan integrasi model
    File model CBR/ML kamu nanti akan dihubungkan ke halaman **Deteksi** pada fungsi `predict_with_user_model()`.
    """.strip()
)
