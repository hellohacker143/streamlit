import streamlit as st
import requests
import re

st.title("Blog Generator")

topic = st.text_input("Blog Topic")

if st.button("Generate Blog"):
    if topic:
        with st.spinner("Generating..."):
            response = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": "Bearer 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",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "sonar",
                    "messages": [{"role": "user", "content": f"Write a 400-word blog post about: {topic}"}],
                    "max_tokens": 800
                }
            )
            
            if response.status_code == 200:
                content = response.json()["choices"][0]["message"]["content"]
                content = re.sub(r'\[\d+\]', '', content)
                st.write(content)
            else:
                st.error("Error generating blog")
    else:
        st.warning("Please enter a topic")
