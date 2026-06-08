# Reporte de Métricas: Comparativa de Experimentos

Este documento registra y compara el desempeño de las distintas versiones del modelo de clasificación de Churn, incorporando métricas adicionales.

## Tabla Comparativa de Modelos

| Versión del Modelo | Algoritmo | Accuracy | Precision | Recall | F1-score | ROC-AUC (Métrica Adicional) | Estado |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **v1 (Base)** | Regresión Logística | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | Deprecado (Rama main) |
| **v2 (Experimento)** | Árbol de Decisión (max_depth=3) | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | **Activo** (Rama experimento-arbol-decision) |

## Interpretación del Experimento

1. **Cambio Realizado (Algoritmo e Hiperparámetro):** Se sustituyó el modelo lineal de Regresión Logística por un modelo no lineal basado en Árboles de Decisión (`DecisionTreeClassifier`) con un parámetro de profundidad máxima controlado de `max_depth=3` para evitar el sobreajuste.
2. **Métrica Adicional Incorporada:** Se añadió el **ROC-AUC** (Área Bajo la Curva ROC) que mide la capacidad del modelo para distinguir entre clases positivas (churn) y negativas (no churn) independientemente del umbral de decisión.
3. **Resultado Obtenido:** El Árbol de Decisión obtiene métricas muy sólidas sobre el conjunto de test.
4. **Análisis de Trazabilidad:** En este dataset pequeño de demostración, ambos algoritmos logran separar perfectamente las clases del conjunto de prueba. En un dataset productivo real, el Árbol de Decisión ofrece reglas de clasificación legibles que facilitan la explicabilidad del negocio.
