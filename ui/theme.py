from __future__ import annotations
import streamlit as st

def inject_glass_theme() -> None:
    st.markdown(
        """
        <style>
          :root {
            --bg0: #050b1f;
            --bg1: #0b1b3a;
            --bg2: #0a3a44;
            --glass: rgba(255, 255, 255, .12);
            --glass2: rgba(255, 255, 255, .08);
            --stroke: rgba(255, 255, 255, .18);
            --text: #ffffff;
            --muted: rgba(255, 255, 255, 0.8);
            --blur: blur(25px);
            --accent: #2dd4bf;
          }

          /* 1. MENGHILANGKAN HEADER PUTIH & DEKORASI ATAS */
          header[data-testid="stHeader"] {
            background: transparent !important;
          }
          
          [data-testid="stDecoration"] {
            display: none;
          }

          /* 2. BACKGROUND UTAMA */
          .stApp {
            background:
              radial-gradient(1200px 650px at 15% 0%, rgba(45, 212, 191, .20), rgba(0,0,0,0) 60%),
              radial-gradient(950px 650px at 85% 10%, rgba(34, 197, 94, .16), rgba(0,0,0,0) 55%),
              linear-gradient(135deg, var(--bg0), var(--bg1) 45%, var(--bg2));
            color: var(--text);
          }

          /* 3. PERBAIKAN SIDEBAR (TEKS & VISUAL) */
          section[data-testid="stSidebar"] {
            width: 300px !important;
          }

          section[data-testid="stSidebar"] > div:first-child {
            /* Menggunakan overlay gelap tipis agar teks putih kontras */
            background: linear-gradient(180deg, rgba(0,0,0,0.4), rgba(0,0,0,0.2)) !important;
            backdrop-filter: var(--blur) !important;
            -webkit-backdrop-filter: var(--blur) !important;
            border-right: 1px solid var(--stroke);
          }

          /* Memaksa semua teks di sidebar berwarna putih terang */
          section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
          section[data-testid="stSidebar"] span,
          section[data-testid="stSidebar"] label,
          section[data-testid="stSidebar"] .st-emotion-cache-17l69k {
            color: #ffffff !important;
            font-weight: 600 !important;
            opacity: 1 !important;
          }

          /* Menghilangkan background putih pada area menu sidebar */
          section[data-testid="stSidebar"] .st-emotion-cache-6qob1r {
            background-color: transparent !important;
          }

          /* 4. TYPOGRAPHY & SPACING */
          .block-container { 
            padding-top: 3.5rem !important; 
            padding-bottom: 2rem; 
          }
          
          h1, h2, h3 { 
            color: white !important; 
            font-weight: 700;
            letter-spacing: -0.02em;
          }

          /* 5. GLASS CARDS & INPUTS */
          .glass {
            background: linear-gradient(180deg, var(--glass), var(--glass2));
            border: 1px solid var(--stroke);
            border-radius: 18px;
            box-shadow: 0 12px 35px rgba(0, 0, 0, .35);
            backdrop-filter: var(--blur);
            -webkit-backdrop-filter: var(--blur);
            padding: 20px;
          }

          div[data-baseweb="input"] > div {
            background: rgba(255,255,255,.08) !important;
            border: 1px solid var(--stroke) !important;
            border-radius: 12px !important;
          }
          
          input {
            color: white !important;
          }

          /* 6. BUTTON CUSTOMIZATION */
          .stButton > button {
            width: 100%;
            border-radius: 12px !important;
            transition: all 0.3s ease;
          }

          .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #2dd4bf, #22c55e) !important;
            color: #050b1f !important;
            font-weight: bold !important;
            border: none !important;
            box-shadow: 0 10px 20px rgba(45, 212, 191, 0.2);
          }
          
          .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 25px rgba(0,0,0,0.3);
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

def card_open() -> None:
    st.markdown('<div class="glass">', unsafe_allow_html=True)

def card_close() -> None:
    st.markdown("</div>", unsafe_allow_html=True)

# --- CONTOH PENGGUNAAN ---
def main():
    st.set_page_config(page_title="Deteksi DM Tipe 2", layout="wide")
    inject_glass_theme()

    # Sidebar
    with st.sidebar:
        st.title("Menu")
        st.radio("Navigasi", ["Deteksi", "Basis Kasus", "Tentang"])
        st.divider()
        st.write("Pengaturan CBR")
        st.slider("Nilai K", 1, 10, 5)

    # Main Content
    st.title("Deteksi / Prediksi Risiko DM Tipe 2")
    st.write("Masukkan data pemeriksaan pasien di bawah ini.")

    col1, col2 = st.columns(2)

    with col1:
        card_open()
        st.subheader("A. Input Data Pasien")
        c1, c2 = st.columns(2)
        with c1:
            st.number_input("Pregnancies", 0)
            st.number_input("Glucose", 0)
            st.number_input("BloodPressure", 0)
            st.number_input("SkinThickness", 0)
        with c2:
            st.number_input("Insulin", 0)
            st.number_input("BMI", 0.0)
            st.number_input("DiabetesPedigree", 0.0)
            st.number_input("Age", 0)
        
        st.button("Proses Deteksi", type="primary")
        card_close()

    with col2:
        card_open()
        st.subheader("B. Hasil Estimasi")
        st.info("Belum ada hasil. Silakan isi form di kiri.")
        card_close()

if __name__ == "__main__":
    main()