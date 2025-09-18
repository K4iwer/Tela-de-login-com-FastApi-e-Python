# Passos para fazer a aplicação rodar (back-end):

Criar um ambiente virtual
```
python -m venv venv
```

Ativar (Windows)
```
.\venv\Scripts\activate
```

Ativar (macOS/Linux)
```
source venv/bin/activate
```

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

```
docker-compose up -d
```

(isso inicializa o banco de dados postgres)

Rodar no root do projeto

```
uvicorn app.main:app --reload --port 8000
```

(isso inicializa a API)

E possível realizar testes individuais para cada endpoint pelo arquivo test_api.py

# Passos para fazer a aplicação rodar (front-end):

Entrar na pasta front

```
cd front/
```

Instalar as dependencias (necessário Node.js 18+)

```
npm install
```

Executar o front

```
npm run dev
```

A aplicação se inicia, por padrão, na porta 8080. Digite no navegador:

```
localhost:8080
```

Divirta-se.
