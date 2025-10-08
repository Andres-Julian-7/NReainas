from typing import List
import unittest
from unittest import mock

from application.use_cases.solve_nqueens import NQueensSolver, NQueensParams
import domain.services.ga_functions_adapter as ga


class ProgressCollector:
    def __init__(self):
        self.messages: List[str] = []

    def __call__(self, text: str):
        self.messages.append(text)


class TestNQueensSolver(unittest.TestCase):
    def setUp(self):
        self.solver = NQueensSolver()

    def test_inicializar_poblacion_uses_generar_individuo_and_reports_progress(self):
        calls = []

        def fake_generar_individuo(n):
            calls.append(n)
            return list(range(n))

        with mock.patch.object(ga, 'generar_individuo', side_effect=fake_generar_individuo):
            progress = ProgressCollector()
            poblacion = self.solver._inicializar_poblacion(3, 4, progress)

        # Debe llamar 3 veces y con num_reinas + 1
        self.assertEqual(calls, [5, 5, 5])
        # La población tiene 3 individuos y cada uno con longitud 5
        self.assertEqual(len(poblacion), 3)
        self.assertTrue(all(len(ind) == 5 for ind in poblacion))
        # Mensajes de progreso contienen el encabezado
        self.assertTrue(any('Inicializando población' in m for m in progress.messages))

    def test_aplicar_cruce_sin_cruce_devuelve_padres(self):
        with mock.patch.object(ga, 'generar_probabilidad', return_value=0.9):
            poblacion = [[10], [20], [30]]
            # ganadores en base 1 (coincide con lo que espera cruce original)
            ganadores = (1, 2)
            hijos = self.solver._aplicar_cruce(ganadores, poblacion, num_reinas=4, prob_cruce_configurada=0.5)
            self.assertEqual(hijos, [poblacion[0], poblacion[1]])

    def test_aplicar_cruce_con_cruce_llama_ga_cruce(self):
        with mock.patch.object(ga, 'generar_probabilidad', return_value=0.1):
            capturado = {}

            def fake_cruce(ganadores, poblacion, num_reinas):
                capturado['args'] = (tuple(ganadores), [list(p) for p in poblacion], num_reinas)
                return [[1, 2, 3], [3, 2, 1]]

            with mock.patch.object(ga, 'cruce', side_effect=fake_cruce):
                poblacion = [[0, 1, 2, 3, 4], [4, 3, 2, 1, 0]]
                ganadores = (1, 2)
                hijos = self.solver._aplicar_cruce(ganadores, poblacion, num_reinas=4, prob_cruce_configurada=0.5)

        self.assertEqual(hijos, [[1, 2, 3], [3, 2, 1]])
        self.assertEqual(capturado['args'], ((1, 2), poblacion, 4))

    def test_aplicar_mutacion_condicional(self):
        # Cuando la probabilidad <= configurada, se aplica mutación a cada hijo
        seq = iter([0.2, 0.8])

        with mock.patch.object(ga, 'generar_probabilidad', side_effect=lambda: next(seq)):
            mutated = []

            def fake_mutar(individuo, nr):
                mutated.append(list(individuo))
                return ['m']

            with mock.patch.object(ga, 'mutar_individuo', side_effect=fake_mutar):
                hijos = [[0], [1]]
                # primera llamada: 0.2 <= 0.5 => muta; segunda prueba: 0.8 > 0.5 => no muta
                hijos_mutados = self.solver._aplicar_mutacion([*hijos], num_reinas=4, prob_mutacion_configurada=0.5)
                self.assertEqual(hijos_mutados, [['m'], ['m']])

                # segunda ejecución con probabilidad > configurada no muta
                hijos_no_mutados = self.solver._aplicar_mutacion([*hijos], num_reinas=4, prob_mutacion_configurada=0.5)
                self.assertEqual(hijos_no_mutados, hijos)

    def test_actualizar_poblacion_invoca_seleccionar_con_torneo_por_cada_hijo(self):
        llamadas = []

        def fake_sel(hijo, poblacion, tamano_poblacion, num_reinas, fitness):
            llamadas.append((list(hijo), list(map(list, poblacion)), tamano_poblacion, num_reinas, list(fitness)))
            # Simular que insertamos el hijo al inicio para observar cambios
            nuevo = [list(hijo)] + [*poblacion][:-1]
            return nuevo

        with mock.patch.object(ga, 'seleccionar_con_torneo_agrupado', side_effect=fake_sel):
            poblacion = [[9], [8], [7]]
            hijos = [[1], [2]]
            fitness = [3, 2, 1]
            nueva = self.solver._actualizar_poblacion(poblacion, hijos, tamano_poblacion=3, num_reinas=4, fitness=fitness)

        # Debe haberse llamado dos veces (una por hijo)
        self.assertEqual(len(llamadas), 2)
        # La población resultante debe reflejar dos inserciones al inicio
        self.assertEqual(nueva, [[2], [1], [9]])

    def test_run_integration_with_deterministic_ga(self):
        solver = NQueensSolver()

        # Configuraciones
        params = NQueensParams(
            tamano_poblacion=3,
            num_reinas=4,
            num_generaciones=1,
            prob_cruce=0.5,
            prob_mutacion=0.5,
        )

        with mock.patch.object(ga, 'generar_individuo', side_effect=lambda n: list(range(n))), \
             mock.patch.object(ga, 'calcular_fitness', side_effect=lambda pobl, tam, nr: [2, 1, 0]), \
             mock.patch.object(ga, 'torneo', side_effect=lambda fitness, tam: (1, 2)), \
             mock.patch.object(ga, 'generar_probabilidad', side_effect=lambda: 0.1), \
             mock.patch.object(ga, 'cruce', side_effect=lambda gan, pob, nr: [[7, 7, 7, 7, 7], [8, 8, 8, 8, 8]]), \
             mock.patch.object(ga, 'mutar_individuo', side_effect=lambda hijo, nr: hijo), \
             mock.patch.object(ga, 'seleccionar_con_torneo_agrupado', side_effect=lambda hijo, pobl, tam, nr, fit: [*pobl[1:], list(hijo)]):

            progress = ProgressCollector()
            result = solver.run(params, progress)

        # Validar estructura del resultado
        self.assertEqual(len(result.poblacion_final), 3)
        self.assertEqual(len(result.fitness_final), 3)
        self.assertEqual(result.mejor_fitness, min(result.fitness_final))
        self.assertTrue(0 <= result.mejor_idx < 3)
        self.assertIsInstance(result.num_soluciones_optimas, int)
        self.assertIsInstance(result.tiempo_ejecucion, float)
        # Debe haber mostrado al menos algún mensaje de progreso significativo
        self.assertTrue(any('Generación' in m for m in progress.messages))


if __name__ == '__main__':
    unittest.main()
