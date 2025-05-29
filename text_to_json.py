from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import openai
from langsmith.wrappers import wrap_openai
from langsmith import traceable
from fastapi.responses import JSONResponse
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

client = wrap_openai(openai.Client())

jsonExtact = APIRouter()

# Load system prompt from prompt.txt
with open("prompt.txt", "r", encoding="utf-8") as f:
    base_prompt = f.read()


class ParagraphInput(BaseModel):
    paragraph: str

@traceable
def generate_dental_json(paragraph: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": base_prompt},
            {"role": "user", "content": paragraph}
        ],
        temperature=0.5,
        top_p=0.95,
        max_tokens=1024
    )
    
    raw = response.choices[0].message.content
    cleaned = re.sub(r"^```json|```$", "", raw.strip()).strip("` \n")
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")

@jsonExtact.post("/extract_json")
def extract_json_from_text(data: ParagraphInput):
    try:
        result = generate_dental_json(data.paragraph)
        return JSONResponse(content=result)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
