from fastapi import FastAPI, Query, Path
from typing import Annotated
from pydantic import AfterValidator
import random

app=FastAPI()

data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxyddqwdw",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}


@app.get("/Homepage/{item_id}")
def greet(q:Annotated[list[str],Query(title="This is a query String")],
          item_id:Annotated[int,Path(description="This is a title for the path")],
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