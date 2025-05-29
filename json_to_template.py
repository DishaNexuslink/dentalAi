from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import openai
from langsmith.wrappers import wrap_openai
from langsmith import traceable
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

load_dotenv()

client = wrap_openai(openai.Client())

jsonPara = APIRouter()

class JsonInput(BaseModel):
    data: Dict[str, Any]

@traceable
def template(jsoninput: Dict[str, Any]) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": 
            '''You are a clinical documentation assistant.

Given structured dental procedure data in JSON format, generate a **clean, professional paragraph** describing the full treatment. At the **end of the paragraph**, display the provider and assistant name in this format:

Dr Ajay Patel  
Assistant: {{assistant name}}

Instructions:
- Merge the procedure into one cohesive clinical paragraph.
- Do not use phrases like "under supervision of..." or embed names into the paragraph.
- After the paragraph, write the doctor and assistant names in separate lines as shown.
- Use plain formatting (no bullets or bold).

Input JSON:
{{Paste your JSON here}}

'''
            },
            {"role": "user", "content": str(jsoninput)}
        ],
        temperature=0.5,
        top_p=0.95,
        max_tokens=1024
    )
    return response.choices[0].message.content

@jsonPara.post("/jsonTOPara")
def extract_json_from_text(data: JsonInput):
    try:
        result = template(data.data)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
