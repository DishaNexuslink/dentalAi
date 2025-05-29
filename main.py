from fastapi import FastAPI
from text_to_json import jsonExtact
from json_to_template import jsonPara

app = FastAPI()

app.include_router(jsonExtact)
app.include_router(jsonPara)