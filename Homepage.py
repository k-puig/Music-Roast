import streamlit as st
import requests
import urllib.parse

SPOTIFY_CLIENT_ID = "YOUR_CLIENT_ID"
SPOTIFY_CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REDIRECT_URI = "http://localhost:8501"  # Change this to match your setup
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

st.set_page_config(page_title="Critique My Music Taste", page_icon="🎵")

st.title("🎵 Critique My Music Taste 🎵")
st.subheader("Discover, Critique, and Grow your music taste!")

query_params = st.query_params
if "code" not in query_params:
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
else:
    # Authorization code received
    auth_code = query_params["code"]
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
        st.write(f"Access Token: {access_token}")
        
        # Testing getting top 5 songs
        SPOTIFY_TRACKS_URL = f"https://api.spotify.com/v1/me/top/tracks?access_token={access_token}" # Replace tracks with artists for artists instead
        req = {
            "token": access_token,
            "time_range": "short_term", # This should stay the same unless you want a larger range of time to pull user info from
            "limit": "10", # This can be user-controlled
            "offset": "0" # This should always stay the same
        }
        tracks = requests.get(SPOTIFY_TRACKS_URL, req)
        st.write(tracks.json()["items"])
    else:
        st.error("Failed to obtain access token. Please try again.")

st.write("---")
st.caption("No personal data will be stored. Your Spotify login is secure.")
