from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security.http import HTTPAuthorizationCredentials

from app.auth.auth_bearer import JWTBearer
from .....config import Settings, get_setting
import requests, json

router = APIRouter()
security = HTTPBasic()

@router.get("/gettoken")
async def get_token(credentials: HTTPBasicCredentials = Depends(security), config: Settings = Depends(get_setting)):    
    data = {
        "grant_type": "password",
        "username": credentials.username,
        "password": credentials.password,
    }
    url = config.pingurl
    clientid = config.pingclientid
    if "uat" in clientid:
        url = url + "?validator_id=ROCredsUAT"
    else:
        url = url + "?validator_id=ROCredsITT3"

    access_token_response = requests.post(
        url,
        data=data,
        verify=False,
        allow_redirects=False,
        auth=(config.pingclientid, config.pingclientpassword))
        
    return json.loads(access_token_response.text)

@router.get("/test")
async def my_test(token: HTTPAuthorizationCredentials = Depends(JWTBearer())):    
    return{'works'}