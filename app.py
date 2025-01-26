import streamlit as st
from streamlit.components.v1 import html
import requests

# Flask server URL
FLASK_BACKEND_URL = "http://127.0.0.1:5000"

# Streamlit App
st.sidebar.title("📚 Navigation")
page = st.sidebar.radio(
    "Go to:",
    ["🏠 Homepage", "🎯 Goal Tracker", "📏 Posture Detector", "🤖 Study Buddy AI Chat"]
)

def start_posture_detection():
    st.markdown("<h1>📏 Posture Detection</h1>", unsafe_allow_html=True)

    # Embed the video feed from Flask
    video_html = f"""
        <div style="text-align: center;">
            <h2>Posture Detection Feed</h2>
            <p>Ensure good posture while studying or working. The feed below updates in real-time.</p>
            <img src="{FLASK_BACKEND_URL}/video_feed" width="800" alt="Posture Detection Video Feed" />
        </div>
    """
    html(video_html, height=700)

if page == "🏠 Homepage":
    st.title("🏠 Welcome to Study Hub")
    st.write("Navigate to explore features like goal tracking, posture detection, and AI chat.")
elif page == "🎯 Goal Tracker":
    st.header("🎯 Goal Tracker")
    st.write("Goal tracking page coming soon...")
elif page == "📏 Posture Detector":
    if st.button("Start Posture Detection"):
        # Start posture detection when the button is pressed
        start_posture_detection()
elif page == "🤖 Study Buddy AI Chat":
    st.header("🤖 Study Buddy AI Chat")
    st.write("AI Chat feature coming soon...")
