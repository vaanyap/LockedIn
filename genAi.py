import vertexai
from vertexai.generative_models import GenerativeModel
import re

# Initialize Vertex AI
PROJECT_ID = "lockedin-448906"
vertexai.init(project=PROJECT_ID, location="us-central1")

# Initialize the generative model
model = GenerativeModel("gemini-1.5-flash-002")

# Function to generate python code from pose description
def generate_python_code_for_pose(pose_description):
    prompt = f"Generate Python code that uses mediapipe and OpenCV to verify if the user is correctly performing the yoga pose: {pose_description}. The output code should dynamically run and display the result in a webcam window. If the pose is hit correctly, the text in the corner should turn green and say 'Pose Correct!'. make it overall pretty easy to hit the poses. you shouldnt have to try too hard"

    response = model.generate_content(prompt)
    
    # Extract Python code between "```python" and "```"
    match = re.search(r"```python\n(.*?)```", response.text, re.DOTALL)
    if match:
        return match.group(1)
    else:
        raise ValueError("No Python code found in the response.")

# Example pose description input
pose_description = input("Enter the yoga pose description: ")

# Generate the Python code to verify the pose
generated_code = generate_python_code_for_pose(pose_description)

# Print the generated Python code
print("\nGenerated Python Code:")
print(generated_code)

# Execute the generated Python code dynamically using exec
try:
    # To prevent running code that may be harmful, you could sanitize or review the generated code
    exec(generated_code)
except Exception as e:
    print(f"Error executing generated code: {e}")
