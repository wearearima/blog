---
layout: post
title:  "Contenedores como funciones en AWS Lambda Container"
date:   2021-05-14 9:00:00
author: urko
lang: es
categories: aws, serverless, cloud
tags: aws, serverless, cloud, faas, java, container
header-image: 2021-04-30-aws-lambda/cloud.jpg
---

Anteriormente hemos hablado de AWS Lambda y de cómo nos introduce al mundo *serverless* y de funciones en cloud. En este post, quiero explorar otra manera de crear funciones con AWS Lambda: **usar contenedores**.

## ¿Por qué contenedores?

Utilizar contenedores en AWS Lambda nos otorga las mismas funcionalidades que antes (autoescalado, pagar por uso, ...) pero nos ofrece mayor flexibilidad a la hora de personalizar nuestra aplicación y su entorno. Por ejemplo, podría darse el caso que los runtimes de AWS Lambda no sean compatibles con nuestra aplicación o que necesite una versión en concreto. También podría pasar que mi aplicación tenga dependencias con una arquitectura en concreto o que necesite utilizar algún recurso del sistema y queremos asegurnarnos de que está disponible.

Para estos casos y más, empaquetar nuestra función en un contenedor es la solución ideal. Podremos elegir el sistema operativo base o la versión concreta del runtime de nuestra aplicación.

## ¿Qué diferencias conlleva utilizar contenedores?

Aunque las similitudes son muchas, es verdad que tiene ciertas implicaciones que es importante tener en cuenta si queremos decidir utilizar contenedores. 

Por un lado, es obligatorio que nuestro contenedor implemente [la API de ejecución de AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-api.html){:target="_blank"}. Para ayudarnos con esta tarea, AWS nos provee de ciertas imágenes base que ya implementan esta API. Si esto no nos parece suficiente, también podemos crear nuestra imagen desde cero e instalar en ella el *Lambda Runtime Interface Client* que soporte nuestro lenguaje de programación. Para hacer esta tarea más sencilla, se puede realizar directamente desde la mayoría de gestores de paquetes de las distribuciones de Linux más populares.

Además de esto, el tamaño máximo de un paquete en Lambda es de 250MB, mientras que si utilizamos un contenedor, esta restricción de tamaño aumenta hasta 10GB. Puede que está sea otra razón más para utilizar AWS Lambda Containers. 

Por otra parte, utilizar contenedores implica tener que encargarnos de las vulnerabilidades que puedan tener y aplicar los respectivos parches de seguridad, un trabajo que AWS nos evitaba con AWS Lambda (incluso se podría discutir que utilizar contenedores deja de ser una experiencia *serverless* verdadera).

## Conclusiones

AWS Lambda Containers nos otorga mayor libertad a la hora de crear nuestras funciones, con la pega de que necesita que nos encarguemos del entorno donde se va a ejecutar nuestra función. Sin duda, habrá proyectos donde encaje y otros donde no tenga sentido utilizarlo, pero disponer de esta opción es beneficioso para todos y hace que AWS Lambda sea una herramienta mucho más completa.