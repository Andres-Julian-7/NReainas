# 🔷 Algoritmo Genético para el Problema de las N-Reinas

![Python](https://img.shields.io/badge/Python-3.12.8-blue.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

Implementación de un **Algoritmo Genético** con interfaz gráfica para resolver el clásico problema de las N-Reinas utilizando técnicas de computación evolutiva.

## 📋 Descripción

El problema de las N-Reinas consiste en colocar N reinas en un tablero de ajedrez de N×N casillas de manera que ninguna reina pueda atacar a otra. Este proyecto utiliza un algoritmo genético para encontrar soluciones óptimas mediante:

- **Representación por permutaciones**: Cada individuo es una permutación que representa las posiciones de las reinas
- **Selección por torneo**: Competencia binaria entre individuos
- **Cruce de un punto**: Intercambio de material genético entre padres
- **Mutación por intercambio**: Cambio aleatorio de genes
- **Selección con torneo agrupado**: Estrategia avanzada de reemplazo poblacional

## ✨ Características

- 🖥️ **Interfaz gráfica moderna** con Tkinter
- 📊 **Visualización en tiempo real** del progreso del algoritmo
- 📋 **Área de resultados con scroll** para revisar toda la ejecución
- 📄 **Copiar resultados** al portapapeles con un clic
- 💾 **Guardado automático** de soluciones óptimas en archivo de texto
- ⚡ **Parámetros configurables** para experimentación
- 📈 **Métricas de rendimiento** (tiempo de ejecución, soluciones encontradas)

## 🚀 Instalación

### Requisitos previos

- Python 3.12.8 o superior
- virtualenv (opcional pero recomendado)

### Pasos de instalación

1. **Clonar el repositorio**
```bash

git clone https://github.com/tuusuario/NReinas.git
cd NReinas
```


2. **Crear entorno virtual (opcional)**

```shell script

python -m venv .venv
```


3. **Activar entorno virtual**

En Windows:
```shell script

.venv\Scripts\activate
```


En Linux/Mac:
```shell script

source .venv/bin/activate
```


4. **Instalar dependencias**

Este proyecto utiliza solo la biblioteca estándar de Python, por lo que no requiere instalaciones adicionales.

## 📖 Uso

### Ejecución básica

```shell script

python main.py
```


### Interfaz gráfica

Una vez ejecutado, aparecerá una ventana con los siguientes parámetros configurables:

| Parámetro | Descripción | Valor por defecto |
|-----------|-------------|-------------------|
| **Número de Reinas** | Tamaño del tablero (N×N) | 8 |
| **Número de Individuos** | Tamaño de la población | 1000 |
| **Número de Generaciones** | Iteraciones del algoritmo | 1000 |
| **Probabilidad de Cruce** | Probabilidad de cruce (0-1) | 0.85 |
| **Probabilidad de Mutación** | Probabilidad de mutación (0-1) | 0.1 |

### Botones de control

- **Iniciar Algoritmo**: Ejecuta el algoritmo genético con los parámetros configurados
- **Copiar Resultados**: Copia los resultados al portapapeles
- **Salir**: Cierra la aplicación

### Ejemplo de uso

1. Ajusta el **Número de Reinas** según el problema que desees resolver (ej: 8, 16, 32)
2. Configura el **Número de Individuos** y **Generaciones** según la complejidad
3. Presiona **Iniciar Algoritmo**
4. Observa el progreso en el área de resultados
5. Una vez finalizado, revisa las métricas y usa **Copiar Resultados** si lo deseas

## 📁 Estructura del Proyecto

```
NReinas/
│
├── main.py                 # Interfaz gráfica y lógica principal
├── Funciones.py            # Operadores del algoritmo genético
├── Ganadores.txt           # Archivo de salida con soluciones óptimas
├── readme.md               # Este archivo
├── .gitignore             # Archivos ignorados por Git
└── .venv/                 # Entorno virtual (no incluido en repo)
```


## 🧬 Algoritmo Genético

### Representación

Cada individuo es una **permutación** de números del 0 a N-1, donde:
- El índice representa la columna
- El valor representa la fila donde se coloca la reina

Ejemplo para N=8: `[3, 1, 6, 2, 5, 7, 4, 0]`

### Función de Fitness

El fitness mide el número de **conflictos diagonales** entre reinas. Un fitness de **0** representa una solución óptima.

```python
fitness = número_de_pares_de_reinas_que_se_atacan_diagonalmente
```


### Operadores Genéticos

#### 1. Selección por Torneo
- Selecciona 2 candidatos aleatorios
- El de mejor fitness (menor) gana
- Se repite para obtener 2 padres

#### 2. Cruce de Un Punto
- Punto de cruce aleatorio
- Copia genes del primer padre hasta el punto
- Completa con genes del segundo padre (sin repetir)

#### 3. Mutación por Intercambio
- Selecciona 2 posiciones aleatorias
- Intercambia los genes en esas posiciones

#### 4. Selección con Torneo Agrupado
- Crea 3 grupos aleatorios de 10 individuos
- Encuentra el menos similar al hijo en cada grupo
- Reemplaza el de peor fitness entre los 3

## 📊 Resultados

Los resultados se muestran en tres lugares:

1. **Área de resultados de la interfaz**: Scroll con información detallada
2. **Consola**: Salida completa para depuración
3. **Archivo Ganadores.txt**: Soluciones óptimas (fitness = 0)

### Métricas reportadas

- ⏱️ Tiempo de ejecución
- 🎯 Número de soluciones óptimas encontradas
- 👑 Mejor individuo y su fitness
- 📋 Población final completa

## 🛠️ Configuración Avanzada

### Modificar constantes del algoritmo

En `Funciones.py` puedes ajustar:

```python
NUMERO_HIJOS = 2                      # Hijos por cruce
NUMERO_CANDIDATOS_TORNEO = 2          # Candidatos en torneo
NUMERO_GRUPOS_SELECCION = 3           # Grupos para selección
TAMANO_GRUPO_SELECCION = 10           # Tamaño de cada grupo
NUMERO_INDIVIDUOS_COMPARACION = 4     # Individuos para comparar
```


## 🐛 Solución de Problemas

### El algoritmo no encuentra soluciones óptimas

- Aumenta el **número de generaciones**
- Aumenta el **tamaño de la población**
- Ajusta las probabilidades de cruce y mutación

### La interfaz se congela

- Es normal durante la ejecución del algoritmo
- La barra de progreso indica que está procesando
- Para problemas grandes (N>20) puede tomar varios minutos

### Error de memoria

- Reduce el tamaño de la población
- Reduce el número de reinas

## 📝 Ejemplos de Configuración

### Problema pequeño (N=8)
```
Reinas: 8
Individuos: 100
Generaciones: 500
```


### Problema mediano (N=16)
```
Reinas: 16
Individuos: 500
Generaciones: 2000
```


### Problema grande (N=32)
```
Reinas: 32
Individuos: 2000
Generaciones: 5000
```


## 📚 Referencias

- [Problema de las N-Reinas - Wikipedia](https://es.wikipedia.org/wiki/Problema_de_las_ocho_reinas)
- [Algoritmos Genéticos - Wikipedia](https://es.wikipedia.org/wiki/Algoritmo_gen%C3%A9tico)
- [Genetic Algorithms in Python](https://towardsdatascience.com/genetic-algorithm-implementation-in-python-5ab67bb124a6)

## 👨‍💻 Autor

**Andres707** - *Desarrollo* - [Andres707](https://github.com/Andres707)

**Andres-Julian-7** - *Desarrollo* - [Andres-Julian-7](https://github.com/Andres-Julian-7)

## 📄 Licencia

Este proyecto está licenciado bajo una **Licencia Dual**:

### 🎓 Uso No Comercial (Libre)
Puedes usar, modificar y distribuir este software **libremente** para:
- 📚 Educación y aprendizaje
- 🔬 Investigación académica
- 👨‍💻 Proyectos personales
- 🌐 Código abierto sin fines de lucro

### 💼 Uso Comercial (Requiere Licencia)
Para uso comercial del software, **debes contactarme**:
- ✉️ Email: [andresj.garciap+github@gmail.com](andresj.garciap@gmail.com)
- 💬 GitHub: [Andres-Julian-7](https://github.com/Andres-Julian-7)
- 📝 Discutiremos términos justos según tu caso de uso

**¿Qué es uso comercial?**
- Integrar en productos o servicios pagos
- Usar en empresas con fines de lucro
- Revender o redistribuir comercialmente
- Ofrecer como SaaS o servicio de pago

Ver el archivo [LICENSE](LICENSE) para más detalles.

---

💡 **Nota**: Si eres estudiante, profesor o investigador, ¡este software es completamente gratis para ti!
## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📮 Contacto

Si tienes preguntas o sugerencias, no dudes en abrir un issue en el repositorio.


