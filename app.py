

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
from goal_page import goal_page

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

    /* Basic button styling */
    .stButton>button {
        background-color: #4F8DF7;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        transition: background-color 0.3s ease;
        border: none;
    }

    .stButton>button:hover {
        background-color: #7cb3f5;
    }


    /* Heading styling */
    h1, h2, h3 {
        color: #2C3E50; /* Darker for headings */
    }

    .stMarkdown {
        color: #34495E; /* Modern, subtle text color for markdown */
    }

    .stTextInput input, .stTextArea textarea {
        background-color: #ecf3f8; /* Soft light background for text input */
        border-radius: 8px;
        border: 1px solid #ccc;
        color: #333;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #4F8DF7;
        box-shadow: 0 0 5px rgba(79,141,247,0.5);
    }

    /* Card-like containers */
    .stCard {
        background: rgba(255, 255, 255, 0.85);
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }

    /* Divider styles */
    .section-divider {
        border: 0;
        border-top: 2px solid #4F8DF7;
        margin: 40px 0;
    }

    </style>
    """, unsafe_allow_html=True
)


# Define the Flask Backend URL
FLASK_BACKEND_URL = "http://127.0.0.1:5000"  # Update this to your actual backend URL



# Streamlit App
st.title("Are you LockedIn?👩‍💻")
st.write("Your all-in-one study assistant. Stay focused, track your goals, and monitor your progress with ease.")

# Custom CSS for styling
st.markdown(
    """
    <style>
    /* Sidebar Styling */
    .sidebar h1 {
        font-size: 45px; 
        color: #000; 
        margin-bottom: 30px; 
        text-align: left;
    }

    .sidebar a {
        font-size: 18px;
        color: white;
        text-decoration: none;
        margin-bottom: 15px;
        display: block;
        padding: 8px;
        border-radius: 5px;
        transition: background-color 0.3s;
    }

    .sidebar a:hover {
        background-color: #4F8DF7;
    }

    /* Fixing anchor positioning */
    .anchor-offset {
        position: relative;
        top: -40px;
    }
    
    

    </style>
    """,
    unsafe_allow_html=True,
)

# Add Smooth Scrolling JavaScript
st.markdown(
    """
    <script>
    document.querySelectorAll('.sidebar a').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
    </script>
    """,
    unsafe_allow_html=True
)
# Add custom CSS to remove underline from links
st.markdown("""
    <style>
        .css-1q6p5i8 a {
            text-decoration: none !important; /* Force remove underline */
        }

        .css-1q6p5i8 a:hover {
            text-decoration: none !important; /* Ensure no underline on hover */
            background-color: #4F8DF7;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar layout
with st.sidebar:
    st.markdown('<div class="sidebar"><h1>LockedIn 👩‍💻</h1></div>', unsafe_allow_html=True)
    st.markdown('<a href="#goal-tracker" class="sidebar">🎯 Goal Tracker</a>', unsafe_allow_html=True)
    st.markdown('<a href="#posture-monitor" class="sidebar">📏 Posture Monitor</a>', unsafe_allow_html=True)
    st.markdown('<a href="#study-buddy-ai-chat" class="sidebar">🤖 Study Buddy AI Chat</a>', unsafe_allow_html=True)


# Info Section for the Study Hub
st.markdown(
    """
    <div class="stCard" id="e23268dd">
        <h2>Why Study Hub?</h2>
        <p>LockedIn is your personalized study companion designed to help you stay organized, track progress, and optimize focus. With a variety of tools like goal tracking, posture detection, and an AI study assistant, you’ll have everything you need to succeed academically.</p>
    </div>
    """, unsafe_allow_html=True
)

# Add a section divider here
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

#goal tracker
st.header("🎯 Goal Tracker", anchor="goal-tracker")
st.write("Track your academic goals and set reminders to stay on track.")
goal_page()


# Add a section divider here
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)





# Posture Monitor Section
st.header("📏 Posture Monitor", anchor="posture-monitor")
st.markdown('<div id="baf9c496"></div>', unsafe_allow_html=True)


# POSTURE STUFF
# Function to start the posture detection and display the timer countdown
def start_posture_detection():
    st.markdown("", unsafe_allow_html=True)
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




# Add a section divider here
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# Study Buddy AI Chat Section
st.header("🤖 Study Buddy AI Chat", anchor="study-buddy-ai-chat")
st.write("Chat with Echo, your AI study assistant, to get personalized help with academic queries.")
st.markdown('<div id="d3f4e54a"></div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="stCard">
        <h3>What Echo Can Do:</h3>
        <ul>
        <li>Answer academic questions and provide explanations on a variety of topics.</li>
        <li>Assist with research and offer suggestions for study techniques.</li>
        <li>Provide motivation and reminders to help you stay focused.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True
)

# Add a section divider here
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# Posture Detection Server Code (Flask integration)
from flask import Flask, Response, render_template_string
import cv2
from posture_detector import detect_posture # Import your posture detection function

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Mediapipe Pose Detection</title>
    <style>
        body {
        background: rgb(28,81,167);
            background: -moz-linear-gradient(45deg, rgba(28,81,167,1) 0%, rgba(103,184,168,1) 65%, rgba(217,230,221,1) 100%);
            background: -webkit-linear-gradient(45deg, rgba(28,81,167,1) 0%, rgba(103,184,168,1) 65%, rgba(217,230,221,1) 100%);
            background: linear-gradient(45deg, rgba(28,81,167,1) 0%, rgba(103,184,168,1) 65%, rgba(217,230,221,1) 100%);
            filter: progid:DXImageTransform.Microsoft.gradient(startColorstr="#1c51a7",endColorstr="#d9e6dd",GradientType=1); /* For IE */
            font-family: 'Helvetica', 'Arial', sans-serif;
            color: #333;
            margin: 0;
            padding: 0;
            text-align: center;
        }

        h1 {
            font-size: 2.5em;
            font-weight: bold;
            color: #FFF;
            padding: 30px 0;
        }

        img {
            border: 5px solid #4ca2cd;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }

        .content {
            font-size: 1.1em;
            color: #FFF;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <h1>Pose Detection Feed</h1>
    <div class="content">
        <p>Ensure you maintain good posture while studying or working. Use this live feed to monitor and improve your posture.</p>
    </div>
    <img src="/video_feed" width="800" alt="Pose Detection Video Feed" />
</body>
</html>
"""

@app.route('/')
def index():
    # Render the styled HTML template
    return render_template_string(HTML_TEMPLATE)

@app.route('/video_feed')
def video_feed():
    cap = cv2.VideoCapture(0)

    def generate():
        while True:
            success, frame = cap.read()
            if not success:
                break

            # Perform posture detection
            frame, posture_text = detect_posture(frame)

        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    cap.release()
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)