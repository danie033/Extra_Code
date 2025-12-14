from fastapi import FastAPI,Form, Depends
from pydantic import BaseModel, EmailStr
from typing import Annotated

app=FastAPI()

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}
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

class FormData(BaseModel):
    email:EmailStr
    password:str

def return_Form(email:EmailStr=Form(...),password:str=Form(...)) -> FormData:
    return FormData(email=email,password=password)

def common_parameters(q:str | None =None,skip:int=0,limit:int=100):
    return {"q":q,"skip":skip,"limit":limit}

commonDep=Annotated[dict,Depends(common_parameters)]

@app.get("/example")
def get_items(commons:commonDep):
    return commons


@app.post("/user/",description="User description here",tags=["Posting"])
def get_user(user:Annotated[FormData,Depends(return_Form)]):
    result={"Message":f"User: {user.email} succesfully logged in!"}

    return result


@app.post("/user2/")
def get_user(email:Annotated[EmailStr,Form(...)],password:Annotated[EmailStr,Form(...)]):
    result={"Message":f"User: {email} succesfully logged in!"}

    return result

@app.get("/")
def initialize():
    return {"Message":"Hello this is a API application"}

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

