# ESTRUCTURA DE DIAPOSITIVA RESUMEN
## Operación y MLOps: API Predictiva de Churn
---

### [PARTE SUPERIOR - CABECERA]
* **Título:** Despliegue y Operación de API Predictiva de Churn
* **Autor:** Nimer David Guzmán Zapata | Maestría en Ciencia de Datos e IA
---

#### Mejora Técnica y Evidencia
* **Endpoint técnico `/info`**: Carga dinámica de metadatos y métricas reales del modelo desde JSON.
* **Validación de esquema (Pydantic)**: Edad (18-100), uso de app (0 o 1), saldo y reclamos ($\ge 0$).
* **Respuesta enriquecida**: Asignación de nivel de riesgo (Bajo/Medio/Alto) y recomendación inmediata.

#### Propuesta de Monitoreo
* **Monitoreo Técnico**:
  * **Disponibilidad**: Estado del endpoint `/health` (Alerta si responde `false` o no responde).
  * **Latencia**: Tiempos de respuesta del endpoint `/predict` (Alerta si supera `200 ms`).
* **Monitoreo del Modelo**:
  * **Comportamiento**: Proporción de predicciones de Alto Riesgo (Alerta si supera el `40%` diario).
  * **Calidad**: Re-evaluación periódica del F1-score con datos reales (Alerta si cae por debajo de `0.85`).

####  Escenario de Error / Incidente
* **Incidente**: Inferencia `/predict` retorna código **HTTP 503** (Servicio no disponible).
* **Causa**: Falta el archivo binario del modelo `.joblib` en la carpeta `/models`.
* **Detección**: `/health` reporta `"modelo_disponible": false`.
* **Solución**: Ejecutar el script `src/entrenar_modelo.py` para regenerar el modelo.
* **Prevención**: Pruebas automáticas en el pipeline CI antes de construir la imagen Docker.

####  Riesgo de Drift y Respuesta
* **Drift detectado**: Aumento sistemático en el promedio de reclamos diarios de los clientes (Data Drift).
* **Impacto**: El modelo genera falsas alarmas de abandono (Falsos Positivos) y se desperdician recursos de retención.
* **Detección**: Promedio de la variable `reclamos` sube de `1.5` a más de `2.5` en una semana.
* **Respuesta**: Pausar alertas automáticas de Churn, diagnosticar la causa de reclamos, y reentrenar el modelo con nuevos datos.
