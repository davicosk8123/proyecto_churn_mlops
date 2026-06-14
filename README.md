# Proyecto Churn MLOps

Este proyecto corresponde a una práctica inicial del módulo de MLOps.

El objetivo es construir una estructura básica de trabajo para un proyecto de Machine Learning que permita:

- Preparar datos.
- Entrenar un modelo.
- Evaluar métricas.
- Guardar el modelo entrenado.
- Exponer el modelo mediante una API.
- Ejecutar pruebas básicas.

## Problema del proyecto

Se trabajará con un caso simplificado de predicción de abandono de clientes, conocido como churn.

El modelo intentará predecir si un cliente podría abandonar un servicio, utilizando variables como edad, antigüedad, saldo promedio, reclamos y uso de aplicación móvil.

## Estructura del proyecto

```text
proyecto_churn_mlops
├── data
├── notebooks
├── src
├── models
├── api
├── tests
├── docs
├── README.md
└── requirements.txt
```

## Carpetas principales

- `data`: contiene los datos del proyecto.
- `notebooks`: contiene análisis exploratorios.
- `src`: contiene los scripts principales del modelo.
- `models`: contiene el modelo entrenado.
- `api`: contiene la API del modelo.
- `tests`: contiene pruebas automáticas.
- `docs`: contiene documentación y métricas.

## Flujo inicial del proyecto

El flujo básico será:

1. Preparar los datos.
2. Entrenar el modelo.
3. Evaluar el modelo.
4. Guardar las métricas.
5. Crear una API básica.
6. Probar el funcionamiento inicial.

---

## DOCUMENTACIÓN DE LA API (Mejoras Técnicas Personalizadas)

La API está desarrollada utilizando **FastAPI** y expone los siguientes endpoints técnicos enriquecidos para consumo, monitoreo e inferencia del modelo:

### 1. Endpoint Raíz (`GET /`)
Retorna el estado del servicio y el autor del proyecto.
- **Respuesta:**
  ```json
  {
    "mensaje": "Servicio ML-Ops activo",
    "estado": "ok",
    "autor": "Nimer David Guzmán Zapata"
  }
  ```

### 2. Endpoint de Estado de Salud (`GET /health`)
Verifica si la API está en línea y si el archivo binario del modelo de Machine Learning (`modelo_churn_v1.joblib`) está cargado y disponible.
- **Respuesta:**
  ```json
  {
    "estado": "ok",
    "modelo_disponible": true
  }
  ```

### 3. Endpoint Informativo (`GET /info`) - *Mejora Técnica*
Retorna información técnica y metadatos del modelo entrenado de manera dinámica (leyendo de `modelo_churn_v1_metadata.json`), incluyendo su versión, algoritmo utilizado, fecha de entrenamiento, variables utilizadas y métricas de evaluación obtenidas en test.
- **Respuesta:**
  ```json
  {
    "nombre_modelo": "Modelo de Predicción de Churn de Clientes",
    "version": "1.0.0",
    "algoritmo": "DecisionTreeClassifier (max_depth=3)",
    "autor": "Nimer David Guzmán Zapata",
    "fecha_entrenamiento": "2026-06-14T00:36:00.111900",
    "variables_utilizadas": [
      "edad",
      "antiguedad_meses",
      "saldo_promedio",
      "reclamos",
      "usa_app"
    ],
    "metricas_evaluacion": {
      "accuracy": 1.0,
      "precision": 1.0,
      "recall": 1.0,
      "f1_score": 1.0,
      "roc_auc": 1.0
    }
  }
  ```

### 4. Endpoint de Inferencia (`POST /predict`)
Recibe los datos del cliente y retorna la clasificación de Churn con su probabilidad, nivel de riesgo y recomendación automatizada.

#### Validaciones del Esquema de Entrada (Pydantic Fields):
- `edad`: Entero entre `18` y `100` años.
- `antiguedad_meses`: Entero mayor o igual a `0`.
- `saldo_promedio`: Flotante mayor o igual a `0.0`.
- `reclamos`: Entero mayor o igual a `0`.
- `usa_app`: Entero restrictivo, únicamente `0` (No) o `1` (Sí).

#### Ejemplo de Petición (Request Body):
```json
{
  "edad": 28,
  "antiguedad_meses": 8,
  "saldo_promedio": 1200.0,
  "reclamos": 3,
  "usa_app": 0
}
```

#### Ejemplo de Respuesta (Response Body):
```json
{
  "churn_predicho": 1,
  "probabilidad_churn": 1.0,
  "nivel_riesgo": "Alto",
  "recomendacion": "Llamada inmediata de soporte técnico y priorización por área de retención."
}
```

---

## Ejecución del Pipeline y Pruebas Unitarias en Docker

Asegúrate de estar situado en la raíz del proyecto y corre:

```powershell
# A. Preparar Datos (Genera archivos CSV en data/)
docker run --rm -v ${PWD}:/app proyecto-churn-mlops python src/preparar_datos.py

# B. Entrenar Modelo (Genera modelo_churn_v1.joblib y modelo_churn_v1_metadata.json en models/)
docker run --rm -v ${PWD}:/app proyecto-churn-mlops python src/entrenar_modelo.py

# C. Evaluar Modelo (Actualiza docs/metricas_modelo.md y actualiza metadatos JSON)
docker run --rm -v ${PWD}:/app proyecto-churn-mlops python src/evaluar_modelo.py

# D. Correr Tests Unitarios (Verifica los 7 casos de prueba de la API)
docker run --rm -v ${PWD}:/app proyecto-churn-mlops pytest
```

