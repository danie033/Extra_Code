from fastapi import FastAPI, BackgroundTasks, Depends
from typing import Annotated
import asyncio


app=FastAPI()


def write_log(message:str):
    with open("file.txt",mode="a") as log:
        log.write(message)

def get_query(background_task:BackgroundTasks,q:str|None=None):
    if q:
        content=f"Found query {q}\n"
        background_task.add_task(write_log,content)
    return q


@app.get("/")
def hello_world():
    return {"Message":"Hello World"}

@app.post("/send_notification/{email}")
def get_notification(email:str,background_task:BackgroundTasks,q:Annotated[str,Depends(get_query)]):
    content=f"message to {email}\n"
    background_task.add_task(write_log,content)

    return {"Notification:":"Message sent"}