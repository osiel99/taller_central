from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends, Header
from sqlalchemy.orm import Session

from . import models
from .deps import get_db

# ============================================================
# CONFIGURACIÓN JWT Y PASSWORD
# ============================================================

# En producción: mover a variables de entorno
SECRET_KEY = "CAMBIA_ESTA_CLAVE_POR_ALGO_MUY_SEGURO"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ------------------------------------------------------------
# UTILIDADES DE PASSWORD
# ------------------------------------------------------------

def verificar_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# ------------------------------------------------------------
# UTILIDADES DE JWT
# ------------------------------------------------------------

def crear_token_acceso(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def obtener_usuario_por_username(db: Session, username: str) -> Optional[models.Usuario]:
    return db.query(models.Usuario).filter(models.Usuario.username == username).first()


def autenticar_usuario(db: Session, username: str, password: str) -> Optional[models.Usuario]:
    usuario = obtener_usuario_por_username(db, username)
    if not usuario:
        return None
    if not verificar_password(password, usuario.hashed_password):
        return None
    if not usuario.activo:
        return None
    return usuario


# ------------------------------------------------------------
# EXTRACCIÓN DEL TOKEN DESDE EL HEADER
# ------------------------------------------------------------

def get_token_from_header(
    authorization: str = Header(..., convert_underscores=False)
) -> str:
    """
    Extrae el token del header Authorization: Bearer <token>.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Formato de autorización inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return authorization.split(" ", 1)[1]


# ------------------------------------------------------------
# DEPENDENCIAS DE SEGURIDAD
# ------------------------------------------------------------

async def get_current_user(
    token: str = Depends(get_token_from_header),
    db: Session = Depends(get_db),
) -> models.Usuario:
    cred_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise cred_exception
    except JWTError:
        raise cred_exception

    usuario = obtener_usuario_por_username(db, username)
    if usuario is None:
        raise cred_exception

    return usuario


async def get_current_active_user(
    current_user: models.Usuario = Depends(get_current_user),
):
    if not current_user.activo:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return current_user
