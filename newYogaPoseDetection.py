import cv2
import mediapipe as mp
from flask import Flask, render_template, request, Response, jsonify
import webbrowser
from genAI import generate_pose_detection_code

app = Flask(__name__)


def run_pose_detection(selected_pose):
    """Run pose detection using the dynamically generated code."""
    # Generate the pose detection code dynamically
    generated_code = generate_pose_detection_code(selected_pose)

    # Execute the generated code to define the pose-checking function
    exec(generated_code, globals())

    # Initialize MediaPipe Pose
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    # Start video capture
    cap = cv2.VideoCapture(0)

    print(f"Perform the {selected_pose} pose. Press 'q' to exit.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Perform pose detection
        results = pose.process(rgb_frame)

        # Draw landmarks on the frame
        if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Call the dynamically generated function
            pose_correct = globals()[f"is_{selected_pose.lower().replace(' ', '_')}"](results.pose_landmarks)

            # Display feedback on the frame
            cv2.putText(
                frame,
                f"Pose Correct: {pose_correct}",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0) if pose_correct else (0, 0, 255),
                2,
            )

        # Display the frame
        cv2.imshow("Pose Detection", frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


@app.route("/")
def home():
    """Home page with pose selection."""
    return """
    <h1>Pose Detection</h1>
    <form action="/start_detection" method="post">
        <label for="pose">Choose a pose:</label>
        <select name="pose" id="pose">
            <option value="Warrior II">Warrior II</option>
            <option value="Tree Pose">Tree Pose</option>
            <option value="Downward Dog">Downward Dog</option>
        </select>
        <button type="submit">Start Detection</button>
    </form>
    """


@app.route("/start_detection", methods=["POST"])
def start_detection():
    """Start the pose detection."""
    selected_pose = request.form.get("pose")
    if not selected_pose:
        return "No pose selected!", 400

    # Run pose detection in a new process/thread to avoid blocking Flask
    from threading import Thread
    detection_thread = Thread(target=run_pose_detection, args=(selected_pose,))
    detection_thread.start()

    return f"""
    <h1>Pose Detection Started</h1>
    <p>Perform the '{selected_pose}' pose. The webcam feed will open in a new window.</p>
    <p><a href="/">Go Back</a></p>
    """


if __name__ == "__main__":
    # Open the browser to the Flask app
    url = "http://127.0.0.1:5000/"
    webbrowser.open(url)

    # Run Flask app
    app.run(debug=True)
