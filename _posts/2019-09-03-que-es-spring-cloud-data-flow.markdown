---
layout: post
title:  "Qué es Spring Cloud Data Flow"
date:   2019-09-03 8:00:00
author: arkaitz
categories: mediator feature
tags: featured
header-image:	2019-09-03-spring-cloud-data-flow/background-beach-color.jpg
---

Descripción de la problemática de gestión de procesos batch y streaming. La diferencia entre un proceso batch y un proceso de streaming es que los procesos batch reciben una cantidad finita de datos, mientras que los procesos de streaming reciben datos de manera indefinida. Los procesos batch, llamados Task en el dashboard de SCDF, son tareas que duran poco tiempo (pueden ser minutos o horas). Reciben una cantidad definida de datos, los procesan y acaban.

Spring Cloud Data Flow (SCDF) es una aplicación para adminitrar de manera visual los procesos batch y streaming y ofrece las siguientes funcionalidades:
- Monitorización
- Arranque y parada de procesos
- Definición de flujos de datos avanzados compuestos de múltiples procesos. (workflos de job)
- API Rest

Aparte 

Spring Cloud Data Flow (SCDF) es un sistema de procesamiento de datos basado en microservicios pensado para sistemas cloud como Cloud Foundry y Kubernetes (aunque también es posible hacer una instalación en local mediante docker compose).

Aunque aparentemente SCDF parezca ser una aplicación web sencilla, en realidad se basa en una infraestructura relativamente compleja compuesta por múltiples componentes. Es importante conocer el propósito de cada componente:

## Spring Cloud Data Flow Server

Es la parte más visual de SCDF ya que se trata del frontend web que utilizamos para administrar y monitorizar los procesos batch y de streaming. 

Generalmente estos procesos se desarrollan sobre el framework [Spring Batch](https://spring.io/projects/spring-batch) para luego ser encapsulados en fat jars de Spring Boot. Para desplegar las aplicaciones Spring Boot en SCDF, es necesario  previamente publicar los binarios en un repositorio de Maven al que tenga acceso SCDF. Una vez publicados en el repositorio de Maven, sólo hace falta indicar la información del artefacto en SCDF. 

![dar-de-alta-artefacto-maven](/assets/images/2019-09-03-spring-cloud-data-flow/create-stream.png)

También existe la posibilidad de que desplegar contenedores de Docker en SCDF. 

<iframe width="420" height="315" src="http://www.youtube.com/embed/MgQyI-oDWD8" frameborder="0" allowfullscreen></iframe>

La información de todas las ejecuciones se quedan guardadaMantiene un historial detallado de todas las ejecuciones de tareas o jobs.

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

El dashboard nos ofrece una interfaz gráfica para la gestión de todo el sistema pero SCDF también ofrece un API REST para crear, desplegar y ejecutar streams o tareas batch.