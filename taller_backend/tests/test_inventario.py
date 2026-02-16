def test_inventario_inicia_vacio(client):
    # Obtener inventario
    response = client.get("/inventario/")
    assert response.status_code == 200

    inventario = response.json()

    # Validar que es una lista vacía
    assert isinstance(inventario, list)
    assert inventario == []
