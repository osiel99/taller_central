from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
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
    if not archivo.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="El archivo debe ser .xlsx")

    try:
        df = pd.read_excel(archivo.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error leyendo Excel: {e}")

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

    for col in columnas_requeridas:
        if col not in df.columns:
            raise HTTPException(status_code=400, detail=f"Falta la columna requerida: {col}")

    # Normaliza NaN a None
    df = df.where(pd.notnull(df), None)

    registros = df.to_dict(orient="records")
    creados = 0
    duplicados = 0
    errores = []

    def clean(v):
        # Convierte None/NaN/"nan" a string vacío, si no, devuelve string limpio
        if v is None:
            return ""
        try:
            if pd.isna(v):
                return ""
        except Exception:
            pass
        s = str(v).strip()
        return "" if s.lower() == "nan" else s

    def empty_to_none(s: str):
        # Convierte "" a None (útil si tienes unique index y quieres NULL en vez de "")
        return s if s else None


    for idx, item in enumerate(registros, start=2):  # fila 1 es header
        try:
            anio_raw = item.get("anio")

            # Convierte anio robusto (soporta 2020, 2020.0)
            try:
                anio = int(float(anio_raw))
            except Exception:
                raise ValueError(f"anio inválido: {anio_raw}")

            data = schemas.VehiculoCreate(
                numero_economico=clean(item.get("numero_economico")),
                tipo=clean(item.get("tipo")),
                placas=empty_to_none(clean(item.get("placas"))),
                marca=clean(item.get("marca")),
                modelo=clean(item.get("modelo")),
                anio=anio,
                numero_serie=clean(item.get("numero_serie")),
                area_asignada=clean(item.get("area_asignada")),
            )

            crud.create_vehiculo(db, data)
            creados += 1

        except IntegrityError as e:
            db.rollback()
            duplicados += 1
            errores.append({"fila_excel": idx, "tipo": "duplicado", "error": str(e.orig)})
            continue

        except Exception as e:
            db.rollback()
            errores.append({"fila_excel": idx, "tipo": "error", "error": str(e)})
            continue

    return {
        "mensaje": f"Importación completada. Creados={creados}, Duplicados={duplicados}, Errores={len(errores)}",
        "creados": creados,
        "duplicados": duplicados,
        "errores": errores[:30],
    }