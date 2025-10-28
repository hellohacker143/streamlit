import streamlit as st
import requests

# Replace with your actual Perplexity API key
API_KEY = "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"

API_URL = "https://api.perplexity.ai/v1/ask"

def ask_perplexity(question):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {"question": question}
    response = requests.post(API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        result = response.json()
        return result.get("answer", "No answer found.")
    else:
        return f"Error: {response.status_code} - {response.text}"

def main():
    st.title("Simple Perplexity API Chat with Streamlit")
    user_input = st.text_input("Ask something:")
    if user_input:
        with st.spinner('Getting response...'):
            answer = ask_perplexity(user_input)
        st.markdown("### Response:")
        st.write(answer)

if __name__ == "__main__":
    main()
