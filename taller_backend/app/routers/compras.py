from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import json

from app.deps import get_db
from app.roles import require_role
from app import crud, schemas

router = APIRouter(
    prefix="/ordenes_compra",
    tags=["Órdenes de Compra"]
)


# ============================================================
# CRUD BÁSICO
# ============================================================

@router.post(
    "/",
    response_model=schemas.OrdenCompra,
    dependencies=[Depends(require_role("compras", "admin"))],
)
def crear_orden_compra(
    oc_in: schemas.OrdenCompraCreate,
    db: Session = Depends(get_db),
):
    return crud.create_orden_compra(db, oc_in)


@router.get(
    "/",
    response_model=list[schemas.OrdenCompra],
    dependencies=[Depends(require_role("compras", "admin"))],
)
def listar_ordenes_compra(db: Session = Depends(get_db)):
    return crud.get_ordenes_compra(db)


# ============================================================
# IMPORTACIONES
# ============================================================

@router.post(
    "/importar",
    dependencies=[Depends(require_role("compras", "admin"))],
)
def importar_oc(
    payload: schemas.OrdenCompraImportar,
    db: Session = Depends(get_db),
):
    if payload.tipo == "json":
        data = json.loads(payload.contenido)
        return crud.importar_orden_compra_desde_json(db, data)

    elif payload.tipo == "texto":
        data = crud.parsear_oc_desde_texto(payload.contenido)
        return crud.importar_orden_compra_desde_json(db, data)

    else:
        raise HTTPException(status_code=400, detail="Tipo no soportado")


@router.post(
    "/importar_excel",
    dependencies=[Depends(require_role("compras", "admin"))],
)
async def importar_oc_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    contenido = await file.read()
    data = crud.parsear_oc_desde_excel(contenido)
    return crud.importar_orden_compra_desde_json(db, data)


@router.post(
    "/importar_pdf",
    dependencies=[Depends(require_role("compras", "admin"))],
)
async def importar_oc_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    contenido = await file.read()
    texto = crud.extraer_texto_de_pdf(contenido)
    data = crud.parsear_oc_desde_texto(texto)
    return crud.importar_orden_compra_desde_json(db, data)
