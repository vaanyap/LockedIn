import streamlit as st
from posture_detector import posture_detector
from ai_assistant import study_buddy_chat
from goal_page import goal_page

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

        .auth-container {
            text-align: center;
            margin-top: 40px;
        }

        .form-container {
            background-color: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border-radius: 10px;
            width: 80%;
            max-width: 400px;
            margin: 20px auto;
        }

        .form-container h3 {
            color: #333;
            font-size: 1.5em;
            margin-bottom: 20px;
        }

        input[type='text'], input[type='email'], input[type='password'] {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            border: 1px solid #ddd;
            font-size: 1.1em;
        }

        .auth-button {
            background-color: #4ca2cd;
            color: white;
            border: none;
            padding: 10px;
            width: 100%;
            border-radius: 5px;
            font-size: 1.1em;
            cursor: pointer;
        }

        .auth-button:hover {
            background-color: #67b26f;
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

    </style>
    """,
    unsafe_allow_html=True
)

# Navigation setup using Streamlit's st.session_state
if "page" not in st.session_state:
    st.session_state.page = "Homepage"
if "auth_state" not in st.session_state:
    st.session_state.auth_state = None
if "user" not in st.session_state:
    st.session_state.user = None  # Track the logged-in user

# Sidebar for navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("<span class='sidebar-title'>📋 Choose a section:</span>", unsafe_allow_html=True)
page = st.sidebar.radio(
    "Go to:",
    ("Homepage", "Goal Tracker", "Posture Detector", "Study Buddy AI Chat"),
    label_visibility="collapsed"  # hides label for a cleaner look
)
st.session_state.page = page

# Define homepage function
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

    # If user is not logged in, show Sign In / Sign Up options
    if not st.session_state.user:
        st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1], gap="large")

        with col1:
            if st.button("Sign In", key="sign_in_button", help="Click to sign in", use_container_width=True):
                st.session_state.auth_state = "sign_in"

        with col2:
            if st.button("Sign Up", key="sign_up_button", help="Click to sign up", use_container_width=True):
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
    else:
        st.markdown("<div class='content'>Welcome back, {}</div>".format(st.session_state.user), unsafe_allow_html=True)

# Main page rendering logic based on selected navigation
if st.session_state.page == "Homepage":
    homepage()
elif st.session_state.page == "Goal Tracker":
    goal_page()
elif st.session_state.page == "Posture Detector":
    posture_detector()
elif st.session_state.page == "Study Buddy AI Chat":
    study_buddy_chat()
