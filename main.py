import tkinter as tk
from tkinter import *  # Carga módulo tk (widgets estándar)
from tkinter import ttk  # Carga ttk (para widgets nuevos 8.5+)
from time import time
import Funciones


class Aplicacion():  # creacion de la ventana
    def __init__(self):
        self.raiz = Tk()
        self.raiz.geometry('300x220')
        self.raiz.configure(bg='beige')
        self.raiz.title('Aplicación')
        # ------------------------Label---------------------------
        self.mensajeNR = Label(self.raiz, text="Numero de reinas", fg="black")
        self.mensajeNR.pack()
        self.mensajePO = Label(self.raiz, text="Numero de Individuos", fg="black")
        self.mensajePO.pack()
        self.mensajeRE = Label(self.raiz, text="Numero de Repeticiones", fg="black")
        self.mensajeRE.pack()
        self.mensajePC = Label(self.raiz, text="Probabilidad de cruce", fg="black")
        self.mensajePC.pack()
        self.mensajePM = Label(self.raiz, text="Probabilidad de Mutacion", fg="black")
        self.mensajePM.pack()

        # ------------------------Cajas---------------------------
        self.caja_NR = ttk.Entry(self.raiz, justify=tk.LEFT)
        self.caja_PO = ttk.Entry(self.raiz, justify=tk.LEFT)
        self.caja_RE = ttk.Entry(self.raiz, justify=tk.LEFT)
        self.caja_PC = ttk.Entry(self.raiz, justify=tk.LEFT)
        self.caja_PM = ttk.Entry(self.raiz, justify=tk.LEFT)
        # ------------------------Botones---------------------------
        self.botonSA = ttk.Button(self.raiz, text='Salir', command=self.raiz.destroy).pack(side=BOTTOM)
        self.botonIn = ttk.Button(self.raiz, text="Iniciar", command=self.algoritmo).pack(side=BOTTOM)
        # ------------------------Posicion---------------------------
        self.mensajeNR.place(x=10, y=5)
        self.caja_NR.place(x=10, y=25)
        self.mensajePO.place(x=150, y=5)
        self.caja_PO.place(x=150, y=25)
        self.mensajeRE.place(x=5, y=50)
        self.caja_RE.place(x=10, y=70)
        self.mensajePC.place(x=150, y=50)
        self.caja_PC.place(x=150, y=70)
        self.mensajePM.place(x=10, y=100)
        self.caja_PM.place(x=160, y=100)
        # ------------------------Valores estaticos------------------
        self.caja_NR.insert(0, 8)
        self.caja_PO.insert(0, 1000)
        self.caja_RE.insert(0, 1000)
        self.caja_PC.insert(0, 0.85)
        self.caja_PM.insert(0, 0.1)
        self.caja_PM.config(state=tk.DISABLED)
        self.caja_PC.config(state=tk.DISABLED)

        self.raiz.mainloop()

    def _inicializar_poblacion(self, tamano_poblacion, num_reinas):
        """
        Crea la población inicial de individuos aleatorios.

        Args:
            tamano_poblacion: Número de individuos en la población
            num_reinas: Número de reinas (tamaño del problema)

        Returns:
            Lista con la población inicial
        """
        poblacion = []
        for i in range(tamano_poblacion):
            individuo = Funciones.generar_individuo(num_reinas + 1)
            poblacion.append(individuo)
            print(f"Individuo {i + 1}: {individuo}")
        return poblacion

    def _aplicar_cruce(self, ganadores, poblacion, num_reinas, prob_cruce_configurada):
        """
        Aplica el operador de cruce entre los padres ganadores.

        Args:
            ganadores: Índices de los padres seleccionados
            poblacion: Población actual
            num_reinas: Número de reinas
            prob_cruce_configurada: Probabilidad de cruce configurada

        Returns:
            Lista con los hijos generados
        """
        prob_cruce = Funciones.generar_probabilidad()

        if prob_cruce > prob_cruce_configurada:
            # No se aplica cruce: hijos son copias de los padres
            hijos = []
            padre1_idx = ganadores[0] - 1
            padre2_idx = ganadores[1] - 1
            hijos.append(poblacion[padre1_idx])
            hijos.append(poblacion[padre2_idx])
        else:
            # Se aplica cruce
            hijos = Funciones.cruce(ganadores, poblacion, num_reinas)

        return hijos

    def _aplicar_mutacion(self, hijos, num_reinas, prob_mutacion_configurada):
        """
        Aplica el operador de mutación a los hijos.

        Args:
            hijos: Lista de hijos a mutar
            num_reinas: Número de reinas
            prob_mutacion_configurada: Probabilidad de mutación configurada

        Returns:
            Lista con los hijos mutados
        """
        prob_mutacion = Funciones.generar_probabilidad()

        if prob_mutacion <= prob_mutacion_configurada:
            for i in range(len(hijos)):
                hijos[i] = Funciones.mutar_individuo(hijos[i], num_reinas)

        return hijos

    def _actualizar_poblacion(self, poblacion, hijos, tamano_poblacion, num_reinas, fitness):
        """
        Actualiza la población insertando los nuevos hijos.

        Args:
            poblacion: Población actual
            hijos: Nuevos individuos a insertar
            tamano_poblacion: Tamaño de la población
            num_reinas: Número de reinas
            fitness: Fitness actual de la población

        Returns:
            Población actualizada
        """
        for hijo in hijos:
            poblacion = Funciones.seleccionar_con_torneo_agrupado(
                hijo, poblacion, tamano_poblacion, num_reinas, fitness
            )
        return poblacion

    def _encontrar_mejor_individuo(self, poblacion, fitness, tamano_poblacion):
        """
        Encuentra el mejor individuo de la población.

        Args:
            poblacion: Población actual
            fitness: Fitness de cada individuo
            tamano_poblacion: Tamaño de la población

        Returns:
            Tupla (índice del mejor, fitness del mejor)
        """
        mejor_idx = 0
        for i in range(tamano_poblacion):
            print(f"Individuo {i + 1}: {poblacion[i]}, Fitness: {fitness[i]}")
            if fitness[mejor_idx] > fitness[i]:
                mejor_idx = i

        return mejor_idx, fitness[mejor_idx]

    def _guardar_resultados(self, poblacion, fitness, tamano_poblacion):
        """
        Guarda los mejores resultados en un archivo.

        Args:
            poblacion: Población final
            fitness: Fitness de cada individuo
            tamano_poblacion: Tamaño de la población
        """
        with open('Ganadores.txt', 'a') as archivo:
            for i in range(tamano_poblacion):
                if fitness[i] == 0:
                    linea = f"Individuo {i + 1}: {poblacion[i]}, Fitness: {fitness[i]}\n"
                    archivo.write(linea)
            archivo.write('\n')

    def _mostrar_resultados(self, tiempo_ejecucion, mejor_individuo, mejor_fitness, num_soluciones_optimas):
        """
        Muestra los resultados en consola y en la interfaz gráfica.

        Args:
            tiempo_ejecucion: Tiempo de ejecución del algoritmo
            mejor_individuo: Mejor individuo encontrado
            mejor_fitness: Fitness del mejor individuo
            num_soluciones_optimas: Número de soluciones con fitness 0
        """
        print("-------------------------Fin-----------------------------------")
        print(f"Lapso de tiempo: {tiempo_ejecucion:.10f} segundos.")
        print(f"Número de individuos con fitness 0: {num_soluciones_optimas}")
        print(f"Ganador: {mejor_individuo}, Fitness: {mejor_fitness}, Autor Andres707")

        texto_ganador = f"Ganador: {mejor_individuo}, Fitness: {mejor_fitness}"

        self.mensajeLT = Label(
            self.raiz,
            text=f"Lapso de tiempo: {tiempo_ejecucion:.10f} segundos.",
            fg="black"
        )
        self.mensajeLT.pack()
        self.mensajeG = Label(self.raiz, text=texto_ganador, fg="black")
        self.mensajeG.pack()
        self.mensajeLT.place(x=10, y=125)
        self.mensajeG.place(x=10, y=150)

    def algoritmo(self):
        """
        Ejecuta el algoritmo genético para resolver el problema de las N-Reinas.
        """
        # Obtener parámetros de configuración
        tamano_poblacion = int(self.caja_PO.get())
        num_reinas = int(self.caja_NR.get())
        num_generaciones = int(self.caja_RE.get())
        prob_cruce = float(self.caja_PC.get())
        prob_mutacion = float(self.caja_PM.get())

        # Inicializar población
        tiempo_inicio = time()
        poblacion = self._inicializar_poblacion(tamano_poblacion, num_reinas)

        # Evolución de la población
        num_soluciones_optimas = 0
        for generacion in range(num_generaciones):
            print(f"Repeticion {generacion + 1}")

            # Evaluar fitness
            fitness = Funciones.calcular_fitness(poblacion, tamano_poblacion, num_reinas)
            num_soluciones_optimas = fitness.count(0)

            # Selección por torneo
            ganadores = Funciones.torneo(fitness, tamano_poblacion)

            # Cruce
            hijos = self._aplicar_cruce(ganadores, poblacion, num_reinas, prob_cruce)

            # Mutación
            hijos = self._aplicar_mutacion(hijos, num_reinas, prob_mutacion)

            # Actualizar población
            poblacion = self._actualizar_poblacion(
                poblacion, hijos, tamano_poblacion, num_reinas, fitness
            )

        # Calcular tiempo de ejecución
        tiempo_ejecucion = time() - tiempo_inicio

        # Evaluación final
        fitness_final = Funciones.calcular_fitness(poblacion, tamano_poblacion, num_reinas)
        mejor_idx, mejor_fitness = self._encontrar_mejor_individuo(
            poblacion, fitness_final, tamano_poblacion
        )

        # Guardar y mostrar resultados
        self._guardar_resultados(poblacion, fitness_final, tamano_poblacion)
        self._mostrar_resultados(
            tiempo_ejecucion,
            poblacion[mejor_idx],
            mejor_fitness,
            num_soluciones_optimas
        )

        return 0


def main():
    mi_app = Aplicacion()
    return 0


if __name__ == '__main__':
    main()