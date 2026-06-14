# Instrucciones de Ejecución del Proyecto Churn MLOps (Entorno Docker)

Este documento describe cómo ejecutar la preparación de datos, entrenamiento, evaluación, pruebas y API de FastAPI **únicamente utilizando Docker**, sin necesidad de instalar Python ni librerías en tu máquina local.

---

## 0. Prerrequisito
Asegúrate de tener Docker corriendo en tu sistema y de estar situado en la raíz del proyecto (`c:\Users\David\OneDrive\Documentos\GitHub\proyecto_churn_mlops`).

---

## 1. Construir la Imagen de Docker

Compila la imagen base que contiene Python 3.12 y todas las librerías necesarias:
```bash
docker build -t proyecto-churn-mlops .
```

---

## 2. Ejecutar el Flujo de Machine Learning en Docker
Utilizaremos volúmenes montados (`-v`) para que los archivos generados dentro del contenedor de Docker aparezcan de inmediato en tu carpeta local en VS Code.

Ejecuta los siguientes comandos según la terminal que estés usando en VS Code:

### Si usas PowerShell:
```powershell
# A. Preparar Datos (Genera archivos CSV en data/)
docker run --rm -v ${PWD}:/app proyecto-churn-mlops python src/preparar_datos.py

# B. Entrenar Modelo (Genera modelo_churn.pkl en models/)
docker run --rm -v ${PWD}:/app proyecto-churn-mlops python src/entrenar_modelo.py

# C. Evaluar Modelo (Actualiza docs/metricas_modelo.md)
docker run --rm -v ${PWD}:/app proyecto-churn-mlops python src/evaluar_modelo.py

# D. Correr Tests Unitarios (Verifica endpoints de la API)
docker run --rm -v ${PWD}:/app proyecto-churn-mlops pytest
```

### Si usas Símbolo del Sistema (CMD):
```cmd
# A. Preparar Datos (Genera archivos CSV en data/)
docker run --rm -v %cd%:/app proyecto-churn-mlops python src/preparar_datos.py

# B. Entrenar Modelo (Genera modelo_churn.pkl en models/)
docker run --rm -v %cd%:/app proyecto-churn-mlops python src/entrenar_modelo.py

# C. Evaluar Modelo (Actualiza docs/metricas_modelo.md)
docker run --rm -v %cd%:/app proyecto-churn-mlops python src/evaluar_modelo.py

# D. Correr Tests Unitarios (Verifica endpoints de la API)
docker run --rm -v %cd%:/app proyecto-churn-mlops pytest
```

*Al finalizar estos pasos, verás que en tu VS Code aparecen automáticamente los archivos `data/churn_clientes.csv`, `data/train.csv`, `data/test.csv`, `models/modelo_churn.pkl` y las métricas en `docs/metricas_modelo.md`.*

---

## 3. Levantar la API en Docker

Para iniciar el servidor web de FastAPI en el contenedor y poder consumirlo desde tu máquina en el puerto 8001:

### En PowerShell:
```powershell
docker run -it --rm -p 8001:8000 -v ${PWD}:/app proyecto-churn-mlops
```

### En CMD:
```cmd
docker run -it --rm -p 8001:8000 -v %cd%:/app proyecto-churn-mlops
```

### Probar la API
Con el contenedor corriendo:
1. Abre [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs) en tu navegador para ver la documentación interactiva de Swagger UI.
2. Despliega `POST /predict`, haz clic en **"Try it out"**, pega el JSON de prueba y presiona **"Execute"**.
3. Para apagar la API, presiona `Ctrl + C` en la terminal del contenedor.

