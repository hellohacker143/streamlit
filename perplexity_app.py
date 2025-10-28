import streamlit as st
import requests
import json
import os

# Set page configuration
st.set_page_config(page_title="Perplexity Research Tool", page_icon="🔍", layout="wide")

# Title and description
st.title("🔍 Perplexity Research Tool")
st.markdown("Get comprehensive summaries, website links, and YouTube channel recommendations on any topic.")

# API Key input (sidebar)
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input(
    "Enter your Perplexity API Key:",
    type="password",
    help="Your API key will not be stored. Get one at https://www.perplexity.ai/settings/api"
)

# Main content area
st.header("Enter a Topic")
topic = st.text_input(
    "What would you like to research?",
    placeholder="e.g., artificial intelligence, climate change, quantum computing...",
    help="Enter any topic you want to learn about"
)

# Button to trigger the search
if st.button("🔎 Get Summary & Suggestions", type="primary", use_container_width=True):
    if not api_key:
        st.error("⚠️ Please enter your Perplexity API key in the sidebar.")
    elif not topic:
        st.error("⚠️ Please enter a topic to research.")
    else:
        # Show loading state
        with st.spinner("🔄 Fetching information from Perplexity AI...")
            try:
                # Perplexity API configuration
                API_URL = "https://api.perplexity.ai/chat/completions"
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                
                # Request for summary
                st.subheader("📝 Summary")
                with st.spinner("Generating summary..."):
                    summary_payload = {
                        "model": "sonar",
                        "messages": [
                            {
                                "role": "user",
                                "content": f"Provide a comprehensive summary about {topic}. Include key information, recent developments, and important facts."
                            }
                        ],
                        "max_tokens": 1000,
                        "temperature": 0.7,
                        "return_citations": True
                    }
                    
                    response = requests.post(API_URL, headers=headers, json=summary_payload)
                    
                    if response.status_code == 200:
                        data = response.json()
                        summary = data.get("choices", [{}])[0].get("message", {}).get("content", "No summary available.")
                        st.write(summary)
                        
                        # Display citations if available
                        citations = data.get("citations", [])
                        if citations:
                            with st.expander("📚 Sources"):
                                for i, citation in enumerate(citations, 1):
                                    st.markdown(f"{i}. [{citation}]({citation})")
                    else:
                        st.error(f"Error generating summary: {response.status_code} - {response.text}")
                
                # Request for website links
                st.subheader("🌐 Recommended Websites")
                with st.spinner("Finding relevant websites..."):
                    websites_payload = {
                        "model": "sonar",
                        "messages": [
                            {
                                "role": "user",
                                "content": f"List 5-7 authoritative and educational websites to learn more about {topic}. For each website, provide the name, URL, and a brief description of why it's valuable. Format as: Website Name - URL - Description"
                            }
                        ],
                        "max_tokens": 800,
                        "temperature": 0.7,
                        "return_citations": True
                    }
                    
                    response = requests.post(API_URL, headers=headers, json=websites_payload)
                    
                    if response.status_code == 200:
                        data = response.json()
                        websites = data.get("choices", [{}])[0].get("message", {}).get("content", "No websites available.")
                        st.write(websites)
                    else:
                        st.error(f"Error fetching websites: {response.status_code}")
                
                # Request for YouTube channels
                st.subheader("📺 YouTube Channel Recommendations")
                with st.spinner("Finding relevant YouTube channels..."):
                    youtube_payload = {
                        "model": "sonar",
                        "messages": [
                            {
                                "role": "user",
                                "content": f"Recommend 5-7 popular and educational YouTube channels about {topic}. For each channel, provide the channel name, approximate subscriber count, and a brief description of their content. Format as: Channel Name - Subscribers - Description"
                            }
                        ],
                        "max_tokens": 800,
                        "temperature": 0.7
                    }
                    
                    response = requests.post(API_URL, headers=headers, json=youtube_payload)
                    
                    if response.status_code == 200:
                        data = response.json()
                        youtube_channels = data.get("choices", [{}])[0].get("message", {}).get("content", "No YouTube channels available.")
                        st.write(youtube_channels)
                    else:
                        st.error(f"Error fetching YouTube channels: {response.status_code}")
                
                st.success("✅ Research complete! Check out the information above.")
                
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Network error: {str(e)}")
            except json.JSONDecodeError as e:
                st.error(f"❌ Error parsing response: {str(e)}")
            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <small>Powered by Perplexity AI | Enter your API key to get started</small>
    </div>
    """,
    unsafe_allow_html=True
)
