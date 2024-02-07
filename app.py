from fastapi import HTTPException,Security,status,FastAPI
from fastapi.security import APIKeyHeader, APIKeyQuery
from langchain_community.llms import LlamaCpp
import requests
from fastapi import Request
from pydantic import BaseModel

class PostData(BaseModel):
   prompt:str
   make_inference:bool
   
# instantiate the llm --> things to be done --> param list, inference endpoint 
class llm:
 def __init__(self,params):
  self.params = params

 def instantiate_llm(self):
  # extract parameters later
    self.llm = LlamaCpp(
    model_path= "llama-2-7b-chat.Q4_K_M.gguf",
    temperature=0.2,
    n_ctx=2048,
    top_p=0.1,
    n_gpu_layers = 10,
    repetition_penalty=1.77)
    return self.llm 
 
 def make_inference(self):
    self.instantiate_llm()
    prompt = self.params['prompt']
    response = self.llm(prompt)
    print(response)
    return response

  
API_KEYS = ["ABC-123-DG"]

api_key_query = APIKeyQuery(name="api-key",auto_error=False)
api_key_header = APIKeyHeader(name="auth_key",auto_error=False)

def get_api_key(api_key_query:str=Security(api_key_query),
                api_key_header:str =Security(api_key_header)) -> str:
    """Retrieve and validate API KEY"""
    if api_key_header in API_KEYS:
        return api_key_header
    if api_key_query in API_KEYS:
        return api_key_query
    raise HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="API-KEY not valid or not provided."
    )


app = FastAPI()

# return llm object 

@app.post('/return_llm_object')
async def return_object(item:PostData,api_key:str = Security(get_api_key)):
    params = {}
    params['prompt'] = item.prompt
    object_llm =  llm(params).make_inference()
    return object_llm
