from fastapi import FastAPI
import models, database
from routers import vinhos

app = FastAPI()

# cria as tabelas (uma vez)
models.Base.metadata.create_all(bind=database.engine)

# inclui routers
app.include_router(vinhos.router)
