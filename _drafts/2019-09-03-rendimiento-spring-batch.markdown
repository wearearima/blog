---
layout: post
title:  "Rendimiento de Spring Batch"
date:   2019-09-03 10:00:00
author: arkaitz
categories: mediator feature
tags: featured
header-image:	2019-09-03-rendimiento-spring-batch/old.jpg
---

Los procesos batch han jugado un papel importante en las organizaciones desde hace mucho tiempo. Muchas tareas que no se podían asumir en aplicaciones online por ser muy pesadas, se posponían para se ejecutadas en horarios nocturnos por ejemplo. 

Actualmente, los procesos batch siguen guardando ese protagonismo, incluso puede que esté creciendo ya que también se utilizan 

Sin embargo, en procesos batch muy pesados o en volumenes de datos muy elevados, surge la duda si un proceso batch se va a ejecutar dentro de la ventana de tiempo establecida. Si el proceso batch supera los límites, tal vez se valoren otras soluciones basadas en arquitecturas distribuídas, tales como Map-Reduce o Spark. 

## Descripción de la prueba

Para quitarnos la duda de cuantos datos podemos procesar utilizando Spring Batch y cuánto tiempo tardaríamos hemos hecho unas pruebas de rendimiento utilizando un job muy sencillito que lee líneas de texto de un fichero CSV y los almacena en dos tablas diferentes de una base de datos.

![csv-to-tables](/assets/images/2019-09-03-rendimiento-spring-batch/csv-to-tables.png)

Una de las tablas contiene 53 columnas con 3 índices configurados y la otra tiene 12 columnas con 3 índices también. 

Asimismo, las pruebas se han repetido con diferentes cantidades de datos para ver el impacto en el tiempo. Empezamos con 50.000 registros en el fichero CSV para ir subiendo de manera progresiva hasta un 1 millón de registros. 

## Tamaño de chunk

Antes de presentar los resultados obtenidos en nuestras pruebas, vamos a explicar qué el parámetro `tamaño de chunk` y qué valor hemos aplicado. 

Spring Batch va ejecutando el proceso batcn en grupos de registros y el tamaño de chunk es el tamaño de dicho grupo de registros. En nuestro ejemplo, si el tamaño de chunk es de 10, se van leyendo registros del fichero csv de 10 en 10 para ir guardándolos en base de datos. 

En nuestra pruebas hemos probado diferentes tamaños de chunk (100, 500 y 1000) y en este post sólo vamos a recoger los resultados con el chunk de 500 ya que resultó ser la configuración que mejor nos rindió. 

## Resultados

### Ejecución secuencial

En la primera prueba programamos el proceso batch para que fuera guardando los registros en base de datos de manera secuencial. Más adelante vamos a repetir la prueba empleando múltiples hilos para valorar cuánto mejoran los tiempo si ejecutamos el proceso en paralelo.

En este modo de ejecución los resultados logrados fueron los siguientes:

| Nº de registros   | 50K | 100K | 250K | 500K | 1M  |
|-------------------|-----|------|------|------|-----|
| Tiempo total (sg) | 17  | 34   | 87   | 174  | 337 |

La primera conclusión que obtenemos es que el crecimiento en el tiempo es directamente proporcional a la cantidad de datos que vamos procesando. Por ejemplo, el tiempo para procesar un millon de registros es aproximádamente el diez veces el tiempo para procesar 100K de registros. 

En la siguiente gráfica podemos ver la diferencia en los tiempos obtenidos en todos los casos:

![rendimiento-mysql](/assets/images/2019-09-03-rendimiento-spring-batch/rendimiento.png)

En base a estos datos, podemos estimar que en un hora podemos leer hasta 10 millones de registros desde un fichero CSV y almacenarlos en dos tablas de base de datos. 

### Ejecución en paralelo (multithread)

Si ejecutando el proceso batch de manera secuencial el rendimiento que logramos no es suficiente, podemos acelerar el proceso ejecutándolo en paralelo mediante múltiples hilos. 

Para valorar la mejora con el multithreading, hemos repetido la prueba configurando el job con un threadpool de 4 hilos (nuestra máquina sólo tiene 2 cores y 4 threads). 

| Nº de registros   | 50K | 100K | 250K | 500K | 1M   |
|-------------------|-----|------|------|------|------|
| Tiempo total (sg) | 10  | 17   | 44   | 84   |  178 |

1 millón de registros leídos del CSV y almacenados en dos tablas (2 millones de inserts) en 178 segundos, apenas 3 minutos. ¡No está nada mal!

A continuación actualizamos la gráfica para comparar los tiempos de ejecución de ejecutar el job en un sólo hilo vs 4 hilos:

![rendimiento-multithread](/assets/images/2019-09-03-rendimiento-spring-batch/rendimiento-multithread.png)

La mejora es muy significativa si podemos permitirnos la ejecución de uno de los steps en paralelo utilizando más hilos. Es importante ser consciente que la ejecución en paralelo supone perder la característica de [restartability de Spring Batch](https://docs.spring.io/spring-batch/3.0.x/reference/html/configureJob.html#restartability). Esta funcionalidad consiste en que cuando falla la ejecución del proceso batch, si reiniciamos el job Spring Batch iniciará el proceso desde el registro que se produjo el error. De lo contrario, si restartability está deshabilitado, el reiniciar el proceso Spring Batch comenzará desde el inicio. 

## Resumen

No está nada mal tratándose de una máquina modesta y una instalación de base de datos por defecto, sin ningún tipo de optimización.

Un rendimiento más que suficiente para la mayoría de empresas que tengan que ejecutar tareas batch para procesar datos periódicamente y sin tener que montar un sistema basado en Hadoop, Spark o MapReduce.

Cuando se realizan pruebas de rendimiento, los datos pueden variar muchos por múltiple factores (versión de java, prestaciones de hw, etc). En nuestro caso las pruebas se han hecho sobre un MacBook Pro de principios de 2015, con un i7 de dos cores a 3,1GHz y 16 GB de RAM DDR3 a 1867 MHz, y se ha empleado la versión Java 8. Para poder contrastar los resultados obtenidos, hemos publicado el proyecto en [este repositorio](#) de Github con todas las instrucciones necesarias. 