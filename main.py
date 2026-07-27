from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from google import genai

app = FastAPI()

class TaskRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"status": "Gemini Service is Active"}

@app.post("/process")
def process_client_work(request: TaskRequest):
    try:
        # Load API key explicitly from Railway environment variable
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=request.prompt,
        )
        return {"status": "success", "result": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
