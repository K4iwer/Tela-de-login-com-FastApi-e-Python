from fastapi import HTTPException, Depends, status
from fastapi import FastAPI
import app.schemas as schemas
import Atividade1.app.services as services
from app.database import get_db
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from database import init_db

if __name__ == "__main__":
    init_db()
    print("Banco de dados inicializado!")

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
def userRegister(registro: schemas.RegistroCreate):
    try:
        return services.create_user_register(registro=registro)
    except HTTPException as e:
        raise e  
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")


# endpoint para obter dados de usuário
@app.get("/user/{user_id}", response_model=schemas.UserSchema)
def get_user(user_id: int):
    try:
        return services.get_user(user_id=user_id)
    except HTTPException as e:
        raise e  
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")
    

# endpoint para deletar usuário
@app.delete("/user/{user_id}")
def delete_user(user_id: int):
    try:
        return services.delete_user(user_id=user_id)
    except HTTPException as e:
        raise e  
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")
    

# endpoint para fazer login
@app.post("/login")
def login(user_data: schemas.UserLoginSchema, Authorize: AuthJWT = Depends()):
    try:
        return services.user_login(user_data=user_data, Authorize=Authorize)
    except HTTPException as e:
        raise e  
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")
    

# endpoint para deletar usuário por username
@app.delete("/user/byname/{username}")
def delete_user_byname(username: str):
    try:
        return services.delete_user_byname(username=username)
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
        return services.logout(Authorize=Authorize)
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
        return services.refresh(Authorize=Authorize)
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
        return services.server_status()
    except HTTPException as e:
        raise e  
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")