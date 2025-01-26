import vertexai
from vertexai.generative_models import GenerativeModel
import cv2
import mediapipe as mp
from flask import Flask, render_template, Response
import webbrowser
import pygame
import os
from threading import Thread
import importlib.util
import json
import re

# Initialize pygame for sound
pygame.mixer.init()
correct_pose_sound = pygame.mixer.Sound('src/acceptPose.mp3')
yogaMusic = pygame.mixer.Sound('src/yogaMusic.mp3')
yogaMusic.play(-1)

# Initialize Vertex AI
vertexai.init(project="lockedin-448906", location="us-central1")
model = GenerativeModel("gemini-1.5-flash-002")

# MediaPipe setup
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Global variable to store the detected pose
detected_pose = "Not in pose"

# Flask setup
app = Flask(__name__, template_folder='templates')

# Function to generate pose detection code and return both the Python code and the JSON structure
def generate_pose_detection_code(pose_name):
    prompt = f"""
    Write a Python function to detect the yoga pose '{pose_name}' using MediaPipe. The name of the function should be detect_yoga_pose.
    The function should analyze the body landmarks and return True if the pose is performed correctly, and False otherwise.
    Include checks for relevant angles and positions of the arms, legs, etc. The angle ranges should be moderately generous so users can get the pose correct relatively easily.
    
    AFTER YOU FINISH THE FUNCTION, PROVIDE A JSON-LIKE STRUCTURE DESCRIBING THE YOGA POSE LANDMARKS AND CRITERIA IN THE FOLLOWING FORMAT:
    {{
        "pose_name": "{pose_name}",
        "landmarks": {{
            "LANDMARK_NAME": {{
                "visibility": VISIBILITY_THRESHOLD,
                "x": [MIN_X, MAX_X],
                "y": [MIN_Y, MAX_Y],
                "z": [MIN_Z, MAX_Z]
            }},
            ...
        }},
        "angles": {{
            "ANGLE_NAME": {{
                "landmarks": ["LANDMARK_1", "LANDMARK_2", "LANDMARK_3"],
                "range": [MIN_ANGLE, MAX_ANGLE]
            }},
            ...
        }}
    }}
    PUT THE STRUCTURE AT THE END AFTER THE CODE. DO NOT ADD ANY EXPLANATION OR EXTRA INFO—ONLY CODE AND THE STRUCTURE.
    """
    response = model.generate_content([prompt])
    if response and response.text:
        generated_code = response.text
        print("Generated Python Code:")
        print(generated_code)
        try:
            # Split response based on structure to separate Python code and JSON
            parts = generated_code.split("```python")
            if len(parts) > 1:
                python_code_part = parts[1].split("```")[0]
            else:
                python_code_part = ""

            # Extract JSON structure from the rest of the response
            json_structure_start = generated_code.find("{")
            json_structure_end = generated_code.rfind("}") + 1
            json_string = generated_code[json_structure_start:json_structure_end]
            json_structure = json.loads(json_string)

            return python_code_part, json_structure
        except Exception as e:
            print(f"Error extracting Python code or JSON structure: {e}")
            return None, None
    return None, None

# Function to save the pose landmarks to a JSON file
def save_pose_landmarks_to_json(pose_name, json_structure):
    try:
        json_filename = f"{pose_name.replace(' ', '_').lower()}_landmarks.json"
        with open(json_filename, 'w') as json_file:
            json.dump(json_structure, json_file, indent=4)
        print(f"Pose landmarks saved to {json_filename}")
    except Exception as e:
        print(f"Error saving JSON file: {e}")

# Video frame generator for Flask streaming
def generate_frames(pose_detection_function):
    cap = cv2.VideoCapture(0)
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        global detected_pose
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Ensure the image is of the expected type and shape
            if isinstance(image, np.ndarray) and len(image.shape) == 3:
                results = pose.process(image)

                # Detect the pose (assuming you have a detect_yoga_pose function)
                if detect_yoga_pose(image):
                    detected_pose = "Pose detected"
                else:
                    detected_pose = "Not in pose"

            # Encode the frame in JPEG for streaming
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                break

            # Yield the frame for Flask streaming
            frame_bytes = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


# Flask route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Flask route to stream video frames
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(pose_detection_function), mimetype='multipart/x-mixed-replace; boundary=frame')

# Function to dynamically import a module from a file
def import_pose_detection_module(module_path):
    spec = importlib.util.spec_from_file_location("generated_pose_detection", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.detect_yoga_pose

# Function to run the Flask server in a separate thread
def run_flask():
    app.run(debug=False, use_reloader=False)

# Main logic
if __name__ == "__main__":
    pose_name = input("Enter Yoga Pose Name (e.g., 'Warrior II Pose'): ")

    generated_code, json_structure = generate_pose_detection_code(pose_name)
    if not generated_code or not json_structure:
        print("Error generating pose detection code or extracting JSON structure. Please try again.")
        exit(1)

    # Save the generated code to a Python file
    generated_code_path = "generated_pose_detection.py"
    if generated_code:
        with open(generated_code_path, "w") as file:
            file.write(generated_code)

    # Save the structure to a JSON file
    if json_structure:
        save_pose_landmarks_to_json(pose_name, json_structure)

    # Import the generated pose detection function
    try:
        pose_detection_function = import_pose_detection_module(generated_code_path)
    except Exception as e:
        print(f"Error importing generated pose detection code: {e}")
        exit(1)

    # Start Flask server in a new thread
    thread = Thread(target=run_flask)
    thread.start()

    # Open the browser to the Flask app
    url = "http://127.0.0.1:5000/"
    webbrowser.open(url)

    # This part should run until the app is closed
    thread.join()
