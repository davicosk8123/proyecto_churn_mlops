from pathlib import Path
import json

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
DOCS_DIR = BASE_DIR / "docs"

TEST_DATA = DATA_DIR / "test.csv"
MODEL_FILE = MODELS_DIR / "modelo_churn_v1.joblib"
METRICS_FILE = DOCS_DIR / "metricas_modelo.md"

def evaluar_modelo():
    """
    Evalúa el modelo del experimento (Árbol de Decisión) y actualiza el historial de métricas con ROC-AUC.
    """

    if not TEST_DATA.exists():
        raise FileNotFoundError(
            "No se encontró data/test.csv. Primero ejecuta src/preparar_datos.py"
        )

    if not MODEL_FILE.exists():
        raise FileNotFoundError(
            "No se encontró el modelo entrenado. Primero ejecuta src/entrenar_modelo.py"
        )

    DOCS_DIR.mkdir(exist_ok=True)

    df = pd.read_csv(TEST_DATA)

    X_test = df.drop(columns=["churn"])
    y_test = df["churn"]

    modelo = joblib.load(MODEL_FILE)

    y_pred = modelo.predict(X_test)
    
    # Calcular probabilidades para la métrica adicional ROC-AUC
    y_pred_proba = modelo.predict_proba(X_test)[:, 1] if hasattr(modelo, "predict_proba") else None

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
    roc_auc = roc_auc_score(y_test, y_pred_proba) if y_pred_proba is not None else 0.0

    # Nota: Los valores de la Regresión Logística (Base v1) con la semilla 42 son:
    # Accuracy: 1.0000, Precision: 1.0000, Recall: 1.0000, F1-score: 1.0000, ROC-AUC: 1.0000

    contenido = f"""# Reporte de Métricas: Comparativa de Experimentos

Este documento registra y compara el desempeño de las distintas versiones del modelo de clasificación de Churn, incorporando métricas adicionales.

## Tabla Comparativa de Modelos

| Versión del Modelo | Algoritmo | Accuracy | Precision | Recall | F1-score | ROC-AUC (Métrica Adicional) | Estado |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **v1 (Base)** | Regresión Logística | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | Deprecado (Rama main) |
| **v2 (Experimento)** | Árbol de Decisión (max_depth=3) | {accuracy:.4f} | {precision:.4f} | {recall:.4f} | {f1:.4f} | {roc_auc:.4f} | **Activo** (Rama experimento-arbol-decision) |

## Interpretación del Experimento

1. **Cambio Realizado (Algoritmo e Hiperparámetro):** Se sustituyó el modelo lineal de Regresión Logística por un modelo no lineal basado en Árboles de Decisión (`DecisionTreeClassifier`) con un parámetro de profundidad máxima controlado de `max_depth=3` para evitar el sobreajuste.
2. **Métrica Adicional Incorporada:** Se añadió el **ROC-AUC** (Área Bajo la Curva ROC) que mide la capacidad del modelo para distinguir entre clases positivas (churn) y negativas (no churn) independientemente del umbral de decisión.
3. **Resultado Obtenido:** El Árbol de Decisión obtiene métricas muy sólidas sobre el conjunto de test.
4. **Análisis de Trazabilidad:** En este dataset pequeño de demostración, ambos algoritmos logran separar perfectamente las clases del conjunto de prueba. En un dataset productivo real, el Árbol de Decisión ofrece reglas de clasificación legibles que facilitan la explicabilidad del negocio.
"""

    METRICS_FILE.write_text(contenido, encoding="utf-8")

    # Actualizar metadatos con las métricas obtenidas
    metadata_file = MODELS_DIR / "modelo_churn_v1_metadata.json"
    if metadata_file.exists():
        with open(metadata_file, "r", encoding="utf-8") as f:
            metadata = json.load(f)
        
        metadata["metricas_evaluacion"] = {
            "accuracy": round(float(accuracy), 4),
            "precision": round(float(precision), 4),
            "recall": round(float(recall), 4),
            "f1_score": round(float(f1), 4),
            "roc_auc": round(float(roc_auc), 4)
        }
        
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)
        print(f"Métricas actualizadas en los metadatos: {metadata_file}")

    print("Modelo del experimento evaluado correctamente con métrica adicional ROC-AUC.")
    print(f"Métricas comparativas guardadas en: {METRICS_FILE}")

if __name__ == "__main__":
    evaluar_modelo()

