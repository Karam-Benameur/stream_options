import streamlit as st
from utils.plotting import hero_home

st.set_page_config(page_title="StreamOptions — Home", page_icon="🏠", layout="wide")

# Style léger pour coller à la maquette (boutons arrondis dans la sidebar)
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
    # Si le logo n'existe pas encore, Streamlit n'affichera juste rien.
    st.image("roadmap/pictures/logo.png", width=64)
    st.page_link("Home.py", label="Home 🏠")
    st.page_link("pages/01_Monte_Carlo.py", label="Monte Carlo Method")
    st.page_link("pages/02_Black_Scholes.py", label="Black and Scholes Method")
    st.page_link("pages/03_Binomial.py", label="Binomial Method")

st.title("Home")
hero_home()
