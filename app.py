

# import streamlit as st
# from streamlit.components.v1 import html
# import requests
# import time

# # Apply the custom gradient background using HTML and CSS
# st.markdown(
#     """
#     <style>
#     body {
#         background: rgb(28,81,167);
#         background: -moz-linear-gradient(45deg, rgba(28,81,167,1) 0%, rgba(103,184,168,1) 65%, rgba(217,230,221,1) 100%);
#         background: -webkit-linear-gradient(45deg, rgba(28,81,167,1) 0%, rgba(103,184,168,1) 65%, rgba(217,230,221,1) 100%);
#         background: linear-gradient(45deg, rgba(28,81,167,1) 0%, rgba(103,184,168,1) 65%, rgba(217,230,221,1) 100%);
#         filter: progid:DXImageTransform.Microsoft.gradient(startColorstr="#1c51a7",endColorstr="#d9e6dd",GradientType=1); /* For IE */
#         font-family: 'Helvetica', 'Arial', sans-serif;
#         color: #333;
#     }

#     /* Styling buttons */
#     .stButton>button {
#         background-color: #4F8DF7;
#         color: white;
#         border-radius: 8px;
#         padding: 10px 20px;
#         font-size: 16px;
#         transition: background-color 0.3s ease;
#     }

#     .stButton>button:hover {
#         background-color: #7cb3f5;
#     }

#     /* Heading styling */
#     h1, h2, h3 {
#         color: #2C3E50;
#     }

#     .stMarkdown {
#         color: #34495E;
#     }

#     .stTextInput input, .stTextArea textarea {
#         background-color: #ecf3f8;
#         border-radius: 8px;
#         border: 1px solid #ccc;
#         color: #333;
#     }

#     .stTextInput input:focus, .stTextArea textarea:focus {
#         border-color: #4F8DF7;
#         box-shadow: 0 0 5px rgba(79,141,247,0.5);
#     }
#     </style>
#     """, unsafe_allow_html=True
# )

# # Define the Flask Backend URL
# FLASK_BACKEND_URL = "http://127.0.0.1:5000"  # Update this to your actual backend URL

# # Streamlit App
# st.title("🏠 Welcome to Study Hub")
# st.write("Navigate through the features below to track your goals, monitor posture, and chat with AI.")

# # POSTURE STUFF
# # Function to start the posture detection and display the timer countdown
# def start_posture_detection():
#     global timer_placeholder  # Use the global variable for timer_placeholder
    
#     # Display Posture Detection UI
#     video_html = f"""
#         <div style="text-align: center;">
#             <h2>Posture Detection Feed</h2>
#             <img src="{FLASK_BACKEND_URL}/video_feed" width="800" alt="Posture Detection Video Feed" />
#         </div>
#     """
#     html(video_html, height=700)
    
#     # Start countdown if timer is set
#     while st.session_state.study_timer > 0 and st.session_state.study_timer_running:
#         minutes = st.session_state.study_timer // 60
#         seconds = st.session_state.study_timer % 60
#         st.session_state.study_timer -= 1

#         # Clear the previous timer output and display the updated timer in place
#         timer_placeholder.empty()  # Clears the previous timer
#         timer_placeholder.write(f"Study Timer: {minutes:02d}:{seconds:02d}")
        
#         # Decrease the timer by one second and update every second
#         time.sleep(1)  # Add a delay for real-time countdown

#     if st.session_state.study_timer == 0:
#         timer_placeholder.write("Timer Finished!")
#         st.session_state.study_timer_running = False
#         st.session_state.detection_status = "paused"  # Stop posture detection when the timer finishes
#         stop_posture_detection()  # Ensure posture detection is stopped when timer ends

# # Initialize session state
# if "detection_status" not in st.session_state:
#     st.session_state.detection_status = "stopped"  # Default state: "stopped"
# if "study_timer" not in st.session_state:
#     st.session_state.study_timer = 0  # Default timer duration
# if "study_timer_running" not in st.session_state:  # Initialize the timer running state
#     st.session_state.study_timer_running = False
# if 'study_timer_set' not in st.session_state:  # Initialize the timer set state
#     st.session_state.study_timer_set = False

# # Define the global timer_placeholder
# timer_placeholder = st.empty()  # Initialize it at the top

# # Function to handle timer input and display
# def study_timer_input():
#     # Display input field for timer only if posture detection isn't paused
#     if st.session_state.detection_status != "paused":
#         time_input = st.text_input("Enter study time (in minutes):", value="", key="study_timer_input")

#         if time_input:
#             # Set the session state to reflect the entered time
#             st.session_state.study_timer = int(time_input) * 60  # Convert to seconds
#             st.session_state.study_timer_set = True  # Flag that time is set

#             st.write(f"Study timer set for {time_input} minutes.")  # Confirm the set time

#     # If timer is set, show the countdown
#     if st.session_state.study_timer_set and st.session_state.study_timer > 0:
#         minutes = st.session_state.study_timer // 60
#         seconds = st.session_state.study_timer % 60
#         timer_display = f"Study Timer: {minutes:02d}:{seconds:02d}"

#         # Display timer above the posture detection section
#         st.write(timer_display)


# # Function to stop posture detection
# def stop_posture_detection():
#     # Simulate pressing "q" in the backend
#     requests.get(f"{FLASK_BACKEND_URL}/stop_posture_detection")
#     st.session_state.detection_status = "stopped"
#     st.write("Posture detection paused!")
#     st.session_state.study_timer_running = False  # Ensure timer stops when posture is paused
#     st.rerun()  # Trigger a UI update

# # Function to resume posture detection
# def resume_posture_detection():
#     # Simulate restarting the posture detection backend process
#     st.session_state.detection_status = "running"
#     st.write("Posture detection resumed!")
#     st.rerun()  # Trigger a UI update

# # Isolate the buttons in columns (just one pair of columns for clarity)
# col1, col2 = st.columns([1, 1])  # Equal width for both columns

# # Button logic
# with col1:
#     # Display the "Resume" button if posture detection is paused
#     if st.session_state.detection_status == "paused":
#         if st.button("Resume Posture Detection", key="resume_button"):
#             resume_posture_detection()

# with col2:
#     # Display the "Pause" button if posture detection is running
#     if st.session_state.detection_status == "running":
#         if st.button("Pause Posture Detection", key="pause_button"):
#             stop_posture_detection()

# # Display "Start" button only when posture detection is stopped and timer is not running
# if st.session_state.detection_status == "stopped" and not st.session_state.study_timer_running:
#     start_button = st.button("Start Posture Detection", key="start_button")
#     if start_button:
#         st.session_state.detection_status = "running"
#         st.session_state.study_timer_running = True  # Ensure the timer runs
#         st.rerun()  # Trigger UI update

# # Ensure the video feed is shown only if posture detection is running
# if st.session_state.detection_status == "running":
#     start_posture_detection()

# # Study Timer input field and functionality
# study_timer_input()  # Allow the user to input timer duration and control the timer







import streamlit as st
from streamlit.components.v1 import html
import requests
import time

# Apply the custom gradient background using HTML and CSS
st.markdown(
    """
    <style>
    body {
        background: rgb(28,81,167);
        background: -moz-linear-gradient(45deg, rgba(28,81,167,1) 0%, rgba(103,184,168,1) 65%, rgba(217,230,221,1) 100%);
        background: -webkit-linear-gradient(45deg, rgba(28,81,167,1) 0%, rgba(103,184,168,1) 65%, rgba(217,230,221,1) 100%);
        background: linear-gradient(45deg, rgba(28,81,167,1) 0%, rgba(103,184,168,1) 65%, rgba(217,230,221,1) 100%);
        filter: progid:DXImageTransform.Microsoft.gradient(startColorstr="#1c51a7",endColorstr="#d9e6dd",GradientType=1); /* For IE */
        font-family: 'Helvetica', 'Arial', sans-serif;
        color: #333;
    }

    /* Styling buttons */
    .stButton>button {
        background-color: #4F8DF7;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        transition: background-color 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #7cb3f5;
    }

    /* Heading styling */
    h1, h2, h3 {
        color: #2C3E50;
    }

    .stMarkdown {
        color: #34495E;
    }

    .stTextInput input, .stTextArea textarea {
        background-color: #ecf3f8;
        border-radius: 8px;
        border: 1px solid #ccc;
        color: #333;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #4F8DF7;
        box-shadow: 0 0 5px rgba(79,141,247,0.5);
    }
    </style>
    """, unsafe_allow_html=True
)

# Define the Flask Backend URL
FLASK_BACKEND_URL = "http://127.0.0.1:5000"  # Update this to your actual backend URL

# Streamlit App
st.title("🏠 Welcome to Study Hub")
st.write("Navigate through the features below to track your goals, monitor posture, and chat with AI.")

# POSTURE STUFF
# Function to start the posture detection and display the timer countdown
def start_posture_detection():
    global timer_placeholder  # Use the global variable for timer_placeholder
    
    # Display Posture Detection UI
    video_html = f"""
        <div style="text-align: center;">
            <h2>Posture Detection Feed</h2>
            <img src="{FLASK_BACKEND_URL}/video_feed" width="800" alt="Posture Detection Video Feed" />
        </div>
    """
    html(video_html, height=700)
    
    # Start countdown if timer is set
    while st.session_state.study_timer > 0 and st.session_state.study_timer_running:
        minutes = st.session_state.study_timer // 60
        seconds = st.session_state.study_timer % 60
        st.session_state.study_timer -= 1

        # Clear the previous timer output and display the updated timer in place
        timer_placeholder.empty()  # Clears the previous timer
        timer_placeholder.write(f"Study Timer: {minutes:02d}:{seconds:02d}")
        
        # Decrease the timer by one second and update every second
        time.sleep(1)  # Add a delay for real-time countdown

    if st.session_state.study_timer == 0:
        timer_placeholder.write("Timer Finished!")
        st.session_state.study_timer_running = False
        st.session_state.detection_status = "paused"  # Stop posture detection when the timer finishes
        stop_posture_detection()  # Ensure posture detection is stopped when timer ends

# Initialize session state
if "detection_status" not in st.session_state:
    st.session_state.detection_status = "stopped"  # Default state: "stopped"
if "study_timer" not in st.session_state:
    st.session_state.study_timer = 0  # Default timer duration
if "study_timer_running" not in st.session_state:  # Initialize the timer running state
    st.session_state.study_timer_running = False
if 'study_timer_set' not in st.session_state:  # Initialize the timer set state
    st.session_state.study_timer_set = False

# Define the global timer_placeholder
timer_placeholder = st.empty()  # Initialize it at the top

# Function to handle timer input and display
def study_timer_input():
    # Display input field for timer only if posture detection isn't paused
    if st.session_state.detection_status != "paused":
        time_input = st.text_input("Enter study time (in minutes):", value="", key="study_timer_input")

        if time_input:
            # Set the session state to reflect the entered time
            st.session_state.study_timer = int(time_input) * 60  # Convert to seconds
            st.session_state.study_timer_set = True  # Flag that time is set

            st.write(f"Study timer set for {time_input} minutes.")  # Confirm the set time

    # If timer is set, show the countdown
    if st.session_state.study_timer_set and st.session_state.study_timer > 0:
        minutes = st.session_state.study_timer // 60
        seconds = st.session_state.study_timer % 60
        timer_display = f"Study Timer: {minutes:02d}:{seconds:02d}"

        # Display timer above the posture detection section
        st.write(timer_display)


# Function to stop posture detection
def stop_posture_detection():
    # Simulate pressing "q" in the backend
    requests.get(f"{FLASK_BACKEND_URL}/stop_posture_detection")
    st.session_state.detection_status = "stopped"
    st.write("Posture detection paused!")
    st.session_state.study_timer_running = False  # Ensure timer stops when posture is paused
    st.rerun()  # Trigger a UI update

# Function to resume posture detection
def resume_posture_detection():
    # Simulate restarting the posture detection backend process
    st.session_state.detection_status = "running"
    st.write("Posture detection resumed!")
    st.rerun()  # Trigger a UI update

# Isolate the buttons in columns (just one pair of columns for clarity)
col1, col2 = st.columns([1, 1])  # Equal width for both columns

# Button logic
with col1:
    # Display the "Resume" button if posture detection is paused
    if st.session_state.detection_status == "paused":
        if st.button("Resume Posture Detection", key="resume_button"):
            resume_posture_detection()

with col2:
    # Display the "Pause" button if posture detection is running
    if st.session_state.detection_status == "running":
        if st.button("Pause Posture Detection", key="pause_button"):
            stop_posture_detection()

# Display "Start" button only when posture detection is stopped and timer is not running
if st.session_state.detection_status == "stopped" and not st.session_state.study_timer_running:
    start_button = st.button("Start Posture Detection", key="start_button")
    if start_button:
        st.session_state.detection_status = "running"
        st.session_state.study_timer_running = True  # Ensure the timer runs
        st.rerun()  # Trigger UI update

# Ensure the video feed is shown only if posture detection is running
if st.session_state.detection_status == "running":
    start_posture_detection()

# Study Timer input field and functionality
study_timer_input()  # Allow the user to input timer duration and control the timer
