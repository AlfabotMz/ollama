from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import requests

app = FastAPI()

# Modelo para receber o corpo da requisição
class EmbedRequest(BaseModel):
    model: str
    input: str

class EmbenddingRequest(BaseModel):
    model: str
    prompt: str

# Rota padrão para verificar se o Ollama está funcionando
@app.get("/")
def read_root():
    return {"message": "Ollama está funcionando"}

# Rota para gerar embeddings recebendo o corpo da requisição como JSON
@app.post("/api/embed")
async def generate_embed(request: Request):
    try:
        # Lê o corpo da requisição como string
        body = await request.body()
        body_str = body.decode("utf-8").strip()  # Remove espaços em branco nas extremidades

        # Tenta interpretar a string como JSON
        data = json.loads(body_str)

        # Verifica se 'model' e 'input' estão presentes
        if 'model' not in data or 'input' not in data:
            raise HTTPException(status_code=400, detail="Campos 'model' e 'input' são obrigatórios.")

        model = data['model']
        input_text = data['input']
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="O corpo da requisição deve ser um JSON válido.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar a requisição: {str(e)}")
    
    # Prepara a requisição para o Ollama
    url = "http://localhost:11434/api/embed"  # Ollama API endpoint
    payload = {
        "model": model,
        "prompt": input_text  # Usa o campo input como prompt
    }
    headers = {"Content-Type": "application/json"}
    
    # Faz a requisição POST ao Ollama
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=500, detail="Erro ao gerar embeddings")

@app.post("/api/embenddings")
async def generate_embeddings(request: EmbenddingRequest):
    try:
        # Extrai o modelo e o prompt do JSON
        model = request.model
        prompt= request.prompt
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar a requisição: {str(e)}")
    
    # Prepara a requisição para o Ollama
    url = "http://localhost:11434/api/embed"  # Ollama API endpoint
    payload = {
        "model": model,
        "prompt": prompt
    }
    headers = {"Content-Type": "application/json"}
    
    # Faz a requisição POST ao Ollama
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=500, detail="Erro ao gerar embeddings")
