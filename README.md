# Vinheria Agnello - Backend

Back-end em **Python/FastAPI** para gerenciamento de vinhos, utilizando **PostgreSQL** como banco de dados.  
Este projeto fornece as APIs que o front-end consome para listar, cadastrar, editar e remover vinhos, além de autenticação via **JWT**.

---

## Descrição

Este projeto é o back-end do sistema [Vinheria Agnello](https://github.com/NahuelAyala00/Vinheria_Agnello_FRONT).  
Ele foi desenvolvido em **FastAPI** e expõe endpoints RESTful para operações de CRUD em vinhos, gestão de usuários e avaliações.  
Conta ainda com autenticação segura baseada em **JWT** e suporte a CORS para comunicação com o front-end.

---

## Pré-requisitos

Antes de rodar o projeto, você precisa ter instalado:

- Python 3.11+
- PostgreSQL (ou Docker para rodar o banco)
- Git
- [Uvicorn](https://www.uvicorn.org/) para rodar a aplicação FastAPI

---

## Instalação e Inicialização

1. Clone o repositório:
```bash
git clone https://github.com/NahuelAyala00/Vinheria_Agnello_BACK.git
cd Vinheria_Agnello_BACK
```
2. Instale as dependências:
pip install -r requirements.txt

3. Configure o banco de dados no arquivo database.py:
DATABASE_URL = "postgresql://usuario:senha@localhost:5432/vinheria"

4. Inicie o servidor FastAPI:
uvicorn main:app --reload

## Estrutura do Projeto

- main.py → Ponto de entrada da aplicação
- routers/ → Rotas organizadas (vinhos, usuários, avaliações)
- schemas/ → Modelos Pydantic para validação
- models/ → Modelos SQLAlchemy para o banco
- database.py → Configuração do banco de dados
- auth/ → Regras de autenticação JWT

## Funcionalidades

- CRUD de vinhos (criar, listar, atualizar e remover)
- Upload de imagens
- Cadastro e autenticação de usuários (JWT)
- Avaliação de vinhos
- Proteção de rotas com permissões
- CORS habilitado para comunicação com o front-end

## Como testar
- Certifique-se que o PostgreSQL está rodando.
- Crie o banco de dados vinheria.
- Rode a aplicação com uvicorn.
- Abra http://127.0.0.1:8000/docs e teste os endpoints.
- Use o front-end em JSP para interagir com a API.

## Dicas / Observações

- Em caso de erro de CORS, verifique as configurações no main.py.
- Tokens JWT expiram após certo tempo → o usuário precisa fazer login novamente.
- Para rodar em produção, use um servidor como Gunicorn ou Docker.
- Sempre mantenha o requirements.txt atualizado com:
```bash
pip freeze > requirements.txt
```