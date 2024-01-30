from fastapi import APIRouter, Depends
from fastapi.security.http import HTTPBasic, HTTPBasicCredentials, HTTPBearer
from pydantic.main import BaseModel
from .....config import Settings, get_setting
from .....connection import cassandra_client
from .....auth import auth_bearer
from typing import List

router = APIRouter()
security = HTTPBearer()

class cashbox(BaseModel):
    cashboxid: str
    cashboxnum: str
    branch: str
    

@router.post("/getmycashbox", response_model=List[cashbox])
async def search_mycashbox(credentials: HTTPBasicCredentials = Depends(security), config: Settings = Depends(get_setting)):    
    client = cassandra_client.cassandraconnect(config)  
    session = client.connect('txcashbox')
    decoded_token = auth_bearer.decodeJWT(credentials.credentials)
    tid = decoded_token['tid']
    username = decoded_token['sub']
    status = 'ACTIVE'
    ps = session.prepare('SELECT * FROM txcashbox.cashbox WHERE tid = ? AND owner = ? AND status = ? ALLOW FILTERING')
    rows = session.execute(ps, [tid, username, status])
    results = list()
    i = 0    
    for cx in rows:                
        item = {
            "cashboxid": str(cx.cashboxid),
            "cashboxnum": str(cx.cashboxnum),
            "branch": str(cx.branchnum),
        }
        results.append(item)

    return results
