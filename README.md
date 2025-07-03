# API de Algoritmo Genético

Una API REST desarrollada con FastAPI que implementa un algoritmo genético para la selección óptima de reactivos basada en debilidades específicas en lectura, escritura y memoria.

## Características

- **Arquitectura modular**: Separación clara de responsabilidades en diferentes componentes
- **API REST**: Endpoints bien documentados con FastAPI
- **Algoritmo genético configurable**: Parámetros ajustables para optimización
- **Validación de datos**: Validación robusta de entrada con Pydantic
- **CORS habilitado**: Soporte para aplicaciones frontend
- **Documentación automática**: Swagger UI disponible en `/docs`

## Estructura del Proyecto

```
genetic_algorithm_api/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py          # Modelos Pydantic
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py          # Configuración de rutas
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           └── genetic_algorithm.py  # Endpoints del algoritmo
│   └── core/
│       ├── __init__.py
│       ├── genetic_algorithm.py    # Algoritmo principal
│       ├── fitness.py             # Función de aptitud
│       ├── selection.py           # Operadores de selección
│       ├── crossover.py           # Operadores de cruce
│       └── mutation.py            # Operadores de mutación
├── main.py                        # Punto de entrada de la aplicación
├── requirements.txt               # Dependencias
├── test_algorithm.py             # Pruebas del algoritmo
├── test_api.py                   # Pruebas de la API
└── README.md                     # Este archivo
```

## Instalación

1. **Clonar o descargar el proyecto**

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación**:
   ```bash
   python main.py
   ```

La API estará disponible en `http://localhost:8000`

## Uso de la API

### Endpoints Principales

#### 1. Ejecutar Algoritmo Genético
- **URL**: `POST /api/v1/algoritmo-genetico/ejecutar`
- **Descripción**: Ejecuta el algoritmo genético con los datos proporcionados

**Ejemplo de petición**:
```json
{
  "debilidades": {
    "lectura": 0.4,
    "escritura": 0.6,
    "memoria": 0.5
  },
  "reactivos": [
    {
      "id_reactivo": 1,
      "lectura": 0.2,
      "escritura": 0.3,
      "memoria": 0.5
    },
    {
      "id_reactivo": 2,
      "lectura": 0.3,
      "escritura": 0.4,
      "memoria": 0.3
    }
  ]
}
```

**Ejemplo de respuesta**:
```json
{
  "mejor_individuo": [1, 0],
  "aptitud": 0.05,
  "generaciones": 100,
  "poblacion_final": [[1, 0], [0, 1], ...],
  "aptitudes_finales": [0.05, 0.15, ...]
}
```

#### 2. Validar Datos
- **URL**: `POST /api/v1/algoritmo-genetico/validar-datos`
- **Descripción**: Valida los datos de entrada sin ejecutar el algoritmo

#### 3. Configuración por Defecto
- **URL**: `GET /api/v1/algoritmo-genetico/configuracion-defecto`
- **Descripción**: Obtiene la configuración por defecto del algoritmo

#### 4. Salud de la API
- **URL**: `GET /`
- **Descripción**: Verifica que la API esté funcionando

### Documentación Interactiva

Visita `http://localhost:8000/docs` para acceder a la documentación interactiva de Swagger UI.

## Configuración del Algoritmo

El algoritmo genético utiliza los siguientes parámetros por defecto:

- **Tamaño de población**: 50
- **Número de generaciones**: 100
- **Probabilidad de cruce**: 0.8
- **Probabilidad de mutación**: 0.1
- **Tamaño de torneo**: 3
- **Elitismo**: Habilitado

## Pruebas

### Ejecutar pruebas del algoritmo:
```bash
python test_algorithm.py
```

### Ejecutar pruebas de la API:
```bash
python test_api.py
```

## Funcionamiento del Algoritmo

1. **Inicialización**: Se crea una población inicial de individuos aleatorios
2. **Evaluación**: Se calcula la aptitud de cada individuo
3. **Selección**: Se seleccionan los mejores individuos para reproducción
4. **Cruce**: Se combinan los genes de los padres seleccionados
5. **Mutación**: Se introducen variaciones aleatorias
6. **Reemplazo**: Se forma la nueva generación
7. **Terminación**: Se repite hasta cumplir el criterio de parada

### Función de Aptitud

La función de aptitud calcula qué tan bien un conjunto de reactivos seleccionados se alinea con las debilidades objetivo. Se busca minimizar la suma de las diferencias absolutas entre:

- Las características promedio de los reactivos seleccionados
- Las debilidades objetivo proporcionadas

## Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido
- **Pydantic**: Validación de datos y serialización
- **Uvicorn**: Servidor ASGI de alto rendimiento
- **Python 3.11+**: Lenguaje de programación

## Contribución

Para contribuir al proyecto:

1. Haz un fork del repositorio
2. Crea una rama para tu feature
3. Implementa tus cambios
4. Ejecuta las pruebas
5. Envía un pull request

## Licencia

Este proyecto está bajo la Licencia MIT.

