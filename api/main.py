from pathlib import Path
import json

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_FILE = BASE_DIR / "models" / "modelo_churn_v1.joblib"

AUTOR = "Nimer David Guzmán Zapata"

app = FastAPI(
    title="Servicio ML-Ops - Churn",
    version="1.0.0",
    description="API avanzada para consumir un modelo de Machine Learning de predicción de churn."
)

class Cliente(BaseModel):
    edad: int = Field(..., ge=18, le=100, description="Edad del cliente (debe estar entre 18 y 100 años)")
    antiguedad_meses: int = Field(..., ge=0, description="Antigüedad del cliente en meses (debe ser >= 0)")
    saldo_promedio: float = Field(..., ge=0.0, description="Saldo promedio mensual (debe ser >= 0.0)")
    reclamos: int = Field(..., ge=0, description="Número de reclamos realizados (debe ser >= 0)")
    usa_app: int = Field(..., ge=0, le=1, description="Indica si usa app móvil: 1 (Sí) o 0 (No)")

def cargar_modelo():
    """
    Carga el modelo entrenado si existe.
    """
    if not MODEL_FILE.exists():
        return None

    return joblib.load(MODEL_FILE)

@app.get("/")
def inicio():
    return {
        "mensaje": "Servicio ML-Ops activo",
        "estado": "ok",
        "autor": AUTOR
    }

@app.get("/health")
def health():
    return {
        "estado": "ok",
        "modelo_disponible": MODEL_FILE.exists()
    }

@app.get("/info")
def info():
    """
    Retorna información técnica sobre el modelo, autor y variables utilizadas.
    Intenta cargar dinámicamente el archivo de metadatos modelo_churn_v1_metadata.json.
    """
    metadata_file = BASE_DIR / "models" / "modelo_churn_v1_metadata.json"
    if metadata_file.exists():
        try:
            with open(metadata_file, "r", encoding="utf-8") as f:
                metadata = json.load(f)
            return {
                "nombre_modelo": metadata.get("nombre_modelo"),
                "version": metadata.get("version"),
                "algoritmo": metadata.get("algoritmo"),
                "autor": metadata.get("autor"),
                "fecha_entrenamiento": metadata.get("fecha_entrenamiento"),
                "variables_utilizadas": metadata.get("variables_utilizadas"),
                "metricas_evaluacion": metadata.get("metricas_evaluacion")
            }
        except Exception:
            pass

    return {
        "nombre_modelo": "Modelo de Predicción de Churn de Clientes",
        "version": "1.0.0",
        "algoritmo": "DecisionTreeClassifier (max_depth=3)",
        "autor": AUTOR,
        "variables_utilizadas": ["edad", "antiguedad_meses", "saldo_promedio", "reclamos", "usa_app"]
    }

@app.post("/predict")
def predict(cliente: Cliente):
    modelo = cargar_modelo()

    if modelo is None:
        raise HTTPException(
            status_code=503,
            detail="El modelo aún no está disponible. Primero se debe entrenar el modelo."
        )

    datos = pd.DataFrame([cliente.model_dump()])

    prediccion = int(modelo.predict(datos)[0])

    probabilidad = 0.0
    if hasattr(modelo, "predict_proba"):
        probabilidad = float(modelo.predict_proba(datos)[0][1])

    # Mejora técnica: Enriquecer la respuesta con nivel de riesgo y recomendación de negocio
    if probabilidad >= 0.70:
        nivel_riesgo = "Alto"
        if cliente.reclamos > 2:
            recomendacion = "Llamada inmediata de soporte técnico y priorización por área de retención."
        else:
            recomendacion = "Ofrecer descuento / Campaña de fidelización personalizada."
    elif probabilidad >= 0.30:
        nivel_riesgo = "Medio"
        recomendacion = "Ofrecer beneficios en servicios complementarios y monitorear actividad."
    else:
        nivel_riesgo = "Bajo"
        recomendacion = "Mantener monitoreo estándar y promover nuevas funcionalidades de la app."

    return {
        "churn_predicho": prediccion,
        "probabilidad_churn": probabilidad,
        "nivel_riesgo": nivel_riesgo,
        "recomendacion": recomendacion
    }

