import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from time import time
import Funciones


class Aplicacion():
    def __init__(self):
        self.raiz = tk.Tk()
        self.raiz.title('Algoritmo Genético - N-Reinas')
        self.raiz.geometry('800x500')
        self.raiz.minsize(600, 500)
        self.raiz.configure(bg='#f0f0f0')

        # Variable para almacenar resultados
        self.resultados_texto = ""

        # Crear la interfaz
        self._crear_interfaz()

        self.raiz.mainloop()

    def _crear_interfaz(self):
        """Crea todos los componentes de la interfaz gráfica."""
        # Frame principal con padding
        main_frame = ttk.Frame(self.raiz, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar peso de filas y columnas para redimensionamiento
        self.raiz.columnconfigure(0, weight=1)
        self.raiz.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Sección de Parámetros
        self._crear_seccion_parametros(main_frame)

        # Sección de Control
        self._crear_seccion_control(main_frame)

        # Sección de Resultados
        self._crear_seccion_resultados(main_frame)

        # Barra de progreso
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        self.progress.grid_remove()  # Ocultar inicialmente

    def _crear_seccion_parametros(self, parent):
        """Crea la sección de parámetros de configuración."""
        frame_params = ttk.LabelFrame(parent, text="Parámetros del Algoritmo", padding="10")
        frame_params.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N), pady=5)

        # Columna izquierda
        ttk.Label(frame_params, text="Número de Reinas:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.caja_nr = ttk.Entry(frame_params, width=15)
        self.caja_nr.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.caja_nr.insert(0, "8")

        ttk.Label(frame_params, text="Número de Individuos:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.caja_po = ttk.Entry(frame_params, width=15)
        self.caja_po.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.caja_po.insert(0, "1000")

        ttk.Label(frame_params, text="Número de Generaciones:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.caja_re = ttk.Entry(frame_params, width=15)
        self.caja_re.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        self.caja_re.insert(0, "1000")

        # Columna derecha
        ttk.Label(frame_params, text="Probabilidad de Cruce:").grid(row=0, column=2, sticky=tk.W, padx=(20, 0), pady=5)
        self.caja_pc = ttk.Entry(frame_params, width=15)
        self.caja_pc.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        self.caja_pc.insert(0, "0.85")

        ttk.Label(frame_params, text="Probabilidad de Mutación:").grid(row=1, column=2, sticky=tk.W, padx=(20, 0), pady=5)
        self.caja_pm = ttk.Entry(frame_params, width=15)
        self.caja_pm.grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)
        self.caja_pm.insert(0, "0.1")

        self.caja_pm.config(state=tk.DISABLED)
        self.caja_pc.config(state=tk.DISABLED)

    def _crear_seccion_control(self, parent):
        """Crea la sección de botones de control."""
        frame_control = ttk.Frame(parent, padding="5")
        frame_control.grid(row=1, column=0, columnspan=2, pady=10)

        self.boton_iniciar = ttk.Button(
            frame_control,
            text="Iniciar Algoritmo",
            command=self._ejecutar_algoritmo,
            width=20
        )
        self.boton_iniciar.grid(row=0, column=0, padx=5)

        self.boton_copiar = ttk.Button(
            frame_control,
            text="Copiar Resultados",
            command=self._copiar_resultados,
            width=20,
            state='disabled'
        )
        self.boton_copiar.grid(row=0, column=1, padx=5)

        self.boton_salir = ttk.Button(
            frame_control,
            text="Salir",
            command=self.raiz.destroy,
            width=20
        )
        self.boton_salir.grid(row=0, column=2, padx=5)

    def _crear_seccion_resultados(self, parent):
        """Crea la sección de visualización de resultados."""
        frame_resultados = ttk.LabelFrame(parent, text="Resultados", padding="10")
        frame_resultados.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        # Configurar expansión
        parent.rowconfigure(2, weight=1)
        frame_resultados.columnconfigure(0, weight=1)
        frame_resultados.rowconfigure(0, weight=1)

        # Área de texto con scroll
        self.texto_resultados = scrolledtext.ScrolledText(
            frame_resultados,
            wrap=tk.WORD,
            width=70,
            height=15,
            font=('Courier', 9),
            bg='#ffffff',
            fg='#000000'
        )
        self.texto_resultados.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.texto_resultados.insert('1.0', 'Presione "Iniciar Algoritmo" para comenzar...')
        self.texto_resultados.config(state='disabled')

    def _ejecutar_algoritmo(self):
        """Wrapper para ejecutar el algoritmo en el hilo principal con feedback visual."""
        # Deshabilitar botones durante ejecución
        self.boton_iniciar.config(state='disabled')
        self.boton_copiar.config(state='disabled')

        # Mostrar barra de progreso
        self.progress.grid()
        self.progress.start(10)

        # Limpiar resultados anteriores
        self.texto_resultados.config(state='normal')
        self.texto_resultados.delete('1.0', tk.END)
        self.texto_resultados.insert('1.0', 'Ejecutando algoritmo genético...\n\n')
        self.texto_resultados.config(state='disabled')

        # Actualizar interfaz
        self.raiz.update()

        # Ejecutar algoritmo
        try:
            self.algoritmo()
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la ejecución: {str(e)}")

        # Ocultar barra de progreso
        self.progress.stop()
        self.progress.grid_remove()

        # Habilitar botones
        self.boton_iniciar.config(state='normal')
        self.boton_copiar.config(state='normal')

    def _copiar_resultados(self):
        """Copia los resultados al portapapeles."""
        self.raiz.clipboard_clear()
        self.raiz.clipboard_append(self.resultados_texto)
        messagebox.showinfo("Éxito", "Resultados copiados al portapapeles")

    def _actualizar_resultados(self, texto):
        """Actualiza el área de resultados con nuevo texto."""
        self.texto_resultados.config(state='normal')
        self.texto_resultados.insert(tk.END, texto)
        self.texto_resultados.see(tk.END)  # Scroll automático al final
        self.texto_resultados.config(state='disabled')
        self.raiz.update()

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
        self._actualizar_resultados("Inicializando población...\n")
        for i in range(tamano_poblacion):
            individuo = Funciones.generar_individuo(num_reinas + 1)
            poblacion.append(individuo)
            if i < 10:  # Mostrar solo los primeros 10
                self._actualizar_resultados(f"Individuo {i + 1}: {individuo}\n")
        if tamano_poblacion > 10:
            self._actualizar_resultados(f"... ({tamano_poblacion - 10} individuos más)\n")
        self._actualizar_resultados("\n")
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
        resultados = "Población final:\n" + "="*50 + "\n"

        for i in range(tamano_poblacion):
            linea = f"Individuo {i + 1}: {poblacion[i]}, Fitness: {fitness[i]}\n"
            print(linea.strip())
            if i < 20:  # Mostrar solo los primeros 20 en interfaz
                resultados += linea
            if fitness[mejor_idx] > fitness[i]:
                mejor_idx = i

        if tamano_poblacion > 20:
            resultados += f"... ({tamano_poblacion - 20} individuos más)\n"

        self._actualizar_resultados(resultados + "\n")
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
        print("="*60)
        print("RESULTADOS FINALES")
        print("="*60)
        print(f"Tiempo de ejecución: {tiempo_ejecucion:.6f} segundos")
        print(f"Soluciones óptimas encontradas (fitness=0): {num_soluciones_optimas}")
        print(f"Mejor individuo: {mejor_individuo}")
        print(f"Fitness del mejor: {mejor_fitness}")
        print("="*60)

        # Formatear resultados para la interfaz y portapapeles
        self.resultados_texto = (
            f"{'='*50}\n"
            f"RESULTADOS FINALES\n"
            f"{'='*50}\n"
            f"Tiempo de ejecución: {tiempo_ejecucion:.6f} segundos\n"
            f"Soluciones óptimas (fitness=0): {num_soluciones_optimas}\n"
            f"Mejor individuo: {mejor_individuo}\n"
            f"Fitness del mejor: {mejor_fitness}\n"
            f"{'='*50}\n"
        )

        self._actualizar_resultados(self.resultados_texto)

    def algoritmo(self):
        """
        Ejecuta el algoritmo genético para resolver el problema de las N-Reinas.
        """
        # Obtener parámetros de configuración
        tamano_poblacion = int(self.caja_po.get())
        num_reinas = int(self.caja_nr.get())
        num_generaciones = int(self.caja_re.get())
        prob_cruce = float(self.caja_pc.get())
        prob_mutacion = float(self.caja_pm.get())

        # Inicializar población
        tiempo_inicio = time()
        poblacion = self._inicializar_poblacion(tamano_poblacion, num_reinas)

        # Evolución de la población
        num_soluciones_optimas = 0
        self._actualizar_resultados("Iniciando evolución...\n\n")

        for generacion in range(num_generaciones):
            if generacion % 100 == 0:
                self._actualizar_resultados(f"Generación {generacion + 1}/{num_generaciones}\n")

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
        self._actualizar_resultados("\n" + "="*50 + "\n")
        self._actualizar_resultados("Evaluación final...\n\n")
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