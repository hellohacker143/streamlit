import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure the API key for Gemini AI (loaded from .env or direct input)
api_key = os.getenv("GOOGLE_API_KEY", "AIzaSyC3kihcAv8ykakwRbMIuJZECxWCSeuCB24")
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get the response from Gemini API
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Streamlit app configuration
st.set_page_config(page_title="Gemini Q&A Demo")
st.header("Gemini LLM Application")

# Initialize session state for chat history if not already initialized
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# User input field for questions
input_query = st.text_input("Ask your question:", key="input")
submit = st.button("Ask the question")

# Handle button click and fetch response
if submit and input_query:
    response = get_gemini_response(input_query)
    
    # Append user input and response to chat history
    st.session_state['chat_history'].append(("You", input_query))
    st.subheader("The Response is:")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))

# Display the chat history
st.subheader("Chat History:")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
