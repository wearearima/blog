---
layout: post
title:  "Kubernetes ha deprecado Docker"
date:   2020-12-04 9:00:00
author: telle
lang: es
categories: kubernetes, docker
tags: kubernetes, docker, cri, containerd, cri-o
header-image: 2020-12-01-tarugo20/header.jpeg
---

Recientemente se anunció a través del [changelog de la versión 1.20.0-rc0 de Kubernetes](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.20.md#deprecation) que en la próxima versión se depreca el soporte a Docker y que en futuras versiones será eliminado. 

[imagen]

Aunque el anuncio explica que ya tenemos una solución, que consiste en migrar de Docker a una implementación de CRI, parece que es un cambio de mucho calado y entre los usuarios de Kubernetes han surgido dudas y cuestiones sobre el impacto que este cambio puede suponer: ¿van a dejar de funcionar mis imágenes Docker? o ¿puedo seguir construyendo mis imágenes con Docker?

Este post intenta aportar su granito de arena para despejar las dudas que hayan podido surgir, pero para ello previamente necesitamos explicar algunos conceptos del anuncio que nos pueden resultar desconocidos, como CRI y DockerShim. 

Kubernetes es un orquestador de contenedores y una de sus tareas es descargar imágenes, arrancar y parar contenedores. El elemento que se ocupa de esta tarea en Kubernetes se llama Container Runtime y el que utilizaba Kubernetes en sus inicios era [Docker](https://docs.docker.com/engine/). Sin embargo, en la comunidad existían otros Container Runtimes además de Docker, como por ejemplo [Rkt de Coreos](https://coreos.com/rkt/). 

Con el objetivo de lograr que Kubernetes pudiera trabajar con otros Container Runtimes, no sólo con Docker, crearon el API “Container Runtime Interface” (CRI) y se incluyó en Kubernetes en la versión 1.5 , allá por el año 2016. Mediante CRI, Kubernetes se abstrae del Container Runtime que se utiliza en el cluster y le permite integrarse con múltiples Container Runtimes de manera transparente, por ejemplo ContainerD, CRI-O, etc. 

El siguiente diagrama explica de manera gráfica y a alto nivel cómo es la comunicación de Kubernetes a través de CRI. 

[imagen]

Dado que Docker no es CRI compliant, se desarrolló el componente docker-shim que hace de interlocutor entre las dos partes que sea posible utilizar Docker dentro de Kubernetes. 

Este nuevo anuncio sobre deprectar Docker en Kubernetes, implica que en el futuro se eliminarán los elementos DockerShim y Docker dentro de Kubernetes y sólo estarán disponibles los elementos que son CRI compliant, como por ejemplo ContainerD o CRI-O. 

Una vez explicado algunos conceptos de Kubernetes, las respuestas a las dudas y preguntas del inicio son:

- ***¿Las imágenes con formato Docker seguirán funcionando a partir de la versión 1.20 de Kubernetes?***

Sí. Todas las implementaciones de CRI que existen actualmente soportan imágenes con formato Docker y OCI.

- ***¿Puedo continuar utilizando Docker para crear las imágenes de contenedores?***

Sí. Puedes seguir creando las imágenes de manera tradicional con el CLI de Docker y el fichero Dockerfile. 

- ***¿Puedo utilizar el stack de Docker para el desarrollo en local?***

Sí. La desaparición de Docker es sólo dentro de Kubernetes. Puedes seguir utilizando Docker y sus herramientas, como docker-compose, para tus pruebas y desarrollos en tu equipo o servidor CICD como hasta ahora. 

- ***¿A qué implementación de CRI debería migrar?***

Dependerá de cada caso y el proveedor de Kubernetes que se esté utilizando. Si utilizas OpenShift probablemente la recomendación sea utilizar CRI-O. En el resto de los casos, lo más fácil será migrar a Containerd porque el propio engine de Docker utiliza internamente Containerd desde la versión 1.11 (en la gráfica anterior he hecho una pequeña trampa porque he omitido una flecha que nace en Docker y apunta a Containerd para simplificar y no confundir :-). 

- ***Pero entonces, ¿por qué tanto revuelo con esta noticia?***

Primero, por el susto que uno se lleva cuando lee que Docker está deprecado. Pero eso ya hemos explicado que está deprecado sólo en Kubernetes y que podemos seguir utilizándolo para desarrollo sin problemas como hasta ahora. 

Y segundo, porque Docker es el Container Runtime más utilizado en Kubernetes, a pesar de que CRI y sus implementaciones están disponibles desde hace mucho tiempo. Estos son datos de un informe del 2019:

[imagen]

El anuncio supone que todos estos usuarios del runtime de Docker tendrán que migrar a una implementación de CRI y las migraciones generalmente implican trabajo. 

En principio, para la mayoría de usuarios de Kubernetes el cambio se supone que va a ser transparente porque las implementaciones de CRI también soportan las imágenes Docker. Sin embargo, sí puede haber situaciones donde la migración a CRI tenga impacto y suponga cambios en la infraestructura. 

Por ejemplo, instalaciones de Kubernetes con contenedores que acceden al daemon de Docker del host mediante técnicas “Docker out of Docker” sí se verán afectadas. Este tipo de técnicas ya no serán posibles ya que el demonio de Docker ya no existirá en las instalaciones de Kubernetes. Si tenéis curiosidad sobre cómo funciona “Docker out of Docker” y otras técnicas similares, podéis consultar [este post de Urko](https://blog.arima.eu/2020/11/11/docker-en-kubernetes.html). 

Por tanto, **Docker no ha muerto**, lo único que va a ocurrir es que Docker (y su daemon) no  van a estar disponibles en las próximas versiones de Kubernetes. Por el momento este cambio sólo va a suponer un aviso en los logs pero tenemos que ir migrando a una implementación de CRI (o quedarnos estancados en una versión obsoleta de Kubernetes, cosa que no os recomendamos). 

Espero que el post haya servido de ayuda para resolver las dudas sobre Docker en Kubernetes. ¡Buena suerte con la migración! :-)
