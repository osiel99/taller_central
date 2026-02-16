# ============================
# IMPORTS ESTÁNDAR
# ============================
import re
import io
from datetime import datetime

# ============================
# IMPORTS DE TERCEROS
# ============================
import pdfplumber
import openpyxl
from fastapi import HTTPException
from sqlalchemy.orm import Session

# ============================
# IMPORTS INTERNOS
# ============================
from . import models, schemas
from .auth_utils import hash_password


# ============================================================
# VEHICULOS
# ============================================================

def create_vehiculo(db: Session, vehiculo_in: schemas.VehiculoCreate):
    db_veh = models.Vehiculo(**vehiculo_in.model_dump())
    db.add(db_veh)
    db.commit()
    db.refresh(db_veh)
    return db_veh


def get_vehiculos(db: Session):
    return db.query(models.Vehiculo).all()


# ============================================================
# ORDENES DE SERVICIO
# ============================================================

def create_orden_servicio(db: Session, os_in: schemas.OrdenServicioCreate):
    db_os = models.OrdenServicio(**os_in.model_dump())
    db.add(db_os)
    db.commit()
    db.refresh(db_os)
    return db_os


def get_ordenes_servicio(db: Session):
    return db.query(models.OrdenServicio).all()


# ============================================================
# SOLICITUDES DE REFACCIONES
# ============================================================

def create_solicitud_refaccion(db: Session, solicitud_in: schemas.SolicitudRefaccionCreate):
    db_solicitud = models.SolicitudRefaccion(
        orden_servicio_id=solicitud_in.orden_servicio_id,
        solicitante=solicitud_in.solicitante,
        estado=solicitud_in.estado or "pendiente"
    )
    db.add(db_solicitud)
    db.commit()
    db.refresh(db_solicitud)

    for det in solicitud_in.detalles:
        db_det = models.SolicitudDetalle(
            solicitud_id=db_solicitud.id,
            refaccion_id=det.refaccion_id,
            cantidad=det.cantidad
        )
        db.add(db_det)

    db.commit()
    db.refresh(db_solicitud)
    return db_solicitud


def get_solicitudes(db: Session):
    return db.query(models.SolicitudRefaccion).all()


# ============================================================
# REFACCIONES
# ============================================================

def create_refaccion(db: Session, refaccion_in: schemas.RefaccionCreate):
    db_ref = models.Refaccion(**refaccion_in.model_dump())
    db.add(db_ref)
    db.commit()
    db.refresh(db_ref)
    return db_ref


def get_refacciones(db: Session):
    return db.query(models.Refaccion).all()


# ============================================================
# ORDENES DE COMPRA
# ============================================================

def create_orden_compra(db: Session, oc_in: schemas.OrdenCompraCreate):
    db_oc = models.OrdenCompra(
        solicitud_id=oc_in.solicitud_id,
        proveedor=oc_in.proveedor,
        estado=oc_in.estado or "pendiente",
        factura=oc_in.factura
    )
    db.add(db_oc)
    db.commit()
    db.refresh(db_oc)

    for det in oc_in.detalles:
        db_det = models.OrdenCompraDetalle(
            oc_id=db_oc.id,
            refaccion_id=det.refaccion_id,
            cantidad=det.cantidad,
            precio_unitario=det.precio_unitario
        )
        db.add(db_det)

    db.commit()
    db.refresh(db_oc)
    return db_oc


def get_ordenes_compra(db: Session):
    return db.query(models.OrdenCompra).all()


# ============================================================
# INVENTARIO
# ============================================================

def agregar_existencia(db: Session, refaccion_id: int, cantidad: int):
    inv = db.query(models.Inventario).filter(
        models.Inventario.refaccion_id == refaccion_id
    ).first()

    if not inv:
        inv = models.Inventario(refaccion_id=refaccion_id, existencia=0)
        db.add(inv)

    inv.existencia += cantidad
    db.commit()
    db.refresh(inv)
    return inv


def descontar_existencia(db: Session, refaccion_id: int, cantidad: int):
    inv = db.query(models.Inventario).filter(
        models.Inventario.refaccion_id == refaccion_id
    ).first()

    if not inv or inv.existencia < cantidad:
        raise HTTPException(status_code=400, detail="No hay suficiente inventario")

    inv.existencia -= cantidad
    db.commit()
    db.refresh(inv)
    return inv


# ============================================================
# KARDEX
# ============================================================

def registrar_movimiento(db: Session, mov: schemas.MovimientoInventarioCreate):
    db_mov = models.MovimientoInventario(**mov.model_dump())
    db.add(db_mov)
    db.commit()
    db.refresh(db_mov)
    return db_mov


def get_kardex(db: Session, refaccion_id: int):
    movimientos = db.query(models.MovimientoInventario).filter(
        models.MovimientoInventario.refaccion_id == refaccion_id
    ).order_by(models.MovimientoInventario.fecha.asc()).all()

    saldo = 0
    resultado = []

    for mov in movimientos:
        if mov.tipo == "entrada":
            saldo += mov.cantidad
        elif mov.tipo == "salida":
            saldo -= mov.cantidad

        resultado.append({
            "id": mov.id,
            "refaccion_id": mov.refaccion_id,
            "tipo": mov.tipo,
            "cantidad": mov.cantidad,
            "saldo": saldo,
            "referencia": mov.referencia,
            "fecha": mov.fecha.isoformat() if mov.fecha else None
        })

    return resultado


# ============================================================
# RECEPCIONES
# ============================================================

def create_recepcion(db: Session, recepcion_in: schemas.RecepcionCreate):
    db_rec = models.Recepcion(
        oc_id=recepcion_in.oc_id,
        recibido_por=recepcion_in.recibido_por
    )
    db.add(db_rec)
    db.commit()
    db.refresh(db_rec)

    for det in recepcion_in.detalles:
        db_det = models.RecepcionDetalle(
            recepcion_id=db_rec.id,
            refaccion_id=det.refaccion_id,
            cantidad_recibida=det.cantidad_recibida,
            cantidad_oc=det.cantidad_oc
        )
        db.add(db_det)

        agregar_existencia(db, det.refaccion_id, det.cantidad_recibida)

        registrar_movimiento(
            db,
            schemas.MovimientoInventarioCreate(
                refaccion_id=det.refaccion_id,
                tipo="entrada",
                cantidad=det.cantidad_recibida,
                referencia=f"Recepción OC {recepcion_in.oc_id}"
            )
        )

    db.commit()
    db.refresh(db_rec)
    return db_rec


def get_recepciones(db: Session):
    return db.query(models.Recepcion).all()


# ============================================================
# SALIDAS DE REFACCIONES
# ============================================================

def create_salida_refaccion(db: Session, salida_in: schemas.SalidaRefaccionCreate):
    db_salida = models.SalidaRefaccion(
        orden_servicio_id=salida_in.orden_servicio_id,
        entregado_por=salida_in.entregado_por,
        recibido_por=salida_in.recibido_por
    )
    db.add(db_salida)
    db.commit()
    db.refresh(db_salida)

    for det in salida_in.detalles:
        descontar_existencia(db, det.refaccion_id, det.cantidad)

        db_det = models.SalidaDetalle(
            salida_id=db_salida.id,
            refaccion_id=det.refaccion_id,
            cantidad=det.cantidad
        )
        db.add(db_det)

        registrar_movimiento(
            db,
            schemas.MovimientoInventarioCreate(
                refaccion_id=det.refaccion_id,
                tipo="salida",
                cantidad=det.cantidad,
                referencia=f"Salida OS {salida_in.orden_servicio_id}"
            )
        )

    db.commit()
    db.refresh(db_salida)
    return db_salida


def get_salidas(db: Session):
    return db.query(models.SalidaRefaccion).all()


# ============================================================
# REPORTES
# ============================================================

def get_inventario(db: Session):
    return db.query(models.Inventario).all()


def get_inventario_detallado(db: Session):
    inventario = db.query(models.Inventario).all()
    return [
        {
            "refaccion_id": item.refaccion_id,
            "clave": item.refaccion.clave,
            "descripcion": item.refaccion.descripcion,
            "unidad_medida": item.refaccion.unidad_medida,
            "existencia": item.existencia
        }
        for item in inventario
    ]


def get_kardex_detallado(db: Session, refaccion_id: int):
    movimientos = db.query(models.MovimientoInventario).filter(
        models.MovimientoInventario.refaccion_id == refaccion_id
    ).order_by(models.MovimientoInventario.fecha.asc()).all()

    saldo = 0
    resultado = []

    for mov in movimientos:
        saldo += mov.cantidad if mov.tipo == "entrada" else -mov.cantidad
        resultado.append({
            "fecha": mov.fecha,
            "tipo": mov.tipo,
            "cantidad": mov.cantidad,
            "saldo": saldo,
            "referencia": mov.referencia
        })

    return resultado


def get_consumo_por_os(db: Session, os_id: int):
    salidas = db.query(models.SalidaRefaccion).filter(
        models.SalidaRefaccion.orden_servicio_id == os_id
    ).all()

    resultado = []

    for salida in salidas:
        for det in salida.detalles:
            resultado.append({
                "refaccion_id": det.refaccion_id,
                "clave": det.refaccion.clave,
                "descripcion": det.refaccion.descripcion,
                "cantidad": det.cantidad,
                "fecha_salida": salida.fecha_salida,
                "entregado_por": salida.entregado_por,
                "recibido_por": salida.recibido_por
            })

    return resultado


def get_diferencias_oc(db: Session, oc_id: int):
    oc = db.query(models.OrdenCompra).filter(models.OrdenCompra.id == oc_id).first()
    recepciones = db.query(models.Recepcion).filter(models.Recepcion.oc_id == oc_id).all()

    resultado = []

    for det in oc.detalles:
        recibido_total = sum(
            d.cantidad_recibida
            for rec in recepciones
            for d in rec.detalles
            if d.refaccion_id == det.refaccion_id
        )

        resultado.append({
            "refaccion_id": det.refaccion_id,
            "clave": det.refaccion.clave,
            "descripcion": det.refaccion.descripcion,
            "cantidad_oc": det.cantidad,
            "recibido": recibido_total,
            "diferencia": det.cantidad - recibido_total
        })

    return resultado


def get_compras_por_proveedor(db: Session, proveedor: str):
    ocs = db.query(models.OrdenCompra).filter(
        models.OrdenCompra.proveedor == proveedor
    ).all()

    return [
        {
            "oc_id": oc.id,
            "fecha": oc.fecha_oc,
            "estado": oc.estado,
            "total": sum(d.cantidad * (d.precio_unitario or 0) for d in oc.detalles)
        }
        for oc in ocs
    ]


def get_refacciones_mas_usadas(db: Session):
    salidas = db.query(models.SalidaDetalle).all()

    conteo = {}
    for det in salidas:
        conteo[det.refaccion_id] = conteo.get(det.refaccion_id, 0) + det.cantidad

    resultado = []
    for ref_id, total in conteo.items():
        ref = db.query(models.Refaccion).filter(models.Refaccion.id == ref_id).first()
        resultado.append({
            "refaccion_id": ref_id,
            "clave": ref.clave,
            "descripcion": ref.descripcion,
            "total_usado": total
        })

    return sorted(resultado, key=lambda x: x["total_usado"], reverse=True)


def get_bajo_inventario(db: Session, minimo: int = 5):
    inventario = db.query(models.Inventario).all()

    return [
        {
            "refaccion_id": item.refaccion_id,
            "clave": item.refaccion.clave,
            "descripcion": item.refaccion.descripcion,
            "existencia": item.existencia
        }
        for item in inventario
        if item.existencia <= minimo
    ]


def get_gasto_por_vehiculo(db: Session):
    salidas = db.query(models.SalidaDetalle).all()
    resultado = {}

    for det in salidas:
        os = det.salida.orden_servicio
        vehiculo_id = os.vehiculo_id

        precio = (
            db.query(models.OrdenCompraDetalle.precio_unitario)
            .filter(models.OrdenCompraDetalle.refaccion_id == det.refaccion_id)
            .order_by(models.OrdenCompraDetalle.id.desc())
            .first()
        )

        precio_unitario = precio[0] if precio else 0
        costo = precio_unitario * det.cantidad

        resultado[vehiculo_id] = resultado.get(vehiculo_id, 0) + costo

    salida_final = []
    for vehiculo_id, total in resultado.items():
        veh = db.query(models.Vehiculo).filter(models.Vehiculo.id == vehiculo_id).first()
        salida_final.append({
            "vehiculo_id": vehiculo_id,
            "placas": veh.placas,
            "marca": veh.marca,
            "modelo": veh.modelo,
            "total_gastado": total
        })

    return salida_final


def get_alertas_compra_cara(db: Session):
    detalles = db.query(models.OrdenCompraDetalle).all()

    historico = {}
    alertas = []

    for det in detalles:
        ref_id = det.refaccion_id
        precio = det.precio_unitario or 0
        historico[ref_id] = min(historico.get(ref_id, precio), precio)

    for det in detalles:
        ref_id = det.refaccion_id
        precio_actual = det.precio_unitario or 0
        precio_min = historico[ref_id]

        if precio_actual > precio_min:
            ref = db.query(models.Refaccion).filter(models.Refaccion.id == ref_id).first()
            diferencia = precio_actual - precio_min
            porcentaje = (diferencia / precio_min) * 100 if precio_min > 0 else 0

            alertas.append({
                "refaccion_id": ref_id,
                "clave": ref.clave,
                "descripcion": ref.descripcion,
                "precio_historico_min": precio_min,
                "precio_actual": precio_actual,
                "diferencia": diferencia,
                "porcentaje": round(porcentaje, 2),
                "mensaje": "ALERTA: compra más cara que el histórico"
            })

    return alertas


def get_dashboard_general(db: Session):
    return {
        "ordenes_abiertas": db.query(models.OrdenServicio).filter(
            models.OrdenServicio.estado != "finalizado"
        ).count(),
        "inventario_total": sum(i.existencia for i in db.query(models.Inventario).all()),
        "refacciones_bajo_inventario": len(
            [i for i in db.query(models.Inventario).all() if i.existencia <= 5]
        ),
        "top_refacciones_usadas": get_refacciones_mas_usadas(db)[:5],
        "alertas_compra_cara": get_alertas_compra_cara(db),
        "gasto_por_vehiculo": get_gasto_por_vehiculo(db)
    }


# ============================================================
# ENDPOINTS PARA UI
# ============================================================

def get_bootstrap_data(db: Session):
    proveedores = db.query(models.OrdenCompra.proveedor).distinct().all()

    return {
        "vehiculos": db.query(models.Vehiculo).all(),
        "refacciones": db.query(models.Refaccion).all(),
        "proveedores": [p[0] for p in proveedores],
        "estados_os": ["pendiente", "en_proceso", "esperando_refacciones", "finalizado"],
        "estados_solicitud": ["pendiente", "aprobada", "rechazada"],
        "estados_oc": ["pendiente", "recibida", "cerrada"]
    }


def get_refacciones_con_inventario(db: Session):
    inventario = db.query(models.Inventario).all()

    return [
        {
            "id": item.refaccion.id,
            "clave": item.refaccion.clave,
            "descripcion": item.refaccion.descripcion,
            "unidad_medida": item.refaccion.unidad_medida,
            "existencia": item.existencia
        }
        for item in inventario
    ]


def get_os_detallada(db: Session, os_id: int):
    os = db.query(models.OrdenServicio).filter(models.OrdenServicio.id == os_id).first()

    return {
        "orden_servicio": os,
        "vehiculo": os.vehiculo,
        "solicitudes": os.solicitudes,
        "salidas": os.salidas
    }


def get_oc_detallada(db: Session, oc_id: int):
    oc = db.query(models.OrdenCompra).filter(models.OrdenCompra.id == oc_id).first()

    return {
        "orden_compra": oc,
        "recepciones": oc.recepciones,
        "diferencias": get_diferencias_oc(db, oc_id)
    }


def buscar_refacciones(db: Session, q: str):
    return db.query(models.Refaccion).filter(
        models.Refaccion.descripcion.ilike(f"%{q}%")
    ).all()


def get_dashboard_ui(db: Session):
    return {
        "inventario_total": sum(i.existencia for i in db.query(models.Inventario).all()),
        "refacciones_bajo_inventario": get_bajo_inventario(db),
        "alertas_compra_cara": get_alertas_compra_cara(db),
        "gasto_por_vehiculo": get_gasto_por_vehiculo(db),
        "top_refacciones_usadas": get_refacciones_mas_usadas(db)[:5]
    }

# ============================================================
# USUARIOS Y ROLES
# ============================================================

def create_rol(db: Session, rol_in: schemas.RolCreate):
    db_rol = models.Rol(**rol_in.model_dump())
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return db_rol


def get_roles(db: Session):
    return db.query(models.Rol).all()


def create_usuario(db: Session, usuario_in: schemas.UsuarioCreate):
    db_user = models.Usuario(
        username=usuario_in.username,
        nombre=usuario_in.nombre,
        rol_id=usuario_in.rol_id,
        hashed_password=hash_password(usuario_in.password),
        activo=True,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_usuarios(db: Session):
    return db.query(models.Usuario).all()

# ============================================================
# IMPORTAR ORDENES DE COMPRA
# ============================================================

def importar_orden_compra_desde_json(db: Session, data: dict):
    detalles = []
    for item in data["detalles"]:
        # Buscar refacción por clave o descripción
        ref = db.query(models.Refaccion).filter(
            models.Refaccion.descripcion == item["descripcion"]
        ).first()
        if not ref:
            ref = models.Refaccion(
                clave=item.get("clave") or item["descripcion"][:20],
                descripcion=item["descripcion"],
                unidad_medida=item.get("unidad", "pieza"),
            )
            db.add(ref)
            db.flush()

        detalles.append(
            models.OrdenCompraDetalle(
                refaccion_id=ref.id,
                cantidad=item["cantidad"],
                precio_unitario=item["precio_unitario"],
            )
        )

    oc = models.OrdenCompra(
        proveedor=data["proveedor"],
        factura=data.get("factura"),
        estado="pendiente",
    )
    db.add(oc)
    db.flush()

    for d in detalles:
        d.oc_id = oc.id
        db.add(d)

    db.commit()
    db.refresh(oc)
    return oc


def parsear_oc_desde_texto(texto: str) -> dict:
    """
    Parser para órdenes de compra del Municipio de Saltillo.
    Convierte el texto del PDF en un diccionario listo para importar.
    """

    # Normalizar texto
    t = texto.replace("\n", " ").replace("\r", " ")
    t = re.sub(r"\s+", " ", t)

    # ============================
    # PROVEEDOR
    # ============================
    proveedor = None
    m = re.search(r"PROVEEDOR\s*:\s*([A-Z0-9\s\.]+)", t)
    if m:
        proveedor = m.group(1).strip()

    # ============================
    # NÚMERO DE OC
    # ============================
    numero_oc = None
    m = re.search(r"NUMERO\s+(\d+)", t)
    if m:
        numero_oc = m.group(1)

    # ============================
    # FECHA
    # ============================
    fecha = None
    m = re.search(r"FECHA DE ELABORACIÓN:\s*([0-9\/\:\samp\.]+)", t, re.IGNORECASE)
    if m:
        try:
            fecha = datetime.strptime(m.group(1).strip(), "%d/%m/%Y %I:%M:%S%p")
        except:
            fecha = None

    # ============================
    # PARTIDAS
    # ============================
    partidas = []
    regex_partida = r"(\d+\.\d+)\s+([A-Z]+)\s+(\d+[\w\s\-]+)\s+\$\s*([\d,]+\.\d+)\s+\$\s*([\d,]+\.\d+)"
    for cant, unidad, desc, precio, importe in re.findall(regex_partida, t):
        partidas.append({
            "cantidad": float(cant),
            "unidad": unidad,
            "descripcion": desc.strip(),
            "precio_unitario": float(precio.replace(",", "")),
        })

    # ============================
    # RESULTADO
    # ============================
    return {
        "proveedor": proveedor or "DESCONOCIDO",
        "factura": None,
        "detalles": partidas,
        "numero_oc": numero_oc,
        "fecha": fecha.isoformat() if fecha else None
    }


# ============================================================
# PDF BINARIO → TEXTO
# ============================================================

def extraer_texto_de_pdf(pdf_bytes: bytes) -> str:
    texto = ""
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            texto += page.extract_text() + "\n"
    return texto


# ============================================================
# EXCEL → JSON
# ============================================================

def parsear_oc_desde_excel(excel_bytes: bytes) -> dict:
    wb = openpyxl.load_workbook(io.BytesIO(excel_bytes))
    ws = wb.active

    proveedor = None
    partidas = []

    for row in ws.iter_rows(values_only=True):
        if not row:
            continue

        # Detectar proveedor
        if "PROVEEDOR" in str(row[0]).upper():
            proveedor = row[1]

        # Detectar partidas (cantidad, unidad, descripción, precio)
        try:
            cantidad = float(row[0])
            unidad = str(row[1])
            descripcion = str(row[2])
            precio = float(str(row[3]).replace("$", "").replace(",", ""))
            partidas.append({
                "cantidad": cantidad,
                "unidad": unidad,
                "descripcion": descripcion,
                "precio_unitario": precio
            })
        except:
            continue

    return {
        "proveedor": proveedor or "DESCONOCIDO",
        "factura": None,
        "detalles": partidas
    }

# ============================================================
# PROVEEDORES
# ============================================================

def get_proveedores(db: Session):
    return (
        db.query(models.Proveedor)
        .filter(models.Proveedor.activo == True)
        .all()
    )

def get_proveedor(db: Session, proveedor_id: int):
    return (
        db.query(models.Proveedor)
        .filter(models.Proveedor.id == proveedor_id)
        .first()
    )

def create_proveedor(db: Session, data: schemas.ProveedorCreate):
    proveedor = models.Proveedor(**data.model_dump())
    db.add(proveedor)
    db.commit()
    db.refresh(proveedor)
    return proveedor

def update_proveedor(db: Session, proveedor_id: int, data: schemas.ProveedorUpdate):
    proveedor = get_proveedor(db, proveedor_id)
    if not proveedor:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(proveedor, key, value)

    db.commit()
    db.refresh(proveedor)
    return proveedor

def delete_proveedor(db: Session, proveedor_id: int):
    proveedor = get_proveedor(db, proveedor_id)
    if not proveedor:
        return None

    proveedor.activo = False
    db.commit()
    return proveedor
