# routers/carrinho.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/carrinho", tags=["carrinho"])

# GET: pega todos os itens do carrinho de um usuário
@router.get("/{usuario_id}", response_model=schemas.CarrinhoResponse)
def get_carrinho(usuario_id: int, db: Session = Depends(get_db)):
    carrinho = db.query(models.Carrinho).filter(models.Carrinho.usuario_id == usuario_id).first()
    if not carrinho:
        raise HTTPException(status_code=404, detail="Carrinho não encontrado")
    return carrinho

# POST: adiciona um vinho ao carrinho
@router.post("/{usuario_id}/adicionar", response_model=schemas.CarrinhoResponse)
def adicionar_ao_carrinho(usuario_id: int, item: schemas.CarrinhoItemCreate, db: Session = Depends(get_db)):
    carrinho = db.query(models.Carrinho).filter(models.Carrinho.usuario_id == usuario_id).first()
    if not carrinho:
        carrinho = models.Carrinho(usuario_id=usuario_id)
        db.add(carrinho)
        db.commit()
        db.refresh(carrinho)

    # Adiciona o vinho
    db_item = models.CarrinhoItem(
        carrinho_id=carrinho.id,
        vinho_id=item.vinho_id,
        quantidade=item.quantidade
    )
    db.add(db_item)
    db.commit()
    db.refresh(carrinho)
    return carrinho

# PUT: atualiza a quantidade de um item
@router.put("/{usuario_id}/atualizar/{item_id}", response_model=schemas.CarrinhoResponse)
def atualizar_item(usuario_id: int, item_id: int, item: schemas.CarrinhoItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(models.CarrinhoItem).filter(
        models.CarrinhoItem.id == item_id,
        models.CarrinhoItem.carrinho.has(usuario_id=usuario_id)
    ).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item do carrinho não encontrado")
    
    db_item.quantidade = item.quantidade
    db.commit()
    db.refresh(db_item)
    return db_item.carrinho

# DELETE: remove um item do carrinho
@router.delete("/{usuario_id}/remover/{item_id}", response_model=schemas.CarrinhoResponse)
def remover_item(usuario_id: int, item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.CarrinhoItem).filter(
        models.CarrinhoItem.id == item_id,
        models.CarrinhoItem.carrinho.has(usuario_id=usuario_id)
    ).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item do carrinho não encontrado")
    
    carrinho = db_item.carrinho
    db.delete(db_item)
    db.commit()
    return carrinho
