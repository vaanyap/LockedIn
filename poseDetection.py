import cv2
import mediapipe as mp
from flask import Flask, render_template, Response

# Mediapipe setup
mpDrawing = mp.solutions.drawing_utils
mpPose = mp.solutions.pose

# PoseLandmarks class for easy reference to landmarks
class PoseLandmarks:
    NOSE = 0
    MOUTH_LEFT = 9
    MOUTH_RIGHT = 10
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_HIP = 23
    RIGHT_HIP = 24

# Flask app
app = Flask(__name__, template_folder='template')

# Video frame generator
def generate_frames():
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
                left_shoulder = results.pose_landmarks.landmark[PoseLandmarks.LEFT_SHOULDER]
                right_shoulder = results.pose_landmarks.landmark[PoseLandmarks.RIGHT_SHOULDER]
                left_hip = results.pose_landmarks.landmark[PoseLandmarks.LEFT_HIP]
                right_hip = results.pose_landmarks.landmark[PoseLandmarks.RIGHT_HIP]

                # Condition 1: Shoulders are uneven (with tolerance)
                if abs(left_shoulder.y - right_shoulder.y) > 0.10:  # Allow for 15% tolerance
                    bad_posture = True
                    posture_text = "Bad posture: Shoulders uneven"

                # # Condition 2: Head too far forward (nose ahead of shoulders with more tolerance)
                # if nose.y < min(left_shoulder.y, right_shoulder.y)+0.1:  # Allow for slight head forward
                #     bad_posture = True
                #     posture_text = "Bad posture: Head forward"

                # Condition 3: Slouching (hips are too far forward compared to shoulders with tolerance)
                if (left_hip.y < left_shoulder.y + 0.12 and right_hip.y < right_shoulder.y + 0.12):  # Allow slight forward tilt
                    bad_posture = True
                    posture_text = "Bad posture: Slouching"

                # Send message if bad posture detected
                if bad_posture:
                    print(posture_text)  # Optionally, you can log this to the console

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
