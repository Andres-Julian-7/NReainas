from dataclasses import dataclass
from time import time
from typing import Callable, List, Tuple

# Domain services (wrapping existing implementation)
from domain.services import ga_functions_adapter as ga


@dataclass
class NQueensParams:
    tamano_poblacion: int
    num_reinas: int
    num_generaciones: int
    prob_cruce: float
    prob_mutacion: float


@dataclass
class NQueensResult:
    poblacion_final: List[List[int]]
    fitness_final: List[int]
    mejor_idx: int
    mejor_fitness: int
    num_soluciones_optimas: int
    tiempo_ejecucion: float


class NQueensSolver:
    def __init__(self):
        pass

    def _inicializar_poblacion(self, tamano_poblacion: int, num_reinas: int, progress: Callable[[str], None]) -> List[List[int]]:
        poblacion: List[List[int]] = []
        progress("Inicializando población...\n")
        for i in range(tamano_poblacion):
            individuo = ga.generar_individuo(num_reinas + 1)
            poblacion.append(individuo)
            if i < 10:
                progress(f"Individuo {i + 1}: {individuo}\n")
        if tamano_poblacion > 10:
            progress(f"... ({tamano_poblacion - 10} individuos más)\n\n")
        else:
            progress("\n")
        return poblacion

    def _aplicar_cruce(self, ganadores: Tuple[int, int], poblacion: List[List[int]], num_reinas: int, prob_cruce_configurada: float) -> List[List[int]]:
        prob_cruce = ga.generar_probabilidad()
        if prob_cruce > prob_cruce_configurada:
            padre1_idx = ganadores[0] - 1
            padre2_idx = ganadores[1] - 1
            return [poblacion[padre1_idx], poblacion[padre2_idx]]
        return ga.cruce(ganadores, poblacion, num_reinas)

    def _aplicar_mutacion(self, hijos: List[List[int]], num_reinas: int, prob_mutacion_configurada: float) -> List[List[int]]:
        prob_mutacion = ga.generar_probabilidad()
        if prob_mutacion <= prob_mutacion_configurada:
            for i in range(len(hijos)):
                hijos[i] = ga.mutar_individuo(hijos[i], num_reinas)
        return hijos

    def _actualizar_poblacion(self, poblacion: List[List[int]], hijos: List[List[int]], tamano_poblacion: int, num_reinas: int, fitness: List[int]) -> List[List[int]]:
        for hijo in hijos:
            poblacion = ga.seleccionar_con_torneo_agrupado(hijo, poblacion, tamano_poblacion, num_reinas, fitness)
        return poblacion

    def _encontrar_mejor(self, poblacion: List[List[int]], fitness: List[int], tamano_poblacion: int, progress: Callable[[str], None]) -> Tuple[int, int]:
        mejor_idx = 0
        resultados = "Población final:\n" + "=" * 50 + "\n"
        for i in range(tamano_poblacion):
            linea = f"Individuo {i + 1}: {poblacion[i]}, Fitness: {fitness[i]}\n"
            if i < 20:
                resultados += linea
            if fitness[mejor_idx] > fitness[i]:
                mejor_idx = i
        if tamano_poblacion > 20:
            resultados += f"... ({tamano_poblacion - 20} individuos más)\n"
        progress(resultados + "\n")
        return mejor_idx, fitness[mejor_idx]

    def run(self, params: NQueensParams, progress: Callable[[str], None] | None = None) -> NQueensResult:
        if progress is None:
            progress = lambda _: None

        tiempo_inicio = time()
        poblacion = self._inicializar_poblacion(params.tamano_poblacion, params.num_reinas, progress)

        num_soluciones_optimas = 0
        progress("Iniciando evolución...\n\n")

        for generacion in range(params.num_generaciones):
            if generacion % 100 == 0:
                progress(f"Generación {generacion + 1}/{params.num_generaciones}\n")

            fitness = ga.calcular_fitness(poblacion, params.tamano_poblacion, params.num_reinas)
            num_soluciones_optimas = fitness.count(0)

            ganadores = ga.torneo(fitness, params.tamano_poblacion)
            hijos = self._aplicar_cruce(ganadores, poblacion, params.num_reinas, params.prob_cruce)
            hijos = self._aplicar_mutacion(hijos, params.num_reinas, params.prob_mutacion)
            poblacion = self._actualizar_poblacion(poblacion, hijos, params.tamano_poblacion, params.num_reinas, fitness)

        tiempo_ejecucion = time() - tiempo_inicio

        progress("\n" + "=" * 50 + "\n")
        progress("Evaluación final...\n\n")

        fitness_final = ga.calcular_fitness(poblacion, params.tamano_poblacion, params.num_reinas)
        mejor_idx, mejor_fitness = self._encontrar_mejor(poblacion, fitness_final, params.tamano_poblacion, progress)

        return NQueensResult(
            poblacion_final=poblacion,
            fitness_final=fitness_final,
            mejor_idx=mejor_idx,
            mejor_fitness=mejor_fitness,
            num_soluciones_optimas=num_soluciones_optimas,
            tiempo_ejecucion=tiempo_ejecucion,
        )
