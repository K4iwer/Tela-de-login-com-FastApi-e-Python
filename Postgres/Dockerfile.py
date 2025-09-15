# Dockerfile para PostgreSQL

# Utiliza a imagem oficial do PostgreSQL
FROM postgres:15

# Define as variáveis de ambiente para o banco de dados
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=42069
ENV POSTGRES_DB=api_db

# Expõe a porta padrão do PostgreSQL
EXPOSE 5432