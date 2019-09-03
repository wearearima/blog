---
layout: post
title:  "Rendimiento de Spring Batch"
date:   2019-09-03 10:00:00
author: arkaitz
categories: mediator feature
tags: featured
header-image:	2017-01-15-view-rendering-performance/post-header2.jpg
---

Para quitarnos la duda de cuantos datos podemos procesar utilizando Spring Batch y cuánto tiempo tardaríamos hemos hecho unas pruebas de rendimiento utilizando un job muy sencillito que lee líneas de texto de un fichero CSV y los almacena en dos tablas diferentes de una base de datos.

Una de las tablas contiene 53 columnas y tiene índices en 3 de ellas y la otra tiene 12 columnas e índices en 3 de ellas también.

El proyecto con el job lo podéis encontrar en este repositorio, donde podéis ver también el esquema de la base de datos que hemos utilizado.

El sistema en el que se han hecho las pruebas ha sido un MacBook Pro de principios de 2015, con un i7 de dos cores a 3,1GHz y 16 GB de RAM DDR3 a 1867 MHz (fácilmente superable con cualquier máquina de hoy en día).

Las bases de datos utilizadas han sido MySQL y Postgresql para así de paso ver la diferencia de rendim201iento entre las dos, si lo hubiera.

Las pruebas se han realizando con diferentes tamaños de chunk, 100 y 500 (hicimos la prueba con 1000 pero no notamos nada de mejoría en nuestra máquina) y aumentando el número de líneas que se leen del fichero CSV en cada ejecución para ver cuántos segundos tarda en almacenar los datos en la base de datos.

## Resultados utilizando Postgresql

|     | 50K | 100K | 250K | 500K | 1M  |
|-----|-----|------|------|------|-----|
| 100 | 19  | 43   | 95   | 198  | 445 |
| 500 | 17  | 34   | 87   | 174  | 337 |

Nos cuesta 337 segundos (5 minutos y medio) en leer 1 millón de registros de un CSV y almacenarlos en dos tablas de la base de datos.

Viendo este artículo de @jerolba y la mejora de rendimiento que conseguía activando el parámetro reWriteBatchedInserts repetimos la prueba del mejor de los casos anterior con este parámetro a true:

|     | 50K | 100K | 250K | 500K | 1M   |
|-----|-----|------|------|------|------|
| 500 | 16  | 31   | 79   | 155  |  322 |

La mejora no es mucha pero algo se nota, 1 millón de registros en 322 segundos.

## Resultados utilizando MySQL

Instalamos una base de datos MySQL y repetimos de nuevo el mejor de los casos pero utilizando esta base de datos:

|     | 50K | 100K | 250K | 500K | 1M   |
|-----|-----|------|------|------|------|
| 500 | 31  | 60   | 153  | 308  |  704 |

Un millón de registros leídos de un CSV y almacenados en base de datos en 704 segundos. Aquí la diferencia con postgresql es muy grande, el doble de tiempo necesario.

Igual que en el caso de postgres repetimos la prueba con el parámetro rewriteBatchedStatements a true:

|     | 50K | 100K | 250K | 500K | 1M   |
|-----|-----|------|------|------|------|
| 500 | 19  | 33   | 88   | 172  |  441 |

La mejora de rendimiento es muy grande en el caso de MySQL al activar este parámetro, 1 millón de líneas almacenadas en 441 segundos. Nos acercamos bastante al rendimiento de Postgres pero sin superarlo.

En la siguiente gráfica podemos ver la diferencia en los tiempos obtenidos en todos los casos:

![rendimiento-mysql](/assets/images/2019-09-04-rendimiento-spring-batch/rendimiento.png)

## Ejecución en paralelo (multithread)

Después de estas pruebas, en las que el step del job se ejecutaba en único hilo, hicimos la prueba de configurar el step para que se ejecute utilizando un threadpool de 4 hilos (nuestra máquina sólo tiene 2 cores y 4 threads). 

En las dos bases de datos mantenemos el rewriteBatch activado con el que hemos conseguido los mejores resultados.

### Postgresql

|     | 50K | 100K | 250K | 500K | 1M   |
|-----|-----|------|------|------|------|
| 500 | 10  | 17   | 44   | 84   |  178 |

1 millón de registros leídos del CSV y almacenados en dos tablas (2 millones de inserts) en 178 segundos, apenas 3 minutos. ¡No está nada mal!

### MySQL

|     | 50K | 100K | 250K | 500K | 1M   |
|-----|-----|------|------|------|------|
| 500 | 9   | 19   | 50   | 94   |  235 |

1 millón de registros leídos del CSV en 235 segundos, casi 4 minutos.

Comparamos los tiempos de ejecución de ejecutar el job en un sólo hilo vs 4 hilos:

![rendimiento-multithread](/assets/images/2019-09-04-rendimiento-spring-batch/rendimiento-multithread.png)

La mejora es muy significativa si podemos permitirnos la ejecución de uno de los steps en paralelo utilizando más hilos para ello. El inconveniente de ejecutar así los steps es que perdemos la opción de reiniciar el job desde el punto en el que falló en el caso de haber tenido algún problema.

Resumiendo, en el mejor de los casos, con un tamaño de chunk de 500, base de datos Postgresql y ejecutando el step en 4 hilos somos capaces de leer 1 millón de líneas de un CSV y almacenarlos en base de datos (2 millones de inserts) en 178 segundos.

No está nada mal tratándose de una máquina modesta y una instalación de base de datos por defecto, sin ningún tipo de optimización.

Un rendimiento más que suficiente para la mayoría de empresas que tengan que ejecutar tareas batch para procesar datos periódicamente y sin tener que montar un sistema basado en Hadoop, Spark o MapReduce.
