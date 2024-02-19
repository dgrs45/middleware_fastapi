import requests
import time

def timer(func):
    def wrapper():
        t1 = time.time()
        func()
        t2 = time.time() - t1
        print(f'{t2-t1}s')
    return wrapper



auth_key="ABC-123-DG"

url = f'http://127.0.0.1:8000/return_llm_object?api-key={auth_key}'

data = {
    'prompt' : 'What is the capital of India',
    'make_inference' : False
}

@timer
async def make_reqs():
    for i in range(0,5):
        time.sleep(1)        
        if i%4==0:
            data['make_inference'] = True
            res = await requests.post(url,json=data)
        else:
            data['make_inference'] = False
            res = await requests.post(url,json=data)
        print(res.reason)

make_reqs()