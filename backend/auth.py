from fastapi import Depends
from fastapi.security import HTTPBearer

import jwt

from settings import SECRET_KEY

security = HTTPBearer()

def get_current_user(credentials = Depends(security)):
    try:
        token = credentials.credentials
        if token.startwith("Bearer "):
            token = token.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print(payload)
        return "1"
    except:
        print("nothing to print")
        return "2"