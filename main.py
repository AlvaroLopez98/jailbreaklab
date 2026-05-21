from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import PromptRequest, AnalysisResult
from app.analyzer import analyze_prompt
from app.database import init_db, save_record, get_all_records
from dotenv import load_dotenv
import os
import httpx

load_dotenv()

app = FastAPI(
    title="JailbreakLab API",
    description="Sistema de deteccion de jailbreak y prompt injection en IA conversacional",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {"mensaje": "JailbreakLab API activa", "docs": "/docs"}

@app.post("/analyze")
def analyze(request: PromptRequest):
    result = analyze_prompt(request.prompt)
    ia_response = None

    if result.decision in ["permitir", "advertir"]:
        try:
            api_key = os.getenv("GROQ_API_KEY")
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": request.prompt}]
            }
            response = httpx.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            data = response.json()
            ia_response = data["choices"][0]["message"]["content"]
        except Exception as e:
            ia_response = f"Error al conectar con Groq: {str(e)}"

    result.ia_response = ia_response
    save_record(result, ia_response)
    return result

@app.get("/registros")
def registros():
    rows = get_all_records()
    return [
        {
            "id": r[0], "fecha": r[1], "prompt": r[2],
            "score": r[3], "risk_level": r[4],
            "triggered_rules": r[5], "decision": r[6],
            "message": r[7], "ia_response": r[8]
        }
        for r in rows
    ]
