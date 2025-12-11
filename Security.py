from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated


app=FastAPI()

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="tokencito")

@app.get("/items/")
def read_items(token:Annotated[str,Depends(oauth2_scheme)]):
    return {"token_url:":token}