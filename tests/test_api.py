from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

def test_inicio():
    response = client.get("/")
    assert response.status_code == 200
    json_resp = response.json()
    assert "mensaje" in json_resp
    assert json_resp["autor"] == "Nimer David Guzmán Zapata"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert "estado" in response.json()
    assert "modelo_disponible" in response.json()

def test_info():
    response = client.get("/info")
    assert response.status_code == 200
    json_resp = response.json()
    assert "nombre_modelo" in json_resp
    assert "autor" in json_resp
    assert json_resp["autor"] == "Nimer David Guzmán Zapata"
    assert "variables_utilizadas" in json_resp

def test_predict_valido():
    """
    Prueba una solicitud válida y verifica que contenga la predicción, 
    probabilidad, nivel de riesgo y recomendación de negocio.
    """
    cliente_ejemplo = {
        "edad": 28,
        "antiguedad_meses": 8,
        "saldo_promedio": 1200.0,
        "reclamos": 3,
        "usa_app": 0
    }
    response = client.post("/predict", json=cliente_ejemplo)
    assert response.status_code == 200
    json_response = response.json()
    assert "churn_predicho" in json_response
    assert "probabilidad_churn" in json_response
    assert "nivel_riesgo" in json_response
    assert "recomendacion" in json_response
    assert json_response["churn_predicho"] in [0, 1]
    assert json_response["nivel_riesgo"] in ["Bajo", "Medio", "Alto"]

def test_predict_campo_faltante():
    """
    Prueba una solicitud con un campo faltante (por ejemplo, falta 'edad').
    Verifica que la API responda con 422 Unprocessable Entity.
    """
    cliente_incompleto = {
        "antiguedad_meses": 8,
        "saldo_promedio": 1200.0,
        "reclamos": 3,
        "usa_app": 0
    }
    response = client.post("/predict", json=cliente_incompleto)
    assert response.status_code == 422

def test_predict_tipo_incorrecto():
    """
    Prueba una solicitud con tipo de dato incorrecto (por ejemplo, 'edad' es un string no convertible).
    Verifica que la API responda con 422 Unprocessable Entity.
    """
    cliente_tipo_erroneo = {
        "edad": "no_es_un_numero",
        "antiguedad_meses": 8,
        "saldo_promedio": 1200.0,
        "reclamos": 3,
        "usa_app": 0
    }
    response = client.post("/predict", json=cliente_tipo_erroneo)
    assert response.status_code == 422

def test_predict_valor_fuera_de_rango():
    """
    Prueba solicitudes con valores fuera del rango definido en Pydantic.
    Verifica que la API responda con 422 Unprocessable Entity.
    """
    # Edad fuera de rango (150 años)
    cliente_edad_invalida = {
        "edad": 150,
        "antiguedad_meses": 8,
        "saldo_promedio": 1200.0,
        "reclamos": 3,
        "usa_app": 0
    }
    response = client.post("/predict", json=cliente_edad_invalida)
    assert response.status_code == 422

    # usa_app fuera de rango (debe ser 0 o 1)
    cliente_app_invalida = {
        "edad": 30,
        "antiguedad_meses": 8,
        "saldo_promedio": 1200.0,
        "reclamos": 3,
        "usa_app": 2
    }
    response = client.post("/predict", json=cliente_app_invalida)
    assert response.status_code == 422

    # saldo_promedio negativo
    cliente_saldo_invalido = {
        "edad": 30,
        "antiguedad_meses": 8,
        "saldo_promedio": -50.0,
        "reclamos": 3,
        "usa_app": 1
    }
    response = client.post("/predict", json=cliente_saldo_invalido)
    assert response.status_code == 422

