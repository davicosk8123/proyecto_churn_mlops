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

## DOCUMENTACIÓN DE LA API (Mejora Técnica del Experimento)

La API está desarrollada utilizando **FastAPI** y expone los siguientes endpoints técnicos para consumo e inferencia del modelo:

### 1. Endpoint Raíz (`GET /`)
Retorna el mensaje de estado de la API.
- **Respuesta:**
  ```json
  {
    "mensaje": "API de predicción de churn activa"
  }
  ```

### 2. Endpoint de Estado de Salud (`GET /health`)
Verifica si la API está en línea y si el archivo binario del modelo de Machine Learning (`modelo_churn.pkl`) está cargado y disponible.
- **Respuesta:**
  ```json
  {
    "estado": "ok",
    "modelo_disponible": true
  }
  ```

### 3. Endpoint de Inferencia (`POST /predict`)
Recibe los datos socio-demográficos y transaccionales del cliente y retorna la clasificación probabilística del Churn.
- **Cuerpo de la Petición (Request Body):**
  ```json
  {
    "edad": 28,
    "antiguedad_meses": 8,
    "saldo_promedio": 1200,
    "reclamos": 3,
    "usa_app": 0
  }
  ```
- **Cuerpo de la Respuesta (Response Body):**
  ```json
  {
    "churn_predicho": 1,
    "probabilidad_churn": 0.95
  }
  ```
