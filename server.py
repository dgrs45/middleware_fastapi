from fastapi import HTTPException,Security,status,FastAPI,Request
from fastapi.security import APIKeyHeader, APIKeyQuery
from langchain_community.llms import LlamaCpp
from pydantic import BaseModel
from token_bucket import TokenBucket
from starlette.middleware.base import BaseHTTPMiddleware

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
    )
    return self.llm 
 
 def make_inference(self):
    self.instantiate_llm()
    prompt = self.params['prompt']
    response = self.llm(prompt)
    print(response)
    return response

app = FastAPI()
API_KEYS = ["ABC-123-DG"]
api_key_query = APIKeyQuery(name="api-key",auto_error=False)
api_key_header = APIKeyHeader(name="auth_key",auto_error=False)



class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, bucket: TokenBucket):
        super().__init__(app)
        self.bucket = bucket

    async def dispatch(self, request: Request, call_next):
        if self.bucket.take_token():
            return await call_next(request)
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")

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

# refilling capacity to be adjusted as per the time taken to process the inference
bucket = TokenBucket(capacity=4, refill_rate=0.5)
# Add the rate limiting middleware to the FastAPI app
app.add_middleware(RateLimiterMiddleware, bucket=bucket)



@app.post('/return_llm_object')
async def return_object(item:PostData,api_key:str = Security(get_api_key)):
    params = {}
    params['prompt'] = item.prompt
    if(item.make_inference):
        object_llm =  llm(params).make_inference()
        return object_llm
    else:
       return "Authorized"
