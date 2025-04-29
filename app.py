import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Get the Google API key from the environment variable
api_key = os.getenv("GOOGLE_API_KEY")

# Check if the API key is available
if not api_key:
    st.error("API key is missing. Please add it to your .env file.")
else:
    # Configure the Google Generative AI API
    genai.configure(api_key=api_key)

    # Initialize the model
    model = genai.GenerativeModel("gemini-pro")
    chat = model.start_chat(history=[])

    # Function to send a message to the Generative AI model and get the response
    def get_gemini_response(question):
        response = chat.send_message(question, stream=True)
        return response

    # Streamlit app setup
    st.set_page_config(page_title="Generative AI Q&A Demo")
    st.header("Generative AI Q&A Application")

    # Initialize session state for chat history if not already initialized
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # User input for question
    input_query = st.text_input("Ask your question:", key="input")
    submit = st.button("Ask")

    # Handle question submission
    if submit and input_query:
        response = get_gemini_response(input_query)

        # Add user query and bot response to session state chat history
        st.session_state['chat_history'].append(("You", input_query))
        st.subheader("The Response is:")
        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))

    # Display the chat history
    st.subheader("Chat History:")
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")
