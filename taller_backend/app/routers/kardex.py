from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_db
from app.roles import require_role
from app import crud, schemas

router = APIRouter(
    prefix="/kardex",
    tags=["Kardex"]
)


@router.get(
    "/{refaccion_id}",
    response_model=list[schemas.MovimientoInventarioKardex],
    dependencies=[Depends(require_role("almacen", "admin"))],
)
def kardex_refaccion(
    refaccion_id: int,
    db: Session = Depends(get_db),
):
    return crud.get_kardex(db, refaccion_id)
