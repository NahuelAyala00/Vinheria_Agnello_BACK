from sqlalchemy.orm import Session
from . import models, schemas

def criar_usuario(db: Session, usuario: schemas.UsuarioCreate):
    novo = models.Usuario(
        nome=usuario.nome, 
        email=usuario.email, 
        senha=usuario.senha
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

def listar_vinhos(db: Session):
    return db.query(models.Vinho).all()
