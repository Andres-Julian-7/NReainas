import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import Callable
import turtle as t
import math

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

    # Dibujo con turtle (adaptado del ejemplo proporcionado)
    def _dibujar_reina_turtle(self, pen: t.Turtle, x: float, y: float, tamano: int, color_reina: str = "#98FF98"):
        pen.penup()
        pen.goto(x + tamano // 2, y + tamano // 2 - tamano // 4)
        pen.pencolor(color_reina)
        pen.pendown()
        pen.write("♛", align="center", font=("Arial", int(tamano * 0.7), "bold"))
        pen.penup()

    def _tablero_ajedrez_con_reinas_turtle(self, posiciones_reinas, tamano_casilla: int = 60, con_coordenadas: bool = True, estilo: str = "clasico"):
        try:
            n = len(posiciones_reinas)
            if n == 0:
                return
            # Configurar pantalla y turtle
            screen = t.Screen()
            screen.title(f"Problema de las {n} Reinas")
            screen.bgcolor("black")
            screen.tracer(False)
            pen = t.Turtle(visible=False)
            pen.speed(0)
            pen.penup()

            # Estilos
            if estilo == "clasico":
                color_claro = "#F0D9B5"
                color_oscuro = "#B58863"
                color_borde = "#8B4513"
                color_texto = "white"
                color_reina = "#0047AB"
            elif estilo == "madera":
                color_claro = "#DEB887"
                color_oscuro = "#8B4513"
                color_borde = "#654321"
                color_texto = "white"
                color_reina = "#FFD700"
            elif estilo == "neon":
                color_claro = "#00FFFF"
                color_oscuro = "#FF00FF"
                color_borde = "#FFD700"
                color_texto = "#FFD700"
                color_reina = "#00FF00"
            else:
                color_claro = "white"
                color_oscuro = "black"
                color_borde = "gray"
                color_texto = "white"
                color_reina = "#FFD700"

            tablero_px = tamano_casilla * n
            inicio_x = -tablero_px / 2
            inicio_y = -tablero_px / 2

            # Borde
            pen.goto(inicio_x - 10, inicio_y - 10)
            pen.pendown()
            pen.pencolor(color_borde)
            pen.pensize(5)
            pen.fillcolor(color_borde)
            pen.begin_fill()
            for _ in range(4):
                pen.forward(tablero_px + 20)
                pen.left(90)
            pen.end_fill()
            pen.penup()

            # Casillas
            for fila in range(n):
                for columna in range(n):
                    color_casilla = color_claro if (fila + columna) % 2 == 0 else color_oscuro
                    x = inicio_x + (columna * tamano_casilla)
                    y = inicio_y + (fila * tamano_casilla)
                    pen.goto(x, y)
                    pen.pendown()
                    pen.fillcolor(color_casilla)
                    pen.setheading(0)
                    pen.begin_fill()
                    for _ in range(4):
                        pen.forward(tamano_casilla)
                        pen.left(90)
                    pen.end_fill()
                    pen.penup()

            # Reinas
            for columna, fila in enumerate(posiciones_reinas):
                if 0 <= fila < n:
                    x = inicio_x + (columna * tamano_casilla)
                    y = inicio_y + (fila * tamano_casilla)
                    # Centro de la casilla de la reina
                    cx = x + tamano_casilla / 2
                    cy = y + tamano_casilla / 2
                    # Dibujar la reina
                    self._dibujar_reina_turtle(pen, x, y, tamano_casilla, color_reina)

                    # Líneas rojas punteadas (filas, columnas y diagonales)
                    min_x, max_x = inicio_x, inicio_x + tablero_px
                    min_y, max_y = inicio_y, inicio_y + tablero_px

                    def _linea_punteada_desde(cx_, cy_, dx_, dy_, largo=8, espacio=6):
                        # dx_,dy_ pueden ser cualquier escala; se normalizan
                        d = math.hypot(dx_, dy_)
                        if d == 0:
                            return
                        ux, uy = dx_ / d, dy_ / d
                        px, py = cx_, cy_
                        pen.pencolor("#FF3333")
                        pen.pensize(2)
                        while (min_x <= px <= max_x) and (min_y <= py <= max_y):
                            nx, ny = px + ux * largo, py + uy * largo
                            # Si el siguiente punto se sale del tablero, detenemos
                            if not (min_x <= nx <= max_x and min_y <= ny <= max_y):
                                break
                            pen.penup()
                            pen.goto(px, py)
                            pen.pendown()
                            pen.goto(nx, ny)
                            px, py = nx + ux * espacio, ny + uy * espacio
                        pen.penup()

                    # Direcciones: solo diagonales
                    dirs = [
                        (1, 1), (-1, 1),
                        (1, -1), (-1, -1),
                    ]
                    for dx, dy in dirs:
                        _linea_punteada_desde(cx, cy, dx, dy)

            # Coordenadas
            if con_coordenadas:
                pen.pencolor(color_texto)
                # letras
                letras = [chr(ord('a') + i) for i in range(n)]
                for i, letra in enumerate(letras):
                    x = inicio_x + (i * tamano_casilla) + (tamano_casilla // 2) - 5
                    y = inicio_y - 30
                    pen.goto(x, y)
                    pen.write(letra, font=("Arial", int(tamano_casilla * 0.3), "bold"))
                # numeros
                for i in range(n):
                    x = inicio_x - 25
                    y = inicio_y + (i * tamano_casilla) + (tamano_casilla // 2) - 8
                    pen.goto(x, y)
                    pen.write(str(i + 1), font=("Arial", int(tamano_casilla * 0.3), "bold"))

            # Título
            pen.goto(0, inicio_y + tablero_px + 20)
            pen.pencolor(color_texto)
            titulo = "♔ Problema de las 8 Reinas ♛" if n == 8 else f"♔ Problema de las {n-1} Reinas ♛"
            pen.write(titulo, align="center", font=("Arial", int(tamano_casilla * 0.4), "bold"))

            # Finalizar dibujo
            screen.update()
            # No llamar a t.mainloop() para no bloquear la app de Tkinter
        except Exception as e:
            print(f"Aviso: error al dibujar con turtle: {e}")

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

        # Intentar dibujar el tablero con la mejor solución encontrada
        try:
            # Elegir una solución a dibujar: una óptima si existe, si no la mejor por fitness
            solucion_a_dibujar = None
            if result.num_soluciones_optimas > 0:
                for i, fit in enumerate(result.fitness_final):
                    if fit == 0:
                        solucion_a_dibujar = result.poblacion_final[i]
                        break
            if solucion_a_dibujar is None:
                solucion_a_dibujar = result.poblacion_final[result.mejor_idx]

            # Dibujar
            self._tablero_ajedrez_con_reinas_turtle(solucion_a_dibujar)
        except Exception as e:
            # No interrumpir la UI si falla el dibujo (por ejemplo, entorno sin GUI)
            print(f"Aviso: No se pudo dibujar el tablero: {e}")


def main():
    Aplicacion()
