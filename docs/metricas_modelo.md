# Reporte de Métricas: Comparativa de Experimentos

Este documento registra y compara el desempeño de las distintas versiones del modelo de clasificación de Churn.

## Tabla Comparativa de Modelos

| Versión del Modelo | Algoritmo | Accuracy | Precision | Recall | F1-score | Estado |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **v1 (Base)** | Regresión Logística | 1.0000 | 1.0000 | 1.0000 | 1.0000 | Deprecado (Rama main) |
| **v2 (Experimento)** | Árbol de Decisión (max_depth=3) | 1.0000 | 1.0000 | 1.0000 | 1.0000 | **Activo** (Rama experimento-arbol-decision) |

## Interpretación del Experimento

1. **Cambio Realizado:** Se sustituyó el modelo lineal de Regresión Logística por un modelo no lineal basado en Árboles de Decisión (`DecisionTreeClassifier`) con un parámetro de profundidad máxima controlado de `max_depth=3` para evitar el sobreajuste.
2. **Resultado Obtenido:** El Árbol de Decisión obtiene métricas muy sólidas sobre el conjunto de test.
3. **Análisis:** En este dataset pequeño de demostración, ambos algoritmos logran separar perfectamente las clases del conjunto de prueba. En un dataset productivo real, el Árbol de Decisión ofrece reglas de clasificación legibles que facilitan la explicabilidad del negocio.
