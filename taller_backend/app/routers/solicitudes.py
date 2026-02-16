from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_db
from app.roles import require_role
from app import crud, schemas

router = APIRouter(
    prefix="/solicitudes",
    tags=["Solicitudes"]
)


@router.post(
    "/",
    response_model=schemas.SolicitudRefaccion,
    dependencies=[Depends(require_role("mecanico", "admin"))],
)
def crear_solicitud(
    solicitud_in: schemas.SolicitudRefaccionCreate,
    db: Session = Depends(get_db),
):
    return crud.create_solicitud_refaccion(db, solicitud_in)


@router.get(
    "/",
    response_model=list[schemas.SolicitudRefaccion],
)
def listar_solicitudes(db: Session = Depends(get_db)):
    return crud.get_solicitudes(db)
