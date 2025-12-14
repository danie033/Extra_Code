from fastapi import FastAPI, Request
import time
import asyncio

import requests

app=FastAPI()

@app.middleware("http")
async def process_time_header(request:Request,call_next):
    star_time=time.perf_counter()

    print(f"Starting time: {0}")
    response=await call_next(request)

    end_time=time.perf_counter()-star_time
    print(f"ending time: {end_time}")
    response.headers["X-Process-Time-daniel"]=str(end_time)
    
    return response



@app.get("/Home")
async def say_Hello(request:Request):
    await asyncio.sleep(2)

    return {"Message:":"Hello, we are testing middleware"}

@app.get("/time_responses")
def get_times():
    r=requests.get("http://127.0.0.1:8080/Home")

    return {"Time for the Home endpoint:":r.headers}