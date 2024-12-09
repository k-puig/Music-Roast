import streamlit as st
import requests
import urllib.parse

# Spotify credentials
SPOTIFY_CLIENT_ID = "*************************"
SPOTIFY_CLIENT_SECRET = "********************"
REDIRECT_URI = "http://localhost:8501"
REDIRECT_URI = "https://crit.kpuig.net"
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"


def get_spotify_auth_url():
    params = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": "user-top-read",
    }
    return f"{SPOTIFY_AUTH_URL}?{urllib.parse.urlencode(params)}"


def homepage():
    st.title("🎵 Critique My Music Taste 🎵")
    st.subheader("Discover, Critique, and Grow your music taste!")

    query_params = st.query_params

    if "code" in query_params:
        auth_code = query_params["code"]

        token_data = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": REDIRECT_URI,
            "client_id": SPOTIFY_CLIENT_ID,
            "client_secret": SPOTIFY_CLIENT_SECRET,
        }

        try:
            response = requests.post(SPOTIFY_TOKEN_URL, data=token_data)

            if response.status_code == 200:
                tokens = response.json()
                access_token = tokens["access_token"]
                st.session_state["access_token"] = access_token
                st.success("Authorization successful! Proceeding to settings...")
                st.session_state["page"] = "settings"
                st.rerun()
            else:
                st.error("Failed to obtain access token. Please try again.")
                st.error(f"Error: {response.text}")

        except Exception as e:
            st.error(f"Exception during token exchange: {str(e)}")
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
