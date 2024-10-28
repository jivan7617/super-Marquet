

from fastapi import FastAPI, Path, Query,Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
import uvicorn


app = FastAPI()
app.title= "Super marquet"
app.version = "0.1"

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth= await super().__call__(request)
        data= validate_token(auth.credentials)
        if data != data["email"]:
            raise HTTPException(status_code=403, detail="invalid credentials")

class User(BaseModel):
    email: str
    password: str
    


class Person(BaseModel):
    id: int 
    name: str= Field(max_length=50)
    phone: str= Field(max_length=10)
    address: Optional[str] = None
    age: int= Field(ge=18)
    category: str= Field(max_length=10)
    
    class Config:
        json_schema_extra = {
            "example":{
                    "id":1,
                    "name":"juan perez labrador zea",
                    "phone": "3005624156",
                    "address": "street 26 cr 55- 54",
                    "age": 18,
                    "category": "customer"
                }
        }
   

people = [
    {
        "id": 1,
        "name": "luis carlos lopez henao",
        "phone": "3225687152",
        "address":"cll 25 crr 78-55", 
        "age": 23,
        "category": "customer"
    },
    {
        "id": 2,
        "name": "juan pablo ramirez zea",
        "phone": "3005872146",
        "address":"cll 26 crr 78-66", 
        "age": 24,
        "category": "employee"
    },
    {
        "id": 3,
        "name": "carlos lopez henao",
        "phone": "3007895426",
        "address":"cll 27 crr 78-55", 
        "age": 25,
        "category": "customer"
    },
    {
        "id": 4,
        "name": "pablo ramirez zea",
        "phone": "3008965472",
        "address":"cll 28 crr 78-66", 
        "age": 26,
        "category": "employee"
    }
]

@app.get('/', tags= ["Home"])
def home():
    return HTMLResponse("<h1>Principal page<h1>")

@app.post("/login", tags= ["auth"])
def login(user:User):
    if user.email== "admin@gmail.com" and user.password == "admin456":
        token:str= create_token(user.model_dump())
    return JSONResponse(status_code=200, content=token)

@app.get("/Users", tags=["Users"], response_model=List[Person])
def get_users():
    return JSONResponse(status_code=201, content= people)

@app.get("/User/{id}",tags=["Users"], response_model=Person)
def get_user_by_id(id:int= Path(ge=1, le=2000)):
    for i in people:
        if i["id"] == id:  
            return JSONResponse(status_code=201, content=i)
    return JSONResponse(content={"message": "invalid ID "})

@app.get("/ID/", tags=["Users"], response_model=int)
def get_id_by_name(name:str):
    for i in people:
        if i["name"] == name:
            Id_number= i["id"]  
            return JSONResponse(status_code=201,content=Id_number) 
    return JSONResponse(content={"message": "name not there "})
    

@app.get("/Phone/", tags= ["Users"], response_model=dict, dependencies=[Depends(JWTBearer())])
def get_phone(id:int= Query(ge=1, le=2000)):
    for i in people:
        if i["id"] == id:
            phone = i ["phone"]
            return  JSONResponse(status_code=201, content= phone) 
    return JSONResponse(content={"message": "ID not there "})

@app.get("/address/", tags= ["Users"], response_model=dict)
def get_address_by_id(id:int):
    for i in people:
        if i["id"] == id:
            address = i ["address"]
            return  JSONResponse(status_code=201, content= address) 
    return JSONResponse(content={"message": "ID not there "})

@app.get("/category/",tags=["Users"], response_model=List[Person])
def get_category(category:str):
    list_category= [i for i in people if i["category"]== category]
    return JSONResponse(status_code=201, content= list_category)

@app.post("/New_User", tags=["Users"], response_model=dict)
def add_new_user(person:Person):
    people.append(person)
    return JSONResponse(content={"message": "user added successfully "})
        

@app.put("/Update_Data/{id}",tags=["Users"], response_model= Person)
def Update_user(id:int, person: Person):
    for i in people:
        if id == i["id"] :        
            i["name"] = person.name
            i["phone"] = person.phone
            i["address"] = person.address
            i["age"] = person.age
            i["category"] = person.category 
            return JSONResponse(content= people) 
    return JSONResponse(content={"message": "ID not there "})
    

@app.delete("/Delete_User/{id}",tags=["Users"], response_model=dict)
def delete_user(id:int):
    for i in people:
        if i["id"] == id:
            people.remove(i)
            return JSONResponse(status_code=201, content={"message": "user deleted successfully "})
    return JSONResponse(content={"message": "ID not there "})
    
    
if __name__ == "__main__":
    uvicorn.run(app  , host= "127.0.0.1", port= 8000) 
    
    