from fastapi import HTTPException, Depends, status
from fastapi import FastAPI
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import app.schemas as schemas
import app.crud as crud
from app.database import get_db

from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel

app = FastAPI()

# ver essa parada de autenticaçao melhor depois
# Configuração do JWT
class Settings(BaseModel):
    authjwt_secret_key: str = "super-secret"  # coloque uma secret key forte

@AuthJWT.load_config
def get_config():
    return Settings()


# endpoint para inserir dados de registro
@app.post("/register", response_model=schemas.UserSchema)
def userRegister(registro: schemas.RegistroCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_user_register(db=db, registro=registro)
    except HTTPException as e:
        raise e  
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Erro de chave primária: o ID já existe.")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")


# endpoint para obter dados de usuário
@app.get("/user/{user_id}", response_model=schemas.UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_user(db=db, user_id=user_id)
    except HTTPException as e:
        raise e  
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")
    

# endpoint para deletar usuário
@app.delete("/user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_user(db=db, user_id=user_id)
    except HTTPException as e:
        raise e  
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")
    

# endpoint para fazer login
@app.post("/login")
def login(user_data: schemas.UserLoginSchema, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        return crud.user_login(db=db, user_data=user_data, Authorize=Authorize)
    except HTTPException as e:
        raise e  
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")
    

# endpoint para deletar usuário por username
@app.delete("/user/byname/{username}")
def delete_user_byname(username: str, db: Session = Depends(get_db)):
    try:
        return crud.delete_user_byname(db=db, username=username)
    except HTTPException as e:
        raise e  
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")


# endpoint para fazer logout
@app.post("/logout")
def logout(Authorize: AuthJWT = Depends()):
    try:
        return crud.logout(Authorize=Authorize)
    except HTTPException as e:
        raise e  
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")


# endpoint para refresh token
@app.post("/refresh")
def refresh(Authorize: AuthJWT = Depends()):
    try:
        return crud.refresh(Authorize=Authorize)
    except HTTPException as e:
        raise e  
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")


# endpoint para verificar status do servidor
@app.get("/status")
def server_status():
    try:
        return crud.server_status()
    except HTTPException as e:
        raise e  
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")