from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Allow frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenRouter API details
API_KEY = "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"  # Replace with your actual API key
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Define input model
class LegalTextRequest(BaseModel):
    text: str

@app.post("/simplify")
def simplify_legal_text(request: LegalTextRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    # Prepare API request
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://www.legaliser.com",
        "X-Title": "LegalEase",
    }
    
    payload = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [{"role": "user", "content": request.text}]
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return {"simplified_text": data["choices"][0]["message"]["content"]}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
