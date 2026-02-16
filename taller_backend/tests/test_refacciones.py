def test_listar_refacciones(client):
    # Crear una refacción
    data = {
        "clave": "TEST-001",
        "descripcion": "Refacción de prueba",
        "unidad_medida": "pieza"
    }

    create_response = client.post("/refacciones/", json=data)
    assert create_response.status_code == 200

    # Listar refacciones
    response = client.get("/refacciones/")
    assert response.status_code == 200

    refacciones = response.json()
    assert isinstance(refacciones, list)
    assert len(refacciones) == 1

    # Validar contenido
    ref = refacciones[0]
    assert ref["clave"] == "TEST-001"
    assert ref["descripcion"] == "Refacción de prueba"
    assert ref["unidad_medida"] == "pieza"
