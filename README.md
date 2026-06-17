# Proyecto Churn MLOps

Este proyecto implementa un pipeline completo de Machine Learning y una API contenerizada para la predicción de abandono de clientes (churn), bajo prácticas de **MLOps**.

El modelo predice si un cliente podría abandonar un servicio (`churn = 1`) o no (`churn = 0`), utilizando variables como: edad, antigüedad en meses, saldo promedio mensual, reclamos y uso de aplicación móvil.

---

## Estructura del Proyecto

```text
proyecto_churn_mlops
├── api/                  # Código de la API (FastAPI)
├── data/                 # Archivos CSV de datos (generados por pipeline)
├── docs/                 # Documentación e informes del proyecto
├── models/               # Archivos del modelo serializado y metadatos
├── src/                  # Scripts del pipeline (datos, entrenamiento, evaluación)
├── tests/                # Pruebas automatizadas (pytest)
├── Dockerfile            # Configuración del contenedor Docker
├── .dockerignore         # Archivos excluidos del contenedor
└── requirements.txt      # Dependencias de Python
```

---

## Documentación de la API (Mejoras Técnicas)

La API cuenta con los siguientes endpoints técnicos y de inferencia:

### 1. Raíz (`GET /`)
* **Función**: Verifica el estado inicial del servicio y el autor.
* **Respuesta**:
  ```json
  {
    "mensaje": "Servicio ML-Ops activo",
    "estado": "ok",
    "autor": "Nimer David Guzmán Zapata"
  }
  ```

### 2. Salud (`GET /health`)
* **Función**: Monitorea que la API esté en línea y que el modelo (`modelo_churn_v1.joblib`) esté correctamente cargado en memoria.

### 3. Informativo (`GET /info`)
* **Función**: Carga de forma dinámica y expone la información técnica del modelo activo (algoritmo, versión, fecha de entrenamiento, variables y métricas F1-score, ROC-AUC, etc.) desde los metadatos JSON.

### 4. Inferencia (`POST /predict`)
* **Función**: Procesa las variables del cliente, valida rangos con `Pydantic` (Edad 18-100, `usa_app` binario 0 o 1, y resto $\ge 0$) y devuelve:
  * Predicción de Churn y Probabilidad.
  * **Nivel de Riesgo**: Categorizado en Bajo, Medio o Alto.
  * **Recomendación de Negocio**: Sugerencias de retención automatizadas basadas en el perfil.

---

## Guía de Ejecución en Docker (PowerShell)

Asegúrate de tener Docker corriendo en tu sistema y de estar situado en la raíz del proyecto en tu terminal de PowerShell.

### 1. Construir la Imagen de Docker
```powershell
docker build -t proyecto-churn-mlops .
```

### 2. Ejecutar el Pipeline de Machine Learning
Ejecuta los siguientes comandos en PowerShell utilizando volúmenes montados (`${PWD}`) para que los archivos generados en el contenedor se guarden inmediatamente en tu carpeta local:

```powershell
# A. Preparar Datos (Genera train.csv y test.csv en data/)
docker run --rm -v "${PWD}:/app" proyecto-churn-mlops python src/preparar_datos.py

# B. Entrenar Modelo (Genera modelo_churn_v1.joblib y metadatos en models/)
docker run --rm -v "${PWD}:/app" proyecto-churn-mlops python src/entrenar_modelo.py

# C. Evaluar Modelo (Actualiza docs/metricas_modelo.md)
docker run --rm -v "${PWD}:/app" proyecto-churn-mlops python src/evaluar_modelo.py

# D. Correr Pruebas Unitarias (Valida endpoints de la API con pytest)
docker run --rm -v "${PWD}:/app" proyecto-churn-mlops pytest
```

### 3. Levantar la API en Modo Interactivo
Inicia el servidor web FastAPI mapeando el puerto `8001` de tu máquina local:

```powershell
docker run -it --rm -p 8001:8000 -v "${PWD}:/app" proyecto-churn-mlops
```

* **Acceso a Swagger UI**: Con la API corriendo, abre tu navegador en **[http://localhost:8001/docs](http://localhost:8001/docs)** para interactuar con los endpoints y realizar pruebas de predicción.
* **Apagar el Servidor**: Presiona `Ctrl + C` en la terminal para apagar y remover el contenedor automáticamente.
