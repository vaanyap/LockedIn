import streamlit as st

def posture_detector():
    st.markdown("<div class='title'><span class='icon'>🪑</span>Posture Detector</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class='content'>
        Ensure you're sitting correctly for optimal focus and health.<br>
        Feature uses MediaPipe for posture analysis.
        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_video = st.file_uploader("Upload a video of yourself sitting (MP4 format):", type="mp4")
    if uploaded_video:
        st.video(uploaded_video)
        st.markdown("<div class='content'>Processing your posture... Feature coming soon!</div>", unsafe_allow_html=True)

