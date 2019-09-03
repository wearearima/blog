---
layout: post
title:  "Spring Cloud Data Flow sucesor de Spring Batch Admin"
date:   2019-09-03 9:00:00
author: arkaitz
categories: mediator feature
tags: featured
header-image:	2017-01-15-view-rendering-performance/post-header2.jpg
---

Después de la “muerte” de Spring Batch Admin, toda la funcionalidad que nos ofrecía se ha movido a [Spring Cloud Data Flow](https://dataflow.spring.io/). 

Pero Spring Cloud Data Flow es un sistema más complejo y con más opciones a parte de lo puramente batch.

¿Cómo hacemos para instalar lo mínimo necesario para utilizarlo como sistema de gestión de nuestros jobs?

Vamos a ver primero qué es SCDF y los diferentes componentes que necesita para funcionar.

Por suerte, toda la parte de streaming del sistema se puede deshabilitar mediante propiedades de configuración. Con esto, nos evitamos tener que instalar Skipper.

Además, toda la parte de monitorización utilizando Prometheus y Grafana también nos la podemos quitar, ya que está más pensada para monitorizar temas de streaming.

Con todo esto, para una instalación en Kubernetes y tomando como ejemplo la guía de instalación oficial, los pasos a seguir serían los siguientes:

## Descargar el proyecto
Para instalar utilizando kubectl necesitamos descargarnos los ficheros de configuración para Kubernetes del repositorio oficial.

```
git clone https://github.com/spring-cloud/spring-cloud-dataflow
cd spring-cloud-dataflow
git checkout v2.1.2.RELEASE
````

## Escoger un sistema de colas de mensajes
Si queremos instalar RabbitMQ:

```
kubectl create -f src/kubernetes/rabbitmq/
```

Si por el contrario queremos utilizar Kafka:

```
kubectl create -f src/kubernetes/kafka/
```

## Desplegar MySQL
El proyecto que nos hemos descargado ya tiene los ficheros de configuración necesarios para desplegar una base de datos MySQL y configurar lo necesario:

```
kubectl create -f src/kubernetes/mysql/
``` 

## Quitar la configuración de Prometheus y Grafana
Para que el servidor no falle al arrancar, debemos quitar la configuración de Prometheus y Grafana que se encuentra en el fichero src/kubernetes/server/server-config.yaml. La sección que debemos eliminar es la siguiente:

``` 
applicationProperties:
  stream:
    management:
      metrics:
        export:
          prometheus:
            enabled: true
      endpoints:
        web:
          exposure:
            include: 'prometheus,info,health'
    spring:
      cloud:
        streamapp:
          security:
            enabled: false
grafana-info:
  url: 'https://grafana:3000'
```

## Crear los roles y el service account
Para crear los roles necesarios y asociarlos debemos ejecutar los siguientes comandos:

```
kubectl create -f src/kubernetes/server/server-roles.yaml
kubectl create -f src/kubernetes/server/server-rolebinding.yaml
kubectl create -f src/kubernetes/server/service-account.yaml
```

## Desactivar la opción de streaming de SCDF
Para desactivar todo lo relacionado con las tareas de streaming de SCDF tenemos que añadir una propiedad en uno de los ficheros de configuración del servidor.

El fichero a modificar es src/kubernetes/server/server-deployment.yaml y tenemos que añadir lo siguiente en la sección env:

```
- name: SPRING_CLOUD_DATAFLOW_FEATURES_STREAMS_ENABLED
         value: 'false'
```         

## Desplegar SCDF server
Con todo esto sólo nos queda desplegar el servidor de SCDF, para esto, ejecutamos los siguientes comandos:

```
kubectl create -f src/kubernetes/server/server-config.yaml
kubectl create -f src/kubernetes/server/server-svc.yaml
kubectl create -f src/kubernetes/server/server-deployment.yaml
```

Para ver la ip asignada y poder entrar al dashboard ejecutamos el comando

```
kubectl get svc scdf-server
```

El valor indicado en EXTERNAL-IP es el que tenemos que utilizar.

Si estás probando a instalarlo usando Minikube, el EXTERNAL-IP lo verás como pending ya que no soporta LoadBalancer. Para saber la URL que tienes que utilizar para conectarte al servidor utiliza el comando siguiente:

```
minikube service --url scdf-server
```
