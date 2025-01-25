import cv2
import mediapipe as mp
import pygame
import time
import math
from flask import Flask, render_template, Response
import numpy as np

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
app.config["ENV"] = "production"

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
phone_looking_threshold = 0.1  # Adjust this threshold based on trial and error
phone_detected = False


pose = mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def generate_frames():
    global posture_timer, posture_is_bad  # Use global variables to track posture state
    cap = cv2.VideoCapture(0)

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
            try:
                nose = results.pose_landmarks.landmark[PoseLandmarks.NOSE]
                left_eye = results.pose_landmarks.landmark[PoseLandmarks.LEFT_EYE]
                right_eye = results.pose_landmarks.landmark[PoseLandmarks.RIGHT_EYE]
                left_shoulder = results.pose_landmarks.landmark[PoseLandmarks.LEFT_SHOULDER]
                right_shoulder = results.pose_landmarks.landmark[PoseLandmarks.RIGHT_SHOULDER]
                left_hip = results.pose_landmarks.landmark[PoseLandmarks.LEFT_HIP]
                right_hip = results.pose_landmarks.landmark[PoseLandmarks.RIGHT_HIP]
            except IndexError:
                # Skip if any landmarks are missing
                continue

            # Normalize based on the nose position (camera reference)
            left_shoulder_normalized = normalize_coordinates(left_shoulder, nose)
            right_shoulder_normalized = normalize_coordinates(right_shoulder, nose)

            # Calculate eyebrow (eye and nose) distance
            eyebrow_to_chest_distance = calculate_distance(nose, left_shoulder)  # Approximate chest position

            # Refined "Looking at Phone" detection based on head tilt (Nose to Shoulders)
            nose_to_shoulder_angle = calculate_distance(nose, left_shoulder)  # Distance between nose and shoulder
            nose_to_hip_angle = calculate_distance(nose, left_hip)  # Distance between nose and hip

            # If nose is closer to the shoulders, it could indicate that the head is tilted downward
            if nose_to_shoulder_angle < nose_to_hip_angle and eyebrow_to_chest_distance < 0.3:  # Threshold to detect tilt
                posture_text = "Bad Posture"
                bad_posture = True
                

            # Apply the check if eyes are pointing downward
            eye_angle = abs(left_eye.y - right_eye.y)
            if eye_angle > phone_looking_threshold:
                bad_posture = True
                posture_text = "Looking at phone"

            # Shoulder-hip alignment check using normalized coordinates
            shoulder_distance = calculate_distance(left_shoulder_normalized, right_shoulder_normalized)
            hip_distance = calculate_distance(left_hip, right_hip)
            if shoulder_distance < hip_distance - 0.2:  # Increased margin for leniency
                bad_posture = True
                posture_text = "Bad posture: Leaning forward"

            # New check for chin too close to chest
            chin_to_chest_distance = calculate_distance(nose, left_shoulder)
            if chin_to_chest_distance < 0.2:  # Threshold for leaning forward
                bad_posture = True
                posture_text = "Bad posture: Chin too close to chest"
                
                    

            # Apply smoothing or a small buffer before triggering posture change (optional)
            if bad_posture:
                posture_timer += 1
                if posture_timer >= posture_timeout:  # If posture is bad for the specified time
                    if not posture_is_bad:  # Trigger sound only once
                        posture_is_bad = True
                        bad_posture_sound.play()
            else:
                posture_timer = 0  # Reset timer if posture is good
                posture_is_bad = False

        # Draw landmarks on the frame (optional for debugging)
        # mpDrawing.draw_landmarks(
        #     image, 
        #     results.pose_landmarks, 
        #     mpPose.POSE_CONNECTIONS,
        #     mpDrawing.DrawingSpec(color=(245, 117, 66), thickness=3, circle_radius=2),
        #     mpDrawing.DrawingSpec(color=(245, 66, 230), thickness=3, circle_radius=2)
        # )

        image = cv2.flip(image, 1)  # 1 for horizontal flip
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
    app.run(debug=True, use_reloader=False)




























# import cv2
# import mediapipe as mp
# import pygame
# import time
# import math
# from flask import Flask, render_template, Response
# import numpy as np

# # Initialize pygame mixer for sound
# pygame.mixer.init()

# # Load the sound file (use a `.wav` or `.mp3` file)
# bad_posture_sound = pygame.mixer.Sound('src/ding.wav')  # Replace with your sound file path
# phone_detected_sound = pygame.mixer.Sound('src/ding.wav')  # Replace with your phone detected sound path

# # Mediapipe setup
# mpDrawing = mp.solutions.drawing_utils
# mpPose = mp.solutions.pose

# # PoseLandmarks class for easy reference to landmarks
# class PoseLandmarks:
#     NOSE = 0
#     LEFT_EYE = 1
#     RIGHT_EYE = 2
#     LEFT_SHOULDER = 11
#     RIGHT_SHOULDER = 12
#     LEFT_HIP = 23
#     RIGHT_HIP = 24

# # Flask app
# app = Flask(__name__, template_folder='template')
# app.config["ENV"] = "production"

# # Function to calculate distance between two points
# def calculate_distance(point1, point2):
#     if isinstance(point1, tuple) and isinstance(point2, tuple):  # for normalized tuples
#         return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
#     else:  # for landmark objects
#         return math.sqrt((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2)

# def normalize_coordinates(landmark, reference_landmark):
#     x_normalized = (landmark.x - reference_landmark.x) / (landmark.z + 1e-6)
#     y_normalized = (landmark.y - reference_landmark.y) / (landmark.z + 1e-6)
#     return x_normalized, y_normalized

# # Timer variables
# posture_timer = 0
# posture_timeout = 3  # Time in seconds for how long bad posture must be detected to trigger sound
# posture_is_bad = False
# phone_looking_threshold = 0.1  # Adjust this threshold based on trial and error

# # Flags to ensure sound plays only once
# bad_posture_played = False
# phone_detected_played = False

# def generate_frames():
#     global posture_timer, posture_is_bad, bad_posture_played, phone_detected_played  # Use global variables to track posture state
#     frame_count = 0  # Initialize frame count

#     cap = cv2.VideoCapture(0)

#     # Load YOLO
#     net = cv2.dnn.readNet("yolo/yolov3.weights", "darknet/cfg/yolov3.cfg")
#     layer_names = net.getLayerNames()
#     output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
#     with open("yolo/coco.names", "r") as f:
#         classes = [line.strip() for line in f.readlines()]

#     with mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             height, width, channels = frame.shape

#             # YOLO detection for phones
#             blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
#             net.setInput(blob)
#             outs = net.forward(output_layers)

#             phone_detected = False
#             for out in outs:
#                 for detection in out:
#                     scores = detection[5:]
#                     class_id = np.argmax(scores)
#                     confidence = scores[class_id]
#                     if confidence > 0.5:
#                         label = str(classes[class_id])
#                         if "cell phone" in label.lower() or "phone" in label.lower():
#                             phone_detected = True
#                             break

#             # Mediapipe processing
#             image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             image.flags.writeable = False
#             results = pose.process(image)
#             image.flags.writeable = True
#             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#             # Check for bad posture
#             bad_posture = False
#             posture_text = "Good posture"
#             phone_looking = False

#             if results.pose_landmarks:
#                 try:
#                     nose = results.pose_landmarks.landmark[PoseLandmarks.NOSE]
#                     left_eye = results.pose_landmarks.landmark[PoseLandmarks.LEFT_EYE]
#                     right_eye = results.pose_landmarks.landmark[PoseLandmarks.RIGHT_EYE]
#                     left_shoulder = results.pose_landmarks.landmark[PoseLandmarks.LEFT_SHOULDER]
#                     right_shoulder = results.pose_landmarks.landmark[PoseLandmarks.RIGHT_SHOULDER]
#                     left_hip = results.pose_landmarks.landmark[PoseLandmarks.LEFT_HIP]
#                     right_hip = results.pose_landmarks.landmark[PoseLandmarks.RIGHT_HIP]
#                 except IndexError:
#                     continue

#                 # Normalize based on the nose position (camera reference)
#                 nose_normalized = normalize_coordinates(nose, nose)
#                 left_shoulder_normalized = normalize_coordinates(left_shoulder, nose)
#                 right_shoulder_normalized = normalize_coordinates(right_shoulder, nose)

#                 # Calculate distances and angles
#                 eyebrow_to_chest_distance = calculate_distance(nose, left_shoulder)
#                 nose_to_shoulder_angle = calculate_distance(nose, left_shoulder)
#                 nose_to_hip_angle = calculate_distance(nose, left_hip)
#                 eye_distance = calculate_distance(left_eye, right_eye)

#                 # Detect looking at phone or bad posture
#                 if nose_to_shoulder_angle < nose_to_hip_angle and eyebrow_to_chest_distance < 0.3:
#                     phone_looking = True
#                     posture_text = "Looking at phone"
                
#                 if eye_distance > phone_looking_threshold:
#                     posture_text = "Looking at phone or bad posture"
#                     posture_timer += 1
#                     if posture_timer >= posture_timeout:
#                         if not bad_posture_played:
#                             bad_posture_played = True
#                             bad_posture_sound.play()

#                 if bad_posture:
#                     posture_timer += 1
#                     if posture_timer >= posture_timeout:
#                         if not posture_is_bad:
#                             posture_is_bad = True
#                             bad_posture_sound.play()
#                             bad_posture_played = True
#                 else:
#                     posture_timer = 0
#                     posture_is_bad = False
#                     bad_posture_played = False
#                     phone_detected_played = False  # Reset phone detection sound flag

        

#             # Flip and show the frame
#             image = cv2.flip(image, 1)
#             # Display posture feedback text on the frame
#             cv2.putText(image, posture_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)


#             ret, buffer = cv2.imencode('.jpg', image)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#     cap.release()

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == "__main__":
#     app.run(debug=True, use_reloader=False)




# import cv2
# import mediapipe as mp
# import pygame
# import time
# import math
# from flask import Flask, render_template, Response
# import numpy as np

# # Initialize pygame mixer for sound
# pygame.mixer.init()

# # Load the sound file (use a `.wav` or `.mp3` file)
# bad_posture_sound = pygame.mixer.Sound('src/ding.wav')  # Replace with your sound file path
# phone_detected_sound = pygame.mixer.Sound('src/ding.wav')
# # Mediapipe setup
# mpDrawing = mp.solutions.drawing_utils
# mpPose = mp.solutions.pose

# # PoseLandmarks class for easy reference to landmarks
# class PoseLandmarks:
#     NOSE = 0
#     LEFT_EYE = 1
#     RIGHT_EYE = 2
#     LEFT_SHOULDER = 11
#     RIGHT_SHOULDER = 12
#     LEFT_HIP = 23
#     RIGHT_HIP = 24

# # Flask app
# app = Flask(__name__, template_folder='template')
# app.config["ENV"] = "production"

# # Function to calculate distance between two points
# def calculate_distance(point1, point2):
#     """
#     Calculate the Euclidean distance between two points.
#     If the points are normalized, we'll adjust the calculation accordingly.
#     """
#     if isinstance(point1, tuple) and isinstance(point2, tuple):  # for normalized tuples
#         return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
#     else:  # for landmark objects
#         return math.sqrt((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2)

# def normalize_coordinates(landmark, reference_landmark):
#     """
#     Normalize the landmark's position based on the reference landmark.
#     This will reduce the effect of perspective by comparing distances relative to a reference point.
#     """
#     # Normalize by the z-coordinate (depth) to account for perspective
#     x_normalized = (landmark.x - reference_landmark.x) / (landmark.z + 1e-6)
#     y_normalized = (landmark.y - reference_landmark.y) / (landmark.z + 1e-6)
#     return x_normalized, y_normalized

# # Timer variables
# posture_timer = 0
# posture_timeout = 3  # Time in seconds for how long bad posture must be detected to trigger sound
# posture_is_bad = False
# phone_looking_threshold = 0.1  # Adjust this threshold based on trial and error
# phone_detected_played = False

# def generate_frames():
#     global posture_timer, posture_is_bad  # Use global variables to track posture state
#     cap = cv2.VideoCapture(0)

#     # Load YOLO
#     net = cv2.dnn.readNet("yolo/yolov3.weights", "darknet/cfg/yolov3.cfg")
#     layer_names = net.getLayerNames()
#     output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
#     with open("yolo/coco.names", "r") as f:
#         classes = [line.strip() for line in f.readlines()]
#     with mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             # Mediapipe processing
#             image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             image.flags.writeable = False
#             results = pose.process(image)
#             image.flags.writeable = True
#             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#  # YOLO detection for phones
#             blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
#             net.setInput(blob)
#             outs = net.forward(output_layers)

#             phone_detected = False
#             for out in outs:
#                 for detection in out:
#                     scores = detection[5:]
#                     class_id = np.argmax(scores)
#                     confidence = scores[class_id]
#                     if confidence > 0.5:
#                         label = str(classes[class_id])
#                         if "cell phone" in label.lower() or "phone" in label.lower():
#                             phone_detected = True
#                             break

                

#             # Check for bad posture
#             bad_posture = False
#             posture_text = "Good posture"

#             phone_looking = False

#             if results.pose_landmarks:
#                 try:
#                     nose = results.pose_landmarks.landmark[PoseLandmarks.NOSE]
#                     left_eye = results.pose_landmarks.landmark[PoseLandmarks.LEFT_EYE]
#                     right_eye = results.pose_landmarks.landmark[PoseLandmarks.RIGHT_EYE]
#                     left_shoulder = results.pose_landmarks.landmark[PoseLandmarks.LEFT_SHOULDER]
#                     right_shoulder = results.pose_landmarks.landmark[PoseLandmarks.RIGHT_SHOULDER]
#                     left_hip = results.pose_landmarks.landmark[PoseLandmarks.LEFT_HIP]
#                     right_hip = results.pose_landmarks.landmark[PoseLandmarks.RIGHT_HIP]
#                 except IndexError:
#                     # Skip if any landmarks are missing
#                     continue

#                 # Normalize based on the nose position (camera reference)
#                 # nose_normalized = normalize_coordinates(nose, nose)
#                 left_shoulder_normalized = normalize_coordinates(left_shoulder, nose)
#                 right_shoulder_normalized = normalize_coordinates(right_shoulder, nose)

#                 # Calculate eyebrow (eye and nose) distance
#                 # eye_distance = calculate_distance(left_eye, right_eye)
#                 eyebrow_to_chest_distance = calculate_distance(nose, left_shoulder)  # Approximate chest position

#                 # Refined "Looking at Phone" detection based on head tilt (Nose to Shoulders)
#                 nose_to_shoulder_angle = calculate_distance(nose, left_shoulder)  # Distance between nose and shoulder
#                 nose_to_hip_angle = calculate_distance(nose, left_hip)  # Distance between nose and hip

#                 # If nose is closer to the shoulders, it could indicate that the head is tilted downward
#                 if nose_to_shoulder_angle < nose_to_hip_angle and eyebrow_to_chest_distance < 0.3:  # Threshold to detect tilt
#                     phone_looking = True
#                     posture_text = "Looking at phone"

#                 # Apply the check if eyes are pointing downward
#                 eye_angle = abs(left_eye.y - right_eye.y)
#                 if eye_angle > phone_looking_threshold:
#                     phone_looking = True
#                     posture_text = "Looking at phone"

#                 # Shoulder-hip alignment check using normalized coordinates
#                 shoulder_distance = calculate_distance(left_shoulder_normalized, right_shoulder_normalized)
#                 hip_distance = calculate_distance(left_hip, right_hip)
#                 if shoulder_distance < hip_distance - 0.05:  # Increased margin for leniency
#                     bad_posture = True
#                     posture_text = "Bad posture: Leaning forward"

#                 # New check for chin too close to chest
#                 chin_to_chest_distance = calculate_distance(nose, left_shoulder)
#                 if chin_to_chest_distance < 0.2:  # Threshold for leaning forward
#                     bad_posture = True
#                     posture_text = "Bad posture: Chin too close to chest"
#                     if phone_detected:
#                         posture_text = "Phone detected!"
#                     if not phone_detected_played:
#                         phone_detected_played = True
#                         phone_detected_sound.play()
#                 # Apply smoothing or a small buffer before triggering posture change (optional)
#                 # If posture has been bad for a few frames, consider it bad, otherwise ignore small variations
#                 if bad_posture:
#                     posture_timer += 1
#                     if posture_timer >= posture_timeout:  # If posture is bad for the specified time
#                         if not posture_is_bad:  # Trigger sound only once
#                             posture_is_bad = True
#                             bad_posture_sound.play()
#                 else:
#                     posture_timer = 0  # Reset timer if posture is good
#                     posture_is_bad = False

#             # Draw landmarks on the frame
#             # mpDrawing.draw_landmarks(
#             #     image, 
#             #     results.pose_landmarks, 
#             #     mpPose.POSE_CONNECTIONS,
#             #     mpDrawing.DrawingSpec(color=(245, 117, 66), thickness=3, circle_radius=2),
#             #     mpDrawing.DrawingSpec(color=(245, 66, 230), thickness=3, circle_radius=2)
#             # )

#             image = cv2.flip(image, 1)  # 1 for horizontal flip
#             # Add the posture text on the frame
#             font = cv2.FONT_HERSHEY_SIMPLEX
#             cv2.putText(image, posture_text, (50, 50), font, 1, (255, 0, 0), 2, cv2.LINE_AA)

#             # Encode frame to JPEG format
#             ret, buffer = cv2.imencode('.jpg', image)
#             if not ret:
#                 continue
#             frame = buffer.tobytes()

#             # Yield the frame in a Flask-compatible format
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#     cap.release()


# @app.route('/')
# def index():
#     # Render the HTML template
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     # Route for video feed
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == "__main__":
#     app.run(debug=True, use_reloader=False)



