import streamlit as st

def show_home():
    st.title("LockedIn - Your Study Hub")
    st.markdown("""
    Welcome to **LockedIn**, your ultimate study companion for staying focused and productive.
    
    Choose your path to get started!
    """)
    
    option = st.radio("Please choose an option:", ("Sign In", "Sign Up"))
    
    if option == "Sign In":
        show_sign_in()
    elif option == "Sign Up":
        show_sign_up()

def show_sign_in():
    st.header("Sign In")
    st.write("Please enter your credentials to sign in.")
    
    email = st.text_input("Email", "")
    password = st.text_input("Password", "", type="password")
    
    if st.button("Sign In"):
        # Here you can add the backend logic for sign-in
        st.success("Signed In Successfully")

def show_sign_up():
    st.header("Sign Up")
    st.write("Create an account to get started.")
    
    email = st.text_input("Email", "")
    password = st.text_input("Password", "", type="password")
    
    if st.button("Sign Up"):
        # Here you can add the backend logic for sign-up
        st.success("Account Created Successfully")

def show_goal_setting():
    st.header("Set Your Goals and Tasks")
    st.markdown("""
    Write down your goals and tasks to stay on track with your study sessions.
    """)
    
    task = st.text_input("Task Name", "")
    goal = st.text_area("Goal Description", "")
    
    if st.button("Save Goal"):
        st.success(f"Goal '{task}' saved!")
        # You can later add backend functionality to store goals

def show_posture_stretch():
    st.header("Posture & Stretch Tips")
    st.markdown("""
    ### Posture Tips:
    - Sit upright with shoulders back.
    - Keep your feet flat on the floor.
    
    ### Stretching:
    - Take a break every 30 minutes to stretch your body.
    - Stretch your back, legs, and arms to prevent stiffness.
    """)
    
    st.video("https://www.youtube.com/watch?v=6p_h5FHzUoQ", start_time=30)  # Optional: Embed a posture/stretching video

def show_ai_assistant():
    st.header("AI Chat Assistant")
    st.markdown("""
    Ask questions and get study tips, productivity advice, and more from our AI Assistant.
    """)
    
    user_input = st.text_input("Ask the AI anything:", "")
    
    if st.button("Send"):
        if user_input:
            # AI response (mocked response for now)
            response = f"Here's the AI response to your question: '{user_input}'"
            st.write(f"AI: {response}")
        else:
            st.warning("Please ask a question.")
