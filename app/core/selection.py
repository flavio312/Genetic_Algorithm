import random
from typing import List, Tuple

def seleccion_torneo(poblacion: List[List[int]], aptitudes: List[float], tamano_torneo: int = 3) -> List[int]:
    """
    Selecciona un individuo usando selección por torneo.
    
    Args:
        poblacion: Lista de individuos
        aptitudes: Lista de aptitudes correspondientes
        tamano_torneo: Número de individuos que participan en el torneo
    
    Returns:
        List[int]: El individuo seleccionado
    """
    # Seleccionar aleatoriamente individuos para el torneo
    indices_torneo = random.sample(range(len(poblacion)), min(tamano_torneo, len(poblacion)))
    
    # Encontrar el mejor individuo del torneo (menor aptitud)
    mejor_indice = min(indices_torneo, key=lambda i: aptitudes[i])
    
    return poblacion[mejor_indice].copy()

def seleccion_ruleta(poblacion: List[List[int]], aptitudes: List[float]) -> List[int]:
    """
    Selecciona un individuo usando selección por ruleta.
    Como estamos minimizando, convertimos las aptitudes a probabilidades inversas.
    
    Args:
        poblacion: Lista de individuos
        aptitudes: Lista de aptitudes correspondientes
    
    Returns:
        List[int]: El individuo seleccionado
    """
    # Convertir aptitudes a fitness (inverso de la aptitud + pequeño valor para evitar división por cero)
    max_aptitud = max(aptitudes) if aptitudes else 1
    fitness_values = [max_aptitud - aptitud + 0.001 for aptitud in aptitudes]
    
    # Calcular probabilidades
    total_fitness = sum(fitness_values)
    probabilidades = [f / total_fitness for f in fitness_values]
    
    # Selección por ruleta
    r = random.random()
    acumulado = 0
    for i, prob in enumerate(probabilidades):
        acumulado += prob
        if r <= acumulado:
            return poblacion[i].copy()
    
    # Fallback: devolver el último individuo
    return poblacion[-1].copy()

def seleccionar_padres(poblacion: List[List[int]], aptitudes: List[float], 
                      num_padres: int, metodo: str = "torneo", tamano_torneo: int = 3) -> List[List[int]]:
    """
    Selecciona múltiples padres para la reproducción.
    
    Args:
        poblacion: Lista de individuos
        aptitudes: Lista de aptitudes correspondientes
        num_padres: Número de padres a seleccionar
        metodo: Método de selección ("torneo" o "ruleta")
        tamano_torneo: Tamaño del torneo (solo para selección por torneo)
    
    Returns:
        List[List[int]]: Lista de padres seleccionados
    """
    padres = []
    
    for _ in range(num_padres):
        if metodo == "torneo":
            padre = seleccion_torneo(poblacion, aptitudes, tamano_torneo)
        elif metodo == "ruleta":
            padre = seleccion_ruleta(poblacion, aptitudes)
        else:
            raise ValueError(f"Método de selección no reconocido: {metodo}")
        
        padres.append(padre)
    
    return padres

