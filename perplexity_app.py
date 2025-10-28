import streamlit as st
import requests
import json
import re
from bs4 import BeautifulSoup

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
                    "model": "sonar",
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
                    content = result["choices"][0]["message"]["content"]
                    content = re.sub(r'\[\d+\]', '', content)
                    st.write(content)
                else:
                    st.error(f"Error: API returned status code {response.status_code}")
                    st.write(response.text)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# URL Summarizer, Rewriter & Improver
st.header("URL Summarizer, Rewriter & Improver")

# URL input box
url_input = st.text_input("Enter URL:", placeholder="Paste URL here...", key="url_input")

# Display the pasted URL
if url_input:
    st.write(f"**URL:** {url_input}")

# Create three buttons in columns
col1, col2, col3 = st.columns(3)

with col1:
    rewrite_button = st.button("Rewrite")

with col2:
    summarize_button = st.button("Summarize")

with col3:
    improve_button = st.button("Improvement")

# Function to extract text from URL
def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract text from <p> tags only
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        
        # Limit to 5000 characters
        text = text[:5000]
        return text
    except Exception as e:
        return None

# Function to call Perplexity AI
def call_perplexity_ai(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "sonar",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            # Clean [number] references with regex
            content = re.sub(r'\[\d+\]', '', content)
            return content
        else:
            return None
    except Exception as e:
        return None

# Handle Rewrite button
if rewrite_button:
    if url_input:
        with st.spinner("Fetching and rewriting content..."):
            original_text = extract_text_from_url(url_input)
            if original_text:
                rewritten_text = call_perplexity_ai(f"Rewrite the following text in a different style while maintaining the same meaning:\n\n{original_text}")
                
                if rewritten_text:
                    col_before, col_after = st.columns(2)
                    
                    with col_before:
                        st.subheader("Before")
                        st.write(original_text)
                    
                    with col_after:
                        st.subheader("After")
                        st.write(rewritten_text)
                else:
                    st.error("Failed to rewrite content.")
            else:
                st.error("Failed to extract text from URL.")
    else:
        st.warning("Please enter a URL first.")

# Handle Summarize button
if summarize_button:
    if url_input:
        with st.spinner("Fetching and summarizing content..."):
            original_text = extract_text_from_url(url_input)
            if original_text:
                summary = call_perplexity_ai(f"Summarize the following text concisely:\n\n{original_text}")
                
                if summary:
                    st.subheader("Article Summarization")
                    st.write(summary)
                else:
                    st.error("Failed to summarize content.")
            else:
                st.error("Failed to extract text from URL.")
    else:
        st.warning("Please enter a URL first.")

# Handle Improvement button
if improve_button:
    if url_input:
        with st.spinner("Fetching and improving content..."):
            original_text = extract_text_from_url(url_input)
            if original_text:
                improved_text = call_perplexity_ai(f"Improve the following text by enhancing clarity, grammar, and readability:\n\n{original_text}")
                
                if improved_text:
                    st.subheader("Improved Article")
                    st.write(improved_text)
                else:
                    st.error("Failed to improve content.")
            else:
                st.error("Failed to extract text from URL.")
    else:
        st.warning("Please enter a URL first.")

st.markdown("*Powered by Perplexity AI*")
