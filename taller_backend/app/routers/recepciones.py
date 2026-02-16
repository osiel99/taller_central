from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_db
from app.roles import require_role
from app import crud, schemas

router = APIRouter(
    prefix="/recepciones",
    tags=["Recepciones"]
)


@router.post(
    "/",
    response_model=schemas.Recepcion,
    dependencies=[Depends(require_role("almacen", "admin"))],
)
def crear_recepcion(
    rec_in: schemas.RecepcionCreate,
    db: Session = Depends(get_db),
):
    return crud.create_recepcion(db, rec_in)


@router.get(
    "/",
    response_model=list[schemas.Recepcion],
    dependencies=[Depends(require_role("almacen", "admin"))],
)
def listar_recepciones(db: Session = Depends(get_db)):
    return crud.get_recepciones(db)
