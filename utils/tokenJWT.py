from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


SECRET_KEY = "Stylo Mate Seccret key"
ALGORITM = "HS256"
REFRESH_TOKEN_EXPIRE_DAYS = 7

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

class TokenData(BaseModel):
    uid: Optional[str] = None


def create_acces_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    # mengatur waktu expired
    expire = datetime.now() + timedelta(days= REFRESH_TOKEN_EXPIRE_DAYS)

    # update data dalam dict
    to_encode.update({"exp": expire})

    # generate jwt token
    encode_JWT = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITM)

    return encode_JWT

def verify_token(token: str, credential_exeption):
    try:
        pyload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITM])
        uid: str = pyload.get("sub")
        if uid is None:
            raise credential_exeption
        token_data = TokenData(uid= uid)

        return token_data
    except JWTError:
        raise credential_exeption

async def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)



