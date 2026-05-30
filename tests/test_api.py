from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

def test_inicio():
    response = client.get("/")

    assert response.status_code == 200
    assert "mensaje" in response.json()

def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert "estado" in response.json()
    assert "modelo_disponible" in response.json()

# NUEVA PRUEBA DE LA API (Requisito de la Parte B)
def test_predict():
    """
    Nueva prueba unitaria que valida el correcto funcionamiento 
    del endpoint /predict al enviar datos de un cliente.
    """
    cliente_ejemplo = {
        "edad": 28,
        "antiguedad_meses": 8,
        "saldo_promedio": 1200,
        "reclamos": 3,
        "usa_app": 0
    }
    
    response = client.post("/predict", json=cliente_ejemplo)
    
    assert response.status_code == 200
    json_response = response.json()
    assert "churn_predicho" in json_response
    assert "probabilidad_churn" in json_response
    assert json_response["churn_predicho"] in [0, 1]
