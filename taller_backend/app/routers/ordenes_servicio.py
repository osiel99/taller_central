from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_db
from app import crud, schemas

router = APIRouter(
    prefix="/ordenes_servicio",
    tags=["Órdenes de Servicio"]
)


@router.post("/", response_model=schemas.OrdenServicio)
def crear_orden_servicio(
    os_in: schemas.OrdenServicioCreate,
    db: Session = Depends(get_db),
):
    return crud.create_orden_servicio(db, os_in)


@router.get("/", response_model=list[schemas.OrdenServicio])
def listar_ordenes_servicio(db: Session = Depends(get_db)):
    return crud.get_ordenes_servicio(db)
