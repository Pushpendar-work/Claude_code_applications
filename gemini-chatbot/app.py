import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
if api_key:
    genai.configure(api_key=api_key)
else:
    # We don't show error immediately because user can provide key in UI
    pass

# Set up the model
model = genai.GenerativeModel('gemini-3.8-flash')

# Streamlit Page Config
st.set_page_config(page_title="Gemini AI Chatbot", page_icon="🤖")
st.title("🤖 Code_Aur_Chintan Answers")
st.markdown("Welcome! Start a conversation with Gemini 3.8 Flash.")

# --- SIDEBAR FOR KEY ---
with st.sidebar:
    st.header("Settings")
    user_api_key = st.text_input("Enter Gemini API Key", value="", type="password")

    if user_api_key:
        genai.configure(api_key=user_api_key)
        st.success("API Key Active ✅")
    else:
        st.warning("Please enter an API key to start.")

    st.markdown("---")
    if st.button("➕ New Chat"):
        st.session_state.messages = []
        st.rerun()

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is on your mind?"):
    if not user_api_key:
        st.error("Please enter your Gemini API Key in the sidebar to start chatting!")
    else:
        # Display user message
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generate response from Gemini
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            try:
                history = [
                    {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
                    for m in st.session_state.messages[:-1]
                ]
                chat = model.start_chat(history=history)
                response = chat.send_message(prompt, stream=True)

                for chunk in response:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)
            except Exception as e:
                st.error(f"An error occurred: {e}")
                full_response = "I'm sorry, I encountered an error while generating a response."
                message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
