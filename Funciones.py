from random import shuffle
import random
import math


# Probabilidad
from typing import List, Any, Union


def Probabilidad():
    ra = round(random.random(), 2)
    return ra


# Poblacion
def cadenaN(numerolimite):
    x = [i for i in range(1, numerolimite)]
    shuffle(x)
    return x


# Valoracion
def valoracion(Matriz, np, nr):
    Valor = []
    contador = 0
    for m in range(np):
        matriz = Matriz[m]
        for i in range(nr):
            oi = matriz[i]
            for j in range(nr):
                oj = matriz[j]
                if (i != j):
                    _v1 = math.fabs(oi - oj)
                    _v2 = math.fabs(i - j)
                    if (_v1 == _v2):
                        contador = contador + 1
        contador = round(contador / 2, 0)
        Valor.append(contador)
        contador = contador * 0
    return Valor


# torneo
def torneo(valores, poblacion):
    Ganadores = []
    for i in range(2):
        a1 = random.randrange(1, poblacion)
        a2 = random.randrange(1, poblacion)
        bandera = True
        while (bandera):
            if (a1 == a2):
                a2 = random.randrange(1, poblacion)
                a1 = random.randrange(1, poblacion)
            else:
                bandera = False
        aa1 = valores[a1]
        aa2 = valores[a2]
        if (aa1 < aa2):
            Ganadores.append(a1)
        else:
            Ganadores.append(a2)
    return Ganadores


# cruse
def cruse(Ganadores, matriz, nr):
    hijos = []
    hijo = []
    Ganadores[0] = Ganadores[0] - 1
    Ganadores[1] = Ganadores[1] - 1
    a1 = random.randrange(1, nr)
    # print('Alelo donde se segmenta: ',a1)
    ax1 = a1
    for j in range(2):
        for i in range(a1):
            hijo.append((matriz[Ganadores[j]][i]))
        for m in range(nr):
            if (j == 0):
                a = hijo.count(matriz[Ganadores[1]][m])
                if (a == 0):
                    hijo.insert(ax1, matriz[Ganadores[1]][m])
                ax1 = ax1 + 1
            else:
                a = hijo.count(matriz[Ganadores[0]][m])
                if (a == 0):
                    hijo.insert(ax1, matriz[Ganadores[0]][m])
                ax1 = ax1 + 1
        hijos.append(hijo)
        hijo = hijo * 0
        ax1 = a1
    return hijos


# mutacion
def mutacion_un_hijo(hijo, nr):
    r1 = random.randrange(nr)
    r2 = random.randrange(nr)
    G1 = hijo[r1]
    G2 = hijo[r2]
    hijo[r1] = G2
    hijo[r2] = G1
    return hijo


# seleccion
def seleccion(padres, hijos, matriz, nr):
    # Insertar padres e hijos a individuos
    padres[0] = padres[0] - 1
    padres[1] = padres[1] - 1
    dk = []
    individuo = hijos
    for i in range(2):
        individuo.append(matriz[padres[i]])
    valor = valoracion(individuo, 4, nr)  # Fitness
    # Se busca al ganador
    ganador = 0
    contador = 0
    for i in range(4):
        if valor[ganador] > valor[i]:
            ganador = i
    a = 0  # Ganador 2
    for m in range(4):
        x = individuo[ganador]
        if ganador == m:
            dk.append(0)
        else:
            for i in range(nr):
                if x[i] != individuo[m][i]:
                    contador = contador + 1
            dk.append(contador)
        if dk[a] < dk[m]:
            a = m
            # 3 = p2
            # 2 = p1
    if ganador == 3:
        if a == 2 or a == 3:
            pass
        elif ganador == 2:
            matriz[padres[0]] = individuo[a]
    elif ganador == 0 or ganador == 1:
        matriz[padres[0]] = individuo[ganador]
        if a == 0 or a == 1:
            matriz[padres[1]] = individuo[a]
    return matriz

# 2
def seleccion2(hijo,Matriz,np,nr,fitness):
    grupos = 3
    s = 10
    cf = []
    cfa = []
    ap = []
    cap = []
    for i in range(grupos):
        for c in range(s):
            ra = random.randint(0, (np-1))
            cfa.append(Matriz[ra])
            cap.append([c, ra,fitness[ra]])
        cf.append(cfa)
        cfa = []
        ap.append(cap)
        cap = []

    ia = []
    contador = 0
    for i in range(grupos):
        x = cf[i]
        for c in range(s):
            aux = x[c]
            for dh in range(nr):
                if hijo[dh] == aux[dh]:
                   contador = contador + 1
            ia.append([i,c,contador])
            contador = 0

    m1 = 0
    for i in range(9):
        if ia[i][2] <= m1:
            m1 = ia[i][2]
            m11 = ia[i]
        elif m1 == 0:
            m11 = ia[i]
    m2 = 0
    for a in range(10, 19):
        if ia[a][2] <= m2:
            m2 = ia[a][2]
            m22 = ia[a]
        elif m2 == 0:
            m22 = ia[a]
    m3 = 0
    for b in range(20, 29):
        if ia[b][2] <= m3:
            m3= ia[b][2]
            m33 = ia[b]
        elif m3 == 0:
            m33 = ia[b]
    gan = 0
    for i in range(3):
       # print(ap[i][m11[i]][2])
        if gan > ap[i][m11[i]][2]:
            gan = ap[i][m11[i]][2]
            ganador = ap[i][m11[i]]
        elif gan == 0:
            ganador = ap[i][m11[i]]
    #print(ganador)
    #print(Matriz[ganador[1]])
    Matriz[ganador[1]] = hijo
    #print(Matriz[ganador[1]])
    return Matriz
