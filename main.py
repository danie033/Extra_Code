from fastapi import FastAPI, Query, Path, Body, Header, Cookie
from typing import Annotated, Literal
from pydantic import AfterValidator, Field, BaseModel,HttpUrl
import random

class FilterParameters(BaseModel):
      limit: int =Field(10,gt=0,lt=100)
      offset: int = Field(1,gt=0,lt=10)
      categories: Literal["chocolate","vanilla","chips","whatever"]="whatever"
      active: bool

class Item(BaseModel):
      id:int
      description:str
      active:bool

class Movies(BaseModel):
      category:str
      duration:int
      url:HttpUrl

class User(BaseModel):
      id:int
      name:str
      age:str
      preferences:set[str]=set()
      movies:Movies

class Exam_Header(BaseModel):
      headerName:str
      headerNumber:int

class Exam_Cookie(BaseModel):
      cookieName:str
      cookieNumber:int



app=FastAPI()

@app.get("/home7/")
def other(h:Annotated[Exam_Header,Header()]):
      results={"headerTitle":h}
      return results

@app.post("/home6/")
def other(movies:list[Movies]):
      return {"movies-passed":movies}

@app.get("/home5/")
def other(itemcito:Annotated[Item,Body(embed=True)]):
      return itemcito

@app.put("/home4/")
def other_method(other_variable:Annotated[str,Body()],
                 user:User|None=None,
                 item:Item|None=None,
                 ):
      
      results={"user":user,"item":item,"other":other_variable}
      return results

@app.get("/home3/")
def check_ouput(q:Annotated[FilterParameters,Query()]):
      return q

@app.get("/home2/{ambri_id}")
def get_item(ambri_id:Annotated[str,Path(description="I love Ambri")],
             q:Annotated[FilterParameters,Query()],
             ):
      result={"limit":q.limit,
              "offset":q.offset,
              "categories":q.categories,
              "active":q.active,
              }
      return result



data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxyddqwdw",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}


@app.get("/Homepage/{item_id}")
def greet(item_id:Annotated[int,Path(description="This is a title for the path",gt=0)],
          q:Annotated[list[str]|None,Query(title="This is a query String")]=None,
          ):
        #result={"items":[{"item_id":"Foo"},{"item_id":"Bar"}]}
        result={"item_id":item_id}
        if q: 
            result.update({"q":q})
        return result


def validator_id(identification:str):
      if not identification.startswith(("isbn","imdb")):
            raise ValueError("Please make sure the id has the correct format")
      
      return identification

@app.get("/Home1/")
def valid_id(q:Annotated[str |None,AfterValidator(validator_id)]=None):
        if q:
              item=data.get(q)
        else:
              q,item = random.choice(list(data.items()))
        return {"id":q,"item":item}
