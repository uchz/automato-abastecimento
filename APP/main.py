from fastapi import FastAPI
from datetime import datetime
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4

app = FastAPI()

ocorrencias = []

@app.get("/")
def home():
    return {"status": "online"}

@app.get("/ocorrencias")
def listar_ocorrencias():
    return ocorrencias

@app.post("/ocorrencias")
def adicionar_ocorrencia(data: dict):
    data["id"] = str(uuid4())
    data["timestamp"] = datetime.now().isoformat()
    ocorrencias.append(data)
    return {"ok": True}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)