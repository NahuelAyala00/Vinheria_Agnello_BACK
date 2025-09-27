from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    senha = Column(String(200), nullable=False)

    avaliacoes = relationship("Avaliacao", back_populates="usuario")
    carrinho = relationship("Carrinho", back_populates="usuario", uselist=False)


class Vinho(Base):
    __tablename__ = "vinhos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    tipo = Column(String)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, nullable=False)
    descricao = Column(Text)
    imagem = Column(String, default="")
    avaliacoes = relationship("Avaliacao", back_populates="vinho")

class Avaliacao(Base):
    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    vinho_id = Column(Integer, ForeignKey("vinhos.id"))
    nota = Column(Integer)
    comentario = Column(Text)

    usuario = relationship("Usuario", back_populates="avaliacoes")
    vinho = relationship("Vinho", back_populates="avaliacoes")


class Carrinho(Base):
    __tablename__ = "carrinhos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    usuario = relationship("Usuario", back_populates="carrinho")
    itens = relationship("ItemCarrinho", back_populates="carrinho")


class ItemCarrinho(Base):
    __tablename__ = "itens_carrinho"

    id = Column(Integer, primary_key=True, index=True)
    carrinho_id = Column(Integer, ForeignKey("carrinhos.id"))
    vinho_id = Column(Integer, ForeignKey("vinhos.id"))
    quantidade = Column(Integer, default=1)

    carrinho = relationship("Carrinho", back_populates="itens")
