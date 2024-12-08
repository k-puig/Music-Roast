import streamlit as st
from spotify_auth import homepage
from settings import settings_page
from results import results_page

# Streamlit page setup
st.set_page_config(page_title="Critique My Music Taste", page_icon="🎵")

# Initialize session state
if "page" not in st.session_state:
    st.session_state["page"] = "home"

# Main navigation logic
if st.session_state["page"] == "home":
    homepage()
elif st.session_state["page"] == "settings":
    settings_page()
elif st.session_state["page"] == "results":
    results_page()
