from fastapi import FastAPI
from . import models, database
from .routers import usuarios, vinhos

app = FastAPI()

# cria as tabelas automaticamente
models.Base.metadata.create_all(bind=database.engine)

# inclui rotas
app.include_router(usuarios.router)
app.include_router(vinhos.router)
