from pydantic import BaseModel, ConfigDict
from datetime import datetime

# ============================================================
# CONFIGURACIÓN BASE
# ============================================================

class BaseSchema(BaseModel):
    """Base para todos los esquemas con configuración estándar."""
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


# ============================================================
# VEHICULOS
# ============================================================

class VehiculoBase(BaseSchema):
    numero_economico: str
    tipo: str
    placas: str
    marca: str
    modelo: str
    anio: int | None = None
    numero_serie: str | None = None
    area_asignada: str | None = None


class VehiculoCreate(VehiculoBase):
    pass


class Vehiculo(VehiculoBase):
    id: int


# ============================================================
# ORDENES DE SERVICIO
# ============================================================

class OrdenServicioBase(BaseSchema):
    vehiculo_id: int
    diagnostico: str | None = None
    estado: str | None = None
    tecnico_asignado: str | None = None


class OrdenServicioCreate(OrdenServicioBase):
    pass


class OrdenServicio(OrdenServicioBase):
    id: int
    fecha_creacion: datetime


# ============================================================
# REFACCIONES
# ============================================================

class RefaccionBase(BaseSchema):
    clave: str
    descripcion: str
    unidad_medida: str | None = "pieza"


class RefaccionCreate(RefaccionBase):
    pass


class Refaccion(RefaccionBase):
    id: int


# ============================================================
# SOLICITUDES DE REFACCIONES
# ============================================================

class SolicitudDetalleBase(BaseSchema):
    refaccion_id: int
    cantidad: int


class SolicitudDetalleCreate(SolicitudDetalleBase):
    pass


class SolicitudDetalle(SolicitudDetalleBase):
    id: int


class SolicitudRefaccionBase(BaseSchema):
    orden_servicio_id: int
    solicitante: str
    estado: str | None = None


class SolicitudRefaccionCreate(SolicitudRefaccionBase):
    detalles: list[SolicitudDetalleCreate]


class SolicitudRefaccion(SolicitudRefaccionBase):
    id: int
    fecha_solicitud: datetime
    detalles: list[SolicitudDetalle]


# ============================================================
# ORDENES DE COMPRA
# ============================================================

class OrdenCompraDetalleBase(BaseSchema):
    refaccion_id: int
    cantidad: int
    precio_unitario: float | None = None


class OrdenCompraDetalleCreate(OrdenCompraDetalleBase):
    pass


class OrdenCompraDetalle(OrdenCompraDetalleBase):
    id: int


class OrdenCompraBase(BaseSchema):
    solicitud_id: int | None = None
    proveedor: str
    estado: str | None = None
    factura: str | None = None


class OrdenCompraCreate(OrdenCompraBase):
    detalles: list[OrdenCompraDetalleCreate]


class OrdenCompra(OrdenCompraBase):
    id: int
    fecha_oc: datetime
    detalles: list[OrdenCompraDetalle]

# ========================================================
# IMPORTAR ORDENES DE COMPRA
# ========================================================

class OrdenCompraImportar(BaseSchema): 
    tipo: str # "json", "texto", "excel", "pdf" 
    contenido: str | None = None # Para JSON o texto pegado


# ============================================================
# RECEPCIONES
# ============================================================

class RecepcionDetalleBase(BaseSchema):
    refaccion_id: int
    cantidad_recibida: int
    cantidad_oc: int | None = None


class RecepcionDetalleCreate(RecepcionDetalleBase):
    pass


class RecepcionDetalle(RecepcionDetalleBase):
    id: int


class RecepcionBase(BaseSchema):
    oc_id: int
    recibido_por: str


class RecepcionCreate(RecepcionBase):
    detalles: list[RecepcionDetalleCreate]


class Recepcion(RecepcionBase):
    id: int
    fecha_recepcion: datetime
    detalles: list[RecepcionDetalle]


# ============================================================
# INVENTARIO
# ============================================================

class Inventario(BaseSchema):
    id: int
    refaccion_id: int
    existencia: int


# ============================================================
# KARDEX
# ============================================================

class MovimientoInventarioBase(BaseSchema):
    refaccion_id: int
    tipo: str
    cantidad: int
    referencia: str | None = None


class MovimientoInventarioCreate(MovimientoInventarioBase):
    pass


class MovimientoInventario(MovimientoInventarioBase):
    id: int
    fecha: datetime

class MovimientoInventarioKardex(BaseModel):
    id: int
    refaccion_id: int
    tipo: str
    cantidad: int
    saldo: int
    referencia: str | None = None
    fecha: datetime | None = None

    class Config:
        orm_mode = True


# ============================================================
# SALIDAS DE REFACCIONES
# ============================================================

class SalidaDetalleBase(BaseSchema):
    refaccion_id: int
    cantidad: int


class SalidaDetalleCreate(SalidaDetalleBase):
    pass


class SalidaDetalle(SalidaDetalleBase):
    id: int


class SalidaRefaccionBase(BaseSchema):
    orden_servicio_id: int
    entregado_por: str
    recibido_por: str


class SalidaRefaccionCreate(SalidaRefaccionBase):
    detalles: list[SalidaDetalleCreate]


class SalidaRefaccion(SalidaRefaccionBase):
    id: int
    fecha_salida: datetime
    detalles: list[SalidaDetalle]
# ============================================================
# ROLES
# ============================================================

class RolBase(BaseSchema):
    nombre: str
    descripcion: str | None = None


class RolCreate(RolBase):
    pass


class Rol(RolBase):
    id: int


# ============================================================
# USUARIOS
# ============================================================

class UsuarioBase(BaseSchema):
    username: str
    nombre: str
    rol_id: int


class UsuarioCreate(UsuarioBase):
    password: str


class Usuario(UsuarioBase):
    id: int
    activo: bool
    rol: Rol | None = None


# ============================================================
# AUTH (TOKEN)
# ============================================================

class Token(BaseSchema):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseSchema):
    username: str | None = None

# ============================================================
# LOGIN (JSON)
# ============================================================

class LoginRequest(BaseSchema):
    username: str
    password: str


# ============================================================
# PROVEEDORES
# ============================================================

class ProveedorBase(BaseSchema):   # ← antes era BaseModel
    nombre: str
    rfc: str | None = None
    telefono: str | None = None
    email: str | None = None
    direccion: str | None = None

class ProveedorCreate(ProveedorBase):
    pass

class ProveedorUpdate(ProveedorBase):
    activo: bool | None = None

class ProveedorOut(ProveedorBase):
    id: int
    activo: bool
