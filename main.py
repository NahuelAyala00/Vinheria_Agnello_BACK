from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models, database
from routers import usuarios, vinhos

app = FastAPI()

# --- Configuração CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Para desenvolvimento, libera todas as origens
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# --- Cria as tabelas automaticamente ---
models.Base.metadata.create_all(bind=database.engine)

# --- Inclui routers depois do middleware ---
app.include_router(usuarios.router)
app.include_router(vinhos.router)

# --- Teste rápido de servidor ---
@app.get("/")
def root():
    return {"message": "Backend da Vinheria Agnello rodando com CORS habilitado!"}
