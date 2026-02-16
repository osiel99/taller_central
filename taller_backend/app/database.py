import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -------------------------------------------------------------------
# LEER LA URL DE LA BASE DE DATOS DESDE .env
# -------------------------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está definida. Revisa tu archivo .env")

# -------------------------------------------------------------------
# MOTOR DE BASE DE DATOS (PostgreSQL o SQLite según DATABASE_URL)
# -------------------------------------------------------------------

# Para SQLite se requiere connect_args, para PostgreSQL NO.
connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    future=True
)

# -------------------------------------------------------------------
# SESIÓN DE BASE DE DATOS
# -------------------------------------------------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# -------------------------------------------------------------------
# BASE PARA MODELOS ORM
# -------------------------------------------------------------------

Base = declarative_base()

# -------------------------------------------------------------------
# DEPENDENCIA get_db PARA FASTAPI
# -------------------------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
