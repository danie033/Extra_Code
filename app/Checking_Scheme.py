from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI, Depends
from typing import Annotated


app=FastAPI()


oauth_shcheme=OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
def get_items(something:Annotated[str,Depends(oauth_shcheme)]):
    return something