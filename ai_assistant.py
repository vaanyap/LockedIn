import streamlit as st

def study_buddy_chat():
    st.markdown("<div class='title'><span class='icon'>🤖</span>Study Buddy AI Chat</div>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class='content'>
        Chat with your AI Study Buddy for personalized study tips, motivation, and guidance.<br>
        Just type your message below, and the AI will respond accordingly!
        </div>
        """,
        unsafe_allow_html=True
    )

    # Create a simple chat interface
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for msg in st.session_state.messages:
        if msg.startswith("You:"):
            st.markdown(f"<div class='chat-message chat-message-user'>{msg}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-message chat-message-bot'>{msg}</div>", unsafe_allow_html=True)

    # Input field for chat
    user_input = st.text_input("Type your message:", key="chat_input")
    if st.button("Send"):
        if user_input:
            # Add user input to the chat
            st.session_state.messages.append(f"You: {user_input}")
            # Simple AI response (can be replaced with actual AI model)
            st.session_state.messages.append(f"Study Buddy: Let me help you with that! (AI is still learning...)")
            st.experimental_rerun()
