from pathlib import Path

import pandas as pd
import streamlit as st


CASE_BASE_PATH = Path("data/case_base.csv")


def load_case_base() -> pd.DataFrame:
    if not CASE_BASE_PATH.exists():
        return pd.DataFrame()
    return pd.read_csv(CASE_BASE_PATH)


st.title("Basis Kasus (Riwayat Retain)")
st.caption("Halaman ini menampilkan kasus-kasus yang sudah disimpan setelah validasi (Revise + Retain).")

df = load_case_base()

if df.empty:
    st.info("Belum ada data. Silakan lakukan deteksi di halaman **Deteksi**, lalu klik **Simpan ke Basis Kasus**.")
else:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Jumlah kasus", len(df))
    with c2:
        if "validated_outcome" in df.columns:
            st.metric("Outcome=1 (validasi)", int((df["validated_outcome"] == 1).sum()))
    with c3:
        if "validated_outcome" in df.columns:
            st.metric("Outcome=0 (validasi)", int((df["validated_outcome"] == 0).sum()))

    st.write("")
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.download_button(
        "Unduh CSV basis kasus",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="case_base.csv",
        mime="text/csv",
        use_container_width=True,
    )
