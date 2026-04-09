# import os
# import streamlit as st
# import vertexai
# from vertexai.generative_models import GenerativeModel, Part
# from google.cloud import storage

# # Initialize Vertex AI API
# vertexai.init(project="lockedin-448906", location="us-central1")

# # Function to upload file to Google Cloud Storage
# def upload_to_gcs(bucket_name, file_path, blob_name):
#     try:
#         # Initialize the GCS client
#         storage_client = storage.Client()
#         bucket = storage_client.get_bucket(bucket_name)
        
#         # Upload the file to GCS
#         blob = bucket.blob(blob_name)
#         blob.upload_from_filename(file_path)

#         # Return the GCS URI for the uploaded file
#         return f"gs://{bucket_name}/{blob_name}"
#     except Exception as e:
#         st.error(f"Failed to upload file to GCS: {e}")
#         return None

# # Function to send prompt to Vertex AI Gemini API
# def get_text_response(prompt: str):
#     model = GenerativeModel("gemini-1.5-flash-002")
#     response = model.generate_content(prompt)
#     return response.text

# # Function to send image and prompt to Vertex AI Gemini API
# def get_image_response(image_uri: str, prompt: str):
#     model = GenerativeModel("gemini-1.5-flash-002")
#     response = model.generate_content(
#         [
#             Part.from_uri(image_uri, mime_type="image/jpeg"),
#             prompt,
#         ]
#     )
#     return response.text

# # Function to send video and prompt to Vertex AI Gemini API
# def get_video_response(video_uri: str, prompt: str):
#     model = GenerativeModel("gemini-1.5-flash-002")
#     video_file = Part.from_uri(uri=video_uri, mime_type="video/mp4")
#     contents = [video_file, prompt]
#     response = model.generate_content(contents)
#     return response.text

# # Streamlit app UI
# def render_study_buddy_ai_chat():
#     st.title("Echo - Your AI Academic Support Owl! 🦉")
#     st.image("src/echoTheOwl.png", width=200)  # Replace with your mascot image path
#     st.write("Hey! My name is Echo and I'm your AI support owl! I'm here to help you with any of your academic inquiries. Let's spread our wings and get to work! 📚")

#     # Chat interface
#     if "conversation_history" not in st.session_state:
#         st.session_state.conversation_history = []

#     # Display past conversations
#     for entry in st.session_state.conversation_history:
#         st.text_area("Prompt:", entry["prompt"], height=100, max_chars=500, key=f'prompt_{entry["id"]}', disabled=True)
#         st.text_area("Answer:", entry["answer"], height=100, max_chars=500, key=f'answer_{entry["id"]}', disabled=True)

#     # User input section
#     user_input = st.text_area("Enter your academic inquiry:", height=100)
#     uploaded_file = st.file_uploader("Upload an image or video:", type=["jpg", "jpeg", "png", "mp4"])

#     # Bucket name
#     bucket_name = "lockedinbucket"

#     # Ensure directories exist for saving uploaded files
#     if uploaded_file:
#         if uploaded_file.type in ["image/jpeg", "image/png"]:
#             # Ensure the directory exists
#             image_dir = "temp_image"
#             os.makedirs(image_dir, exist_ok=True)
#             image_path = os.path.join(image_dir, uploaded_file.name)
            
#             # Save image locally (temporarily) before uploading to GCS
#             with open(image_path, "wb") as f:
#                 f.write(uploaded_file.getbuffer())
            
#             # Upload the image to GCS
#             gcs_image_uri = upload_to_gcs(bucket_name, image_path, uploaded_file.name)
            
#             # Get text from the image
#             if gcs_image_uri and user_input:
#                 response = get_image_response(gcs_image_uri, user_input)
#             elif gcs_image_uri:
#                 response = get_image_response(gcs_image_uri, "What is shown in this image?")
            
#             # Optional: Clean up the local file
#             os.remove(image_path)

#         elif uploaded_file.type == "video/mp4":
#             # Ensure the directory exists
#             video_dir = "temp_video"
#             os.makedirs(video_dir, exist_ok=True)
#             video_path = os.path.join(video_dir, uploaded_file.name)
            
#             # Save video locally (temporarily) before uploading to GCS
#             with open(video_path, "wb") as f:
#                 f.write(uploaded_file.getbuffer())
            
#             # Upload the video to GCS
#             gcs_video_uri = upload_to_gcs(bucket_name, video_path, uploaded_file.name)
            
#             # Get description and transcription from the video
#             if gcs_video_uri and user_input:
#                 response = get_video_response(gcs_video_uri, user_input)
#             elif gcs_video_uri:
#                 response = get_video_response(gcs_video_uri, "Provide a description of the video and any important dialogue.")

#             # Optional: Clean up the local file
#             os.remove(video_path)
#     else:
#         # Handle text-based query
#         if user_input:
#             response = get_text_response(user_input)
#         else:
#             response = None

#     # Display response and save the conversation
#     if response:
#         st.text_area("Answer:", response, height=100, max_chars=500, disabled=True)
#         # Save the conversation in session state to persist during the session
#         conversation_id = len(st.session_state.conversation_history) + 1
#         st.session_state.conversation_history.append({
#             "id": conversation_id,
#             "prompt": user_input,
#             "answer": response,
#         })

# if __name__ == "__main__":
#     render_study_buddy_ai_chat()



import os
import tempfile

import streamlit as st

try:
    import vertexai
    from google.cloud import storage
    from vertexai.generative_models import GenerativeModel, Part
except ImportError:
    vertexai = None
    storage = None
    GenerativeModel = None
    Part = None


PROJECT_ID = os.getenv("VERTEX_PROJECT_ID", "lockedin-448906")
VERTEX_LOCATION = os.getenv("VERTEX_LOCATION", "us-central1")
MODEL_NAME = os.getenv("VERTEX_MODEL", "gemini-1.5-flash-002")
BUCKET_NAME = os.getenv("LOCKEDIN_BUCKET", "lockedinbucket")


@st.cache_resource(show_spinner=False)
def get_model():
    if vertexai is None or GenerativeModel is None:
        raise RuntimeError("Vertex AI dependencies are not installed.")

    vertexai.init(project=PROJECT_ID, location=VERTEX_LOCATION)
    return GenerativeModel(MODEL_NAME)

# Function to upload file to Google Cloud Storage
def upload_to_gcs(file_path, blob_name):
    if storage is None:
        raise RuntimeError("Google Cloud Storage dependencies are not installed.")

    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(file_path)
    return f"gs://{BUCKET_NAME}/{blob_name}"

# Function to send prompt to Vertex AI Gemini API
def get_text_response(prompt: str):
    model = get_model()
    response = model.generate_content(prompt)
    return response.text

# Function to send image and prompt to Vertex AI Gemini API
def get_image_response(image_uri: str, prompt: str):
    model = get_model()
    response = model.generate_content([Part.from_uri(image_uri, mime_type="image/jpeg"), prompt])
    return response.text

# Function to send video and prompt to Vertex AI Gemini API
def get_video_response(video_uri: str, prompt: str):
    model = get_model()
    video_file = Part.from_uri(uri=video_uri, mime_type="video/mp4")
    response = model.generate_content([video_file, prompt])
    return response.text


def render_setup_notice():
    st.info("Echo is optional. Install Vertex AI dependencies and authenticate with Google Cloud to enable the chat features.")
    st.caption("If you want this live, configure application default credentials or set GOOGLE_APPLICATION_CREDENTIALS before launching the app.")

# Streamlit app UI
def render_study_buddy_ai_chat():
    st.subheader("Echo, your AI academic support owl")
    st.image("src/echoTheOwl.png", width=180)
    st.write("Ask a study question, or upload an image or short video for multimodal analysis when Vertex AI is configured.")

    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

    # Display past conversations
    for entry in st.session_state.conversation_history:
        st.text_area("Prompt:", entry["prompt"], height=100, max_chars=500, key=f'prompt_{entry["id"]}', disabled=True)
        st.text_area("Answer:", entry["answer"], height=100, max_chars=500, key=f'answer_{entry["id"]}', disabled=True)

    with st.form("study_buddy_form"):
        user_input = st.text_area("Enter your academic inquiry:", height=120)
        uploaded_file = st.file_uploader("Upload an image or video:", type=["jpg", "jpeg", "png", "mp4"])
        submitted = st.form_submit_button("Ask Echo")

    if not submitted:
        return

    if not user_input and uploaded_file is None:
        st.warning("Enter a question or upload a file first.")
        return

    if vertexai is None or GenerativeModel is None or Part is None or storage is None:
        render_setup_notice()
        return

    try:
        if uploaded_file:
            suffix = os.path.splitext(uploaded_file.name)[1] or ".bin"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_file.write(uploaded_file.getbuffer())
                temp_path = temp_file.name

            try:
                gcs_uri = upload_to_gcs(temp_path, uploaded_file.name)
            finally:
                os.remove(temp_path)

            if uploaded_file.type in ["image/jpeg", "image/png"]:
                response = get_image_response(gcs_uri, user_input or "What is shown in this image?")
            else:
                response = get_video_response(gcs_uri, user_input or "Provide a description of the video and any important dialogue.")
        else:
            response = get_text_response(user_input)

        st.text_area("Answer:", response, height=140, disabled=True)
        conversation_id = len(st.session_state.conversation_history) + 1
        st.session_state.conversation_history.append({
            "id": conversation_id,
            "prompt": user_input or uploaded_file.name,
            "answer": response,
        })
    except Exception as error:
        st.error(f"Echo could not answer right now: {error}")
        render_setup_notice()

if __name__ == "__main__":
    render_study_buddy_ai_chat()
