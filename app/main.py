from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
import database
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
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(vinhos.router, prefix="/vinhos", tags=["Vinhos"])

# --- Teste rápido de servidor ---
@app.get("/")
def root():
    return {"message": "Backend rodando e CORS habilitado!"}
