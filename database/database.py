# database/database.py
import os
import psycopg2
from dotenv import load_dotenv
import logging

# Logger
logger = logging.getLogger("database")

# Carrega variáveis do .env na raiz do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"BASE_DIR as {BASE_DIR}")
ENV_PATH = os.path.join(BASE_DIR, ".env")
print(f"ENV_PATH as {ENV_PATH}")
load_dotenv(ENV_PATH)


def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "project_01"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    logger.info(f"[DB] Opening PostgreSQL connection (connection={conn})")
    conn.set_session(autocommit=True)
    return conn
