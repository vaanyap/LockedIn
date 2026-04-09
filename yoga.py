import re
from textwrap import dedent

try:
    import vertexai
    from vertexai.generative_models import GenerativeModel
except ImportError:
    vertexai = None
    GenerativeModel = None

PROJECT_ID = "lockedin-448906"


def get_model():
    if vertexai is None or GenerativeModel is None:
        raise RuntimeError("Vertex AI is not installed.")

    vertexai.init(project=PROJECT_ID, location="us-central1")
    return GenerativeModel("gemini-1.5-flash-002")


def fallback_pose_code(pose_description):
    return dedent(
        f"""
        import cv2
        import mediapipe as mp

        TARGET_POSE = {pose_description!r}

        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        mp_drawing = mp.solutions.drawing_utils

        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            message = f"Trying to match: {{TARGET_POSE}}"
            color = (0, 165, 255)

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                left_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
                right_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
                left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
                right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]

                if left_wrist.y < left_shoulder.y and right_wrist.y < right_shoulder.y:
                    message = "Pose Correct!"
                    color = (0, 200, 0)
                else:
                    message = "Adjust your posture and try again"
                    color = (0, 0, 255)

            cv2.putText(frame, message, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2, cv2.LINE_AA)
            cv2.imshow("Yoga Pose Verifier", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
        """
    ).strip()

def generate_python_code_for_pose(pose_description):
    prompt = f"""
    Generate Python code that uses mediapipe and OpenCV to verify if the user is correctly performing the yoga pose: {pose_description}.
    The output code should:
    - Dynamically run and display the result in a webcam window.
    - If the pose is hit correctly, the text in the corner should turn green and say 'Pose Correct!'.
    - Add a simple check for pose correctness based on pose landmarks.
    - Replace 'imshow()' with logic to save the frame as an image and display it using Streamlit.
    """

    model = get_model()
    response = model.generate_content(prompt)
    
    # Extract Python code between "```python" and "```"
    match = re.search(r"```python\n(.*?)```", response.text, re.DOTALL)
    if match:
        code = match.group(1)

        # Replace any imshow() with Streamlit logic
        code = re.sub(r'cv2.imshow\((.*?)\)', 'st.image(img_path, caption="Yoga Pose Frame", use_column_width=True)', code)
        
        # Add the import statement for os and Streamlit at the top of the generated code
        code_with_imports = "import os\nimport streamlit as st\n" + code
        return code_with_imports
    else:
        raise ValueError("No Python code found in the response.")

# Create a function that will be called to generate code
def render_generated_code(pose_description):
    try:
        return generate_python_code_for_pose(pose_description)
    except Exception:
        return fallback_pose_code(pose_description)

# Entry point for standalone execution (if needed)
if __name__ == "__main__":
    pose_description = "downward dog"
    code = render_generated_code(pose_description)
    print(code)
