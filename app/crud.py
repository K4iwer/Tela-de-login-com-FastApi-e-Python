from fastapi import HTTPException
from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas
from sqlalchemy.exc import SQLAlchemyError
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
import bcrypt


# precisa fazer as funções de busca do banco de dados


# Cria um novo registro
def create_user_register(db: Session, registro: schemas.RegistroCreate):
    try:
        db_registro = models.Registro(
            username=registro.username,
            email=registro.email,
            password=registro.password
        )

        # precisa fazer as funções de busca do banco de dados
        if db.find_by_username(db_registro.username):
            raise HTTPException(status_code=400, detail={"error": "Usuário já existe"})
        if db.find_by_email(db_registro.email):
            raise HTTPException(status_code=400, detail={"error": "Usuário já existe"})

        db.add(db_registro)
        db.commit()
        db.refresh(db_registro)
        return db_registro
    except SQLAlchemyError as e:
        db.rollback()
        raise e


# Busca usuário por id
def get_user(db: Session, user_id: int):
    try:
        user = db.find_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return user.to_dict()
    except SQLAlchemyError as e:
        raise e


# Deleta usuário por id
def delete_user(db: Session, user_id: int):
    try:
        user = db.find_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        user.delete_from_db()
        return {"message": "Usuário de id {user_id} deletado com sucesso"}
    except SQLAlchemyError as e:
        raise e


# Faz login do usuário
def user_login(db: Session, user_data: schemas.UserLoginSchema, Authorize: AuthJWT):
    try:
        user = db.find_by_username(user_data.username)
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
    except SQLAlchemyError as e:
        raise e



# Deleta o usuário por nome de usuário
def delete_user_byname(db: Session, username: str):
    try:
        user = db.find_by_username(username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.delete_from_db()
        return {"message": "Usuário {username} deletado com sucesso"}
    except SQLAlchemyError as e:
        raise e


# Faz logout do usuário
def logout(Authorize: AuthJWT):
    try:
        Authorize.jwt_required()
        user_id = Authorize.get_jwt_subject()
        return {"message": f"Usuário {user_id} saiu da seção"}
    except SQLAlchemyError as e:
        raise e



# Faz refresh do token
def refresh(Authorize: AuthJWT):
    try:
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()
        new_token = Authorize.create_access_token(subject=current_user, fresh=False)
        return {"access_token": new_token}
    except SQLAlchemyError as e:
        raise e


# Diz o status do servidor
def server_status():
    return {"message": "O servidor está rodando"}

