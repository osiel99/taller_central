def test_flujo_completo(client):
    # 1. Crear vehículo
    veh_data = {
        "placas": "XYZ-999",
        "marca": "Toyota",
        "modelo": "Hilux",
        "anio": 2021
    }
    veh_resp = client.post("/vehiculos/", json=veh_data)
    assert veh_resp.status_code == 200
    veh = veh_resp.json()
    assert veh["placas"] == "XYZ-999"

    # 2. Crear OS
    os_resp = client.post("/ordenes_servicio/", json={
        "vehiculo_id": veh["id"],
        "diagnostico": "Frenos desgastados"
    })
    assert os_resp.status_code == 200
    os = os_resp.json()
    assert os["vehiculo_id"] == veh["id"]

    # 3. Crear refacción
    ref_resp = client.post("/refacciones/", json={
        "clave": "FRE-002",
        "descripcion": "Balatas traseras",
        "unidad_medida": "juego"
    })
    assert ref_resp.status_code == 200
    ref = ref_resp.json()
    assert ref["clave"] == "FRE-002"

    # 4. Crear solicitud
    sol_resp = client.post("/solicitudes/", json={
        "orden_servicio_id": os["id"],
        "solicitante": "Mecánico Juan",
        "detalles": [
            {"refaccion_id": ref["id"], "cantidad": 2}
        ]
    })
    assert sol_resp.status_code == 200
    sol = sol_resp.json()
    assert sol["orden_servicio_id"] == os["id"]

    # 5. Crear OC
    oc_resp = client.post("/ordenes_compra/", json={
        "solicitud_id": sol["id"],
        "proveedor": "Refaccionaria López",
        "detalles": [
            {"refaccion_id": ref["id"], "cantidad": 2, "precio_unitario": 300}
        ]
    })
    assert oc_resp.status_code == 200
    oc = oc_resp.json()
    assert oc["proveedor"] == "Refaccionaria López"

    # 6. Recepción
    rec_resp = client.post("/recepciones/", json={
        "oc_id": oc["id"],
        "recibido_por": "Almacén",
        "detalles": [
            {"refaccion_id": ref["id"], "cantidad_recibida": 2, "cantidad_oc": 2}
        ]
    })
    assert rec_resp.status_code == 200

    # 7. Inventario debe tener 2
    inv = client.get("/inventario/").json()
    assert len(inv) == 1
    assert inv[0]["existencia"] == 2

    # 8. Salida
    salida_resp = client.post("/salidas/", json={
        "orden_servicio_id": os["id"],
        "entregado_por": "Almacén",
        "recibido_por": "Mecánico Juan",
        "detalles": [
            {"refaccion_id": ref["id"], "cantidad": 1}
        ]
    })
    assert salida_resp.status_code == 200

    # 9. Inventario debe quedar en 1
    inv2 = client.get("/inventario/").json()
    assert inv2[0]["existencia"] == 1

    # 10. Kardex debe tener 2 movimientos
    kardex = client.get(f"/kardex/{ref['id']}").json()
    assert len(kardex) == 2

    # Validar tipos de movimiento
    assert kardex[0]["tipo"] == "entrada"
    assert kardex[1]["tipo"] == "salida"

    # Validar saldos
    assert kardex[0]["saldo"] == 2
    assert kardex[1]["saldo"] == 1
