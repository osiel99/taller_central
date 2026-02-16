import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import create_app
from app.database import Base
from app.deps import get_db
from app import models
from app.auth_utils import hash_password


# ============================================================
# BASE DE DATOS TEMPORAL EN ARCHIVO (ESTABLE)
# ============================================================

TEST_DB_URL = "sqlite:///./test_database.db"

engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ============================================================
# FIXTURE: SESIÓN DE BASE DE DATOS
# ============================================================

@pytest.fixture(scope="function")
def db():

    # Borrar archivo previo
    if os.path.exists("test_database.db"):
        os.remove("test_database.db")

    # Crear tablas
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


# ============================================================
# FIXTURE: CLIENTE AUTENTICADO
# ============================================================

@pytest.fixture(scope="function")
def client(db):
    app = create_app()

    # Desactivar startup para evitar engine real
    app.router.on_startup = []

    # Override de get_db
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    # Crear rol admin
    rol_admin = models.Rol(nombre="admin", descripcion="Administrador del sistema")
    db.add(rol_admin)
    db.commit()
    db.refresh(rol_admin)

    # Crear usuario admin
    admin_user = models.Usuario(
        username="admin_test",
        nombre="Administrador de Pruebas",
        hashed_password=hash_password("admin123"),
        rol_id=rol_admin.id,
        activo=True,
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)

    # Crear TestClient
    test_client = TestClient(app)

    # Login automático
    login_response = test_client.post(
        "/auth/login",
        data={"username": "admin_test", "password": "admin123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    test_client.headers.update({"Authorization": f"Bearer {token}"})

    yield test_client

    app.dependency_overrides.clear()
