from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from pydantic import BaseModel
from pwdlib import PasswordHash
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone



app=FastAPI()

hasher_password=PasswordHash.recommended()

def pass_hashed_method(plain_password):
    hash_pass=hasher_password.hash(plain_password)
    return hash_pass
SECRET_KEY="2570ec3fa958a64b20180e925de0ef5f36bb53d22f037dc6bf1f1e36778a8be1"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": f"{pass_hashed_method("secret")}",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": f"{pass_hashed_method("secret2")}",
        "disabled": True,
    },
}

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

class Token(BaseModel):
    access_token:str
    token_type:str

class TokeData(BaseModel):
    username:str

class User(BaseModel):
    username:str
    email: str|None=None
    full_name: str|None=None
    disabled: bool|None=None

class UserInDB(User):
    hashed_password:str


def verify_password(plain_password,hashed_password):
    verify=hasher_password.verify(plain_password,hashed_password)
    return verify

def get_user(db:dict,username:str):
    if username in db:
        user=db.get(username)
        return UserInDB(**user)

def authenticate_user(db:dict,username,password):
    user = get_user(db,username)

    if user is None:
        return False
    if not verify_password(password,user.hashed_password):
        return False
    
    return user
    

def create_access_token(data:dict,expires_time:timedelta):
    data_to_encode=data.copy()

    if expires_time:
        expire=datetime.now(timezone.utc)+expires_time
    else: 
        expire=datetime.now(timezone.utc)+timedelta(minutes=15)

    data_to_encode.update({"exp":expire})

    encoded_jwt=jwt.encode(data_to_encode,SECRET_KEY,ALGORITHM)
    return encoded_jwt

def check_current_user(token:Annotated[str,Depends(oauth2_scheme)]):

    credential_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail="User not authorized",
                                      headers={"WWW-Authenticate":"Bearer"})
    
    try:
        payload=jwt.decode(token,SECRET_KEY,ALGORITHM)
        username=payload.get("sub") 
        if username is None:
            raise credential_exception
        user_data=TokeData(username=username)
    except:
        raise credential_exception

    user=get_user(fake_users_db,user_data.username)

    if user is None:
        raise credential_exception
    return user
    

def check_current_active_user(user:Annotated[UserInDB,Depends(check_current_user)]):
    if user.disabled:
        raise HTTPException("User not active")
    return user

@app.post("/login")
def check_credentials(user_credentials:Annotated[OAuth2PasswordRequestForm,Depends()]) -> Token:

    #Authenticate User
    credential_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail="User not authorized",
                                      headers={"WWW-Authenticate":"Bearer"})
    
    user=authenticate_user(fake_users_db,user_credentials.username,user_credentials.password)
    
    if not user:
        raise credential_exception
    
    #Now create the Token

    delta_time=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    jwt_token=create_access_token({"sub":user.username},delta_time)
    
    token=Token(access_token=jwt_token,token_type="bearer")

    return token

@app.get("/items")
def read_items(user:Annotated[User,Depends(check_current_active_user)]):
    return {f"{user.username} authenticated. list of items:":fake_users_db}