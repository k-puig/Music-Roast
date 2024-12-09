import streamlit as st
import pandas as pd
import altair as alt
import requests


def get_spotify_data(access_token, analysis_type, time_range, limit):
    """
    Fetch top tracks or artists from Spotify API based on user settings
    """
    # Convert time range to Spotify API format
    time_range_map = {
        "4 weeks": "short_term",
        "6 months": "medium_term",
        "All time": "long_term"
    }
    spotify_time_range = time_range_map[time_range]

    # Set up request headers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        if analysis_type == "Top Songs":
            endpoint = f"https://api.spotify.com/v1/me/top/tracks"
            params = {
                "time_range": spotify_time_range,
                "limit": limit,
                "offset": 0
            }
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()

            tracks_data = response.json()["items"]

            # Process tracks data
            processed_data = []
            for i, track in enumerate(tracks_data, 1):
                # Get track genres from its artists
                artist_genres = []
                for artist in track["artists"]:
                    artist_response = requests.get(
                        f"https://api.spotify.com/v1/artists/{artist['id']}",
                        headers=headers
                    )
                    if artist_response.status_code == 200:
                        artist_genres.extend(artist_response.json().get("genres", []))

                track_info = {
                    "Rank": i,
                    "Song": track["name"],
                    "Artist": ", ".join(artist["name"] for artist in track["artists"]),
                    "Album": track["album"]["name"],
                    "Popularity": track["popularity"],
                    "Preview URL": track["preview_url"],
                    "Genres": ", ".join(set(artist_genres)) if artist_genres else "Unknown"
                }
                processed_data.append(track_info)

            return pd.DataFrame(processed_data)

        else:  # Top Artists
            endpoint = f"https://api.spotify.com/v1/me/top/artists"
            params = {
                "time_range": spotify_time_range,
                "limit": limit,
                "offset": 0
            }
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()

            artists_data = response.json()["items"]

            # Process artists data
            processed_data = []
            for i, artist in enumerate(artists_data, 1):
                artist_info = {
                    "Rank": i,
                    "Artist": artist["name"],
                    "Genres": ", ".join(artist["genres"]) if artist["genres"] else "Unknown",
                    "Popularity": artist["popularity"],
                    "Followers": artist["followers"]["total"],
                    "Image URL": artist["images"][0]["url"] if artist["images"] else None
                }
                processed_data.append(artist_info)
                print(processed_data)

            return pd.DataFrame(processed_data)

    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching Spotify data: {str(e)}")


def settings_page():
    st.title("🎵 Critique My Music Taste - Settings")

    # Sidebar for color customization
    with st.sidebar:
        st.header("Customize Data Appearance")
        page_color = st.color_picker("Choose page accent color", "#1DB954")
        st.markdown(f"""
            <style>
                .stButton button {{
                    background-color: {page_color};
                    color: white;
                }}
                .stProgress .st-bo {{
                    background-color: {page_color};
                }}
            </style>
        """, unsafe_allow_html=True)

    # Main settings container
    with st.container():
        st.info("""
            Customize your Critique below! Choose what you want to analyze,
            how detailed you want the Critique to be, and add your own twist to make it personal.
        """)

        # Analysis Type Selection
        analysis_type = st.radio(
            "What would you like to Critique?",
            ["Top Songs", "Top Artists"],
            help="Choose whether to analyze your most played songs or artists"
        )

        col1, col2 = st.columns(2)

        with col1:
            # Number of items to analyze
            num_items = st.number_input(
                "How many items to analyze?",
                min_value=1,
                max_value=10,
                value=10,
                help="Choose between 1-10 items to analyze"
            )

            # Roast length selection
            roast_length = st.selectbox(
                "How long should the Critique be?",
                ["Short & Sweet", "Medium", "Fully Judged"],
                help="Choose the length and detail of your Critique"
            )

        with col2:
            # Custom roast style input
            roast_style = st.text_area(
                "Add your personal touch to the Critique (optional)",
                placeholder="e.g., 'Make it nerdy' or 'Critique like Gordon Ramsay'",
                help="Add specific instructions to personalize your Critique"
            )

        # Time range selection
        st.subheader("Time Range")
        time_range = st.select_slider(
            "Select time range to analyze",
            options=["4 weeks", "6 months", "All time"],
            value="6 months"
        )

        # Example preview table/chart
        st.subheader("Preview of Data to Analyze")
        if analysis_type == "Top Songs":
            # Example data
            data = pd.DataFrame({
                'Rank': range(1, num_items + 1),
                'Song': [f"Example Song {i}" for i in range(1, num_items + 1)],
                'Plays': [100 - i * 5 for i in range(num_items)]
            })

            # Create chart
            chart = alt.Chart(data).mark_bar().encode(
                x='Plays',
                y=alt.Y('Song', sort='-x'),
                color=alt.value(page_color)
            ).properties(
                height=num_items * 25
            )

            st.altair_chart(chart, use_container_width=True)
        else:
            # Display as table for artists
            data = pd.DataFrame({
                'Rank': range(1, num_items + 1),
                'Artist': [f"Example Artist {i}" for i in range(1, num_items + 1)],
                'Genre': (["Pop", "Rock", "Hip-Hop", "Jazz", "Electronic", "Country"] * 10)[0:num_items],
                'Monthly Listeners': [1000000 - i * 50000 for i in range(num_items)]
            })
            st.dataframe(data, hide_index=True)

        # Generate button with API integration
        if st.button("Generate Critique 🔥", use_container_width=True):
            try:
                st.session_state["roast_text"] = ""
                del st.session_state["roast_text"]
                with st.spinner("Analyzing your questionable music taste..."):
                    # Check for access token
                    if "access_token" not in st.session_state:
                        st.error("Please log in with Spotify first!")
                        return

                    # Get the actual data from Spotify
                    data = get_spotify_data(
                        st.session_state["access_token"],
                        analysis_type,
                        time_range,
                        num_items
                    )

                    # Store everything in session state for the results page
                    st.session_state["analysis_data"] = data
                    st.session_state["analysis_type"] = analysis_type
                    st.session_state["roast_length"] = roast_length
                    st.session_state["roast_style"] = roast_style

                    st.success("Analysis complete! Proceeding to Critique...")
                    st.session_state["page"] = "results"
                    st.rerun()

            except Exception as e:
                st.error(f"Oops! Something went wrong: {str(e)}")
                st.info("Please make sure you're properly connected to Spotify and try again.")

        # Reset button
        if st.button("Reset Settings ↺", use_container_width=True):
            st.rerun()


if __name__ == "__main__":
    settings_page()
