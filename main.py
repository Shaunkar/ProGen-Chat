import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import re
import string

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


# Display the chatbot's title on the page
st.title("🤖 Gemini Pro - ChatBot")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Button to start a new chat session
with st.sidebar:
    if st.button("Start a new chat session"):
        st.session_state.chat_session = model.start_chat(history=[])
def sanitize_input(text):
    # Remove non-alphanumeric characters
    text = re.sub(f'[{re.escape(string.punctuation)}]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Remove any words that contain offensive language
    words = text.split()
    filtered_words = [word for word in words if not any(offensive_word in word for offensive_word in offensive_words)]
    text = ' '.join(filtered_words)
    return text

offensive_words = ['fuck', 'lewd', 'adult']

# Input field for user's message
user_prompt = st.chat_input("Ask Gemini-Pro...")
if user_prompt:
    # Sanitize user input
    sanitized_prompt = sanitize_input(user_prompt)
    if sanitized_prompt:
        # Add user's message to chat and display it
        st.chat_message("user").markdown(user_prompt)

        # Send sanitized user input to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(sanitized_prompt)

        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)


