from fastapi import HTTPException
from psycopg2 import Error as PsycopgError
import app.schemas as schemas
from fastapi_jwt_auth import AuthJWT
import bcrypt
import app.database as database
from app.blocklist import BLOCKLIST


# Cria um novo registro
def create_user_register(registro: schemas.UserSchema):
    try:
        print("chegou aqui")
        if database.get_user_by_email(registro.email):
            raise HTTPException(status_code=400, detail={"error": "Usuário já existe"})
        
        print("passou ai")
        senha_bytes = registro.password.encode('utf-8')
        hash_bytes = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
        hash_para_salvar_no_db = hash_bytes.decode('utf-8')

        print("passou aqui")
        new_user = database.create_user(registro.username, registro.email, hash_para_salvar_no_db)
        if not new_user:
            raise HTTPException(status_code=500, detail="Erro ao criar usuário")

        return new_user
    except HTTPException as e:
        print(e)
        raise e
    except PsycopgError as e:
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro interno no servidor")


# Busca usuário por id
def get_user(user_id: int):
    try:
        user = database.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return dict(user)
    except HTTPException as e:
        print(e)
        raise e
    except PsycopgError as e:
        raise e
    except Exception as e:
        print(e)
        raise e

# Deleta usuário por id
def delete_user(user_id: int):
    try:
        user = database.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        database.delete_user(user_id)
        return {"message": f"Usuário de id {user_id} deletado com sucesso"}
    except HTTPException as e:
        print(e)
        raise e
    except PsycopgError as e:
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro interno no servidor")


# Faz login do usuário
def user_login(user_data: schemas.UserLoginSchema, Authorize: AuthJWT):
    try:
        user = database.get_user_by_username(user_data.username)

        print("Passou1")
        if not user or not bcrypt.checkpw(user_data.password.encode('utf-8'), user['password'].encode('utf-8')):
            raise HTTPException(status_code=401, detail="Credenciais inválidas")

        print("Passou2")
        user_id = user['id']
        access_token = Authorize.create_access_token(subject=user_id, fresh=True)
        refresh_token = Authorize.create_refresh_token(subject=user_id)

        print("Passou3")

        Authorize.set_access_cookies(access_token)
        Authorize.set_refresh_cookies(refresh_token)

        print("Passou4")
        return {"access_token": access_token, "refresh_token": refresh_token}
    except HTTPException as e:
        print(e)
        raise e
    except PsycopgError as e:
        print(e)
        raise e
    except Exception as e:
        print(e)
        raise e



# Deleta o usuário por nome de usuário
def delete_user_byname(username: str):
    try:
        user = database.get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        database.delete_user(user["id"])
        return {"message": "fUsuário {username} deletado com sucesso"}
    except HTTPException as e:
        print(e)
        raise e
    except PsycopgError as e:
        raise e
    except Exception as e:
        print(e)
        raise e

# Faz logout do usuário
def logout(Authorize: AuthJWT):
    try:
        print("PASSOU LOGOUT1")
        Authorize.jwt_required()
        print("PASSOU LOGOUT2")
        jti_access = Authorize.get_raw_jwt()['jti']
        print("PASSOU LOGOUT3")
        BLOCKLIST.add(jti_access)
        print("PASSOU LOGOUT4")
        Authorize.unset_jwt_cookies()
        return {"message": f"Usuário saiu da seção"}
    except HTTPException as e:
        print(e)
        raise e
    except Exception as e:
        print(e)
        raise e



# Faz refresh do token
def refresh(Authorize: AuthJWT):
    try:
        print("PASSOU1")
        Authorize.jwt_refresh_token_required()
        print("PASSOU2")
        current_user = Authorize.get_jwt_subject()
        print("PASSOU3")
        new_token = Authorize.create_access_token(subject=current_user, fresh=False)
        print("PASSOU4")
        return {"access_token": new_token}
    except Exception as e:
        print(e)
        raise e


# Diz o status do servidor
def server_status():
    return {"message": "O servidor está rodando"}

