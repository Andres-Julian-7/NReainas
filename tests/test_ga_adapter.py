import unittest
from unittest import mock

import Funciones
from domain.services import ga_functions_adapter as ga


class TestGaFunctionsAdapter(unittest.TestCase):
    def test_generar_individuo_delegation(self):
        with mock.patch.object(Funciones, 'generar_individuo', return_value=['ok']) as m:
            res = ga.generar_individuo(5)
        self.assertEqual(res, ['ok'])
        m.assert_called_once_with(5)

    def test_calcular_fitness_delegation(self):
        with mock.patch.object(Funciones, 'calcular_fitness', return_value=[1, 2, 3]) as m:
            pobl = [[0], [1], [2]]
            res = ga.calcular_fitness(pobl, 3, 4)
        self.assertEqual(res, [1, 2, 3])
        m.assert_called_once_with(pobl, 3, 4)

    def test_torneo_delegation(self):
        with mock.patch.object(Funciones, 'torneo', return_value=(1, 2)) as m:
            res = ga.torneo([3, 2, 1], 3)
        self.assertEqual(res, (1, 2))
        m.assert_called_once_with([3, 2, 1], 3)

    def test_cruce_delegation(self):
        with mock.patch.object(Funciones, 'cruce', return_value=[[1], [2]]) as m:
            res = ga.cruce((1, 2), [[0], [1]], 4)
        self.assertEqual(res, [[1], [2]])
        m.assert_called_once_with((1, 2), [[0], [1]], 4)

    def test_mutar_individuo_delegation(self):
        with mock.patch.object(Funciones, 'mutar_individuo', return_value=[9]) as m:
            res = ga.mutar_individuo([0], 4)
        self.assertEqual(res, [9])
        m.assert_called_once_with([0], 4)

    def test_generar_probabilidad_delegation(self):
        with mock.patch.object(Funciones, 'generar_probabilidad', return_value=0.42) as m:
            res = ga.generar_probabilidad()
        self.assertEqual(res, 0.42)
        m.assert_called_once_with()

    def test_seleccionar_con_torneo_agrupado_delegation(self):
        with mock.patch.object(Funciones, 'seleccionar_con_torneo_agrupado', return_value=[[1]]) as m:
            res = ga.seleccionar_con_torneo_agrupado([0], [[2]], 1, 4, [5])
        self.assertEqual(res, [[1]])
        m.assert_called_once_with([0], [[2]], 1, 4, [5])


if __name__ == '__main__':
    unittest.main()
    # python - m unittest discover - s tests - p 'test_*.py'