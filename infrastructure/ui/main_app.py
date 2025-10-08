import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import Callable

from application.use_cases.solve_nqueens import NQueensParams, NQueensResult, NQueensSolver


class Aplicacion:
    def __init__(self):
        self.raiz = tk.Tk()
        self.raiz.title('Algoritmo Genético - N-Reinas')
        self.raiz.geometry('800x500')
        self.raiz.minsize(600, 500)
        self.raiz.configure(bg='#f0f0f0')

        # Variable para almacenar resultados
        self.resultados_texto = ""

        # Use case
        self.solver = NQueensSolver()

        # Crear la interfaz
        self._crear_interfaz()

        self.raiz.mainloop()

    # UI building
    def _crear_interfaz(self):
        main_frame = ttk.Frame(self.raiz, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.raiz.columnconfigure(0, weight=1)
        self.raiz.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        self._crear_seccion_parametros(main_frame)
        self._crear_seccion_control(main_frame)
        self._crear_seccion_resultados(main_frame)
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        self.progress.grid_remove()

    def _crear_seccion_parametros(self, parent):
        frame_params = ttk.LabelFrame(parent, text="Parámetros del Algoritmo", padding="10")
        frame_params.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N), pady=5)
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
        frame_control = ttk.Frame(parent, padding="5")
        frame_control.grid(row=1, column=0, columnspan=2, pady=10)
        self.boton_iniciar = ttk.Button(frame_control, text="Iniciar Algoritmo", command=self._ejecutar_algoritmo, width=20)
        self.boton_iniciar.grid(row=0, column=0, padx=5)
        self.boton_copiar = ttk.Button(frame_control, text="Copiar Resultados", command=self._copiar_resultados, width=20, state='disabled')
        self.boton_copiar.grid(row=0, column=1, padx=5)
        self.boton_salir = ttk.Button(frame_control, text="Salir", command=self.raiz.destroy, width=20)
        self.boton_salir.grid(row=0, column=2, padx=5)

    def _crear_seccion_resultados(self, parent):
        frame_resultados = ttk.LabelFrame(parent, text="Resultados", padding="10")
        frame_resultados.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        parent.rowconfigure(2, weight=1)
        frame_resultados.columnconfigure(0, weight=1)
        frame_resultados.rowconfigure(0, weight=1)
        self.texto_resultados = scrolledtext.ScrolledText(frame_resultados, wrap=tk.WORD, width=70, height=15, font=('Courier', 9), bg='#ffffff', fg='#000000')
        self.texto_resultados.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.texto_resultados.insert('1.0', 'Presione "Iniciar Algoritmo" para comenzar...')
        self.texto_resultados.config(state='disabled')

    # UI helpers
    def _actualizar_resultados(self, texto: str):
        self.texto_resultados.config(state='normal')
        self.texto_resultados.insert(tk.END, texto)
        self.texto_resultados.see(tk.END)
        self.texto_resultados.config(state='disabled')
        self.raiz.update()

    def _copiar_resultados(self):
        self.raiz.clipboard_clear()
        self.raiz.clipboard_append(self.resultados_texto)
        messagebox.showinfo("Éxito", "Resultados copiados al portapapeles")

    # Run algorithm via use case
    def _ejecutar_algoritmo(self):
        self.boton_iniciar.config(state='disabled')
        self.boton_copiar.config(state='disabled')
        self.progress.grid()
        self.progress.start(10)
        self.texto_resultados.config(state='normal')
        self.texto_resultados.delete('1.0', tk.END)
        self.texto_resultados.insert('1.0', 'Ejecutando algoritmo genético...\n\n')
        self.texto_resultados.config(state='disabled')
        self.raiz.update()
        try:
            params = NQueensParams(
                tamano_poblacion=int(self.caja_po.get()),
                num_reinas=int(self.caja_nr.get()),
                num_generaciones=int(self.caja_re.get()),
                prob_cruce=float(self.caja_pc.get()),
                prob_mutacion=float(self.caja_pm.get()),
            )

            def progress_cb(text: str):
                self._actualizar_resultados(text)

            result = self.solver.run(params, progress_cb)
            self._post_procesar_resultado(result)
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la ejecución: {str(e)}")
        finally:
            self.progress.stop()
            self.progress.grid_remove()
            self.boton_iniciar.config(state='normal')
            self.boton_copiar.config(state='normal')

    def _post_procesar_resultado(self, result: NQueensResult):
        # Guardar soluciones óptimas
        with open('Ganadores.txt', 'a') as archivo:
            for i, fit in enumerate(result.fitness_final):
                if fit == 0:
                    linea = f"Individuo {i + 1}: {result.poblacion_final[i]}, Fitness: {fit}\n"
                    archivo.write(linea)
            archivo.write('\n')

        # Mostrar resultados resumen y preparar texto para copiar
        resumen = (
            f"{'='*50}\n"
            f"RESULTADOS FINALES\n"
            f"{'='*50}\n"
            f"Tiempo de ejecución: {result.tiempo_ejecucion:.6f} segundos\n"
            f"Soluciones óptimas (fitness=0): {result.num_soluciones_optimas}\n"
            f"Mejor individuo: {result.poblacion_final[result.mejor_idx]}\n"
            f"Fitness del mejor: {result.mejor_fitness}\n"
            f"{'='*50}\n"
        )
        self.resultados_texto = resumen
        self._actualizar_resultados(resumen)


def main():
    Aplicacion()
