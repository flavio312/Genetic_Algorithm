import random
from typing import List

def mutacion_intercambio(individuo: List[int]) -> List[int]:
    """
    Realiza mutación por intercambio de dos genes aleatorios.
    
    Args:
        individuo: Individuo a mutar
    
    Returns:
        List[int]: Individuo mutado
    """
    if len(individuo) < 2:
        return individuo.copy()
    
    individuo_mutado = individuo.copy()
    
    # Seleccionar dos posiciones aleatorias
    pos1, pos2 = random.sample(range(len(individuo)), 2)
    
    # Intercambiar los genes
    individuo_mutado[pos1], individuo_mutado[pos2] = individuo_mutado[pos2], individuo_mutado[pos1]
    
    return individuo_mutado

def mutacion_inversion(individuo: List[int]) -> List[int]:
    """
    Realiza mutación por inversión de un segmento del cromosoma.
    
    Args:
        individuo: Individuo a mutar
    
    Returns:
        List[int]: Individuo mutado
    """
    if len(individuo) < 2:
        return individuo.copy()
    
    individuo_mutado = individuo.copy()
    
    # Seleccionar dos puntos para definir el segmento a invertir
    punto1 = random.randint(0, len(individuo) - 1)
    punto2 = random.randint(0, len(individuo) - 1)
    
    # Asegurar que punto1 <= punto2
    if punto1 > punto2:
        punto1, punto2 = punto2, punto1
    
    # Invertir el segmento
    individuo_mutado[punto1:punto2+1] = reversed(individuo_mutado[punto1:punto2+1])
    
    return individuo_mutado

def mutacion_insercion(individuo: List[int]) -> List[int]:
    """
    Realiza mutación por inserción: toma un gen y lo inserta en otra posición.
    
    Args:
        individuo: Individuo a mutar
    
    Returns:
        List[int]: Individuo mutado
    """
    if len(individuo) < 2:
        return individuo.copy()
    
    individuo_mutado = individuo.copy()
    
    # Seleccionar posición del gen a mover y nueva posición
    pos_origen = random.randint(0, len(individuo) - 1)
    pos_destino = random.randint(0, len(individuo) - 1)
    
    # Extraer el gen y insertarlo en la nueva posición
    gen = individuo_mutado.pop(pos_origen)
    individuo_mutado.insert(pos_destino, gen)
    
    return individuo_mutado

def mutacion_aleatoria(individuo: List[int], num_reactivos: int) -> List[int]:
    """
    Realiza mutación aleatoria: cambia un gen por un valor aleatorio válido.
    
    Args:
        individuo: Individuo a mutar
        num_reactivos: Número total de reactivos disponibles
    
    Returns:
        List[int]: Individuo mutado
    """
    if not individuo or num_reactivos <= 0:
        return individuo.copy()
    
    individuo_mutado = individuo.copy()
    
    # Seleccionar una posición aleatoria
    pos = random.randint(0, len(individuo) - 1)
    
    # Asignar un nuevo valor aleatorio (índice de reactivo)
    individuo_mutado[pos] = random.randint(0, num_reactivos - 1)
    
    return individuo_mutado

def aplicar_mutacion(poblacion: List[List[int]], probabilidad_mutacion: float = 0.1, 
                    metodo: str = "intercambio", num_reactivos: int = None) -> List[List[int]]:
    """
    Aplica mutación a una población.
    
    Args:
        poblacion: Lista de individuos
        probabilidad_mutacion: Probabilidad de que ocurra la mutación
        metodo: Método de mutación ("intercambio", "inversion", "insercion", "aleatoria")
        num_reactivos: Número total de reactivos (necesario para mutación aleatoria)
    
    Returns:
        List[List[int]]: Población mutada
    """
    poblacion_mutada = []
    
    for individuo in poblacion:
        if random.random() < probabilidad_mutacion:
            if metodo == "intercambio":
                individuo_mutado = mutacion_intercambio(individuo)
            elif metodo == "inversion":
                individuo_mutado = mutacion_inversion(individuo)
            elif metodo == "insercion":
                individuo_mutado = mutacion_insercion(individuo)
            elif metodo == "aleatoria":
                if num_reactivos is None:
                    raise ValueError("num_reactivos es requerido para mutación aleatoria")
                individuo_mutado = mutacion_aleatoria(individuo, num_reactivos)
            else:
                raise ValueError(f"Método de mutación no reconocido: {metodo}")
        else:
            individuo_mutado = individuo.copy()
        
        poblacion_mutada.append(individuo_mutado)
    
    return poblacion_mutada