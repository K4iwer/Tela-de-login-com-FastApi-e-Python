import psycopg2
from psycopg2 import sql, OperationalError
from contextlib import contextmanager

DATABASE_URL = "postgresql://username:password@localhost:5432/seu_banco"

def get_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except OperationalError as e:
        print(f"Erro ao conectar no banco: {e}")
        raise e

@contextmanager
def get_cursor():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
