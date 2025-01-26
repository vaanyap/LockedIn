import cv2
import mediapipe as mp
from flask import Flask, render_template, Response
import math
import pygame
import webbrowser

pygame.mixer.init()

# Mediapipe setup
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

correct_pose_sound = pygame.mixer.Sound('src/acceptPose.mp3')
yogaMusic = pygame.mixer.Sound('src/yogaMusic.mp3')
yogaMusic.play()

# Flask app
app = Flask(__name__, template_folder='template')

# Function to calculate the angle between three points
def calculate_angle(a, b, c):
    """
    Calculate the angle between three points (a, b, c).
    """
    a = (a.x, a.y)
    b = (b.x, b.y)
    c = (c.x, c.y)
    angle = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    angle = abs(angle)  # Ensure the angle is positive
    return angle if angle <= 180 else 360 - angle

# Yoga pose detection logic
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


# Video frame generator
def generate_frames():
    cap = cv2.VideoCapture(0)
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Mediapipe processing
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Check for yoga pose
            pose_text = "Not in pose"
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                if detect_warrior_ii(landmarks):
                    pose_text = "Warrior II Pose Detected!"

            # Draw landmarks and text
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(66, 245, 230), thickness=2, circle_radius=2),
            )

            image = cv2.flip(image, 1)
            cv2.putText(image, pose_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # Encode frame to JPEG
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    url = "http://127.0.0.1:5000/"
    webbrowser.open(url)
    app.run(debug=True)
