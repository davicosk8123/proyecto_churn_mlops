from pathlib import Path
import json
from datetime import datetime

import joblib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

TRAIN_DATA = DATA_DIR / "train.csv"
MODEL_FILE = MODELS_DIR / "modelo_churn_v1.joblib"

def entrenar_modelo():
    """
    Entrena un modelo de árbol de decisión para predecir churn (Experimento).
    """

    if not TRAIN_DATA.exists():
        raise FileNotFoundError(
            "No se encontró data/train.csv. Primero ejecuta src/preparar_datos.py"
        )

    MODELS_DIR.mkdir(exist_ok=True)

    df = pd.read_csv(TRAIN_DATA)

    X = df.drop(columns=["churn"])
    y = df["churn"]

    # EXPERIMENTO: Usar DecisionTreeClassifier con max_depth controlado
    modelo = Pipeline(
        steps=[
            ("escalado", StandardScaler()),
            ("clasificador", DecisionTreeClassifier(max_depth=3, random_state=42))
        ]
    )

    modelo.fit(X, y)

    joblib.dump(modelo, MODEL_FILE)

    # Guardar metadatos del modelo
    metadata_file = MODELS_DIR / "modelo_churn_v1_metadata.json"
    metadata = {
        "nombre_modelo": "Modelo de Predicción de Churn de Clientes",
        "version": "1.0.0",
        "algoritmo": "DecisionTreeClassifier (max_depth=3)",
        "autor": "Nimer David Guzmán Zapata",
        "fecha_entrenamiento": datetime.now().isoformat(),
        "variables_utilizadas": list(X.columns)
    }
    
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)

    print("Modelo entrenado correctamente (Árbol de Decisión - Experimento).")
    print(f"Modelo guardado en: {MODEL_FILE}")
    print(f"Metadatos guardados en: {metadata_file}")

if __name__ == "__main__":
    entrenar_modelo()

