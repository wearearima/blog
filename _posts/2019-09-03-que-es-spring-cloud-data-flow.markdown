---
layout: post
title:  "Qué es Spring Cloud Data Flow"
date:   2019-09-03 8:00:00
author: arkaitz
categories: mediator feature
tags: featured
header-image:	2017-01-15-view-rendering-performance/post-header2.jpg
---

Spring Cloud Data Flow es un sistema de procesamiento de datos basado en microservicios pensado para sistemas cloud como Cloud Foundry y Kubernetes (aunque también es posible hacer una instalación en local mediante docker compose).

Con spring cloud data flow podemos crear complejos flujos de datos tanto para streaming como para batch. Estos flujos de datos consisten en diferentes aplicaciones Spring Boot que se conectan entre sí y se desarrollan utilizando los frameworks [Spring Cloud Stream](https://spring.io/projects/spring-cloud-stream) o [Spring Cloud Task](https://spring.io/projects/spring-cloud-task).

Las tareas batch, llamadas Task en el dashboard de SCDF, son tareas que duran poco tiempo (pueden ser minutos o horas). Reciben una cantidad definida de datos, los procesan y acaban.

Estos task pueden ser aplicaciones Spring Batch, con sus diferentes steps, readers o writers y desde el dashboard de SCDF seremos capaces de ver el resumen de las ejecuciones de estos jobs, si han ido bien o mal y de volver a arrancarlos si fuera necesario.

Con SCDF se pueden definir tareas compuestas, muy útiles para cuando tienes que ejecutar más de una tarea, una detrás de la otra de forma secuencial. El servidor se encarga de que una tarea no se ejecute hasta que la anterior acabe y se cumpla la condición que hayamos definido.

![scdf-create-task](/assets/images/2019-09-03-spring-cloud-data-flow/create-task.png)

Las tareas de streaming son tareas que siempre están en marcha, a la espera de que les lleguen datos a procesar.

Mediante el dashboard de SCDF podemos crear el flujo que procesamiento de estas tareas de streaming, conectando las diferentes salidas y entradas hasta obtener el resultado que queramos.

![scdf-create-task-2](/assets/images/2019-09-03-spring-cloud-data-flow/create-stream.png)

Spring ya tiene una serie de aplicaciones de ejemplo, tanto [stream](https://cloud.spring.io/spring-cloud-stream-app-starters/) como [task](https://cloud.spring.io/spring-cloud-task-app-starters/), que podemos desplegar en nuestro servidor de forma sencilla y empezar a hacer pruebas con diferentes orígenes de datos, procesados y destinos de almacenamiento.

El dashboard nos ofrece una interfaz gráfica para la gestión de todo el sistema pero SCDF también ofrece un [API REST](https://docs.spring.io/spring-cloud-dataflow/docs/current/reference/htmlsingle/#api-guide-resources) para crear, desplegar y ejecutar streams o tareas batch.

Para el correcto funcionamiento de todo el sistema SCDF necesita de los siguientes productos:

## Spring Cloud Data Flow Server
El servidor principal del sistema y encargado de parsear, validar y guardar las definiciones de los streams y tareas.

Es capaz de registrar ficheros .jar o imágenes de docker para poder utilizarlos después en la definición de stremas o task.

Mantiene un historial detallado de todas las ejecuciones de tareas o jobs.

## Spring Cloud Skipper Server
Skipper es una herramienta para gestionar el despliegue de aplicaciones Spring Boot a diferentes plataformas cloud.

SCDF delega en skipper toda la parte de streaming del servidor, este se encarga de gestionar el ciclo de vida de los streams, del despliegue de los mismos, actualizaciones o rollbacks.

## Base de datos
SCDF necesita configurada una base de datos relacional para guardar el historial de las aplicaciones desplegadas, sus ejecuciones y logs.

Por defecto, SCDF trae los drivers para funcionar utilizando MySQL, Postgres, H2, Oracle, DB2 y SqlServer.

## Sistema de colas de mensajes
Para que las aplicaciones desplegadas en el sistema puedan comunicarse entre sí, es necesario la instalación de un sistema de encolado de mensajes.

SCDF viene preconfigurado para poder utilizar RabbitMQ o Kafka. Podemos instalar cualquiera de las dos opciones.

## Prometheus y Grafana
Para la monitorización del sistema se utilizan Prometheus, encargado de sacar las diferentes métricas, y Grafana para generar diferentes dashboards para consultar estos datos.