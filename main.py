"""
    Autor Andres707
"""

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
        self.mensajeRE = Label(self.raiz,text="Numero de Repeticiones",fg="black")
        self.mensajeRE.pack()
        self.mensajePC = Label(self.raiz, text="Probabilidad de cruse", fg="black")
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
        self.botonIn = ttk.Button(self.raiz, text="Iniciar",command=self.algoritmo).pack(side=BOTTOM)
#        self.botonSA.pack(side=RIGHT)
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
        self.caja_PM.insert(0,0.1)
        self.caja_PM.config(state=tk.DISABLED)
        self.caja_PC.config(state=tk.DISABLED)


        self.raiz.mainloop()

    def algoritmo(self):
        poblacion=int(self.caja_PO.get())
        nr=int(self.caja_NR.get())
        re=int(self.caja_RE.get())
        proCruse=float(self.caja_PC.get())
        proMutacion = float(self.caja_PM.get())
        Matriz = []
        Ganadores = []
        start_time = time()
        for m in range(poblacion):
            Matriz.append(Funciones.generar_individuo(nr + 1))
        for i in range(poblacion):
            print("Individuo", (i + 1), ": ", Matriz[i])
        for secuencia in range(re):
            print("Repeticion ", secuencia + 1)
            Fitnes = (Funciones.calcular_fitness(Matriz, poblacion, nr))
            axx = Fitnes.count(0)
            Ganadores = (Funciones.torneo(Fitnes, poblacion))
            probCruce = Funciones.generar_probabilidad()
            if (probCruce > proCruse):
                hijos = []
                # print("hijos igual a los padres")
                Ganadores[0] = Ganadores[0] - 1
                Ganadores[1] = Ganadores[1] - 1
                for hj in range(2):
                    hij = Matriz[Ganadores[hj]]
                    hijos.append(hij)
            else:
                hijos = Funciones.cruce(Ganadores, Matriz, nr)
            probMutacion = Funciones.generar_probabilidad()
            if (probMutacion > proMutacion):
                # print("sin mutacion")
                pass
            else:
                for hm in range(2):
                    hijos[hm] = Funciones.mutar_individuo(hijos[hm], nr)
            # Autor Andres707
            # Matriz = Funciones.seleccion(Ganadores,hijos,Matriz,nr)
            for i in range(2):
                Matriz = Funciones.seleccionar_con_torneo_agrupado(hijos[i],Matriz,poblacion,nr,Fitnes)
        elapsed_time = time() - start_time
        print("-------------------------Fin-----------------------------------")
        Fitnes = (Funciones.calcular_fitness(Matriz, poblacion, nr))
        Ganador = 0
        libro = open('Ganadores.txt', 'a')
        for i in range(poblacion):
            print("Individuo", (i + 1), ": ", Matriz[i], "Fitnes :", Fitnes[i])
            if (Fitnes[Ganador] > Fitnes[i]):
                Ganador = i
            if (Fitnes[i] == 0):
                parrafo = "Inividuo", (i + 1), ": ", Matriz[i], "Fitness: ", Fitnes[i]
                parrafo = str(parrafo)
                libro.write('\n' + parrafo)
        libro.write('\n')
        libro.close()

        print("Lapso de tiempo: %.10f segundos." % elapsed_time)
        print("numero de individuaos con un 0: ", axx)
        print("Ganador: ", Ganador + 1)
        print("Ganador: ", Matriz[Ganador], "Fitness: ", Fitnes[Ganador], "Autor Andres707")
        p="Ganador: ", Matriz[Ganador], "Fitness: ", Fitnes[Ganador]
        p=str(p)
        self.mensajeLT = Label(self.raiz, text="Lapso de tiempo: %.10f segundos." % elapsed_time,fg="black")
        self.mensajeLT.pack()
        self.mensajeG = Label(self.raiz, text=p, fg="black")
        self.mensajeG.pack()
        self.mensajeLT.place(x=10, y=125)
        self.mensajeG.place(x=10, y=150)

        return 0

def main():
    mi_app = Aplicacion()
    return 0


if __name__ == '__main__':
    main()
