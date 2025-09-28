from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException
from google.auth.transport import requests
from google.oauth2 import id_token
from config import settings
from pydantic import BaseModel

# ------------------- Schemas -------------------
class TokenData(BaseModel):
    email: str

# ------------------- Funções -------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Cria um token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    """Verifica e decodifica um token JWT"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    return token_data

async def verify_google_token(token: str):
    """Verifica token do Google"""
    try:
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), settings.GOOGLE_CLIENT_ID
        )
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        return {
            'email': idinfo['email'],
            'name': idinfo['name'],
            'google_id': idinfo['sub'],
            'picture': idinfo.get('picture', '')
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Token inválido: {str(e)}")
