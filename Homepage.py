import streamlit as st
import requests
import urllib.parse

# Spotify credentials
SPOTIFY_CLIENT_ID = "cee3edb46ee74db3be7da87e6e6d31fc"
SPOTIFY_CLIENT_SECRET = "d133568850cf41a58995323c9a012b59"
REDIRECT_URI = "http://localhost:8501"
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"


# Function to generate Spotify authorization URL
def get_spotify_auth_url():
    params = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": "user-top-read",
    }
    return f"{SPOTIFY_AUTH_URL}?{urllib.parse.urlencode(params)}"


# Streamlit page setup
st.set_page_config(page_title="Critique My Music Taste", page_icon="🎵")

# Navigation Logic
if "page" not in st.session_state:
    st.session_state["page"] = "home"

if st.session_state["page"] == "home":
    # Home Page
    st.title("🎵 Critique My Music Taste 🎵")
    st.subheader("Discover, Critique, and Grow your music taste!")

    query_params = st.query_params
    st.write(f"Query Params: {query_params}")  # Debugging

    if "code" in query_params:
        auth_code = query_params["code"]
        st.write(f"Authorization Code: {auth_code}")
        st.success("Authorization successful! Exchanging token...")

        # Exchange authorization code for access token
        token_data = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": REDIRECT_URI,
            "client_id": SPOTIFY_CLIENT_ID,
            "client_secret": SPOTIFY_CLIENT_SECRET,
        }
        response = requests.post(SPOTIFY_TOKEN_URL, data=token_data)
        if response.status_code == 200:
            tokens = response.json()
            access_token = tokens["access_token"]
            st.success("Access token obtained successfully!")

            # Save the token in session state
            st.session_state["access_token"] = access_token

            # Add "Let's Get Started" button
            if st.button("Let's Get Started"):
                st.session_state["page"] = "settings"  # Navigate to settings page
        else:
            st.error("Failed to obtain access token. Please try again.")
    else:
        st.write("""
        Welcome to **Critique My Music Taste**, a web app that analyzes your top Spotify artists and songs.
        Sign in with your Spotify account to begin!
        """)
        spotify_auth_url = get_spotify_auth_url()
        st.markdown(f"""
            <a href="{spotify_auth_url}" target="_self">
                <button style="
                    background-color: #1DB954; 
                    color: white; 
                    border: none; 
                    padding: 10px 20px; 
                    text-align: center; 
                    text-decoration: none; 
                    font-size: 16px; 
                    border-radius: 25px;
                    cursor: pointer;">
                    Log in with Spotify
                </button>
            </a>
        """, unsafe_allow_html=True)

elif st.session_state["page"] == "settings":
    # Critique Settings Page
    st.title("Settings for Your Critique")
    st.subheader("Customize your experience")
    st.write("This is where users will set parameters for the critique (e.g., number of artists, roast length).")
    if st.button("Go Back"):
        st.session_state["page"] = "home"
