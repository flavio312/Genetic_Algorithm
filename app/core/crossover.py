import random
from typing import List, Tuple

def cruce_un_punto(padre1: List[int], padre2: List[int]) -> Tuple[List[int], List[int]]:
    """
    Realiza cruce de un punto entre dos padres.
    
    Args:
        padre1: Primer padre
        padre2: Segundo padre
    
    Returns:
        Tuple[List[int], List[int]]: Dos hijos resultantes del cruce
    """
    if len(padre1) <= 1 or len(padre2) <= 1:
        return padre1.copy(), padre2.copy()
    
    # Seleccionar punto de cruce
    punto_cruce = random.randint(1, min(len(padre1), len(padre2)) - 1)
    
    # Crear hijos
    hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
    hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]
    
    return hijo1, hijo2

def cruce_dos_puntos(padre1: List[int], padre2: List[int]) -> Tuple[List[int], List[int]]:
    """
    Realiza cruce de dos puntos entre dos padres.
    
    Args:
        padre1: Primer padre
        padre2: Segundo padre
    
    Returns:
        Tuple[List[int], List[int]]: Dos hijos resultantes del cruce
    """
    if len(padre1) <= 2 or len(padre2) <= 2:
        return cruce_un_punto(padre1, padre2)
    
    # Seleccionar dos puntos de cruce
    longitud_min = min(len(padre1), len(padre2))
    punto1 = random.randint(1, longitud_min - 2)
    punto2 = random.randint(punto1 + 1, longitud_min - 1)
    
    # Crear hijos
    hijo1 = padre1[:punto1] + padre2[punto1:punto2] + padre1[punto2:]
    hijo2 = padre2[:punto1] + padre1[punto1:punto2] + padre2[punto2:]
    
    return hijo1, hijo2

def cruce_uniforme(padre1: List[int], padre2: List[int], probabilidad: float = 0.5) -> Tuple[List[int], List[int]]:
    """
    Realiza cruce uniforme entre dos padres.
    
    Args:
        padre1: Primer padre
        padre2: Segundo padre
        probabilidad: Probabilidad de tomar el gen del primer padre
    
    Returns:
        Tuple[List[int], List[int]]: Dos hijos resultantes del cruce
    """
    longitud_min = min(len(padre1), len(padre2))
    
    hijo1 = []
    hijo2 = []
    
    for i in range(longitud_min):
        if random.random() < probabilidad:
            hijo1.append(padre1[i])
            hijo2.append(padre2[i])
        else:
            hijo1.append(padre2[i])
            hijo2.append(padre1[i])
    
    # Agregar genes restantes si los padres tienen diferentes longitudes
    if len(padre1) > longitud_min:
        hijo1.extend(padre1[longitud_min:])
    if len(padre2) > longitud_min:
        hijo2.extend(padre2[longitud_min:])
    
    return hijo1, hijo2

def aplicar_cruce(poblacion_padres: List[List[int]], probabilidad_cruce: float = 0.8, 
                 metodo: str = "un_punto") -> List[List[int]]:
    """
    Aplica cruce a una población de padres.
    
    Args:
        poblacion_padres: Lista de padres seleccionados
        probabilidad_cruce: Probabilidad de que ocurra el cruce
        metodo: Método de cruce ("un_punto", "dos_puntos", "uniforme")
    
    Returns:
        List[List[int]]: Lista de hijos resultantes
    """
    hijos = []
    
    # Asegurar que tenemos un número par de padres
    if len(poblacion_padres) % 2 != 0:
        poblacion_padres.append(poblacion_padres[-1].copy())
    
    # Aplicar cruce por pares
    for i in range(0, len(poblacion_padres), 2):
        padre1 = poblacion_padres[i]
        padre2 = poblacion_padres[i + 1]
        
        if random.random() < probabilidad_cruce:
            if metodo == "un_punto":
                hijo1, hijo2 = cruce_un_punto(padre1, padre2)
            elif metodo == "dos_puntos":
                hijo1, hijo2 = cruce_dos_puntos(padre1, padre2)
            elif metodo == "uniforme":
                hijo1, hijo2 = cruce_uniforme(padre1, padre2)
            else:
                raise ValueError(f"Método de cruce no reconocido: {metodo}")
        else:
            # Sin cruce, los hijos son copias de los padres
            hijo1, hijo2 = padre1.copy(), padre2.copy()
        
        hijos.extend([hijo1, hijo2])
    
    return hijos

