# AspiradoraMesa

Este código es una simulación multiagente de un escenario de limpieza de robots hecho con la librería mesa. Para simular el entorno, se utilizo una cuadrícula de N x M tamaño donde se generan cuadros aleatorios de tierra que los agentes buscan limpiar. Cada agente tiene implementado 4 algoritmos de búsqueda los cuales son BFS, Djikstra, aleatorio y tierra_adyacente. 

## Instalación

Para poder ejectutar el código, es necesario descargar este repositorio y adentro del directorio utilizar un entorno de python, aunque se recomienda ir por un entorno virtual (sea con el módulo venv o conda) e instalar las dependencias de requirements.txt.

Para ejecutar el código, es necesario abrir una terminal en el directorio del proyecto (o utilizar el comando `cd`), y correr el comando python:
`python main.py`

## Estructura del código

El código se divide en 3 archivos: agents.py, models.py y main.py

El archivo **agents.py** contiene el código del agente del robot de limpieza (en este caso su nombre es LukeAgent). El archivo **models.py** contiene el modelo para correr esta simulación (VacuumModel) y por último main.py contiene las variables que definen el tamaño de la cuadrícula, número de agentes y porcentaje de suciedad, al igual que las gráficas desplegadas y el código para levantar un servidor web.

## Modificar parámetros del programa

Para modificar el tamaño de la cuadrícula, el número de agentes y el porcentaje de suciedad es necesario ir a la linea 22 del archivo main.py y modificar los valores de M y N (para el tamaño de la cuadrícula), num_agents (para la cantidad de agentes) y dirty_percentage (el porcentaje)

```python
# Parameters for the model
M, N = 10, 10
num_agents = 3
dirty_percentage = 0.7

server_params = {
    "M": M,
    "N": N,
    "num_agents": num_agents,
    "dirty_percentage": dirty_percentage,
    "max_time": Slider("Max_Time", 100, 10, 250, 5)
}
```