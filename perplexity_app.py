import streamlit as st
import requests

st.title("Blog Generator")

topic = st.text_input("Enter Blog Topic:")

if st.button("Generate Blog"):
    if topic:
        with st.spinner("Generating your blog..."):
            try:
                response = requests.post(
                    "https://api.perplexity.ai/chat/completions",
                    headers={
                        "Authorization": "Bearer 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",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.1-sonar-small-128k-online",
                        "messages": [
                            {
                                "role": "user",
                                "content": f"Write a 400-word blog post about: {topic}"
                            }
                        ]
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    blog_content = result["choices"][0]["message"]["content"]
                    st.subheader("Generated Blog:")
                    st.write(blog_content)
                else:
                    st.error(f"API Error: Status {response.status_code} - {response.text}")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a topic")
