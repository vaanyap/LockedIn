import streamlit as st
from mediapipe import solutions as mp_solutions

# Set a soft blue background color and add global styling using CSS
st.markdown(
    """
    <style>
        /* Apply a background color to the body */
        body {
            background-color: #e6f7ff !important;
        }
        .title {
            font-size: 2.5em;
            font-weight: bold;
            color: #004080;
            text-align: center;
            margin-bottom: 20px;
        }
        .content {
            font-size: 1.2em;
            color: #333;
            line-height: 1.6;
            margin: 20px;
        }
        .icon {
            font-size: 1.5em;
            color: #0073e6;
            vertical-align: middle;
            margin-right: 10px;
        }
        .auth-container {
            text-align: center;
            margin-top: 30px;
        }
        .auth-button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-size: 1.1em;
            cursor: pointer;
            margin: 10px;
            transition: background-color 0.3s ease;
        }
        .auth-button:hover {
            background-color: #45a049;
        }
        .form-container {
            margin-top: 20px;
            background: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            width: 50%;
            margin-left: auto;
            margin-right: auto;
        }
        .chat-container {
            background: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            width: 70%;
            margin-left: auto;
            margin-right: auto;
        }
        .chat-message {
            padding: 10px;
            background: #f1f1f1;
            margin: 5px;
            border-radius: 5px;
        }
        .button-container {
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Navigation setup using Streamlit's st.session_state
if "page" not in st.session_state:
    st.session_state.page = "Homepage"
if "auth_state" not in st.session_state:
    st.session_state.auth_state = None

def navigate_to(page):
    st.session_state.page = page

def homepage():
    st.markdown("<div class='title'><span class='icon'>🏠</span>Welcome to Study Hub</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class='content'>
        Study Hub is your one-stop solution for focused learning, mindfulness, and achieving your study goals.<br>
        Navigate to different sections using the menu to explore features like goal tracking, posture detection, and AI assistance.
        </div>
        """,
        unsafe_allow_html=True
    )

    # Sign In / Sign Up section
    st.markdown("<div class='auth-container'>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        if st.button("Sign In", key="sign_in_button", help="Click to sign in", 
                     use_container_width=True):
            st.session_state.auth_state = "sign_in"

    with col2:
        if st.button("Sign Up", key="sign_up_button", help="Click to sign up", 
                     use_container_width=True):
            st.session_state.auth_state = "sign_up"

    if st.session_state.auth_state == "sign_in":
        st.markdown(
            """
            <div class='form-container'>
                <h3>Sign In</h3>
                <form>
                    <label for='username'>Username:</label><br>
                    <input type='text' id='username' name='username'><br><br>
                    <label for='password'>Password:</label><br>
                    <input type='password' id='password' name='password'><br><br>
                    <button type='submit' class='auth-button'>Sign In</button>
                </form>
            </div>
            """,
            unsafe_allow_html=True
        )

    elif st.session_state.auth_state == "sign_up":
        st.markdown(
            """
            <div class='form-container'>
                <h3>Sign Up</h3>
                <form>
                    <label for='username'>Username:</label><br>
                    <input type='text' id='username' name='username'><br><br>
                    <label for='email'>Email:</label><br>
                    <input type='email' id='email' name='email'><br><br>
                    <label for='password'>Password:</label><br>
                    <input type='password' id='password' name='password'><br><br>
                    <button type='submit' class='auth-button'>Sign Up</button>
                </form>
            </div>
            """,
            unsafe_allow_html=True
        )

def goal_page():
    st.markdown("<div class='title'><span class='icon'>🎯</span>Goal Tracker</div>", unsafe_allow_html=True)
    goal = st.text_input("What is your primary goal for today?")
    st.markdown(
        """
        <div class='content'>
        - Add smaller sub-goals below to break your primary goal into actionable steps.<br>
        - Check them off as you progress!
        </div>
        """,
        unsafe_allow_html=True
    )
    if goal:
        st.markdown(f"<div class='content'>Your main goal is: {goal}</div>", unsafe_allow_html=True)

    if st.button("Add sub-goal"):
        st.markdown("<div class='content'>Feature to add sub-goals coming soon!</div>", unsafe_allow_html=True)

def posture_detector():
    st.markdown("<div class='title'><span class='icon'>🪑</span>Posture Detector</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class='content'>
        Ensure you're sitting correctly for optimal focus and health.<br>
        Feature uses MediaPipe for posture analysis.
        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_video = st.file_uploader("Upload a video of yourself sitting (MP4 format):", type="mp4")

    if uploaded_video:
        st.video(uploaded_video)
        st.markdown("<div class='content'>Processing your posture... Feature coming soon!</div>", unsafe_allow_html=True)

# New Study Buddy AI Chat Assistant Page
def study_buddy_chat():
    st.markdown("<div class='title'><span class='icon'>🤖</span>Study Buddy AI Chat</div>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class='content'>
        Chat with your AI Study Buddy for personalized study tips, motivation, and guidance.<br>
        Just type your message below, and the AI will respond accordingly!
        </div>
        """,
        unsafe_allow_html=True
    )

    # Create a simple chat interface
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for msg in st.session_state.messages:
        st.markdown(f"<div class='chat-message'>{msg}</div>", unsafe_allow_html=True)

    # Input field for chat
    user_input = st.text_input("Type your message:", key="chat_input")
    if st.button("Send"):
        if user_input:
            # Add user input to the chat
            st.session_state.messages.append(f"You: {user_input}")
            # Simple AI response (can be replaced with actual AI model)
            st.session_state.messages.append(f"Study Buddy: Let me help you with that! (AI is still learning...)")
            st.experimental_rerun()

# Sidebar for navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("<span class='icon'>📋</span> Choose a section:", unsafe_allow_html=True)
page = st.sidebar.radio(
    "Go to:",
    ("Homepage", "Goal Tracker", "Posture Detector", "Study Buddy AI Chat")
)
st.session_state.page = page

# Page rendering based on navigation
if st.session_state.page == "Homepage":
    homepage()
elif st.session_state.page == "Goal Tracker":
    goal_page()
elif st.session_state.page == "Posture Detector":
    posture_detector()
elif st.session_state.page == "Study Buddy AI Chat":
    study_buddy_chat()
