from typing import Optional, List
from pydantic import BaseModel

# ------------------ Usuários ------------------
class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str

class UsuarioLogin(BaseModel):
    email: str
    senha: str

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str

    model_config = {
        "from_attributes": True
    }

# ------------------ Vinhos ------------------
class VinhoCreate(BaseModel):
    nome: str
    tipo: Optional[str] = None
    preco: float
    estoque: int
    descricao: Optional[str] = None
    imagem: Optional[str] = None

class AvaliacaoOut(BaseModel):
    id: int
    usuario_id: int
    vinho_id: int
    nota: int
    comentario: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class VinhoResponse(BaseModel):
    id: int
    nome: str
    tipo: Optional[str] = None
    preco: float
    estoque: int
    descricao: Optional[str] = None
    imagem: Optional[str] = None
    avaliacoes: Optional[List[AvaliacaoOut]] = []

    model_config = {
        "from_attributes": True
    }

class Token(BaseModel):
    access_token: str
    token_type: str
    usuario_id: int

class TokenData(BaseModel):
    email: Optional[str] = None

class GoogleLoginRequest(BaseModel):
    credential: str  # JWT token do Google

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None

class PasswordChange(BaseModel):
    senha_atual: str
    nova_senha: str
