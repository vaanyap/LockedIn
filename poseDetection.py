import cv2
import mediapipe as mp
from flask import Flask, render_template, Response
import math
import pygame
import time

# Initialize pygame mixer for sound
pygame.mixer.init()

# Load the sound file (use a `.wav` or `.mp3` file)
bad_posture_sound = pygame.mixer.Sound('src/ding.wav')  # Replace with your sound file path

# Mediapipe setup
mpDrawing = mp.solutions.drawing_utils
mpPose = mp.solutions.pose

# PoseLandmarks class for easy reference to landmarks
class PoseLandmarks:
    NOSE = 0
    LEFT_EYE = 1
    RIGHT_EYE = 2
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_HIP = 23
    RIGHT_HIP = 24

# Flask app
app = Flask(__name__, template_folder='template')

# Function to calculate distance between two points
def calculate_distance(point1, point2):
    """
    Calculate the Euclidean distance between two points.
    If the points are normalized, we'll adjust the calculation accordingly.
    """
    if isinstance(point1, tuple) and isinstance(point2, tuple):  # for normalized tuples
        return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
    else:  # for landmark objects
        return math.sqrt((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2)

def normalize_coordinates(landmark, reference_landmark):
    """
    Normalize the landmark's position based on the reference landmark.
    This will reduce the effect of perspective by comparing distances relative to a reference point.
    """
    # Normalize by the z-coordinate (depth) to account for perspective
    x_normalized = (landmark.x - reference_landmark.x) / (landmark.z + 1e-6)
    y_normalized = (landmark.y - reference_landmark.y) / (landmark.z + 1e-6)
    return x_normalized, y_normalized

# Timer variables
posture_timer = 0
posture_timeout = 3  # Time in seconds for how long bad posture must be detected to trigger sound
posture_is_bad = False

# Video frame generator
def generate_frames():
    global posture_timer, posture_is_bad  # Use global variables to track posture state
    cap = cv2.VideoCapture(0)
    with mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Mediapipe processing
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Check for bad posture
            bad_posture = False
            posture_text = "Good posture"

            if results.pose_landmarks:
                # Get landmarks for relevant body parts
                nose = results.pose_landmarks.landmark[PoseLandmarks.NOSE]
                left_eye = results.pose_landmarks.landmark[PoseLandmarks.LEFT_EYE]
                right_eye = results.pose_landmarks.landmark[PoseLandmarks.RIGHT_EYE]
                left_shoulder = results.pose_landmarks.landmark[PoseLandmarks.LEFT_SHOULDER]
                right_shoulder = results.pose_landmarks.landmark[PoseLandmarks.RIGHT_SHOULDER]
                left_hip = results.pose_landmarks.landmark[PoseLandmarks.LEFT_HIP]
                right_hip = results.pose_landmarks.landmark[PoseLandmarks.RIGHT_HIP]

                # Normalize based on the nose position (camera reference)
                nose_normalized = normalize_coordinates(nose, nose)
                left_shoulder_normalized = normalize_coordinates(left_shoulder, nose)
                right_shoulder_normalized = normalize_coordinates(right_shoulder, nose)

                # Calculate eyebrow (eye and nose) distance
                eye_distance = calculate_distance(left_eye, right_eye)
                eyebrow_to_chest_distance = calculate_distance(nose, left_shoulder)  # Approximate chest position

                # Adjust bad posture detection by checking normalized distances
                if eyebrow_to_chest_distance > eye_distance + 0.2:
                    bad_posture = True
                    posture_text = "Bad posture: Head forward"

                # Shoulder-hip alignment check using normalized coordinates
                shoulder_distance = calculate_distance(left_shoulder_normalized, right_shoulder_normalized)
                hip_distance = calculate_distance(left_hip, right_hip)
                if shoulder_distance < hip_distance - 0.2:
                    bad_posture = True
                    posture_text = "Bad posture: Leaning forward"

            # Posture timer logic
            if bad_posture:
                posture_timer += 1  # Increase timer if posture is bad
                if posture_timer >= posture_timeout:  # If posture is bad for a certain time
                    if not posture_is_bad:  # Trigger sound only once
                        posture_is_bad = True
                        bad_posture_sound.play()
            else:
                posture_timer = 0  # Reset timer if posture is good
                posture_is_bad = False

            # Draw landmarks on the frame
            mpDrawing.draw_landmarks(
                image, 
                results.pose_landmarks, 
                mpPose.POSE_CONNECTIONS,
                mpDrawing.DrawingSpec(color=(245, 117, 66), thickness=3, circle_radius=2),
                mpDrawing.DrawingSpec(color=(245, 66, 230), thickness=3, circle_radius=2)
            )

            # Add the posture text on the frame
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(image, posture_text, (50, 50), font, 1, (255, 0, 0), 2, cv2.LINE_AA)

            # Encode frame to JPEG format
            ret, buffer = cv2.imencode('.jpg', image)
            if not ret:
                continue
            frame = buffer.tobytes()

            # Yield the frame in a Flask-compatible format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/')
def index():
    # Render the HTML template
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    # Route for video feed
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
