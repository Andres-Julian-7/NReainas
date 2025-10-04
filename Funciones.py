from random import shuffle
import random
import math

# Constantes
NUMERO_HIJOS = 2
NUMERO_CANDIDATOS_TORNEO = 2
NUMERO_GRUPOS_SELECCION = 3
TAMANO_GRUPO_SELECCION = 10
NUMERO_INDIVIDUOS_COMPARACION = 4


def generar_probabilidad():
    """Genera un número aleatorio entre 0 y 1 con 2 decimales."""
    return round(random.random(), 2)


def generar_individuo(numero_limite):
    """
    Genera un individuo (permutación) para el problema de las N-Reinas.

    Args:
        numero_limite: Número de elementos en la permutación (0 a numero_limite-1)

    Returns:
        Lista con números del 0 a numero_limite-1 en orden aleatorio
    """
    individuo = [i for i in range(numero_limite)]
    shuffle(individuo)
    return individuo


def calcular_fitness(poblacion, num_individuos, num_reinas):
    """
    Calcula el fitness (número de conflictos) para cada individuo.

    Args:
        poblacion: Lista de individuos
        num_individuos: Número de individuos en la población
        num_reinas: Número de reinas (tamaño del tablero)

    Returns:
        Lista con el fitness de cada individuo
    """
    fitness = []
    for m in range(num_individuos):
        individuo = poblacion[m]
        conflictos = 0

        for i in range(num_reinas):
            posicion_i = individuo[i]
            for j in range(num_reinas):
                posicion_j = individuo[j]
                if i != j:
                    diferencia_vertical = math.fabs(posicion_i - posicion_j)
                    diferencia_horizontal = math.fabs(i - j)
                    if diferencia_vertical == diferencia_horizontal:
                        conflictos += 1

        conflictos = round(conflictos / 2, 0)
        fitness.append(conflictos)

    return fitness


def torneo(fitness_valores, tamano_poblacion):
    """
    Selecciona dos ganadores mediante torneo binario.

    Args:
        fitness_valores: Lista con fitness de cada individuo
        tamano_poblacion: Tamaño de la población

    Returns:
        Lista con índices de los dos ganadores
    """
    ganadores = []

    for _ in range(NUMERO_CANDIDATOS_TORNEO):
        candidato1 = random.randrange(0, tamano_poblacion)
        candidato2 = random.randrange(0, tamano_poblacion)

        # Asegurar que los candidatos sean diferentes
        while candidato1 == candidato2:
            candidato2 = random.randrange(0, tamano_poblacion)
            candidato1 = random.randrange(0, tamano_poblacion)

        fitness_candidato1 = fitness_valores[candidato1]
        fitness_candidato2 = fitness_valores[candidato2]

        if fitness_candidato1 < fitness_candidato2:
            ganadores.append(candidato1)
        else:
            ganadores.append(candidato2)

    return ganadores


def cruce(indices_ganadores, poblacion, num_reinas):
    """
    Realiza cruce de un punto entre dos padres.

    Args:
        indices_ganadores: Índices de los padres seleccionados
        poblacion: Población actual
        num_reinas: Número de reinas

    Returns:
        Lista con dos hijos generados
    """
    hijos = []
    indices_ganadores[0] = indices_ganadores[0] - 1
    indices_ganadores[1] = indices_ganadores[1] - 1

    punto_cruce = random.randrange(1, num_reinas)

    for j in range(NUMERO_HIJOS):
        hijo = []

        # Copiar genes hasta el punto de cruce
        for i in range(punto_cruce):
            hijo.append(poblacion[indices_ganadores[j]][i])

        posicion_insercion = punto_cruce

        # Completar con genes del otro padre
        for m in range(num_reinas):
            padre_contrario = 1 if j == 0 else 0
            gen = poblacion[indices_ganadores[padre_contrario]][m]

            if gen not in hijo:
                hijo.insert(posicion_insercion, gen)
                posicion_insercion += 1

        hijos.append(hijo)

    return hijos


def mutar_individuo(individuo, num_reinas):
    """
    Realiza mutación por intercambio de dos genes aleatorios.

    Args:
        individuo: Individuo a mutar
        num_reinas: Número de reinas

    Returns:
        Individuo mutado
    """
    posicion1 = random.randrange(num_reinas)
    posicion2 = random.randrange(num_reinas)

    gen1 = individuo[posicion1]
    gen2 = individuo[posicion2]

    individuo[posicion1] = gen2
    individuo[posicion2] = gen1

    return individuo


def seleccion(indices_padres, hijos, poblacion, num_reinas):
    """
    Selecciona los mejores entre padres e hijos (no utilizada actualmente).

    Args:
        indices_padres: Índices de los padres
        hijos: Lista de hijos generados
        poblacion: Población actual
        num_reinas: Número de reinas

    Returns:
        Población actualizada
    """
    indices_padres[0] = indices_padres[0] - 1
    indices_padres[1] = indices_padres[1] - 1

    distancias = []
    individuos = hijos[:]

    for i in range(NUMERO_CANDIDATOS_TORNEO):
        individuos.append(poblacion[indices_padres[i]])

    fitness = calcular_fitness(individuos, NUMERO_INDIVIDUOS_COMPARACION, num_reinas)

    # Buscar el mejor individuo
    indice_mejor = 0
    contador = 0
    for i in range(NUMERO_INDIVIDUOS_COMPARACION):
        if fitness[indice_mejor] > fitness[i]:
            indice_mejor = i

    # Calcular distancia del mejor con los demás
    indice_mas_distante = 0
    for m in range(NUMERO_INDIVIDUOS_COMPARACION):
        individuo_mejor = individuos[indice_mejor]
        if indice_mejor == m:
            distancias.append(0)
        else:
            for i in range(num_reinas):
                if individuo_mejor[i] != individuos[m][i]:
                    contador += 1
            distancias.append(contador)

        if distancias[indice_mas_distante] < distancias[m]:
            indice_mas_distante = m

    # Actualizar población
    if indice_mejor == 3:
        if indice_mas_distante == 2 or indice_mas_distante == 3:
            pass
        elif indice_mejor == 2:
            poblacion[indices_padres[0]] = individuos[indice_mas_distante]
    elif indice_mejor == 0 or indice_mejor == 1:
        poblacion[indices_padres[0]] = individuos[indice_mejor]
        if indice_mas_distante == 0 or indice_mas_distante == 1:
            poblacion[indices_padres[1]] = individuos[indice_mas_distante]

    return poblacion


def seleccionar_con_torneo_agrupado(hijo, poblacion, num_individuos, num_reinas, fitness):
    """
    Selecciona y reemplaza el peor individuo usando torneo agrupado.

    Args:
        hijo: Nuevo individuo a insertar
        poblacion: Población actual
        num_individuos: Número de individuos
        num_reinas: Número de reinas
        fitness: Fitness de la población actual

    Returns:
        Población actualizada
    """
    grupos_individuos = []
    grupos_info = []

    # Crear grupos aleatorios
    for i in range(NUMERO_GRUPOS_SELECCION):
        individuos_grupo = []
        info_grupo = []

        for c in range(TAMANO_GRUPO_SELECCION):
            indice_aleatorio = random.randint(0, num_individuos - 1)
            individuos_grupo.append(poblacion[indice_aleatorio])
            info_grupo.append([c, indice_aleatorio, fitness[indice_aleatorio]])

        grupos_individuos.append(individuos_grupo)
        grupos_info.append(info_grupo)

    # Calcular similitud con el hijo para cada individuo de los grupos
    similitudes = []
    for i in range(NUMERO_GRUPOS_SELECCION):
        grupo = grupos_individuos[i]
        for c in range(TAMANO_GRUPO_SELECCION):
            individuo = grupo[c]
            genes_iguales = 0

            for posicion in range(num_reinas):
                if hijo[posicion] == individuo[posicion]:
                    genes_iguales += 1

            similitudes.append([i, c, genes_iguales])

    # Encontrar el menos similar en cada grupo
    menos_similar_grupo1 = similitudes[0]
    for i in range(1, TAMANO_GRUPO_SELECCION):
        if similitudes[i][2] <= menos_similar_grupo1[2]:
            menos_similar_grupo1 = similitudes[i]

    menos_similar_grupo2 = similitudes[TAMANO_GRUPO_SELECCION]
    for a in range(TAMANO_GRUPO_SELECCION, 2 * TAMANO_GRUPO_SELECCION):
        if similitudes[a][2] <= menos_similar_grupo2[2]:
            menos_similar_grupo2 = similitudes[a]

    menos_similar_grupo3 = similitudes[2 * TAMANO_GRUPO_SELECCION]
    for b in range(2 * TAMANO_GRUPO_SELECCION, 3 * TAMANO_GRUPO_SELECCION):
        if similitudes[b][2] <= menos_similar_grupo3[2]:
            menos_similar_grupo3 = similitudes[b]

    # Encontrar el peor fitness entre los menos similares
    peor_fitness = 0
    peor_individuo = None

    menos_similares = [menos_similar_grupo1, menos_similar_grupo2, menos_similar_grupo3]
    for i, menos_similar in enumerate(menos_similares):
        fitness_actual = grupos_info[i][menos_similar[1]][2]

        if peor_fitness < fitness_actual or peor_individuo is None:
            peor_fitness = fitness_actual
            peor_individuo = grupos_info[i][menos_similar[1]]

    # Reemplazar el peor individuo con el hijo
    poblacion[peor_individuo[1]] = hijo

    return poblacion