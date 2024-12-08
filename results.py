# results_page.py
import streamlit as st
import openai
import json


def generate_roast(data, roast_style, roast_length):
    # Configure OpenAI
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # Convert DataFrame to readable format
    data_str = data.to_string()

    # Adjust token length based on roast length
    max_tokens = {
        "Short & Sweet": 100,
        "Medium": 200,
        "Fully Judged": 400
    }

    # Create prompt based on analysis type
    prompt = f"""Given this user's music taste data:
    {data_str}

    Generate a humorous critique/roast of their music taste. 
    Style instruction: {roast_style if roast_style else 'Standard roast'}

    Make specific references to the artists/songs and their genres.
    Keep it playful and not mean-spirited."""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a witty music critic with a sense of humor."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens[roast_length],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating roast: {str(e)}"


def results_page():
    st.title("🎵 Your Music Taste Critique 🎵")

    # Check if we have the necessary data
    if "analysis_data" not in st.session_state:
        st.error("No music data found! Please go back and analyze your music first.")
        if st.button("Back to Settings"):
            st.session_state["page"] = "settings"
            st.rerun()
        return

    # Display the roast in a styled container
    with st.container():
        st.subheader("Here's what we think about your music taste...")

        # Generate roast if not already generated
        if "roast_text" not in st.session_state:
            with st.spinner("Generating your personalized critique..."):
                roast = generate_roast(
                    st.session_state["analysis_data"],
                    st.session_state["roast_style"],
                    st.session_state["roast_length"]
                )
                st.session_state["roast_text"] = roast

        # Display the roast in a text area
        st.text_area(
            "Your Personalized Critique",
            value=st.session_state["roast_text"],
            height=300,
            key="roast_display",
            disabled=True
        )

        # Add some visual flair
        st.markdown("""
            <style>
                .stTextArea textarea {
                    background-color: #f0f2f6;
                    font-size: 18px !important;
                    font-family: 'Georgia', serif;
                    padding: 20px;
                    border-radius: 10px;
                }
            </style>
        """, unsafe_allow_html=True)

    # Display the analyzed data
    with st.expander("View Your Music Data"):
        st.dataframe(st.session_state["analysis_data"])

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate New Critique"):
            del st.session_state["roast_text"]
            st.rerun()

    with col2:
        if st.button("Back to Settings"):
            st.session_state["page"] = "settings"
            st.rerun()

    # Add download button
    st.download_button(
        label="Download Critique",
        data=st.session_state["roast_text"],
        file_name="my_music_critique.txt",
        mime="text/plain"
    )
