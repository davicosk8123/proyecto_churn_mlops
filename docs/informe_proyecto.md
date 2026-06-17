# INFORME TÉCNICO FINAL
## Proyecto Final Integrador: API Predictiva de Churn con MLOps

**Módulo:** ML-Ops y Puesta en Producción  
**Autor:** Nimer David Guzmán Zapata  
**Fecha:** 16 de Junio de 2026  

---

## 1. Problema y Objetivo

* **Contexto**: Retener clientes es más rentable que adquirir nuevos. Predecir a tiempo quién podría irse permite tomar acciones de retención.
* **Modelo**: Clasificación binaria (`churn = 1` abandona, `churn = 0` se queda) basado en: edad, antigüedad (meses), saldo promedio, reclamos y uso de app móvil.
* **Objetivo**: Implementar un pipeline de machine learning reproducible (datos, entrenamiento, evaluación) y exponer una API lista para producción dentro de un contenedor Docker.

---

## 2. Mejora Técnica Incorporada

Se implementaron tres mejoras clave respecto a la base del laboratorio:

1. **Endpoint Informativo (`GET /info`)**: Retorna de manera dinámica la información y métricas reales del modelo leyendo el archivo `modelo_churn_v1_metadata.json` (versión, algoritmo, fecha y métricas de evaluación).
2. **Respuesta de Inferencia Enriquecida**: El endpoint `/predict` no solo devuelve `0` o `1`, sino que calcula la probabilidad y categoriza el riesgo:
   * **Riesgo Alto ($\ge 70\%$)**: Recomienda "Llamada inmediata de soporte técnico" (si tiene reclamos) o "Campaña de fidelización personalizada".
   * **Riesgo Medio ($30\% - 70\%$)**: Recomienda "Ofrecer beneficios complementarios".
   * **Riesgo Bajo ($< 30\%$)**: Recomienda "Monitoreo estándar".
3. **Validación Estricta de Entradas**: Validación de datos con `Pydantic`:
   * `edad`: Entero entre 18 y 100 años.
   * `antiguedad_meses`, `saldo_promedio`, `reclamos`: Valores no negativos ($\ge 0$).
   * `usa_app`: Entero binario obligatorio (`0` o `1`).

---

## 3. API y Endpoints

Desarrollada en **FastAPI**. Cuenta con los siguientes endpoints:

* **`GET /`**: Mensaje de bienvenida y confirmación de servicio activo.
* **`GET /health`**: Retorna si la API funciona y si el archivo del modelo está cargado en el servidor.
* **`GET /info`**: Metadatos y métricas del modelo activo.
* **`POST /predict`**: Recibe datos del cliente y devuelve la predicción con recomendación.
* **`GET /docs`**: Documentación interactiva de Swagger para pruebas manuales.

---

## 4. Ejecución en Docker

La API y los scripts están encapsulados en una imagen basada en `python:3.12-slim`.

### Comandos de Ejecución en PowerShell / CMD:

1. **Construir la imagen**:
   ```bash
   docker build -t churn-api-guzman .
   ```
2. **Ejecutar Pipeline y Pruebas**:
   ```bash
   # Preparar datos (genera train.csv y test.csv)
   docker run --rm -v "${PWD}:/app" churn-api-guzman python src/preparar_datos.py
   
   # Entrenar modelo (genera modelo_churn_v1.joblib y metadatos)
   docker run --rm -v "${PWD}:/app" churn-api-guzman python src/entrenar_modelo.py
   
   # Evaluar modelo (genera reporte metricas_modelo.md)
   docker run --rm -v "${PWD}:/app" churn-api-guzman python src/evaluar_modelo.py
   
   # Ejecutar tests automáticos
   docker run --rm -v "${PWD}:/app" churn-api-guzman pytest
   ```
3. **Correr la API**:
   ```bash
   docker run -d --name churn-container -p 8001:8000 -v "${PWD}:/app" churn-api-guzman
   ```

---

## 5. Propuesta de Monitoreo Aplicada

Se definieron las métricas clave indicadas en la guía del proyecto:

| Métrica Seleccionada | Tipo | ¿Qué permite observar? | Señal de Alerta | Acción Propuesta |
| :--- | :--- | :--- | :--- | :--- |
| **Estado de `/health`** | Técnica | Si el servidor responde y tiene el modelo cargado. | El endpoint no responde o `modelo_disponible` es `false`. | Verificar la existencia física del archivo del modelo y reiniciar la API. |
| **Latencia de `/predict`** | Técnica | Tiempo de respuesta de la predicción. | Latencia promedio superior a `200 ms`. | Revisar recursos del host o capacidad del contenedor Docker. |
| **Proporción de Alto Riesgo** | Modelo | Porcentaje de respuestas predichas como `churn=1`. | Predicciones de Churn superan el `40%` del volumen diario. | Analizar datos de entrada por posibles cambios en el perfil del cliente. |
| **F1-score Histórico** | Modelo | Rendimiento del modelo con datos reales nuevos. | El F1-score cae por debajo de `0.85`. | Reentrenar el modelo con datos recientes recolectados. |

* **Alerta Prioritaria**: La tasa de errores de validación (HTTP 422) supera el `15%` de peticiones totales en 10 minutos.
* **Acción de Respuesta**: Validar la estructura de datos que envía la app móvil o el sitio web del banco, ya que indica problemas de formato en el origen.

---

## 6. Escenario de Error o Incidente

| Elemento | Respuesta del Maestrante |
| :--- | :--- |
| **Síntoma** | La API responde con error de servidor HTTP 503 ("El modelo aún no está disponible"). El endpoint `/health` responde `modelo_disponible: false`. |
| **Posible causa** | El archivo del modelo `modelo_churn_v1.joblib` no se encuentra en el directorio `models/` del servidor. |
| **Forma de detección** | Al consumir el endpoint `/health` (reporta `modelo_disponible: false`). |
| **Evidencia que revisaría** | Revisar la presencia física del archivo dentro de la carpeta `models` del contenedor Docker. |
| **Acción correctiva** | Ejecutar de nuevo el script de entrenamiento [src/entrenar_modelo.py](file:///c:/Users/David/OneDrive/Documentos/GitHub/proyecto_churn_mlops/src/entrenar_modelo.py) para regenerar el archivo `.joblib`. |
| **Acción preventiva** | Asegurar que el pipeline de integración contenga pruebas automatizadas previas que bloqueen el despliegue si no existe un modelo entrenado y funcional. |

---

## 7. Riesgo de Drift y Respuesta Operativa

| Elemento | Respuesta del Maestrante |
| :--- | :--- |
| **Riesgo identificado** | Incremento sistemático en el número de reclamos promedio de los clientes en producción. |
| **Tipo de drift** | **Data Drift (Covariate Shift)**: Cambia la distribución de la variable de entrada `reclamos`. |
| **Impacto** | Como el modelo árbol de decisión le da gran peso a los reclamos para decidir, el modelo empezará a predecir Churn masivamente (falsos positivos), causando que la empresa regale promociones o descuentos de retención innecesarios. |
| **Señal de alerta** | El valor promedio de la variable `reclamos` en las peticiones recibidas pasa de `1.5` (promedio de entrenamiento) a más de `2.5` en una semana. |
| **Respuesta operativa** | 1. Pausar temporalmente las campañas de retención automáticas basadas solo en reclamos.<br>2. Recolectar datos del comportamiento real de estos usuarios.<br>3. Reentrenar el modelo incorporando los datos de este nuevo comportamiento de reclamos. |

---

## 8. Conclusión

1. **Robustez y Seguridad**: Las validaciones automáticas de FastAPI con Pydantic garantizan que no entren datos inválidos al modelo predictivo.
2. **Fácil Operación**: Docker permite aislar el sistema y reproducir el pipeline completo de datos, entrenamiento, evaluación y API en cualquier computador.
3. **Mantenimiento Simple**: Monitorear endpoints básicos como `/health` y evaluar periódicamente las métricas permite mantener el modelo controlado y saber cuándo reentrenar.

---

## 9. Enlace al Repositorio

El código fuente completo del proyecto está disponible en:
* **Repositorio**: [https://github.com/davicosk8123/proyecto_churn_mlops](https://github.com/davicosk8123/proyecto_churn_mlops)
