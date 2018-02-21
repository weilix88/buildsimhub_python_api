[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE.txt)
[![Twitter Follow](https://img.shields.io/twitter/follow/sendgrid.svg?style=social&label=Follow)](https://twitter.com/buildsimhub)

**Esta librería te permite usar rápida y fácilmente el API v1 de WEB BuildSimHub via Python.**

Esta librería representa el comienzo de la función de Cloud Simulation en BuildSimHub. Queremos que esta librería sea llevada por la comunidad y guiada por BuildSimHub. Necesitamos tu ayuda para alcanzar esta meta. Para ayudar, asegúrate que estamos creando las cosas correctas en el orden correcto, te pedimos que crees issues y pull requests,
o simplemente que votes o comentes issues o pull requests ya existentes. Apreciamos su apoyo continuo, ¡gracias!

# Tabla de Contenidos
* [Instalación](#installation)
* [Empezar](#quick-start)
* [Funciones y Objetos](#functions)
* [Hoja de Ruta](#roadmap)
* [Acerca De](#about)
* [Licencia](#license)

<a name="installation"></a>

# Instalación

## Prerrequisitos
- El servicio BuildSimHub, empezando en el [free level](https://my.buildsim.io/register.html)
- Python version 2.6, 2.7, 3.4, 3.5 or 3.6

## Instalación de Paquete
Simplemente clona este repositorio y colócalo dentro de la carpeta en la que quieras crear la aplicación. Ejemplos:
![picture alt](https://imgur.com/x60rk2O.png)

## Preparación del entorno
Después que has descargado todo el paquete. Lo primero que necesitas hacer es reconfigurar el API de usuario en el archivo [info.config](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/info.config) file.
Puedes conseguir la llave API asociada a tu cuenta en la página de perfil:

![picture alt](https://imgur.com/gHehDiN.png)

Simplemente edita el [info.config](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/info.config)
`user_api_key:[YOUR_API_KEY]`

## Modelo clave
La clave del modelo se puede encontrar en su proyecto buildsimhub.

<a name="quick-start"></a>

# Empezar

## Corre la simulación
Lo siguiente es el código mínimo requerido para iniciar una simulación regular con el [helpers/simulationJob](https://github.com/weilix88/buildsimhub_python_api/tree/master/BuildSimHubAPI/helpers)

### Con SimulationJob Class
```python
from BuildSimHubAPI import buildsimhub
#this key can be found under an energy model
model_key="0ade3a46-4d07-4b99-907f-0cfeece321072"

#absolute directory to the energyplus model
file_dir = "/Users/weilixu/Desktop/5ZoneAirCooled.idf"

############### AHORA, UTILIZA EL CÓDIGO ########################

bsh = buildsimhub.BuildSimHubAPIClient()
newSJ = bsh.new_simulation_job(model_key,'my first cloud simulation', 'regular',1)
response = newSj.create_model(file_dir)

############### LISTO! #################################

#Puedes imprimir las respuestas para verificar si la simulación
#tuvo éxito o no.
print (response)
```
El `BuildSimHubAPIClient` crea un [portal object](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/buildsimhub.py) que maneja el flujo de trabajo de la simulación.
Desde este objeto, puedes iniciar un [simulationJob](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/helpers/simulationJob.py) para conducir una Cloud Simulation. Llama el método createModel() con parámetros que puedan empezar la Cloud Simulation.

### Sigue el progreso de la Cloud Simulation
```python
from BuildSimHubAPI import buildsimhub
bsh = buildsimhub.BuildSimHubAPIClient()

#this key can be found under your project folder
model_key="0ade3a46-4d07-4b99-907f-0cfeece321072"

#absolute directory to the energyplus model
file_dir = "/Users/weilixu/Desktop/5ZoneAirCooled.idf"

newSJ = bsh.new_simulation_job(model_key)
response = newSj.create_model(file_dir)

######DEBAJO ESTÁ EL CODIGO PARA SEGUIR LA SIMULACIÓN#########
if(response == 'success'):
  while newSJ.track_simulation():
    print (newSJ.trackStatus)
    time.sleep(5)
```
Como fue mencionado previamente, [BuildSimHubAPIClient](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/buildsimhub.py)  maneja la totalidad de flujo de trabajo de la simulación. Así que una vez que la Cloud Simulation ha sido correctamente empezada por la clase [SimulationJob](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/helpers/simulationJob.py) puedes simplemente llamar la función `trackSimulation()` para recibir el progreso de la simulación.

### Obtener los resultados de la Cloud Simulation
```python
from BuildSimHubAPI import buildsimhub
bsh = buildsimhub.BuildSimHubAPIClient()

#this key can be found under your project folder
model_key="0ade3a46-4d07-4b99-907f-0cfeece321072"

#absolute directory to the energyplus model
file_dir = "/Users/weilixu/Desktop/5ZoneAirCooled.idf"

newSJ = bsh.new_simulation_job(model_key)
response = newSj.create_model(file_dir)

if(response == 'success'):
  while newSJ.track_simulation():
    print (newSJ.trackStatus)
    time.sleep(5)
  
  ######DEBAJO ESTÁ EL CODIGO PARA OBTENER LOS RESULTADOS DE LA SIMULACION#########
  response = newSJ.get_simulation_results('html')
  print(response)
```
Si el trabajo se completó, puedes obtener los resultados llamando la funcion `get_simulation_results(type)`.

<a name="functions"></a>

#Funciones y Objetos
## SimulationJob
La manera más fácil de generar una clase [SimulationJob](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/helpers/simulationJob.py) es llamando el método `newSimulationJob()` en el [BuildSimHubAPIClient](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/buildsimhub.py).
 Sin embargo, tienes que proveer una `folder_key` para poder crear una nueva instancia [SimulationJob](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/helpers/simulationJob.py).

La `folder_key` puede ser encontrada en cada carpeta de tu proyecto
![picture alt](https://imgur.com/jNrghIZ.png)

## simulationType
La clase [SimulationType](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/helpers/simulationType.py) te ayuda a configurar la Cloud Simulation. Hay dos tipos de simulación: `regular` y `fast`. Además, puedes incrementar el número de agentes llamando la función `increaseAgents()`.
```python
simulationType = bsh.get_simulation_type()
numOfAgents = simulationType.increaseAgents();
print (numOfAgents)
```
Hay que tomar en cuenta que el número máximo de agentes laborando en un trabajo de simulación está limitado a 12, y mientras más agentes asignaste a un trabajo de simulación, más rápido será tu simulación. También podrías llamar la función `resetAgent()` para resetear el número de agentes a 2.

## SimulationJob
Un trabajo de simulación maneja un solo tipo de Cloud Simulation. Este contiene tres funciones principales las cuales son mostradas a continuación:

### create_model
la función `create_model()`tiene un total de 4 parámetros.
1. `file_dir` (requerido): el directorio local absoluto de tu EnergyPlus / OpenStudio model (p.ej., "/Users/weilixu/Desktop/5ZoneAirCooled.idf")
2. `comment`(opcional): La descripción de la version del modelo que será subido a tu carpeta. El mensaje por defecto es `Upload through Python API`
3. `simulationType` (opcional): El simulation Type debería ser generado de la clase [SimulationType](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/helpers/simulationType.py). Esta clase maneja el simulation type además de la cantidad de agentes que quieras asignar al trabajo de simulación. **Hay que tomar en cuenta que si este parámetro no es usado, entonces el create_model método no lanzará la simulación**
4. `agent` (opcional): El número de agentes es propiedad de la clase [SimulationType](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/helpers/simulationType.py). Si se selecciona la simulación rápida, Entonces la cantidad de agentes por defecto será de 2.

Este método devuelve dos tipos de información:
Si es exitoso: `success`
o un mensaje de error mostrará que estuvo mal en tu pedido.

### run_simulation
La función `run_simulation()` puede ser llamada dentro de un trabajo de simulación si la simulación no es conducida. La función tiene dos parámetros:
1. `simulationType` (optional): El simulation Type debería ser generado de la clase [SimulationType](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/helpers/simulationType.py).  Esta clase maneja el simulation type además de la cantidad de agentes que quieras asignar al trabajo de simulación. **Hay que tomar en cuenta que si este parámetro no es usado, entonces el create_model método no lanzará la simulación**

### track_simulaiton
La función `track_simulation()` no requiere ningún parámetro. Sin embargo, es necesario que una cloud simulation exitosa sea creada y lanzada en la nube. De otra manera, recibirás un mensaje llamando esta función:
`No simulation is running or completed in this Job - please start simulation using createModel method.`
Si hay una simulación corriendo en la nube para este simulationJob, entonces, esta función se convertirá en `true` y podrás obtener el estatus de la simulación mediante el parámetro de la clase trackStatus.Ejemplo a continuación:
```python
if(newSimulationJob.track_simulation()):
  print(newSimulationJob.trackStatus)
```
### get_simulation_results
La función `get_simulation_results(type)` requiere 1 parámetro, el result type. Actualmente, puedes obtener tres tipos de resultados: el archive error (`err`), archivo eso (`eso`) y archivo html (`html`), generado de la simulación EnergyPlus.

```python
response = newSimulationJob.get_simulation_results('err')
print (response)
```
## Model
La clase model contiene una serie de métodos que provee la información del modelo y resultados (después de la simulación)
### Pre-simulation methods
1. *num_total_floor()*: puede ser llamado antes de que la simulación se complete. Este obtiene el número de suelos, o -1 si hay un error.
2. *num_zones()*: puede ser llamado antes que la simulación se complete. Este obtiene el número total de zonas termales, o -1 si hay un error.
3. *num_condition_zones()*: puede ser llamado antes que la simulación se complete. Este obtiene el número total de zonas condicionadas, o -1 si hay un error.
4. *conditioned_floor_area (unit)*:  puede ser llamado antes que la simulación se complete. Este obtiene las áreas de suelo de espacios condicionados, o -1 si hay un error. Este método tiene una entrada adicional: unit. Si deseas obtener la unidad ft2, entonces necesitas especificar ‘ip’ para el parámetro de la unidad:
`  m.condition_floor_area("ip")
`
5. *gross_floor_area(unit)*:  puede ser llamado antes que la simulación se complete. Este obtiene el total de áreas de suelo (incluyendo espacios plenum), o -1 si hay un error. Este método tiene una entrada opcional: unit. Si deseas obtener la unidad ft2, entonces necesitas especificar ‘ip’ para el parámetro de la unidad:
`  m.gross_floor_area("ip")
`
6. *window_wall_ratio()*: puede ser llamado antes que la simulación se complete. Este obtiene el radio total de ventana a pared (por encima del area de superficie del suelo) o -1 si hay un error.

### Métodos Pre-simulación
1. *new_site_eui()*:  Obtiene el net site eui de la simulación (incluye generadores como PV). La unidad debería basarse en la especificación de modelo: SI (kWh/m2 or MJ/m2), IP(kWh/m2).
2. *total_site_eui()*: Obtiene el total site eui de la simulación. La unidad debería basarse en la especificación de modelo: SI (kWh/m2 or MJ/m2), IP(kWh/m2).
3. *not_met_hour_cooling()*: Regresa el setpoint de tiempo ‘not met hours’ durante el periodo enfriamiento. unidad: hora
4. *not_met_hour_heating()*: Regresa el setpoint de tiempo ‘not met hours’ durante del periodo de calentamiento. unidad: hora
5. *not_met_hour_total()*: Regresa el setpoint de tiempo ‘not met hours’ durante el periodo total de enfriamiento y calentamiento. unidad: hora
6. *total_end_use_electricity()*: Obtiene el total de consumo eléctrico del diseño. unidad: kWh or GJ, IP is kBtu
7. *total_end_use_naturalgas()*: Obtiene el total de consumo de gas natural del diseño. unidad: kWh or GJ, IP is kBtu


### Métodos diversos y variables
1. lastParameterUnit: Puedes verificar el valor de la variable pedida por la llamada API más reciente.
```python
m = newSj.model
print(str(m.net_site_eui())+ " " + m.lastParameterUnit)
#Output: 242.98 MJ/m2
print(str(m.total_end_use_electricity())+ " " + m.lastParameterUnit)
#Output: 156.67 GJ
```

<a name="roadmap"></a>
# Hoja de Ruta
1. También estamos en APIs para obtención de resultados, los cuales permiten a los usuarios obtener resultados de la simulación para el post-procesamiento.
2. Si estás interesado en el futuro de este proyecto, por favor echa un vistazo a nuestros [issues](https://github.com/weilix88/buildsimhub_python_api/issues) y [pull requests](https://github.com/weilix88/buildsimhub_python_api/pulls). Nos encantaría escuchar tus opiniones y recomendaciones.


<a name="about"></a>
# Acerca De

buildsimhub-python  está guíado y apoyado por el BuildSimHub [Developer Experience Team](mailto:haopeng.wang@buildsimhub.net).

buildsimhub-python es mantenido y financiado por BuildSimHub, Inc. Los nombres y logos de buildsimhub-python son trademarks de BuildSimHub, Inc.

<a name="license"></a>
# Licencia
[The MIT License (MIT)](LICENSE.txt)
