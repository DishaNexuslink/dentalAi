# test_api.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TestInput(BaseModel):
    paragraph: str

@app.post("/test")
def test_route(data: TestInput):
    return {"message": "OK"}
