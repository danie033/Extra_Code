from fastapi import FastAPI, Depends,Form
from typing import Annotated
from pydantic import BaseModel

app=FastAPI()



fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class CommonQueryParam:
    def __init__(s,q:str|None=None,skip:int=0,limit:int=100):
        s.q=q
        s.skip=skip
        s.limit=limit

commonDP=Annotated[CommonQueryParam,Depends()]

def secondDP(commons:commonDP):
    if not commons.q:
        return {"Message":"No q parameter at this moment"}
    return {"q":commons.q,"skip":commons.skip,"limit":commons.limit}

@app.get("/extra/")
def extra_method(param:Annotated[dict,Depends(secondDP)]):
    return param
    
@app.post("/items/")
def get_item(comons:commonDP):
    response={}
    if comons.q:
        response.update({"q":comons.q})
    items=fake_items_db[comons.skip:comons.skip+comons.limit]

    response.update({"items":items})

    return response