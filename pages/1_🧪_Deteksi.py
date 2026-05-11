from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import streamlit as st

from cbr.engine import ZERO_AS_MISSING, build_artifacts_from_case_base, load_case_base_df, predict_cbr
from ui.theme import card_close, card_open, inject_glass_theme


CASE_BASE_PATH = Path("data/case_base.csv")
# Fallback basis kasus awal (dataset dari GitHub). Kalau repo kamu pakai branch `master`,
# otomatis akan dicoba juga.
CASE_BASE_SEED_URLS = [
    "https://raw.githubusercontent.com/aimeenatyaoui/SKRIPSI/main/SKRIPSI/data.xlsx",
    "https://raw.githubusercontent.com/aimeenatyaoui/SKRIPSI/master/SKRIPSI/data.xlsx",
]


@dataclass(frozen=True)
class PatientInput:
    Pregnancies: float
    Glucose: float
    BloodPressure: float
    SkinThickness: float
    Insulin: float
    BMI: float
    DiabetesPedigreeFunction: float
    Age: float


def load_case_base() -> pd.DataFrame:
    if not CASE_BASE_PATH.exists():
        return pd.DataFrame(
            columns=[
                "timestamp",
                "Pregnancies",
                "Glucose",
                "BloodPressure",
                "SkinThickness",
                "Insulin",
                "BMI",
                "DiabetesPedigreeFunction",
                "Age",
                "predicted_outcome",
                "validated_outcome",
                "validation_note",
            ]
        )
    return pd.read_csv(CASE_BASE_PATH)


def retain_case(row: dict[str, Any]) -> None:
    CASE_BASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    df = load_case_base()
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(CASE_BASE_PATH, index=False)


def validate_input(pi: PatientInput) -> list[str]:
    errors: list[str] = []
    d = asdict(pi)
    for k, v in d.items():
        if v is None or (isinstance(v, float) and (np.isnan(v) or np.isinf(v))):
            errors.append(f"Atribut **{k}** wajib diisi (angka valid).")

    # Meniru cleaning di eksperimen: 0 pada kolom tertentu dianggap missing.
    for k in ZERO_AS_MISSING:
        if k in d and float(d[k]) == 0.0:
            errors.append(
                f"Atribut **{k}** tidak boleh 0 (pada dataset training, 0 dianggap missing). "
                "Mohon isi nilai pemeriksaan sebenarnya."
            )
    return errors


def predict_with_user_model(pi: PatientInput) -> dict[str, Any]:
    # Basis kasus untuk retrieve:
    # 1) prioritas: `data/case_base.csv` (hasil retain)
    # 2) fallback: dataset Excel dari GitHub (raw)
    df = load_case_base_df(CASE_BASE_PATH)
    source = "data/case_base.csv"
    if df.empty:
        for url in CASE_BASE_SEED_URLS:
            df = load_case_base_df(url)
            if not df.empty:
                source = url
                break

    artifacts = build_artifacts_from_case_base(df)

    # Untuk sekarang, bobot MultiSURF belum dibaca dari file (kamu nanti lampirkan).
    # Kalau sudah ada bobot final (8 angka), kita load dari file dan pakai di sini.
    weights = None

    u = asdict(pi)
    k = int(st.session_state.get("k_value", 5))

    pred = predict_cbr(artifacts, u, k=k, weights=weights)
    pred["case_base_source"] = source
    pred["explain"] = (
        "CBR: normalisasi MinMax (fit dari basis kasus yang tersedia) → "
        "hitung Weighted Euclidean Distance → ambil k tetangga terdekat → voting mayoritas."
    )
    return pred


inject_glass_theme()

st.title("Deteksi / Prediksi Risiko DM Tipe 2")
st.caption("Masukkan data pemeriksaan pasien (semua atribut wajib). Setelah hasil keluar, lakukan validasi klinis (Revise) lalu simpan (Retain).")

with st.sidebar:
    st.markdown("### Pengaturan CBR")
    st.session_state["k_value"] = st.select_slider("Nilai k (tetangga terdekat)", options=[1, 3, 5, 7, 9], value=5)
    st.caption("Bobot MultiSURF akan dipakai setelah kamu lampirkan bobot finalnya.")

left, right = st.columns([1.15, 1], gap="large")

with left:
    card_open()
    st.subheader("A. Input Data Pemeriksaan Pasien", anchor=False)

    with st.form("patient_form", clear_on_submit=False):
        c1, c2 = st.columns(2)

        with c1:
            pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=0, step=1)
            glucose = st.number_input("Glucose", min_value=0, max_value=500, value=0, step=1, help="mg/dL")
            blood_pressure = st.number_input("BloodPressure", min_value=0, max_value=300, value=0, step=1, help="mmHg")
            skin_thickness = st.number_input("SkinThickness", min_value=0, max_value=200, value=0, step=1, help="mm")

        with c2:
            insulin = st.number_input("Insulin", min_value=0, max_value=2000, value=0, step=1, help="mu U/mL")
            bmi = st.number_input("BMI", min_value=0.0, max_value=80.0, value=0.0, step=0.1)
            dpf = st.number_input("DiabetesPedigreeFunction", min_value=0.0, max_value=5.0, value=0.0, step=0.01)
            age = st.number_input("Age", min_value=0, max_value=120, value=0, step=1)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        submitted = st.form_submit_button("Proses Deteksi", type="primary", use_container_width=True)

    if submitted:
        pi = PatientInput(
            Pregnancies=float(pregnancies),
            Glucose=float(glucose),
            BloodPressure=float(blood_pressure),
            SkinThickness=float(skin_thickness),
            Insulin=float(insulin),
            BMI=float(bmi),
            DiabetesPedigreeFunction=float(dpf),
            Age=float(age),
        )

        errors = validate_input(pi)
        if errors:
            for e in errors:
                st.error(e)
        else:
            with st.spinner("Menghitung kemiripan kasus dan estimasi risiko..."):
                try:
                    pred = predict_with_user_model(pi)
                except Exception as e:
                    st.error(f"Gagal melakukan prediksi: {e}")
                    pred = None

            if pred is not None:
                st.session_state["latest_input"] = asdict(pi)
                st.session_state["latest_pred"] = pred
                st.success("Analisis selesai. Silakan lakukan validasi (Revise) di panel kanan.")

    card_close()

with right:
    card_open()
    st.subheader("B. Hasil Estimasi & Validasi (Revise)", anchor=False)

    latest_input = st.session_state.get("latest_input")
    latest_pred = st.session_state.get("latest_pred")

    if not latest_input or not latest_pred:
        st.markdown(
            '<p class="muted">Belum ada hasil. Isi form di kiri lalu klik <b>Proses Deteksi</b>.</p>',
            unsafe_allow_html=True,
        )
        card_close()
    else:
        predicted = int(latest_pred["predicted_outcome"])
        risk_score = float(latest_pred.get("risk_score", 0.0))

        label = "RISIKO TINGGI" if predicted == 1 else "RISIKO RENDAH"
        pill_class = "bad" if predicted == 1 else "good"
        st.markdown(
            f'<div class="pill {pill_class}">{label}</div>',
            unsafe_allow_html=True,
        )
        st.write("")
        st.metric("Skor risiko (proporsi Outcome=1 pada tetangga)", f"{risk_score:.2f}")
        st.caption(latest_pred.get("explain", ""))
        if latest_pred.get("case_base_source"):
            st.caption(f"Sumber basis kasus: `{latest_pred['case_base_source']}`")

        preview = latest_pred.get("nearest_cases_preview")
        if isinstance(preview, pd.DataFrame) and not preview.empty:
            with st.expander("Lihat tetangga terdekat (preview)"):
                st.dataframe(preview, use_container_width=True, hide_index=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("#### H. Validasi hasil oleh user (Revise)")

        validated = st.radio(
            "Apakah hasil estimasi sesuai pertimbangan klinis?",
            options=["Sesuai", "Tidak sesuai"],
            horizontal=True,
        )

        if validated == "Sesuai":
            validated_outcome = predicted
        else:
            validated_outcome = st.radio(
                "Tentukan outcome akhir (hasil validasi klinis)",
                options=[0, 1],
                format_func=lambda v: "0 — Tidak diabetes" if v == 0 else "1 — Diabetes",
                horizontal=True,
            )

        note = st.text_area(
            "Catatan (opsional)",
            placeholder="Misal: pertimbangan klinis, hasil lab tambahan, rujukan, dll.",
            height=90,
        )

        st.markdown("#### I. Penyimpanan ke basis kasus (Retain)")
        col_save, col_clear = st.columns([1, 1])

        with col_save:
            if st.button("Simpan ke Basis Kasus", type="primary", use_container_width=True):
                row = {
                    "timestamp": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
                    **latest_input,
                    "predicted_outcome": predicted,
                    "validated_outcome": int(validated_outcome),
                    "validation_note": note.strip(),
                }
                retain_case(row)
                st.success("Tersimpan ke basis kasus.")

        with col_clear:
            if st.button("Reset Hasil", use_container_width=True):
                st.session_state.pop("latest_input", None)
                st.session_state.pop("latest_pred", None)
                st.rerun()

        card_close()

st.markdown("")
st.caption(
    "Catatan: bobot MultiSURF dan parameter min/max training final sebaiknya disimpan sebagai artefak (file) "
    "agar normalisasi & pembobotan konsisten. Saat ini normalisasi MinMax di-fit dari basis kasus yang tersedia."
)
