import streamlit as st
from posture_detector import detect_posture  # Corrected import
from ai_assistant import study_buddy_chat
from goal_page import goal_page
import cv2

# Set a modern background and improved global CSS
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(135deg, #67b26f, #4ca2cd) !important;
            font-family: 'Helvetica', 'Arial', sans-serif;
            color: #333;
            margin: 0;
            padding: 0;
        }

        /* Global Styles */
        .title {
            font-size: 2.5em;
            font-weight: bold;
            color: #000;
            text-align: center;
            padding: 30px 0;
        }

        .icon {
            font-size: 1.5em;
            margin-right: 10px;
        }

        .content {
            font-size: 1.1em;
            color: #000;
            text-align: center;
            margin: 20px 0;
        }

        .sidebar-title {
            font-size: 1.5em;
            font-weight: bold;
        }

        .sidebar-radio {
            margin-top: 20px;
        }

        .sidebar-markdown {
            font-size: 1.1em;
            color: #555;
        }

        /* Button Styling */
        .stButton button {
            background-color: #4ca2cd;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s ease, color 0.3s ease, transform 0.2s ease;
        }

        .stButton button:hover {
            background-color: #5cb3d6;
            color: #0056b3;
            transform: scale(1.05);
        }

        .stButton button:active {
            transform: scale(0.98);
        }

        /* Section Headers */
        .section-header {
            font-size: 1.8em;
            font-weight: bold;
            color: #333;
            text-align: left;
            margin-bottom: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Navigation setup using Streamlit's st.session_state
if "page" not in st.session_state:
    st.session_state.page = "Homepage"

# Sidebar for navigation
st.sidebar.title("📚 Navigation")
st.sidebar.markdown("<span class='sidebar-title'>📋 Choose a section:</span>", unsafe_allow_html=True)
page = st.sidebar.radio(
    "Go to:",
    (
        "🏠 Homepage",
        "🎯 Goal Tracker",
        "📏 Posture Detector",
        "🤖 Study Buddy AI Chat"
    ),
    label_visibility="collapsed"  # hides label for a cleaner look
)
st.session_state.page = page

# Define homepage function
def homepage():
    st.markdown("<div class='title'><span class='icon'>🏠</span>Welcome to Study Hub</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class='content'>
        <strong>Study Hub</strong> is your one-stop solution for focused learning, mindfulness, and achieving your study goals.<br>
        Navigate to different sections using the menu to explore features like goal tracking, posture detection, and AI assistance.
        </div>
        """,
        unsafe_allow_html=True
    )

# Posture Detection functionality
def video_feed():
    # Open the webcam
    cap = cv2.VideoCapture(0)

    # Create placeholders for the image display and posture feedback
    image_placeholder = st.empty()
    feedback_placeholder = st.empty()

    while True:
        ret, frame = cap.read()  # Read frame from webcam
        if not ret:
            break

        # Perform posture detection
        frame, posture_text = detect_posture(frame)

        # Convert BGR frame to RGB for Streamlit compatibility
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Update the image in the placeholder (this avoids creating new Streamlit elements)
        image_placeholder.image(frame, channels="RGB", use_container_width=True)

        # Update posture feedback text
        feedback_placeholder.text(posture_text)

    cap.release()  # Release the webcam once done

# Main page rendering logic based on selected navigation
if st.session_state.page == "🏠 Homepage":
    homepage()
elif st.session_state.page == "🎯 Goal Tracker":
    st.markdown("<div class='section-header'><span class='icon'>🎯</span>Goal Tracker</div>", unsafe_allow_html=True)
    goal_page()
elif st.session_state.page == "📏 Posture Detector":
    st.markdown("<div class='section-header'><span class='icon'>📏</span>Posture Detection App</div>", unsafe_allow_html=True)
    # Streamlit component to start the video feed
    if st.button("Start Posture Detection"):
        video_feed()
elif st.session_state.page == "🤖 Study Buddy AI Chat":
    st.markdown("<div class='section-header'><span class='icon'>🤖</span>Study Buddy AI Chat</div>", unsafe_allow_html=True)
    study_buddy_chat()
