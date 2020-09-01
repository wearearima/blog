---
layout: post
title:  "Utilizando Docker dentro de Kubernetes"
date:   2020-08-15 9:00:00
author: urko
lang: es
categories: docker, kubernetes
tags: docker, kubernetes, k8s, jenkins, privileged
header-image: 2020-09-15-docker-en-kubernetes/whale.jpg
---

En un [post anterior](){:target="_blank"} (TODO: enlace al post)hablé sobre el problema de otorgar privilegios a un contenedor y los riesgos que esto supone. Hoy quiero presentaros un caso concreto en el que se otorgan privilegios a un contenedor y algunas alternativas.

Una de las herramientas de Integración Contínua más populares es [Jenkins](https://www.jenkins.io/){:target="_blank"}. Destaca por la cantidad de *plugins* que su comunidad pone a disposición de los usuarios y la libertad que otorga para crear *pipelines*. Además, nos ofrece imágenes con las que podremos desplegarlo en contenedores, ¡incluso en un cluster Kubernetes!

Y hace esto deberia ser sencillo, ¿no? Escribes un despliegue que tenga un pod con la imagen de Jenkins y ya lo tienes (aparte de instalar plugins y configurarlo). Pero, ¿y si quiero hacer *building* de imágenes dentro de un *pipeline*?

Entonces necesitas Docker CLI o [Docker plugin for Jenkins](https://plugins.jenkins.io/docker-plugin/){:target="_blank"}. Pero estos a su vez necesitan que exista un Docker daemon al que poder hacer las peticiones que corresponda. La cosa se complica. 

En este post vamos a explorar, paso a paso, diferentes planteamientos para desplegar Jenkins con Docker en Kubernetes, y explicar la evolución que hay en cada uno.

## Despliegues

### 1. Docker in Docker

El despliegue más obvio es: ¿Que necesito un Docker daemon? Pues lo instalo. Coges la imagen base de Jenkins, instalas Docker Engine y creas una imagen personalizada con ambos programas.

Esto es posible, lo puedes probar y funciona. Pero tiene ciertas implicaciones que lo hacen una mala opción:

* **Drivers de almacenamiento**: Este problema surge por las incompatibilidades entre diferentes sistemas de ficheros de contenedores. Sin entrar en detalle, los contenedores utilizan sistemas de ficheros propios (AUFS, BTRFS, Device Mapper, ...) y estos pueden no ser compatibles entre sí. Según el tipo de sistema que utilice el *container runtime* del nodo y el que utilice el Docker daemon del contenedor, pueden ocasionarse problemas. Probablemente estas incompatibilidades se vayan solucionando según se publiquen nuevas versiones de DinD (Docker in Docker), pero el riesgo sigue latente.
* **Cache**: Si quieres usar la cache de Docker, que seguramente quieras, y quieres que esta caché sea accesible entre diferentes replicas, deberás montar `/var/lib/docker` como un volumen en cada contenedor. Pero Docker está pensado para tener acceso exclusivo a este directorio, y que dos o más daemons accedan a la vez puede acarrear problemas de corrupción de datos.
* **Seguridad**: Para poder ejecutar el Docker daemon dentro de un contenedor, es necesario ejecutarlo con privilegios (`--privileged` en Docker o `securityContext.privileged: true` en Kubernetes). **Es un requisito**. Eso implica serios riesgos de serguridad, explicamos en [este post](){:target="_blank"} (TODO: enlace al post).

<p align="center">
    <img src="/assets/images/2020-09-15-docker-en-kubernetes/dind.png">
</p>

### 2. Docker out of Docker

En esta variante, se utiliza el Docker Daemon del nodo del cluster. Para ello, hay que utilizar una imagen con Jenkins y Docker CLI, montar el socket desde el nodo al contenedor, y ejecutar el contenedor con un grupo que tenga acceso al socket.

Ventajas sobre Docker in Docker:

* Soluciona los problemas del driver de almacenamiento y de la cache, que son inherentes de Docker in Docker.
* No creamos más Docker daemons y reutilizamos el ya existente, lo que minimiza el uso de recursos.
* Evita utilizar contenedores privilegiados.

Aún así, también tiene sus problemas:

* Mantenemos los riesgos de seguridad, ya que al tener acceso al socket de Docker, podemos arrancar un contenedor privilegiado que nos dará acceso al *host* de manera sencilla.
* Montar directorios del nodo en un *pod* es una mala práctica. De hecho, en este caso en concreto, no podemos asumir que el socket de Docker vaya a existir en el nodo. Según el *container runtime* del cluster, puede que no exista, por lo que esta solución no se podría aplicar
  > Nota: A día de hoy (abril 2020), los tres mayores proveedores cloud de Kubernetes (AWS, Azure y Google Cloud) proveen nodos con el container runtime Docker, que sí que tiene socket de Docker. TODO: actualizar a septiembre
* Al estar usando el demonio del nodo, todos los contenedores que lancemos son hermanos del contenedor desde que los lanzamos. Esto trae riesgos de por sí, ya que pueden ocurrir problemas al dar nombres a los contenedores (nombrar dos contenedores igual, o dos volúmenes). Además, los contenedores que no se han ejecutado desde Kubernetes no están gestionados por Kubernetes, por lo que podemos llegar a problemas de asignación de recursos (el contenedor utiliza recursos del nodo pero Kubernetes no se da cuenta).

<p align="center">
    <img src="/assets/images/2020-09-15-docker-en-kubernetes/dood.png">
</p>

### 3. Docker in Docker sidecar

La última alternativa, consiste en desplegar dos contenedores en el mismo pod, uno con Jenkins y Docker CLI (igual que en Docker out of Docker) y otro con Docker Engine, y utilizar el socket TCP, ya que la red en el mismo pod es compartida.

Aunque en principio parezca que es dar un paso atrás, tiene una explicación: somos capaces de modificar las opciones del Docker daemon. ¿Y para que queremos eso? Podemos instalar *plugins* de autorización que impidan lanzar contenedores privilegiados en ese daemon (se explica en más detalle [en el post anterior](){:target="_blank"} (TODO: enlace al post)).

Ventajas sobre Docker out of Docker:

* Resolvemos los problemas de seguridad. Al no tener permisos para lanzar contenedores privilegiados ni se monta ningún directorio del nodo, el nodo está aislado del pod.

Desventajas:

* Damos un paso atrás y retomamos los posibles problemas de cache y de drivers de almacenamiento. 
* El contenedor con Docker Engine tendrá que ser ejecutado en modo privilegiado.

<p align="center">
    <img src="/assets/images/2020-09-15-docker-en-kubernetes/dind-sidecar.png">
</p>

## Conclusión

Ninguno de los métodos para desplegar Jenkins en Kubernetes es bueno. Todos conllevan riesgos de seguridad y ciertas pegas, y habrá que decidir cuál de ellas preferimos para nuestro despliegue. Si sirve de algo, en el [Helm chart oficial](https://github.com/helm/charts/tree/master/stable/jenkins){:target="_blank"} lo resuelven utilizando el método de montar el *socket* del nodo (DooD) y sin lanzar contenedores privilegiados, pero como hemos explicado, esto sigue teniendo riesgos de seguridad.

La recomendación es no usar Docker como herramienta de *building* de imágenes en Jenkins. Existen soluciones *dockerless* que evitan los problemas descritos en este documento sobre las que hablaremos en un futuro post.
