# Passos para fazer a aplicação rodar:

Criar um ambiente virtual
```
python -m venv venv
```

Ativar (Windows)
```.\venv\Scripts\activate```

Ativar (macOS/Linux)
```source venv/bin/activate```

Instalar as bibliotecas necessárias:

```
pip install requests
pip install fastapi
pip install psycopg2
pip install fastapi-jwt-auth
pip install bcrypt
pip install "pydantic<2.0"
```

Abrir a aplicação do docker no desktop

Rodar no root do projeto:

```docker exec -it postgressql psql -U postgres -d api_db```

(isso inicializa o banco de dados postgres)

Rodar no root do projeto

```uvicorn app.main:app --reload --port 8000```

(isso inicializa a API)

