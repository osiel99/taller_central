from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_db
from app.roles import require_role
from app import crud

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get(
    "/gasto_por_vehiculo",
    dependencies=[Depends(require_role("auditor", "admin"))],
)
def dashboard_gasto_por_vehiculo(db: Session = Depends(get_db)):
    return crud.get_gasto_por_vehiculo(db)


@router.get(
    "/alertas_compra_cara",
    dependencies=[Depends(require_role("auditor", "admin"))],
)
def dashboard_alertas_compra_cara(db: Session = Depends(get_db)):
    return crud.get_alertas_compra_cara(db)


@router.get(
    "/general",
    dependencies=[Depends(require_role("auditor", "admin"))],
)
def dashboard_general(db: Session = Depends(get_db)):
    return crud.get_dashboard_general(db)
