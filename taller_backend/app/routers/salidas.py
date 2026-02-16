from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_db
from app.roles import require_role
from app import crud, schemas

router = APIRouter(
    prefix="/salidas",
    tags=["Salidas"]
)


@router.post(
    "/",
    response_model=schemas.SalidaRefaccion,
    dependencies=[Depends(require_role("almacen", "admin"))],
)
def crear_salida(
    salida_in: schemas.SalidaRefaccionCreate,
    db: Session = Depends(get_db),
):
    return crud.create_salida_refaccion(db, salida_in)


@router.get(
    "/",
    response_model=list[schemas.SalidaRefaccion],
    dependencies=[Depends(require_role("almacen", "admin"))],
)
def listar_salidas(db: Session = Depends(get_db)):
    return crud.get_salidas(db)
