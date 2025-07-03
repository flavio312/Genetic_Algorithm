from pydantic import BaseModel
from typing import List, Dict

class Debilidades(BaseModel):
    lectura: float
    escritura: float
    memoria: float

class Reactivo(BaseModel):
    id_reactivo: int
    lectura: float
    escritura: float
    memoria: float

class AlgoritmoGeneticoInput(BaseModel):
    debilidades: Debilidades
    reactivos: List[Reactivo]

class AlgoritmoGeneticoOutput(BaseModel):
    mejor_individuo: List[int]
    aptitud: float
    generaciones: int
    poblacion_final: List[List[int]]
    aptitudes_finales: List[float]

class ConfiguracionAlgoritmo(BaseModel):
    tamano_poblacion: int = 50
    numero_generaciones: int = 100
    probabilidad_cruce: float = 0.8
    probabilidad_mutacion: float = 0.1
    tamano_torneo: int = 3
    elitismo: bool = True

