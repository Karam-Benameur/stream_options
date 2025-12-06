import os, sys
from pathlib import Path          

# — Assure que le dossier du projet est dans le PYTHONPATH —
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# — Import robuste du composant d'accueil —
try:
    from utils.plotting import hero_home
except ModuleNotFoundError:
    import importlib.util
    plotting_path = os.path.join(BASE_DIR, "utils", "plotting.py")
    spec = importlib.util.spec_from_file_location("plotting", plotting_path)
    plotting = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(plotting)
    hero_home = plotting.hero_home

import streamlit as st

st.set_page_config(page_title="StreamOptions — Home", page_icon="🏠", layout="wide")

# ======= chemin vers le logo (robuste) =======
LOGO_PATH = Path(__file__).resolve().parent / "roadmap" / "pictures" / "logo.png"

# Style léger pour coller à la maquette
st.markdown("""
<style>
section[data-testid="stSidebar"] {min-width: 260px;}
a.stPageLink, div.stPageLink {
  display:block; padding:14px 18px; margin:14px 8px;
  border-radius: 28px; background:#D9D9D9;
  text-decoration:none; color:#111; font-weight:600;
  text-align:center; transition: all .15s ease-in-out;
  border:1px solid #cfcfcf;
}
a.stPageLink:hover { transform: translateY(-1px); box-shadow: 0 1px 6px rgba(0,0,0,.08);}
a.stPageLink.selected { background:#FF7A3A; color:white; border-color:#FF7A3A;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image(str(LOGO_PATH), width=64)
    st.markdown("**Home 🏠**")
    st.page_link("pages/01_Monte_Carlo.py", label="Monte Carlo")
    st.page_link("pages/02_Black_Scholes.py", label="Black Scholes")
    st.page_link("pages/03_Binomial.py", label="Binomial")

st.title("Home")
hero_home()

# ==========================
#  GROS LOGO CENTRÉ AU MILIEU
# ==========================
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    st.image(
       str(LOGO_PATH),
       use_container_width=True,   # ✅ nouvelle version
       caption="StreamOptions"
    )

