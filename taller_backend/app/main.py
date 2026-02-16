from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine, SessionLocal
from .auth_utils import hash_password
from . import models

# ============================================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ============================================================

def create_app():
    app = FastAPI(
        title="Taller Municipal API",
        description="Backend profesional para gestión de taller, inventario y compras",
        version="1.0.0",
    )

    # Routers
    from .routers import (
    vehiculos,
    auth,
    ordenes_servicio,
    solicitudes,
    refacciones,
    compras,
    recepciones,
    inventario,
    kardex,
    salidas,
    reportes,
    dashboard,
    ui,
    proveedores,
)

    app.include_router(vehiculos.router)
    app.include_router(auth.router)
    app.include_router(ordenes_servicio.router)
    app.include_router(solicitudes.router)
    app.include_router(refacciones.router)
    app.include_router(compras.router)
    app.include_router(recepciones.router)
    app.include_router(inventario.router)
    app.include_router(kardex.router)
    app.include_router(salidas.router)
    app.include_router(reportes.router)
    app.include_router(dashboard.router)
    app.include_router(ui.router)
    app.include_router(proveedores.router)

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = create_app()


# ============================================================
# CREAR ADMIN INICIAL
# ============================================================

def crear_admin_inicial():
    db = SessionLocal()
    try:
        rol_admin = (
            db.query(models.Rol)
            .filter(models.Rol.nombre == "admin")
            .first()
        )

        if not rol_admin:
            rol_admin = models.Rol(
                nombre="admin",
                descripcion="Administrador del sistema",
            )
            db.add(rol_admin)
            db.commit()
            db.refresh(rol_admin)

        admin = (
            db.query(models.Usuario)
            .filter(models.Usuario.username == "admin")
            .first()
        )

        if not admin:
            admin = models.Usuario(
                username="admin",
                nombre="Administrador",
                hashed_password=hash_password("admin123"),
                rol_id=rol_admin.id,
                activo=True,
            )
            db.add(admin)
            db.commit()

    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)

    # Crear admin inicial
    crear_admin_inicial()



# ============================================================
# ENDPOINT PRINCIPAL
# ============================================================

@app.get("/")
def read_root():
    return {"mensaje": "Backend del taller municipal funcionando"}
