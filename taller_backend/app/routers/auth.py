from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps import get_db
from app import schemas, crud
from app.auth_utils import autenticar_usuario, crear_token_acceso, get_current_active_user
from app.roles import require_role

router = APIRouter(prefix="/auth", tags=["Auth"])


# ============================================================
# LOGIN PROFESIONAL (JSON)
# ============================================================

@router.post("/login", response_model=schemas.Token)
def login(
    credentials: schemas.LoginRequest,
    db: Session = Depends(get_db),
):
    usuario = autenticar_usuario(db, credentials.username, credentials.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )

    access_token = crear_token_acceso(data={"sub": usuario.username})
    return {"access_token": access_token, "token_type": "bearer"}


# ============================================================
# USUARIO ACTUAL
# ============================================================

@router.get("/me", response_model=schemas.Usuario)
def leer_usuario_actual(current_user=Depends(get_current_active_user)):
    return current_user


# ============================================================
# ROLES
# ============================================================

@router.post("/roles/", response_model=schemas.Rol, dependencies=[Depends(require_role("admin"))])
def crear_rol(rol_in: schemas.RolCreate, db: Session = Depends(get_db)):
    return crud.create_rol(db, rol_in)


@router.get("/roles/", response_model=list[schemas.Rol], dependencies=[Depends(require_role("admin"))])
def listar_roles(db: Session = Depends(get_db)):
    return crud.get_roles(db)


# ============================================================
# USUARIOS
# ============================================================

@router.post("/usuarios/", response_model=schemas.Usuario, dependencies=[Depends(require_role("admin"))])
def crear_usuario(usuario_in: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.create_usuario(db, usuario_in)


@router.get("/usuarios/", response_model=list[schemas.Usuario], dependencies=[Depends(require_role("admin"))])
def listar_usuarios(db: Session = Depends(get_db)):
    return crud.get_usuarios(db)
