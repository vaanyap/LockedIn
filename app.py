import streamlit as st
from utils import show_home, show_goal_setting, show_posture_stretch, show_ai_assistant

def main():
    st.set_page_config(page_title="Study Hub", page_icon="📚", layout="centered")
    
    # Set background image
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url('assets/background.png');
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Navbar - pages
    page = st.sidebar.radio("Choose a Page", ("Home", "Goal Setting", "Posture & Stretch", "AI Assistant"))
    
    if page == "Home":
        show_home()
    elif page == "Goal Setting":
        show_goal_setting()
    elif page == "Posture & Stretch":
        show_posture_stretch()
    elif page == "AI Assistant":
        show_ai_assistant()

if __name__ == "__main__":
    main()
