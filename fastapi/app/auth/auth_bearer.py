from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os
import time

from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend

def decodeJWT(token: str) -> dict:
    try:
        cert_str = open(os.path.join(os.getcwd(), 'app', 'ssl', 'uat-federation-signing.usbank.com.pem'), 'rb').read()
        cert_obj = load_pem_x509_certificate(cert_str, default_backend())
        public_key = cert_obj.public_key()
        decoded_token = jwt.decode(token, public_key, algorithms=['RS256'])
        return decoded_token if decoded_token["exp"] >= time.time() else None        
    except:
        return {}

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)    
        if credentials:            
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")                        
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid
