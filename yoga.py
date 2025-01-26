import vertexai
from vertexai.generative_models import GenerativeModel
import re

# Initialize Vertex AI
PROJECT_ID = "lockedin-448906"
vertexai.init(project=PROJECT_ID, location="us-central1")

# Initialize the generative model
model = GenerativeModel("gemini-1.5-flash-002")

def generate_python_code_for_pose(pose_description):
    prompt = f"""
    Generate Python code that uses mediapipe and OpenCV to verify if the user is correctly performing the yoga pose: {pose_description}.
    The output code should:
    - Dynamically run and display the result in a webcam window.
    - If the pose is hit correctly, the text in the corner should turn green and say 'Pose Correct!'.
    - Add a simple check for pose correctness based on pose landmarks.
    - Replace 'imshow()' with logic to save the frame as an image and display it using Streamlit.
    """

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
        generated_code = generate_python_code_for_pose(pose_description)
        return generated_code
    except Exception as e:
        return f"Error generating code: {e}"

# Entry point for standalone execution (if needed)
if __name__ == "__main__":
    pose_description = "downward dog"
    code = render_generated_code(pose_description)
    print(code)
