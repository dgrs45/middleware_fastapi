import requests

auth_key="ABC-123-DG"

url = f'http://127.0.0.1:8000/return_llm_object?api-key={auth_key}'

data = {
    'prompt' : 'What is the capital of India',
    'make_inference' : True
}

res =  requests.post(url,json=data)

print(res.text)
