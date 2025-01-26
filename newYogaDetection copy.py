import cv2
import mediapipe as mp
from flask import Flask, render_template, Response
import pygame
import random
import math
import webbrowser

# Initialize pygame for sound and music
pygame.mixer.init()

# Load sounds
correct_pose_sound = pygame.mixer.Sound('src/acceptPose.mp3')
yogaMusic = pygame.mixer.Sound('src/yogaMusic.mp3')
yogaMusic.play()  # Start the yoga music

# Flask app setup
app = Flask(__name__, template_folder='template')

# Mediapipe setup
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# List of yoga poses
yoga_poses = [
    "Warrior II",
    "Tree Pose",
    "Downward Dog",
    "Mountain Pose",
    "Child's Pose",
    "Cobra Pose",
]

# Function to calculate the angle between three points
def calculate_angle(a, b, c):
    a = (a.x, a.y)
    b = (b.x, b.y)
    c = (c.x, c.y)
    angle = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    angle = abs(angle)
    return angle if angle <= 180 else 360 - angle

# Yoga pose detection logic for Warrior II
def detect_warrior_ii(landmarks, visibility_threshold=0.5):
    """
    Detect the Warrior II yoga pose ensuring visibility of key landmarks for both sides of the body.
    """
    # Critical landmarks for both sides
    critical_landmarks_left = [
        mp_pose.PoseLandmark.LEFT_SHOULDER.value,
        mp_pose.PoseLandmark.LEFT_ELBOW.value,
        mp_pose.PoseLandmark.LEFT_WRIST.value,
        mp_pose.PoseLandmark.LEFT_HIP.value,
        mp_pose.PoseLandmark.LEFT_KNEE.value,
        mp_pose.PoseLandmark.LEFT_ANKLE.value,
    ]
    
    critical_landmarks_right = [
        mp_pose.PoseLandmark.RIGHT_SHOULDER.value,
        mp_pose.PoseLandmark.RIGHT_ELBOW.value,
        mp_pose.PoseLandmark.RIGHT_WRIST.value,
        mp_pose.PoseLandmark.RIGHT_HIP.value,
        mp_pose.PoseLandmark.RIGHT_KNEE.value,
        mp_pose.PoseLandmark.RIGHT_ANKLE.value,
    ]

    # Ensure critical landmarks are visible for either side
    for landmark in critical_landmarks_left + critical_landmarks_right:
        if landmarks[landmark].visibility < visibility_threshold:
            return False  # Skip if any critical landmark is not visible

    # Calculate angles for left side
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
    left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
    left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]

    left_shoulder_angle = calculate_angle(left_hip, left_shoulder, left_elbow)
    left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
    left_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)

    # Calculate angles for right side
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
    right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
    right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
    right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]

    right_shoulder_angle = calculate_angle(right_hip, right_shoulder, right_elbow)
    right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
    right_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)

    # Relaxed thresholds for Warrior II pose for both sides
    if ((80 <= left_shoulder_angle <= 110 and 110 <= left_elbow_angle <= 190 and 50 <= left_knee_angle <= 160) or
        (80 <= right_shoulder_angle <= 110 and 110 <= right_elbow_angle <= 190 and 50 <= right_knee_angle <= 160)):
        correct_pose_sound.play()
        return True

    return False

# Function to select pose via terminal
def select_pose():
    print("Please choose a yoga pose from the following list:")
    for i, pose in enumerate(yoga_poses, 1):
        print(f"{i}. {pose}")
    
    selected_pose_idx = int(input("Enter the number of your selected pose: ")) - 1
    if 0 <= selected_pose_idx < len(yoga_poses):
        return yoga_poses[selected_pose_idx]
    else:
        print("Invalid choice. Defaulting to Warrior II Pose.")
        return "Warrior II"

# Video frame generator for pose detection
def generate_frames(selected_pose):
    cap = cv2.VideoCapture(0)
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                continue

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            pose_text = "Not in pose"
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                # Check for the selected pose
                if selected_pose == "Warrior II" and detect_warrior_ii(landmarks):
                    pose_text = "Warrior II Pose Detected!"
                    correct_pose_sound.play()  # Play sound when correct pose is detected
                # Add checks for other poses as well, using their detection functions

            # Draw landmarks
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            image = cv2.flip(image, 1)
            cv2.putText(image, pose_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # Encode frame to JPEG
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

# Web app routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(selected_pose), mimetype='multipart/x-mixed-replace; boundary=frame')

# Start the Flask app after user input
if __name__ == "__main__":
    # Prompt user for pose selection
    selected_pose = select_pose()

    # Open the web browser after pose is selected
    url = "http://127.0.0.1:5000/"
    webbrowser.open(url)

    # Start Flask app
    app.run(debug=True)
