import os
from fastapi import FastAPI, HTTPException
from google import genai
from pydantic import BaseModel

app = FastAPI()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

class TaskRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"status": "Gemini Service is Active"}

@app.post("/process")
def process_client_work(request: TaskRequest):
    if not client:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not configured.")

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=request.prompt,
        )
        return {"status": "success", "result": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
