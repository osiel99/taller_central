from .database import SessionLocal

# -------------------------------------------------------------------
# DEPENDENCIA DE BASE DE DATOS PARA FASTAPI
# -------------------------------------------------------------------

def get_db():
    """
    Crea una sesión de base de datos por request.
    Garantiza que la conexión se cierre correctamente.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
