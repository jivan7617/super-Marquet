
# archivo # 8
from jwt import encode, decode


def create_token(data:dict):
    token: str= encode(payload= data, key= "secret456", algorithm= "HS256")
    return token

def validate_token(token:str):
    data: dict= decode(token, key="secret456", algorithms=["HS256"])
    return data
