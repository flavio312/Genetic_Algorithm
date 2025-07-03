from typing import List
from app.models.schemas import Reactivo, Debilidades

def calcular_aptitud(individuo: List[int], reactivos: List[Reactivo], debilidades_objetivo: Debilidades) -> float:
    """
    Calcula la aptitud de un individuo basándose en qué tan bien se alinea
    con las debilidades objetivo.
    
    Args:
        individuo: Lista de índices de reactivos seleccionados
        reactivos: Lista completa de reactivos disponibles
        debilidades_objetivo: Debilidades que se quieren abordar
    
    Returns:
        float: Valor de aptitud (menor es mejor)
    """
    if not individuo:
        return float('inf')  # Penalizar individuos vacíos
    
    # Calcular las debilidades totales del individuo
    lectura_total = sum(reactivos[i].lectura for i in individuo if i < len(reactivos))
    escritura_total = sum(reactivos[i].escritura for i in individuo if i < len(reactivos))
    memoria_total = sum(reactivos[i].memoria for i in individuo if i < len(reactivos))
    
    # Normalizar por el número de reactivos seleccionados
    num_reactivos = len(individuo)
    lectura_promedio = lectura_total / num_reactivos
    escritura_promedio = escritura_total / num_reactivos
    memoria_promedio = memoria_total / num_reactivos
    
    # Calcular la diferencia absoluta con las debilidades objetivo
    diferencia_lectura = abs(lectura_promedio - debilidades_objetivo.lectura)
    diferencia_escritura = abs(escritura_promedio - debilidades_objetivo.escritura)
    diferencia_memoria = abs(memoria_promedio - debilidades_objetivo.memoria)
    
    # La aptitud es la suma de las diferencias (menor es mejor)
    aptitud = diferencia_lectura + diferencia_escritura + diferencia_memoria
    
    return aptitud

def evaluar_poblacion(poblacion: List[List[int]], reactivos: List[Reactivo], debilidades_objetivo: Debilidades) -> List[float]:
    """
    Evalúa la aptitud de toda una población.
    
    Args:
        poblacion: Lista de individuos (cada uno es una lista de índices)
        reactivos: Lista completa de reactivos disponibles
        debilidades_objetivo: Debilidades que se quieren abordar
    
    Returns:
        List[float]: Lista de aptitudes correspondientes a cada individuo
    """
    return [calcular_aptitud(individuo, reactivos, debilidades_objetivo) for individuo in poblacion]

