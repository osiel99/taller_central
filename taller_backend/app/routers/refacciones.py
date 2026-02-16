from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_db
from app import crud, schemas

router = APIRouter(
    prefix="/refacciones",
    tags=["Refacciones"]
)


@router.post("/", response_model=schemas.Refaccion)
def crear_refaccion(
    ref_in: schemas.RefaccionCreate,
    db: Session = Depends(get_db),
):
    return crud.create_refaccion(db, ref_in)


@router.get("/", response_model=list[schemas.Refaccion])
def listar_refacciones(db: Session = Depends(get_db)):
    return crud.get_refacciones(db)
