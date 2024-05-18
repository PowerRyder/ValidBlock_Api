from datetime import timedelta, datetime
from fastapi import HTTPException, Security, status
from jose import JWTError, jwt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.utilities.utils import config

jwt_config = config['JWT']

SECRET_KEY = jwt_config['SecretKey']
ALGORITHM = jwt_config['Algorithm']
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24*7  # 1 week

security = HTTPBearer()

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print(data)
        
        expiry = data.get('exp')
        payload = data.get("payload")

        if payload is None:
            raise credentials_exception
        
        if datetime.utcfromtimestamp(expiry)<datetime.utcnow():
            raise credentials_exception
            
        return payload
    except JWTError:
        raise credentials_exception


async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials.replace('Bearer ','')
    token_payload = verify_token(token)
    print(token_payload)
    return token_payload

