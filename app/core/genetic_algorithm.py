import random
from typing import List, Tuple
from app.models.schemas import Reactivo, Debilidades, ConfiguracionAlgoritmo, AlgoritmoGeneticoOutput
from app.core.fitness import evaluar_poblacion
from app.core.selection import seleccionar_padres
from app.core.crossover import aplicar_cruce
from app.core.mutation import aplicar_mutacion

class AlgoritmoGenetico:
    def __init__(self, reactivos: List[Reactivo], debilidades_objetivo: Debilidades, 
                 configuracion: ConfiguracionAlgoritmo = None):
        """
        Inicializa el algoritmo genético.
        
        Args:
            reactivos: Lista de reactivos disponibles
            debilidades_objetivo: Debilidades que se quieren abordar
            configuracion: Configuración del algoritmo
        """
        self.reactivos = reactivos
        self.debilidades_objetivo = debilidades_objetivo
        self.config = configuracion or ConfiguracionAlgoritmo()
        self.poblacion = []
        self.aptitudes = []
        self.mejor_individuo = None
        self.mejor_aptitud = float('inf')
        self.historial_aptitudes = []
    
    def generar_individuo_aleatorio(self, min_reactivos: int = 3, max_reactivos: int = 10) -> List[int]:
        """
        Genera un individuo aleatorio.
        
        Args:
            min_reactivos: Número mínimo de reactivos en el individuo
            max_reactivos: Número máximo de reactivos en el individuo
        
        Returns:
            List[int]: Individuo aleatorio (lista de índices de reactivos)
        """
        num_reactivos_total = len(self.reactivos)
        if num_reactivos_total == 0:
            return []
        
        # Determinar el número de reactivos para este individuo
        max_reactivos = min(max_reactivos, num_reactivos_total)
        min_reactivos = min(min_reactivos, max_reactivos)
        num_reactivos = random.randint(min_reactivos, max_reactivos)
        
        # Seleccionar reactivos aleatorios sin repetición
        return random.sample(range(num_reactivos_total), num_reactivos)
    
    def inicializar_poblacion(self):
        """Inicializa la población con individuos aleatorios."""
        self.poblacion = []
        for _ in range(self.config.tamano_poblacion):
            individuo = self.generar_individuo_aleatorio()
            self.poblacion.append(individuo)
    
    def evaluar_poblacion_actual(self):
        """Evalúa la aptitud de la población actual."""
        self.aptitudes = evaluar_poblacion(self.poblacion, self.reactivos, self.debilidades_objetivo)
        
        # Actualizar el mejor individuo
        mejor_indice = min(range(len(self.aptitudes)), key=lambda i: self.aptitudes[i])
        if self.aptitudes[mejor_indice] < self.mejor_aptitud:
            self.mejor_aptitud = self.aptitudes[mejor_indice]
            self.mejor_individuo = self.poblacion[mejor_indice].copy()
    
    def aplicar_elitismo(self, nueva_poblacion: List[List[int]], nuevas_aptitudes: List[float]) -> Tuple[List[List[int]], List[float]]:
        """
        Aplica elitismo manteniendo los mejores individuos de la generación anterior.
        
        Args:
            nueva_poblacion: Nueva población generada
            nuevas_aptitudes: Aptitudes de la nueva población
        
        Returns:
            Tuple[List[List[int]], List[float]]: Población y aptitudes finales
        """
        if not self.config.elitismo or not self.poblacion:
            return nueva_poblacion, nuevas_aptitudes
        
        # Combinar poblaciones
        poblacion_combinada = self.poblacion + nueva_poblacion
        aptitudes_combinadas = self.aptitudes + nuevas_aptitudes
        
        # Seleccionar los mejores individuos
        indices_ordenados = sorted(range(len(aptitudes_combinadas)), 
                                 key=lambda i: aptitudes_combinadas[i])
        
        mejores_indices = indices_ordenados[:self.config.tamano_poblacion]
        
        poblacion_final = [poblacion_combinada[i] for i in mejores_indices]
        aptitudes_finales = [aptitudes_combinadas[i] for i in mejores_indices]
        
        return poblacion_final, aptitudes_finales
    
    def ejecutar(self) -> AlgoritmoGeneticoOutput:
        """
        Ejecuta el algoritmo genético completo.
        
        Returns:
            AlgoritmoGeneticoOutput: Resultados del algoritmo
        """
        # Inicialización
        self.inicializar_poblacion()
        self.evaluar_poblacion_actual()
        self.historial_aptitudes.append(self.mejor_aptitud)
        
        # Evolución
        for generacion in range(self.config.numero_generaciones):
            # Selección
            padres = seleccionar_padres(
                self.poblacion, 
                self.aptitudes, 
                self.config.tamano_poblacion,
                metodo="torneo",
                tamano_torneo=self.config.tamano_torneo
            )
            
            # Cruce
            hijos = aplicar_cruce(
                padres, 
                self.config.probabilidad_cruce,
                metodo="un_punto"
            )
            
            # Mutación
            hijos_mutados = aplicar_mutacion(
                hijos,
                self.config.probabilidad_mutacion,
                metodo="intercambio",
                num_reactivos=len(self.reactivos)
            )
            
            # Evaluación de la nueva población
            aptitudes_hijos = evaluar_poblacion(hijos_mutados, self.reactivos, self.debilidades_objetivo)
            
            # Elitismo
            if self.config.elitismo:
                self.poblacion, self.aptitudes = self.aplicar_elitismo(hijos_mutados, aptitudes_hijos)
            else:
                self.poblacion = hijos_mutados
                self.aptitudes = aptitudes_hijos
            
            # Actualizar el mejor individuo
            self.evaluar_poblacion_actual()
            self.historial_aptitudes.append(self.mejor_aptitud)
        
        # Preparar resultados
        return AlgoritmoGeneticoOutput(
            mejor_individuo=self.mejor_individuo,
            aptitud=self.mejor_aptitud,
            generaciones=self.config.numero_generaciones,
            poblacion_final=self.poblacion,
            aptitudes_finales=self.aptitudes
        )

def ejecutar_algoritmo_genetico(reactivos: List[Reactivo], debilidades_objetivo: Debilidades, 
                               configuracion: ConfiguracionAlgoritmo = None) -> AlgoritmoGeneticoOutput:
    """
    Función de conveniencia para ejecutar el algoritmo genético.
    
    Args:
        reactivos: Lista de reactivos disponibles
        debilidades_objetivo: Debilidades que se quieren abordar
        configuracion: Configuración del algoritmo
    
    Returns:
        AlgoritmoGeneticoOutput: Resultados del algoritmo
    """
    algoritmo = AlgoritmoGenetico(reactivos, debilidades_objetivo, configuracion)
    return algoritmo.ejecutar()

