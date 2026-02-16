def test_listar_vehiculos(client):
    # Crear un vehículo
    data = {
        "placas": "AAA-111",
        "marca": "Nissan",
        "modelo": "Versa",
        "anio": 2020
    }

    create_response = client.post("/vehiculos/", json=data)
    assert create_response.status_code == 200

    # Listar vehículos
    response = client.get("/vehiculos/")
    assert response.status_code == 200

    vehiculos = response.json()
    assert isinstance(vehiculos, list)
    assert len(vehiculos) == 1

    # Validar contenido
    assert vehiculos[0]["placas"] == "AAA-111"
    assert vehiculos[0]["marca"] == "Nissan"
