# routers/vinhos.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine

# cria as tabelas (uma vez)
models.Base.metadata.create_all(bind=engine)

router = APIRouter(tags=["vinhos"])

# Dependência para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------ POST ------------------
@router.post("/vinhos", response_model=schemas.VinhoResponse)
def criar_vinho(vinho: schemas.VinhoCreate, db: Session = Depends(get_db)):
    db_vinho = models.Vinho(
        nome=vinho.nome,
        tipo=vinho.tipo,
        preco=vinho.preco,
        estoque=vinho.estoque,
        descricao=vinho.descricao,
        imagem=vinho.imagem
    )
    db.add(db_vinho)
    db.commit()
    db.refresh(db_vinho)
    return db_vinho


# ------------------ GET ------------------
@router.get("/vinhos", response_model=list[schemas.VinhoResponse])
def listar_vinhos(db: Session = Depends(get_db)):
    return db.query(models.Vinho).all()


@router.get("/vinhos/{vinho_id}", response_model=schemas.VinhoResponse)
def obter_vinho(vinho_id: int, db: Session = Depends(get_db)):
    vinho = db.query(models.Vinho).filter(models.Vinho.id == vinho_id).first()
    if not vinho:
        raise HTTPException(status_code=404, detail="Vinho não encontrado")
    return vinho


# ------------------ PUT ------------------
@router.put("/vinhos/{vinho_id}", response_model=schemas.VinhoResponse)
def atualizar_vinho(vinho_id: int, vinho: schemas.VinhoCreate, db: Session = Depends(get_db)):
    db_vinho = db.query(models.Vinho).filter(models.Vinho.id == vinho_id).first()
    if not db_vinho:
        raise HTTPException(status_code=404, detail="Vinho não encontrado")

    db_vinho.nome = vinho.nome
    db_vinho.tipo = vinho.tipo
    db_vinho.preco = vinho.preco
    db_vinho.estoque = vinho.estoque
    db_vinho.descricao = vinho.descricao
    db_vinho.imagem = vinho.imagem
    
    db.commit()
    db.refresh(db_vinho)
    return db_vinho


# ------------------ DELETE ------------------
@router.delete("/vinhos/{vinho_id}")
def deletar_vinho(vinho_id: int, db: Session = Depends(get_db)):
    db_vinho = db.query(models.Vinho).filter(models.Vinho.id == vinho_id).first()
    if not db_vinho:
        raise HTTPException(status_code=404, detail="Vinho não encontrado")

    db.delete(db_vinho)
    db.commit()
    return {"detail": "Vinho deletado com sucesso"}
