import os
from urllib.parse import urlparse, unquote

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql

pymysql.install_as_MySQLdb()

DATABASE_URL = os.getenv("DATABASE_URL") or "mysql+pymysql://root:@localhost:3306/bima_resto_api"

def ensure_database_exists(sqlalchemy_url: str) -> None:
    parsed = urlparse(sqlalchemy_url)
    db_name = parsed.path.lstrip('/') if parsed.path else None
    if not db_name:
        return

    host = parsed.hostname or 'localhost'
    port = parsed.port or 3306
    user = unquote(parsed.username) if parsed.username else 'root'
    password = unquote(parsed.password) if parsed.password else ''

    try:
        # Connect to MySQL server without selecting a database
        conn = pymysql.connect(host=host, user=user, password=password, port=port)
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            conn.commit()
            print(f"Ensured database '{db_name}' exists.")
        finally:
            conn.close()
    except Exception as e:
        # Print a helpful warning but don't crash here; let create_engine surface real errors later if needed.
        print(f"Warning: could not ensure database '{db_name}' exists: {e}")

# Try to create the database if it doesn't exist so SQLAlchemy's create_all won't fail.
ensure_database_exists(DATABASE_URL)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()