from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import crud, schemas

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])

@router.get("/", response_model=list[schemas.ProveedorOut])
def listar_proveedores(db: Session = Depends(get_db)):
    return crud.get_proveedores(db)

@router.get("/{proveedor_id}", response_model=schemas.ProveedorOut)
def obtener_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    proveedor = crud.get_proveedor(db, proveedor_id)
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return proveedor

@router.post("/", response_model=schemas.ProveedorOut)
def crear_proveedor(data: schemas.ProveedorCreate, db: Session = Depends(get_db)):
    return crud.create_proveedor(db, data)

@router.put("/{proveedor_id}", response_model=schemas.ProveedorOut)
def actualizar_proveedor(
    proveedor_id: int,
    data: schemas.ProveedorUpdate,
    db: Session = Depends(get_db),
):
    proveedor = crud.update_proveedor(db, proveedor_id, data)
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return proveedor

@router.delete("/{proveedor_id}")
def eliminar_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    proveedor = crud.delete_proveedor(db, proveedor_id)
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return {"detail": "Proveedor eliminado"}
