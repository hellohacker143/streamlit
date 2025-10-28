import streamlit as st
import requests
import json

# Set page title
st.title("Perplexity AI Query App")

# API configuration
API_KEY = "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"
API_URL = "https://api.perplexity.ai/chat/completions"

# Create text input for user query
user_query = st.text_input("Enter your query:", placeholder="Type your question here...")

# Create submit button
if st.button("Submit Query"):
    if user_query:
        # Show loading spinner while processing
        with st.spinner("Getting response from Perplexity AI..."):
            try:
                # Prepare the API request
                headers = {
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": "sonar-small-online",
                    "messages": [
                        {
                            "role": "user",
                            "content": user_query
                        }
                    ]
                }
                
                # Make the API request
                response = requests.post(API_URL, headers=headers, json=payload)
                
                # Check if request was successful
                if response.status_code == 200:
                    result = response.json()
                    # Display the response
                    st.success("Response received!")
                    st.subheader("Perplexity AI Response:")
                    st.write(result["choices"][0]["message"]["content"])
                else:
                    st.error(f"Error: API returned status code {response.status_code}")
                    st.write(response.text)
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a query before submitting.")

# Add some information at the bottom
st.markdown("---")
st.markdown("*Powered by Perplexity AI*")
