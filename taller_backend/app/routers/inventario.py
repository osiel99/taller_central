from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_db
from app.roles import require_role
from app import crud, schemas

router = APIRouter(
    prefix="/inventario",
    tags=["Inventario"]
)


@router.get(
    "/",
    response_model=list[schemas.Inventario],
    dependencies=[Depends(require_role("almacen", "admin"))],
)
def listar_inventario(db: Session = Depends(get_db)):
    return crud.get_inventario(db)
