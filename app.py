from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

# Modelo para receber o corpo da requisição
class EmbedRequest(BaseModel):
    model: str
    input: str

# Rota padrão para verificar se o Ollama está funcionando
@app.get("/")
def read_root():
    return {"message": "Ollama está funcionando"}

# Rota para gerar embeddings recebendo o corpo da requisição como JSON
@app.post("/api/embed")
async def generate_embedding(request: EmbedRequest):
    try:
        # Extrai o modelo e o prompt do JSON
        model = request.model
        input = request.input
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar a requisição: {str(e)}")
    
    # Prepara a requisição para o Ollama
    url = "http://localhost:11434/api/embed"  # Ollama API endpoint
    payload = {
        "model": model,
        "input": input
    }
    headers = {"Content-Type": "application/json"}
    
    # Faz a requisição POST ao Ollama
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=500, detail="Erro ao gerar embeddings")

