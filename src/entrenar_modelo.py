from pathlib import Path

import joblib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

TRAIN_DATA = DATA_DIR / "train.csv"
MODEL_FILE = MODELS_DIR / "modelo_churn.pkl"

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

    print("Modelo entrenado correctamente (Árbol de Decisión - Experimento).")
    print(f"Modelo guardado en: {MODEL_FILE}")

if __name__ == "__main__":
    entrenar_modelo()
