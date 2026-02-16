from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_db
from app import crud

router = APIRouter(
    prefix="/ui",
    tags=["UI"]
)


@router.get("/bootstrap")
def ui_bootstrap(db: Session = Depends(get_db)):
    return crud.get_bootstrap_data(db)


@router.get("/refacciones_inventario")
def ui_refacciones_inventario(db: Session = Depends(get_db)):
    return crud.get_refacciones_con_inventario(db)


@router.get("/os/{os_id}")
def ui_os_detallada(
    os_id: int,
    db: Session = Depends(get_db),
):
    return crud.get_os_detallada(db, os_id)


@router.get("/oc/{oc_id}")
def ui_oc_detallada(
    oc_id: int,
    db: Session = Depends(get_db),
):
    return crud.get_oc_detallada(db, oc_id)


@router.get("/buscar_refacciones")
def ui_buscar_refacciones(
    q: str,
    db: Session = Depends(get_db),
):
    return crud.buscar_refacciones(db, q)


@router.get("/dashboard")
def ui_dashboard(db: Session = Depends(get_db)):
    return crud.get_dashboard_ui(db)
