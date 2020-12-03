---
layout: post
title:  "Buenas prácticas para crear Dockerfiles en proyectos Java"
date:   2020-03-09 9:00:00
author: telle
categories: docker, containers, java
tags: docker, containers, java, contenedores
header-image: 2020-02-11-java-en-contenedores-docker/fondo-cafe-min.jpg
---

Utilizar la jre para ejecutar sino se va a compilar. 

Fijar versión del from, no usar lates, qué es latest. 

Builds reproducibles:
- Prevent incosistencies between environments
- The "source of truth" is the source code, not the build artifact

Diferentes versiones de Openjdk, cada uno con un tamaño diferente:
- jre
- jre-slim
- jre-alpine

¿Qué diferencias hay? ¿Cuál es el criterio para elegir la jre?

Además, también existen otras distribuciones de java. 

El usuario que ejecuta la imagen?

tags y sha hash??



