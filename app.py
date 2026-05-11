import streamlit as st

from ui.theme import inject_glass_theme, kpi

st.set_page_config(
    page_title="Deteksi Dini DM Tipe 2 (CBR)",
    page_icon="🩺",
    layout="wide",
)

inject_glass_theme()

st.markdown(
    """
    <div style="margin-bottom:.2rem">
      <div style="font-size:1.7rem;font-weight:820;letter-spacing:-.02em;color:rgba(255,255,255,.95);">
        Sistem Deteksi Dini Diabetes Mellitus Tipe 2
      </div>
      <div style="color:rgba(255,255,255,.72);margin-top:.25rem;">
        Berbasis <b>Case-Based Reasoning</b> (Retrieve–Reuse–Revise–Retain) untuk mendukung skrining awal di Faskes 1.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

col_a, col_b = st.columns([1.35, 1], gap="large")

with col_a:
    st.markdown('<div class="glass card">', unsafe_allow_html=True)
    st.markdown("### Mulai cepat", help=None)
    st.markdown(
        """
        - Buka menu **Deteksi** untuk input data pasien (8 atribut).
        - Sistem akan menampilkan estimasi risiko (hasil CBR/ML).
        - User melakukan **Revise** (konfirmasi klinis).
        - Sistem menyimpan ke basis kasus (**Retain**).
        """.strip()
    )
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### Catatan implementasi")
    st.markdown(
        """
        Aplikasi ini disiapkan untuk Streamlit Cloud.
        Saat ini UI sudah lengkap; modul prediksi CBR/ML akan kamu lampirkan dan nanti kita integrasikan.
        """.strip()
    )
    st.markdown("</div>", unsafe_allow_html=True)

with col_b:
    kpi("Peran pengguna", "Petugas Faskes 1")
    st.markdown('<div style="height:.65rem"></div>', unsafe_allow_html=True)
    kpi("Metode", "CBR + Weighted Euclidean Distance")
    st.markdown('<div style="height:.65rem"></div>', unsafe_allow_html=True)
    kpi("Alur", "Input → Validasi → Normalisasi → Retrieve → Voting → Revise → Retain")

st.info("Gunakan navigasi di sidebar (kiri) untuk masuk ke halaman **Deteksi**.")
