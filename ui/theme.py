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
            --stroke2: rgba(255, 255, 255, .12);
            --text: rgba(255, 255, 255, .92);
            --muted: rgba(255, 255, 255, .72);
            --muted2: rgba(255, 255, 255, .60);
            --shadow: 0 12px 35px rgba(0, 0, 0, .35);
            --shadow2: 0 8px 18px rgba(0, 0, 0, .22);
            --radius: 18px;
            --radius2: 14px;
            --blur: blur(22px);
            --accent: #2dd4bf;   /* teal */
            --accent2: #22c55e;  /* emerald */
            --danger: #fb7185;   /* rose */
            --warning: #fbbf24;  /* amber */
          }

          /* App background */
          .stApp {
            background:
              radial-gradient(1200px 650px at 15% 0%, rgba(45, 212, 191, .20), rgba(0,0,0,0) 60%),
              radial-gradient(950px 650px at 85% 10%, rgba(34, 197, 94, .16), rgba(0,0,0,0) 55%),
              linear-gradient(135deg, var(--bg0), var(--bg1) 45%, var(--bg2));
            color: var(--text);
          }
          .stApp::before{
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background-image:
              url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='180' height='180' filter='url(%23n)' opacity='.18'/%3E%3C/svg%3E");
            opacity: .20;
            mix-blend-mode: overlay;
          }

          /* Container spacing */
          .block-container { padding-top: 1.25rem; padding-bottom: 2.2rem; }

          /* Sidebar glass */
          section[data-testid="stSidebar"] > div {
            background: linear-gradient(180deg, rgba(255,255,255,.10), rgba(255,255,255,.06));
            border-right: 1px solid rgba(255,255,255,.10);
            backdrop-filter: var(--blur);
            -webkit-backdrop-filter: var(--blur);
          }
          section[data-testid="stSidebar"] * { color: var(--text); }
          section[data-testid="stSidebar"] .stCaptionContainer,
          section[data-testid="stSidebar"] p,
          section[data-testid="stSidebar"] span { color: var(--muted); }

          /* Typography */
          h1, h2, h3, h4 { letter-spacing: -0.02em; color: var(--text); }
          p, li { color: var(--muted); }
          code { color: rgba(255,255,255,.88); }

          /* Glass building blocks */
          .glass {
            background: linear-gradient(180deg, var(--glass), var(--glass2));
            border: 1px solid var(--stroke);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            backdrop-filter: var(--blur);
            -webkit-backdrop-filter: var(--blur);
          }
          .card { padding: 1rem 1.05rem; }
          .kpi { padding: .95rem 1.05rem; box-shadow: var(--shadow2); border-radius: var(--radius2); }
          .kpi .label { font-size: .85rem; color: var(--muted2); }
          .kpi .value { font-size: 1.25rem; font-weight: 780; margin-top: .25rem; color: var(--text); }
          .divider { height: 1px; background: rgba(255, 255, 255, .14); margin: .9rem 0; }
          .muted { color: var(--muted); }
          .tiny { font-size: .92rem; }

          /* Pills */
          .pill {
            display: inline-block;
            padding: .30rem .65rem;
            border-radius: 999px;
            font-weight: 750;
            border: 1px solid var(--stroke);
            background: rgba(255,255,255,.10);
            box-shadow: 0 10px 22px rgba(0,0,0,.25);
            backdrop-filter: var(--blur);
            -webkit-backdrop-filter: var(--blur);
          }
          .pill.good { border-color: rgba(34,197,94,.35); background: rgba(34,197,94,.12); }
          .pill.bad  { border-color: rgba(251,113,133,.40); background: rgba(251,113,133,.12); }

          /* Inputs (Streamlit widgets) */
          div[data-baseweb="input"] > div,
          div[data-baseweb="textarea"] > div,
          div[data-baseweb="select"] > div,
          div[data-baseweb="popover"] > div {
            background: rgba(255,255,255,.10) !important;
            border: 1px solid rgba(255,255,255,.16) !important;
            border-radius: 14px !important;
            backdrop-filter: var(--blur);
            -webkit-backdrop-filter: var(--blur);
          }
          div[data-baseweb="input"] input,
          div[data-baseweb="textarea"] textarea {
            color: var(--text) !important;
            caret-color: var(--accent) !important;
          }
          .stMarkdown a { color: rgba(45, 212, 191, .92); }

          /* Buttons */
          .stButton > button {
            border-radius: 14px !important;
            border: 1px solid rgba(255,255,255,.18) !important;
            background: rgba(255,255,255,.10) !important;
            color: var(--text) !important;
            box-shadow: 0 10px 22px rgba(0,0,0,.20);
            transition: transform .05s ease, box-shadow .2s ease;
          }
          .stButton > button:hover { box-shadow: 0 14px 30px rgba(0,0,0,.28); }
          .stButton > button:active { transform: translateY(1px); }
          .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, rgba(45,212,191,.95), rgba(34,197,94,.90)) !important;
            border: 1px solid rgba(255,255,255,.22) !important;
            box-shadow: 0 18px 45px rgba(45,212,191,.18);
            color: rgba(3, 7, 18, .92) !important;
            font-weight: 800 !important;
          }

          /* Info/success/warning/error containers */
          div[data-testid="stAlert"] {
            background: rgba(255,255,255,.10) !important;
            border: 1px solid rgba(255,255,255,.16) !important;
            border-radius: 16px !important;
            box-shadow: var(--shadow2);
            backdrop-filter: var(--blur);
            -webkit-backdrop-filter: var(--blur);
          }
          div[data-testid="stAlert"] * { color: var(--text) !important; }

          /* Dataframe */
          div[data-testid="stDataFrame"] {
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,.14);
            box-shadow: var(--shadow2);
          }

          /* Expander */
          details[data-testid="stExpander"] {
            background: rgba(255,255,255,.08);
            border: 1px solid rgba(255,255,255,.12);
            border-radius: 16px;
            padding: .25rem .75rem;
            box-shadow: 0 10px 22px rgba(0,0,0,.18);
          }
          details[data-testid="stExpander"] summary { color: var(--text); }
        </style>
        """,
        unsafe_allow_html=True,
    )


def card_open() -> None:
    st.markdown('<div class="glass card">', unsafe_allow_html=True)


def card_close() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def kpi(label: str, value: str) -> None:
    st.markdown(
        f'<div class="glass kpi"><div class="label">{label}</div><div class="value">{value}</div></div>',
        unsafe_allow_html=True,
    )

