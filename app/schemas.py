from pydantic import BaseModel
from typing import Optional

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str

class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: str
    class Config:
        orm_mode = True

class VinhoCreate(BaseModel):
    nome: str
    tipo: Optional[str]
    safra: Optional[int]
    preco: float
    estoque: int

class VinhoOut(BaseModel):
    id: int
    nome: str
    preco: float
    class Config:
        orm_mode = True
