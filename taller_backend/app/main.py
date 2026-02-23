import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine, SessionLocal
from .auth_utils import hash_password
from . import models


# ============================================================
# UTILIDADES CORS (CONFIGURABLE)
# ============================================================

def _parse_origins(value: str) -> list[str]:
    # Espera: "http://localhost:8080,https://tudominio.com"
    return [x.strip() for x in (value or "").split(",") if x.strip()]


# ============================================================
# CREAR ADMIN INICIAL
# ============================================================

def crear_admin_inicial():
    db = SessionLocal()
    try:
        rol_admin = db.query(models.Rol).filter(models.Rol.nombre == "admin").first()

        if not rol_admin:
            rol_admin = models.Rol(
                nombre="admin",
                descripcion="Administrador del sistema",
            )
            db.add(rol_admin)
            db.commit()
            db.refresh(rol_admin)

        admin = db.query(models.Usuario).filter(models.Usuario.username == "admin").first()

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


# ============================================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ============================================================

def create_app() -> FastAPI:
    app = FastAPI(
        title="Taller Municipal API",
        description="Backend profesional para gestión de taller, inventario y compras",
        version="1.0.0",
    )

    # -------------------------
    # CORS PROFESIONAL / CONFIGURABLE
    # -------------------------
    ENV = os.getenv("ENV", "dev").strip().lower()  # dev | prod
    CORS_MODE = os.getenv("CORS_MODE", "bearer").strip().lower()  # bearer | cookies

    origins = _parse_origins(os.getenv("CORS_ORIGINS", ""))

    if ENV == "dev":
        if not origins:
            origins = [
                "http://localhost:8080",
                "http://127.0.0.1:8080",
                "http://localhost:5173",
                "http://127.0.0.1:5173",
            ]
    else:
        # En prod, si no configuras CORS_ORIGINS, queda cerrado (más seguro)
        if not origins:
            origins = []

    allow_credentials = (CORS_MODE == "cookies")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=allow_credentials,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "Accept", "Origin", "X-Requested-With"],
        expose_headers=["Content-Disposition"],
    )

    # -------------------------
    # Routers (NO CAMBIAMOS NADA)
    # -------------------------
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

    # -------------------------
    # Endpoints base
    # -------------------------
    @app.get("/")
    def read_root():
        return {"mensaje": "Backend del taller municipal funcionando"}

    @app.get("/health")
    def health():
        return {
            "status": "ok",
            "env": ENV,
            "cors_mode": CORS_MODE,
            "origins": origins,
        }

    return app


app = create_app()


# ============================================================
# STARTUP: crear tablas + admin inicial
# ============================================================

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    crear_admin_inicial()
    