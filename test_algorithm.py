import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.schemas import Reactivo, Debilidades, ConfiguracionAlgoritmo
from app.core.genetic_algorithm import ejecutar_algoritmo_genetico

def test_algoritmo_genetico():
    """Prueba el algoritmo genético con datos de ejemplo."""
    
    print("=== Prueba del Algoritmo Genético ===\n")
    
    # Datos de ejemplo basados en el JSON proporcionado
    debilidades_objetivo = Debilidades(
        lectura=0.4,
        escritura=0.6,
        memoria=0.5
    )
    
    reactivos = [
        Reactivo(id_reactivo=1, lectura=0.2, escritura=0.3, memoria=0.5),
        Reactivo(id_reactivo=2, lectura=0.3, escritura=0.4, memoria=0.3),
        Reactivo(id_reactivo=3, lectura=0.2, escritura=0.3, memoria=0.5),
        Reactivo(id_reactivo=4, lectura=0.5, escritura=0.7, memoria=0.4),
        Reactivo(id_reactivo=5, lectura=0.4, escritura=0.5, memoria=0.6),
        Reactivo(id_reactivo=6, lectura=0.3, escritura=0.8, memoria=0.3),
        Reactivo(id_reactivo=7, lectura=0.6, escritura=0.4, memoria=0.7),
        Reactivo(id_reactivo=8, lectura=0.1, escritura=0.2, memoria=0.4),
    ]
    
    configuracion = ConfiguracionAlgoritmo(
        tamano_poblacion=20,
        numero_generaciones=50,
        probabilidad_cruce=0.8,
        probabilidad_mutacion=0.1,
        tamano_torneo=3,
        elitismo=True
    )
    
    print("Datos de entrada:")
    print(f"Debilidades objetivo: lectura={debilidades_objetivo.lectura}, "
          f"escritura={debilidades_objetivo.escritura}, memoria={debilidades_objetivo.memoria}")
    print(f"Número de reactivos disponibles: {len(reactivos)}")
    print(f"Configuración: población={configuracion.tamano_poblacion}, "
          f"generaciones={configuracion.numero_generaciones}")
    print()
    
    try:
        # Ejecutar el algoritmo genético
        print("Ejecutando algoritmo genético...")
        resultado = ejecutar_algoritmo_genetico(reactivos, debilidades_objetivo, configuracion)
        
        print("=== Resultados ===")
        print(f"Mejor individuo (índices de reactivos): {resultado.mejor_individuo}")
        print(f"Aptitud del mejor individuo: {resultado.aptitud:.4f}")
        print(f"Generaciones ejecutadas: {resultado.generaciones}")
        print()
        
        # Mostrar los reactivos seleccionados
        print("Reactivos seleccionados:")
        for i, indice in enumerate(resultado.mejor_individuo):
            if indice < len(reactivos):
                reactivo = reactivos[indice]
                print(f"  {i+1}. Reactivo {reactivo.id_reactivo}: "
                      f"lectura={reactivo.lectura}, escritura={reactivo.escritura}, memoria={reactivo.memoria}")
        
        # Calcular las características promedio de la solución
        if resultado.mejor_individuo:
            lectura_promedio = sum(reactivos[i].lectura for i in resultado.mejor_individuo if i < len(reactivos)) / len(resultado.mejor_individuo)
            escritura_promedio = sum(reactivos[i].escritura for i in resultado.mejor_individuo if i < len(reactivos)) / len(resultado.mejor_individuo)
            memoria_promedio = sum(reactivos[i].memoria for i in resultado.mejor_individuo if i < len(reactivos)) / len(resultado.mejor_individuo)
            
            print()
            print("Características promedio de la solución:")
            print(f"  Lectura: {lectura_promedio:.4f} (objetivo: {debilidades_objetivo.lectura})")
            print(f"  Escritura: {escritura_promedio:.4f} (objetivo: {debilidades_objetivo.escritura})")
            print(f"  Memoria: {memoria_promedio:.4f} (objetivo: {debilidades_objetivo.memoria})")
            
            print()
            print("Diferencias con el objetivo:")
            print(f"  Lectura: {abs(lectura_promedio - debilidades_objetivo.lectura):.4f}")
            print(f"  Escritura: {abs(escritura_promedio - debilidades_objetivo.escritura):.4f}")
            print(f"  Memoria: {abs(memoria_promedio - debilidades_objetivo.memoria):.4f}")
        
        print("\n✅ Prueba completada exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error durante la ejecución: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_algoritmo_genetico()
    sys.exit(0 if success else 1)