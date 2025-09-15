from fastapi import HTTPException
from psycopg2 import Error as PsycopgError
import app.schemas as schemas
from fastapi_jwt_auth import AuthJWT
import bcrypt
import app.database as database


# precisa fazer as funções de busca do banco de dados


# Cria um novo registro
def create_user_register(registro: schemas.RegistroCreate):
    try:
        if database.get_user_by_email(registro.email):
            raise HTTPException(status_code=400, detail={"error": "Usuário já existe"})

        new_user = database.create_user(registro.username, registro.email, registro.password)
        if not new_user:
            raise HTTPException(status_code=500, detail="Erro ao criar usuário")

        return new_user
    except PsycopgError as e:
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno no servidor")


# Busca usuário por id
def get_user(user_id: int):
    try:
        user = database.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return user.to_dict()
    except PsycopgError as e:
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno no servidor")


# Deleta usuário por id
def delete_user(user_id: int):
    try:
        user = database.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        database.delete_user(user_id)
        return {"message": "Usuário de id {user_id} deletado com sucesso"}
    except PsycopgError as e:
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno no servidor")


# Faz login do usuário
def user_login(user_data: schemas.UserLoginSchema, Authorize: AuthJWT):
    try:
        user = database.get_user_by_username(user_data.username)
        if not user:
            raise HTTPException(status_code=401, detail="Credenciais inválidas")

        password_encoded = user_data.password.encode("utf-8")
        if not bcrypt.checkpw(password_encoded, user.password.encode("utf-8")):
            raise HTTPException(status_code=401, detail="Credenciais inválidas")

        access_token = Authorize.create_access_token(
            subject=user.id,
            user_claims={"username": user.username, "email": user.email},
            fresh=True,
        )
        refresh_token = Authorize.create_refresh_token(subject=user.id)
        return {"access_token": access_token, "refresh_token": refresh_token}
    except PsycopgError as e:
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno no servidor")



# Deleta o usuário por nome de usuário
def delete_user_byname(username: str):
    try:
        user = database.get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        database.delete_user(user.id)
        return {"message": "Usuário {username} deletado com sucesso"}
    except PsycopgError as e:
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

# Faz logout do usuário
def logout(Authorize: AuthJWT):
    try:
        Authorize.jwt_required()
        user_id = Authorize.get_jwt_subject()
        return {"message": f"Usuário {user_id} saiu da seção"}
    except PsycopgError as e:
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno no servidor")



# Faz refresh do token
def refresh(Authorize: AuthJWT):
    try:
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()
        new_token = Authorize.create_access_token(subject=current_user, fresh=False)
        return {"access_token": new_token}
    except PsycopgError as e:
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno no servidor")


# Diz o status do servidor
def server_status():
    return {"message": "O servidor está rodando"}

