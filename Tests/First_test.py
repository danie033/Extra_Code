from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

#Be careful with headers and query parameters. They have to passed as strings but the response will be parsed!!

def test_read_body():
    response=client.get("/home7/", headers={"headerName":"Title of the header","headerNumber":"1024"})
    result= {"headerTitle":{"headerName":"Title of the header","headerNumber":1024}}

    assert response.status_code==200
    assert response.json()==result
    
def test_read_movies():
    payload=[{"category":"Action","duration":120,"url":"https://www.fastapi.com/"}]
    response=client.post("/home6/",json=payload)
    assert response.status_code==200
    assert response.json()=={"movies-passed":payload}

def test_query_parameters():
    payload={"limit":"40","offset":"6","categories":"chocolate","active":"true"}

    response=client.get("/home3/",params=payload)
    assert response.status_code==200
    assert response.json()=={"limit":40,"offset":6,"categories":"chocolate","active":True}

def test_query_parameters_path():
    payload={"limit":"40","offset":"6","categories":"chocolate","active":"true"}

    response=client.get("/home2/I love you",params=payload)
    assert response.status_code==200
    assert response.json()=={"limit":40,"offset":6,"categories":"chocolate","active":True,"Ambri":"I love you"}