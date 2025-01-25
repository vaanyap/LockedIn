import streamlit as st
from datetime import datetime, timedelta

# Function to display the profile page
def profile_page():
    # Set the page title and description
    st.title("Your Profile")
    st.write("View and update your profile, goals, and streak below.")

    # Display user avatar with circular frame
    st.subheader("Upload Avatar")
    avatar = st.file_uploader("Upload your avatar", type=["jpg", "png", "jpeg"])

    # If avatar is uploaded, display it inside a circular frame
    if avatar:
        avatar_image = avatar.read()
        st.markdown(
            """
            <style>
                .avatar-frame {
                    width: 150px;
                    height: 150px;
                    border-radius: 50%;
                    overflow: hidden;
                    margin: auto;
                    border: 3px solid #4CAF50;
                }
                .avatar-frame img {
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                }
            </style>
            <div class="avatar-frame">
                <img src="data:image/jpeg;base64,{0}" alt="avatar">
            </div>
            """.format(st.image(avatar_image, use_column_width=True).getvalue().decode('utf-8')),
            unsafe_allow_html=True
        )

    # Display user goals (view-only)
    st.subheader("Your Goals")
    
    # Ensure goals are stored in session state
    if 'goals' not in st.session_state:
        st.session_state.goals = []  # Initialize an empty goal list if it doesn't exist

    # Display goals as a list
    if st.session_state.goals:
        st.write("Here are your current goals:")
        for goal in st.session_state.goals:
            st.markdown(f"- {goal}")
    else:
        st.write("You haven't set any goals yet.")
    
    # Remove the option to add new goals (view-only)
    # No text input or button for adding goals

    # Display user's study streak (keep track of streak in session state)
    st.subheader("Your Study Streak")
    
    if 'last_study_date' not in st.session_state:
        st.session_state.last_study_date = None
        st.session_state.study_streak = 0  # Initialize streak if it's not already initialized

    # Check if the user has logged a study session today
    today = datetime.today().date()
    if st.session_state.last_study_date == today:
        st.write(f"Your streak is {st.session_state.study_streak} days today!")
    else:
        # Update streak if last study session is not today
        if st.session_state.last_study_date:
            last_study = datetime.strptime(st.session_state.last_study_date, "%Y-%m-%d").date()
            if today - last_study == timedelta(days=1):
                st.session_state.study_streak += 1
            else:
                st.session_state.study_streak = 1
        
        st.session_state.last_study_date = today.strftime("%Y-%m-%d")
        st.write(f"Your current streak is {st.session_state.study_streak} days.")

    # type: ignore # Remove the option to reset the streak (view-only)
    # No button for resetting the streak
