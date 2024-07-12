from fastapi import FastAPI
from pydantic import BaseModel
import requests
from fake_useragent import UserAgent
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestModel(BaseModel):
    login: str
    password: str

@app.post('/')
def main(data: RequestModel):
    session = requests.Session()

    ua = UserAgent()
    session.headers.update({'User-Agent': str(ua.random)})

    url = 'https://passport.43edu.ru/auth/login'
    data = {'login': data.login, 'password': data.password, "submit": "submit", "returnTo": "https://one.43edu.ru"}
    
    session.post(url, data=data, cert=('/cert.pem', '/key.pem'))

    token = next((i for i in session.cookies if i.name == 'X1_SSO'), None)

    return token.value if token else 'None'