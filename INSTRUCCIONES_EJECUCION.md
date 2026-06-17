# Instrucciones de Ejecución del Proyecto Churn MLOps (Entorno Docker)

Este documento describe cómo ejecutar la preparación de datos, entrenamiento, evaluación, pruebas y API de FastAPI utilizando Docker en una terminal de **PowerShell**.

---

## 0. Prerrequisito
Asegúrate de tener Docker activo en tu sistema y estar situado en la raíz del proyecto (`c:\Users\David\OneDrive\Documentos\GitHub\proyecto_churn_mlops`).

---

## 1. Construir la Imagen de Docker
Compila la imagen base que contiene Python y todas las dependencias necesarias:
```powershell
docker build -t proyecto-churn-mlops .
```

---

## 2. Ejecutar el Flujo de Machine Learning en Docker
Utilizaremos volúmenes montados (`-v "${PWD}:/app"`) para que los archivos generados dentro de la imagen de Docker aparezcan de inmediato en tu carpeta de trabajo local.

Corre los siguientes comandos desde tu terminal de **PowerShell**:

```powershell
# A. Preparar Datos (Genera archivos CSV en data/)
docker run --rm -v "${PWD}:/app" proyecto-churn-mlops python src/preparar_datos.py

# B. Entrenar Modelo (Genera modelo_churn_v1.joblib y metadatos JSON en models/)
docker run --rm -v "${PWD}:/app" proyecto-churn-mlops python src/entrenar_modelo.py

# C. Evaluar Modelo (Actualiza docs/metricas_modelo.md)
docker run --rm -v "${PWD}:/app" proyecto-churn-mlops python src/evaluar_modelo.py

# D. Correr Tests Unitarios (Valida la integridad de la API)
docker run --rm -v "${PWD}:/app" proyecto-churn-mlops pytest
```

---

## 3. Levantar la API en Docker
Para levantar el servidor web de FastAPI de forma interactiva y probarlo en tu navegador en el puerto `8001`:

```powershell
docker run -it --rm -p 8001:8000 -v "${PWD}:/app" proyecto-churn-mlops
```

### Probar la API:
1. Abre **[http://localhost:8001/docs](http://localhost:8001/docs)** en tu navegador.
2. Despliega `POST /predict`, haz clic en **"Try it out"**, edita los valores del JSON y presiona **"Execute"**.
3. Revisa la terminal en tiempo real para observar los logs de latencia y monitoreo autogenerados.
4. Para apagar la API, presiona `Ctrl + C` en tu terminal de PowerShell.
