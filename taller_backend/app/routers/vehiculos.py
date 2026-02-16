from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas
from app.roles import require_role
import pandas as pd

router = APIRouter(
    prefix="/vehiculos",
    tags=["Vehículos"],
    dependencies=[Depends(require_role("almacen", "admin"))],
)

@router.post("/", response_model=schemas.Vehiculo)
def crear_vehiculo(vehiculo_in: schemas.VehiculoCreate, db: Session = Depends(get_db)):
    return crud.create_vehiculo(db, vehiculo_in)

@router.get("/", response_model=list[schemas.Vehiculo])
def listar_vehiculos(db: Session = Depends(get_db)):
    return crud.get_vehiculos(db)

@router.post("/importar-excel")
def importar_excel_vehiculos(
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validar extensión
    if not archivo.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="El archivo debe ser .xlsx")

    # Leer Excel
    try:
        df = pd.read_excel(archivo.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error leyendo Excel: {e}")

    # Columnas requeridas
    columnas_requeridas = [
        "numero_economico",
        "tipo",
        "placas",
        "marca",
        "modelo",
        "anio",
        "numero_serie",
        "area_asignada",
    ]

    # Validar columnas
    for col in columnas_requeridas:
        if col not in df.columns:
            raise HTTPException(
                status_code=400,
                detail=f"Falta la columna requerida: {col}"
            )

    registros = df.to_dict(orient="records")
    creados = 0

    for item in registros:
        try:
            data = schemas.VehiculoCreate(
                numero_economico=str(item["numero_economico"]),
                tipo=str(item["tipo"]),
                placas=str(item["placas"]),
                marca=str(item["marca"]),
                modelo=str(item["modelo"]),
                anio=int(item["anio"]),
                numero_serie=str(item["numero_serie"]),
                area_asignada=str(item["area_asignada"]),
            )
            crud.create_vehiculo(db, data)
            creados += 1
        except Exception as e:
            print("Error creando vehículo:", e)
            continue

    return {"mensaje": f"Vehículos importados: {creados}"}
