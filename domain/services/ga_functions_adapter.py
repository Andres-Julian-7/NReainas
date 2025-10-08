# Domain services adapter for genetic algorithm operations
# This module wraps the existing Funciones.py to provide a stable, importable
# interface from the domain layer without coupling upper layers to infrastructure.

from typing import List, Tuple
import Funciones  # Reuse existing implementation to minimize changes


def generar_individuo(tamano: int) -> List[int]:
    return Funciones.generar_individuo(tamano)


def calcular_fitness(poblacion: List[List[int]], tamano_poblacion: int, num_reinas: int) -> List[int]:
    return Funciones.calcular_fitness(poblacion, tamano_poblacion, num_reinas)


def torneo(fitness: List[int], tamano_poblacion: int) -> Tuple[int, int]:
    return Funciones.torneo(fitness, tamano_poblacion)


def cruce(ganadores: Tuple[int, int], poblacion: List[List[int]], num_reinas: int) -> List[List[int]]:
    return Funciones.cruce(ganadores, poblacion, num_reinas)


def mutar_individuo(individuo: List[int], num_reinas: int) -> List[int]:
    return Funciones.mutar_individuo(individuo, num_reinas)


def generar_probabilidad() -> float:
    return Funciones.generar_probabilidad()


def seleccionar_con_torneo_agrupado(hijo: List[int], poblacion: List[List[int]], tamano_poblacion: int, num_reinas: int, fitness: List[int]) -> List[List[int]]:
    return Funciones.seleccionar_con_torneo_agrupado(hijo, poblacion, tamano_poblacion, num_reinas, fitness)
