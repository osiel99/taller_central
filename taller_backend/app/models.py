from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean
from datetime import datetime
from .database import Base


# ============================================================
# VEHICULOS
# ============================================================

class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id = Column(Integer, primary_key=True, index=True)
    numero_economico = Column(String, unique=True, index=True, nullable=False)
    tipo = Column(String, nullable=False)
    placas = Column(String, unique=True, index=True, nullable=False)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    anio = Column(Integer)
    numero_serie = Column(String, unique=True, nullable=True)
    area_asignada = Column(String, nullable=True)

    # Relaciones útiles para reportes
    ordenes_servicio = relationship("OrdenServicio", back_populates="vehiculo")


# ============================================================
# ORDENES DE SERVICIO
# ============================================================

class OrdenServicio(Base):
    __tablename__ = "ordenes_servicio"

    id = Column(Integer, primary_key=True, index=True)
    vehiculo_id = Column(Integer, ForeignKey("vehiculos.id"), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    diagnostico = Column(Text, nullable=True)
    estado = Column(String, default="pendiente")
    tecnico_asignado = Column(String, nullable=True)

    vehiculo = relationship("Vehiculo", back_populates="ordenes_servicio")
    solicitudes = relationship("SolicitudRefaccion", back_populates="orden_servicio")
    salidas = relationship("SalidaRefaccion", back_populates="orden_servicio")


# ============================================================
# REFACCIONES
# ============================================================

class Refaccion(Base):
    __tablename__ = "refacciones"

    id = Column(Integer, primary_key=True, index=True)
    clave = Column(String, unique=True, index=True, nullable=False)
    descripcion = Column(String, nullable=False)
    unidad_medida = Column(String, default="pieza")

    # Relaciones útiles para reportes
    inventario = relationship("Inventario", uselist=False, back_populates="refaccion")


# ============================================================
# SOLICITUDES DE REFACCIONES
# ============================================================

class SolicitudRefaccion(Base):
    __tablename__ = "solicitudes_refacciones"

    id = Column(Integer, primary_key=True, index=True)
    orden_servicio_id = Column(Integer, ForeignKey("ordenes_servicio.id"), nullable=False)
    fecha_solicitud = Column(DateTime, default=datetime.utcnow)
    solicitante = Column(String, nullable=False)
    estado = Column(String, default="pendiente")

    orden_servicio = relationship("OrdenServicio", back_populates="solicitudes")
    detalles = relationship("SolicitudDetalle", back_populates="solicitud")


class SolicitudDetalle(Base):
    __tablename__ = "solicitudes_detalle"

    id = Column(Integer, primary_key=True, index=True)
    solicitud_id = Column(Integer, ForeignKey("solicitudes_refacciones.id"), nullable=False)
    refaccion_id = Column(Integer, ForeignKey("refacciones.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)

    solicitud = relationship("SolicitudRefaccion", back_populates="detalles")
    refaccion = relationship("Refaccion")


# ============================================================
# ORDENES DE COMPRA
# ============================================================

class OrdenCompra(Base):
    __tablename__ = "ordenes_compra"

    id = Column(Integer, primary_key=True, index=True)
    solicitud_id = Column(Integer, ForeignKey("solicitudes_refacciones.id"), nullable=True)
    proveedor = Column(String, nullable=False)
    fecha_oc = Column(DateTime, default=datetime.utcnow)
    estado = Column(String, default="pendiente")
    factura = Column(String, nullable=True)

    detalles = relationship("OrdenCompraDetalle", back_populates="oc")
    recepciones = relationship("Recepcion", back_populates="oc")


class OrdenCompraDetalle(Base):
    __tablename__ = "ordenes_compra_detalle"

    id = Column(Integer, primary_key=True, index=True)
    oc_id = Column(Integer, ForeignKey("ordenes_compra.id"), nullable=False)
    refaccion_id = Column(Integer, ForeignKey("refacciones.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=True)

    oc = relationship("OrdenCompra", back_populates="detalles")
    refaccion = relationship("Refaccion")


# ============================================================
# RECEPCIONES
# ============================================================

class Recepcion(Base):
    __tablename__ = "recepciones"

    id = Column(Integer, primary_key=True, index=True)
    oc_id = Column(Integer, ForeignKey("ordenes_compra.id"), nullable=False)
    fecha_recepcion = Column(DateTime, default=datetime.utcnow)
    recibido_por = Column(String, nullable=False)

    oc = relationship("OrdenCompra", back_populates="recepciones")
    detalles = relationship("RecepcionDetalle", back_populates="recepcion")


class RecepcionDetalle(Base):
    __tablename__ = "recepciones_detalle"

    id = Column(Integer, primary_key=True, index=True)
    recepcion_id = Column(Integer, ForeignKey("recepciones.id"), nullable=False)
    refaccion_id = Column(Integer, ForeignKey("refacciones.id"), nullable=False)
    cantidad_recibida = Column(Integer, nullable=False)
    cantidad_oc = Column(Integer, nullable=True)

    recepcion = relationship("Recepcion", back_populates="detalles")
    refaccion = relationship("Refaccion")


# ============================================================
# SALIDAS DE REFACCIONES
# ============================================================

class SalidaRefaccion(Base):
    __tablename__ = "salidas_refacciones"

    id = Column(Integer, primary_key=True, index=True)
    orden_servicio_id = Column(Integer, ForeignKey("ordenes_servicio.id"), nullable=False)
    fecha_salida = Column(DateTime, default=datetime.utcnow)
    entregado_por = Column(String, nullable=False)
    recibido_por = Column(String, nullable=False)

    orden_servicio = relationship("OrdenServicio", back_populates="salidas")
    detalles = relationship("SalidaDetalle", back_populates="salida")


class SalidaDetalle(Base):
    __tablename__ = "salidas_detalle"

    id = Column(Integer, primary_key=True, index=True)
    salida_id = Column(Integer, ForeignKey("salidas_refacciones.id"), nullable=False)
    refaccion_id = Column(Integer, ForeignKey("refacciones.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)

    salida = relationship("SalidaRefaccion", back_populates="detalles")
    refaccion = relationship("Refaccion")


# ============================================================
# INVENTARIO
# ============================================================

class Inventario(Base):
    __tablename__ = "inventario"

    id = Column(Integer, primary_key=True, index=True)
    refaccion_id = Column(Integer, ForeignKey("refacciones.id"), nullable=False)
    existencia = Column(Integer, default=0)

    refaccion = relationship("Refaccion", back_populates="inventario")


# ============================================================
# KARDEX
# ============================================================

class MovimientoInventario(Base):
    __tablename__ = "movimientos_inventario"

    id = Column(Integer, primary_key=True, index=True)
    refaccion_id = Column(Integer, ForeignKey("refacciones.id"), nullable=False)
    tipo = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)
    referencia = Column(String, nullable=True)

    refaccion = relationship("Refaccion")


# ============================================================
# USUARIOS Y ROLES
# ============================================================

class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True, nullable=False)
    descripcion = Column(String, nullable=True)

    usuarios = relationship("Usuario", back_populates="rol")


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    activo = Column(Boolean, default=True)
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    rol = relationship("Rol", back_populates="usuarios")


# ============================================================
# PROVEEDORES
# ============================================================

class Proveedor(Base):
    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    rfc = Column(String, nullable=True)
    telefono = Column(String, nullable=True)
    email = Column(String, nullable=True)
    direccion = Column(String, nullable=True)
    activo = Column(Boolean, default=True)
