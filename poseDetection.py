# Import dependencies
import cv2
import mediapipe as mp
from flask import Flask, render_template, Response

# Mediapipe setup
mpDrawing = mp.solutions.drawing_utils
mpPose = mp.solutions.pose

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

            # Draw landmarks
            mpDrawing.draw_landmarks(
                image, 
                results.pose_landmarks, 
                mpPose.POSE_CONNECTIONS,
                mpDrawing.DrawingSpec(color=(245, 117, 66), thickness=3, circle_radius=2),
                mpDrawing.DrawingSpec(color=(245, 66, 230), thickness=3, circle_radius=2)
            )

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
