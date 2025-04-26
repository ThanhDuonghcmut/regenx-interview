from fastapi import Depends
from fastapi.security import HTTPBearer

import jwt

from settings import SECRET_KEY

security = HTTPBearer()

def get_current_user(credentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_aud": False})
        return payload['sub']
    except:
        return None