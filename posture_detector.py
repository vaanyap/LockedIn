import cv2
import mediapipe as mp
import math
import pygame

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

# Function to calculate distance between two points
def calculate_distance(point1, point2):
    """ Calculate the Euclidean distance between two points """
    return math.sqrt((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2)

def normalize_coordinates(landmark, reference_landmark):
    """ Normalize landmark position based on a reference point """
    x_normalized = (landmark.x - reference_landmark.x) / (landmark.z + 1e-6)
    y_normalized = (landmark.y - reference_landmark.y) / (landmark.z + 1e-6)
    return x_normalized, y_normalized

def detect_posture(frame):
    """ Main posture detection logic using mediapipe """
    posture_text = "Good posture"
    bad_posture = False
    
    # Mediapipe Pose detection
    with mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if results.pose_landmarks:
            nose = results.pose_landmarks.landmark[PoseLandmarks.NOSE]
            left_eye = results.pose_landmarks.landmark[PoseLandmarks.LEFT_EYE]
            right_eye = results.pose_landmarks.landmark[PoseLandmarks.RIGHT_EYE]
            left_shoulder = results.pose_landmarks.landmark[PoseLandmarks.LEFT_SHOULDER]
            right_shoulder = results.pose_landmarks.landmark[PoseLandmarks.RIGHT_SHOULDER]
            left_hip = results.pose_landmarks.landmark[PoseLandmarks.LEFT_HIP]
            right_hip = results.pose_landmarks.landmark[PoseLandmarks.RIGHT_HIP]

            # Check for bad posture based on head alignment (forward head posture)
            eye_distance = calculate_distance(left_eye, right_eye)
            nose_to_chest_distance = calculate_distance(nose, left_shoulder)

            if nose_to_chest_distance > eye_distance + 0.2:
                bad_posture = True
                posture_text = "Bad posture: Head forward"

            # Check for shoulder-hip misalignment (leaning forward)
            shoulder_distance = calculate_distance(left_shoulder, right_shoulder)
            hip_distance = calculate_distance(left_hip, right_hip)
            if shoulder_distance < hip_distance - 0.2:
                bad_posture = True
                posture_text = "Bad posture: Leaning forward"
                
        if bad_posture:
            bad_posture_sound.play()

        # Draw landmarks and posture text
        mpDrawing.draw_landmarks(image, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        cv2.putText(image, posture_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    return image, posture_text
