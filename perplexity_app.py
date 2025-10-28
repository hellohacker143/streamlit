import requests

API_KEY = 'your_perplexity_api_key'
url = "https://api.perplexity.ai/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "perplexity-1",
    "messages": [
        {"role": "user", "content": "What are the latest trends in AI for 2025?"}
    ]
}

response = requests.post(url, headers=headers, json=data)
answer = response.json()
print(answer)
