from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_db
from app.roles import require_role
from app import crud, schemas

router = APIRouter(
    prefix="/reportes",
    tags=["Reportes"]
)


@router.get(
    "/inventario",
    dependencies=[Depends(require_role("auditor", "admin"))],
)
def reporte_inventario(db: Session = Depends(get_db)):
    return crud.get_inventario_detallado(db)


@router.get(
    "/kardex/{refaccion_id}",
    dependencies=[Depends(require_role("auditor", "admin"))],
)
def reporte_kardex(
    refaccion_id: int,
    db: Session = Depends(get_db),
):
    return crud.get_kardex_detallado(db, refaccion_id)


@router.get(
    "/consumo/{os_id}",
    dependencies=[Depends(require_role("auditor", "admin"))],
)
def reporte_consumo_os(
    os_id: int,
    db: Session = Depends(get_db),
):
    return crud.get_consumo_por_os(db, os_id)


@router.get(
    "/diferencias_oc/{oc_id}",
    dependencies=[Depends(require_role("auditor", "admin"))],
)
def reporte_diferencias_oc(
    oc_id: int,
    db: Session = Depends(get_db),
):
    return crud.get_diferencias_oc(db, oc_id)


@router.get(
    "/compras/{proveedor}",
    dependencies=[Depends(require_role("auditor", "admin"))],
)
def reporte_compras_proveedor(
    proveedor: str,
    db: Session = Depends(get_db),
):
    return crud.get_compras_por_proveedor(db, proveedor)


@router.get(
    "/refacciones_mas_usadas",
    dependencies=[Depends(require_role("auditor", "admin"))],
)
def reporte_refacciones_mas_usadas(db: Session = Depends(get_db)):
    return crud.get_refacciones_mas_usadas(db)


@router.get(
    "/bajo_inventario",
    dependencies=[Depends(require_role("auditor", "admin"))],
)
def reporte_bajo_inventario(
    minimo: int = 5,
    db: Session = Depends(get_db),
):
    return crud.get_bajo_inventario(db, minimo)
