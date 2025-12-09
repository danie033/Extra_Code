from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app=FastAPI()

class Item(BaseModel):
    name: str
    description:str|None=None
    price:float
    tax:float=10.5
    tags: list[str]=[]

class UserBase(BaseModel):
    name:str
    age:int
    email:EmailStr

class UserIn(UserBase):
    password:str

class UserOut(UserBase):
    pass

class UserInDB(UserBase):
    hashed_password:str



items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

@app.get("/Home/{item}",
         response_model=Item,
         response_model_include={"name","tags"})

def method(item:str):
    response=items.get(item)
    return response

def hashfaked_save_user(user:UserIn):
    hashed_password="secret"+user.password
    userindb=UserInDB(**user.model_dump(),hashed_password=hashed_password)

    return userindb

@app.post("/Home1/",response_model=UserOut)
def get_user(user:UserIn):
    userindb=hashfaked_save_user(user)

    return userindb

