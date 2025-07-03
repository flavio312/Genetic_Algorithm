from fastapi import APIRouter, HTTPException
from typing import Optional
from app.models.schemas import (
    AlgoritmoGeneticoInput, 
    AlgoritmoGeneticoOutput, 
    ConfiguracionAlgoritmo
)
from app.core.genetic_algorithm import ejecutar_algoritmo_genetico

router = APIRouter()

@router.post("/ejecutar", response_model=AlgoritmoGeneticoOutput)
async def ejecutar_algoritmo(request: AlgoritmoGeneticoInput):
    """
    Ejecuta el algoritmo genético con los datos proporcionados.
    
    Args:
        request: Datos de entrada que incluyen debilidades y reactivos
    
    Returns:
        AlgoritmoGeneticoOutput: Resultados del algoritmo genético
    """
    try:
        # Validar que hay reactivos disponibles
        if not request.reactivos:
            raise HTTPException(
                status_code=400, 
                detail="Debe proporcionar al menos un reactivo"
            )
        
        # Validar que las debilidades están en el rango válido [0, 1]
        debilidades = request.debilidades
        if not (0 <= debilidades.lectura <= 1 and 
                0 <= debilidades.escritura <= 1 and 
                0 <= debilidades.memoria <= 1):
            raise HTTPException(
                status_code=400,
                detail="Las debilidades deben estar en el rango [0, 1]"
            )
        
        # Validar que los reactivos tienen valores válidos
        for i, reactivo in enumerate(request.reactivos):
            if not (0 <= reactivo.lectura <= 1 and 
                    0 <= reactivo.escritura <= 1 and 
                    0 <= reactivo.memoria <= 1):
                raise HTTPException(
                    status_code=400,
                    detail=f"El reactivo {reactivo.id_reactivo} tiene valores fuera del rango [0, 1]"
                )
        
        # Usar configuración por defecto
        configuracion = ConfiguracionAlgoritmo()
        
        # Ejecutar el algoritmo genético
        resultado = ejecutar_algoritmo_genetico(
            request.reactivos, 
            request.debilidades, 
            configuracion
        )
        
        return resultado
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.get("/configuracion-defecto", response_model=ConfiguracionAlgoritmo)
async def obtener_configuracion_defecto():
    """
    Obtiene la configuración por defecto del algoritmo genético.
    
    Returns:
        ConfiguracionAlgoritmo: Configuración por defecto
    """
    return ConfiguracionAlgoritmo()

@router.post("/validar-datos")
async def validar_datos(datos: AlgoritmoGeneticoInput):
    """
    Valida los datos de entrada sin ejecutar el algoritmo.
    
    Args:
        datos: Datos de entrada que incluyen debilidades y reactivos
    
    Returns:
        dict: Resultado de la validación
    """
    try:
        # Validaciones básicas
        if not datos.reactivos:
            return {
                "valido": False,
                "mensaje": "Debe proporcionar al menos un reactivo"
            }
        
        # Validar debilidades
        debilidades = datos.debilidades
        if not (0 <= debilidades.lectura <= 1 and 
                0 <= debilidades.escritura <= 1 and 
                0 <= debilidades.memoria <= 1):
            return {
                "valido": False,
                "mensaje": "Las debilidades deben estar en el rango [0, 1]"
            }
        
        # Validar reactivos
        for reactivo in datos.reactivos:
            if not (0 <= reactivo.lectura <= 1 and 
                    0 <= reactivo.escritura <= 1 and 
                    0 <= reactivo.memoria <= 1):
                return {
                    "valido": False,
                    "mensaje": f"El reactivo {reactivo.id_reactivo} tiene valores fuera del rango [0, 1]"
                }
        
        return {
            "valido": True,
            "mensaje": "Datos válidos",
            "num_reactivos": len(datos.reactivos)
        }
        
    except Exception as e:
        return {
            "valido": False,
            "mensaje": f"Error en la validación: {str(e)}"
        }