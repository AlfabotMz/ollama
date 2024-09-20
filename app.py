from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

# Rota padrão para verificar se o Ollama está funcionando
@app.get("/")
def read_root():
    return {"message": "Ollama está funcionando"}

# Modelo para receber dados via POST
class EmbedRequest(BaseModel):
    model: str
    prompt: str

# Rota para gerar embeddings usando o modelo especificado
@app.post("/api/embed")
def generate_embedding(request: EmbedRequest):
    url = "http://localhost:11434/api/embed"  # Ollama API endpoint
    payload = {
        "model": request.model,
        "prompt": request.prompt
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=500, detail="Erro ao gerar embeddings")

