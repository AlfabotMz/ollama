from fastapi import FastAPI, HTTPException, Request
import json
import requests

app = FastAPI()

# Rota padrão para verificar se o Ollama está funcionando
@app.get("/")
def read_root():
    return {"message": "Ollama está funcionando"}

# Rota para gerar embeddings recebendo o corpo da requisição como string e convertendo para dicionário
@app.post("/api/embed")
async def generate_embedding(request: str):
    try:
        
        # Converte a string para um dicionário
        data = json.loads(request)

        # Verifica se 'model' e 'prompt' estão no dicionário
        if 'model' not in data or 'prompt' not in data:
            raise HTTPException(status_code=400, detail="Campos 'model' e 'prompt' são obrigatórios.")
        
        model = data['model']
        prompt = data['prompt']

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Erro ao decodificar a string JSON.")
    
    # Prepara a requisição para o Ollama
    url = "http://localhost:11434/api/embed"  # Ollama API endpoint
    payload = {
        "model": model,
        "prompt": prompt
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=500, detail="Erro ao gerar embeddings")
