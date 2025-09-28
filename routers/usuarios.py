from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import timedelta
import models, schemas
from database import get_db
from config import settings
from auth import create_access_token, verify_google_token

router = APIRouter(prefix="/usuarios", tags=["usuarios"])
security = HTTPBearer()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ------------------- Helpers -------------------
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def get_user_by_google_id(db: Session, google_id: str):
    return db.query(models.Usuario).filter(models.Usuario.google_id == google_id).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == user_id).first()

# ------------------- POST: criar usuário -------------------
@router.post("/", response_model=schemas.UsuarioResponse)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = get_user_by_email(db, usuario.email)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    novo_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=hash_password(usuario.senha),
        is_google_user=False
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

# ------------------- POST: login tradicional -------------------
@router.post("/login", response_model=schemas.Token)
def login(usuario: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    db_usuario = get_user_by_email(db, usuario.email)
    if not db_usuario:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    
    if db_usuario.is_google_user:
        raise HTTPException(
            status_code=401, 
            detail="Esta conta foi criada com Google. Use o login do Google."
        )
    
    if not verify_password(usuario.senha, db_usuario.senha):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_usuario.email, "user_id": db_usuario.id}, 
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "usuario_id": db_usuario.id
    }

# ------------------- POST: login com Google -------------------
@router.post("/login/google", response_model=schemas.Token)
async def google_login(google_data: schemas.GoogleLoginRequest, db: Session = Depends(get_db)):
    try:
        user_info = await verify_google_token(google_data.credential)
        db_usuario = get_user_by_email(db, user_info['email'])
        
        if not db_usuario:
            db_usuario = models.Usuario(
                nome=user_info['name'],
                email=user_info['email'],
                google_id=user_info['google_id'],
                is_google_user=True,
                senha=None
            )
            db.add(db_usuario)
            db.commit()
            db.refresh(db_usuario)
        else:
            if not db_usuario.is_google_user:
                raise HTTPException(
                    status_code=400, 
                    detail="Email já cadastrado com senha. Use login tradicional ou vincule as contas."
                )
            if not db_usuario.google_id:
                db_usuario.google_id = user_info['google_id']
                db.commit()
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": db_usuario.email, "user_id": db_usuario.id}, 
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "usuario_id": db_usuario.id
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro no login com Google: {str(e)}")

# ------------------- GET: perfil do usuário logado -------------------
@router.get("/me", response_model=schemas.UsuarioResponse)
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    from auth import verify_token
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(credentials.credentials, credentials_exception)
    user = get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

# ------------------- GET: listar usuários -------------------
@router.get("/", response_model=list[schemas.UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(models.Usuario).all()

# ------------------- GET: obter usuário por ID -------------------
@router.get("/{usuario_id}", response_model=schemas.UsuarioResponse)
def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = get_user_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

# ------------------- PUT: atualizar perfil -------------------
@router.put("/me", response_model=schemas.UsuarioResponse)
def atualizar_perfil(usuario_update: schemas.UsuarioUpdate,
                     credentials: HTTPAuthorizationCredentials = Depends(security),
                     db: Session = Depends(get_db)):
    from auth import verify_token
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(credentials.credentials, credentials_exception)
    db_usuario = get_user_by_email(db, email=token_data.email)
    if not db_usuario:
        raise credentials_exception
    
    if usuario_update.nome:
        db_usuario.nome = usuario_update.nome
    if usuario_update.email:
        existing_user = get_user_by_email(db, usuario_update.email)
        if existing_user and existing_user.id != db_usuario.id:
            raise HTTPException(status_code=400, detail="Email já está em uso")
        db_usuario.email = usuario_update.email
    if usuario_update.senha and not db_usuario.is_google_user:
        db_usuario.senha = hash_password(usuario_update.senha)
    
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# ------------------- POST: alterar senha -------------------
@router.post("/change-password")
def alterar_senha(password_change: schemas.PasswordChange,
                   credentials: HTTPAuthorizationCredentials = Depends(security),
                   db: Session = Depends(get_db)):
    from auth import verify_token
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(credentials.credentials, credentials_exception)
    db_usuario = get_user_by_email(db, email=token_data.email)
    if not db_usuario:
        raise credentials_exception
    
    if db_usuario.is_google_user:
        raise HTTPException(status_code=400, detail="Usuários do Google não possuem senha")
    if not verify_password(password_change.senha_atual, db_usuario.senha):
        raise HTTPException(status_code=400, detail="Senha atual incorreta")
    
    db_usuario.senha = hash_password(password_change.nova_senha)
    db.commit()
    
    return {"msg": "Senha alterada com sucesso"}

# ------------------- POST: vincular conta Google -------------------
@router.post("/link-google")
async def vincular_google(google_data: schemas.GoogleLoginRequest,
                          credentials: HTTPAuthorizationCredentials = Depends(security),
                          db: Session = Depends(get_db)):
    from auth import verify_token
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(credentials.credentials, credentials_exception)
    db_usuario = get_user_by_email(db, email=token_data.email)
    if not db_usuario:
        raise credentials_exception
    
    try:
        user_info = await verify_google_token(google_data.credential)
        if user_info['email'] != db_usuario.email:
            raise HTTPException(status_code=400, detail="O email da conta Google deve ser o mesmo da conta atual")
        
        existing_google_user = get_user_by_google_id(db, user_info['google_id'])
        if existing_google_user and existing_google_user.id != db_usuario.id:
            raise HTTPException(status_code=400, detail="Esta conta Google já está vinculada a outro usuário")
        
        db_usuario.google_id = user_info['google_id']
        db_usuario.is_google_user = True
        db.commit()
        
        return {"msg": "Conta Google vinculada com sucesso"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao vincular conta Google: {str(e)}")

# ------------------- POST: logout -------------------
@router.post("/logout")
def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return {"msg": "Logout realizado com sucesso"}

# ------------------- DELETE: deletar usuário -------------------
@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = get_user_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    db.delete(usuario)
    db.commit()
    return

# ------------------- DELETE: deletar minha conta -------------------
@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def deletar_minha_conta(credentials: HTTPAuthorizationCredentials = Depends(security),
                        db: Session = Depends(get_db)):
    from auth import verify_token
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(credentials.credentials, credentials_exception)
    db_usuario = get_user_by_email(db, email=token_data.email)
    if not db_usuario:
        raise credentials_exception
    
    db.delete(db_usuario)
    db.commit()
    return
