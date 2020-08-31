---
layout: post
title:  "¿Deberías utilizar contenedores privilegiados?"
date:   2020-08-01 9:00:00
author: urko
lang: es
categories: docker
tags: docker
header-image: 2020-04-21-buenas-practicas-para-escribir-un-dockerfile/skyline.jpg
---

Al trabajar con contenedores es importante tener siempre en cuenta la seguridad del contenedor, o más importante, de la máquina que lo ejecuta. Una mala decisión a la hora de desplegar un contenedor puede otorgarle acceso total sobre el *host*, y esto puede tener consecuencias negativas si este contenedor tiene un propósito malicioso o si una persona no autorizada consigue acceso a él.

Al leer sobre buenas prácticas a seguir a la hora de lanzar contenedores, una de las recomendaciones más comunes es: "*No ejecutes el contenedor en modo privilegiado y dale únicamente las capacidades que necesite, a poder ser ninguna*". Es una buena recomendación, pero surgen algunas preguntas:
* ¿Qué es el modo privilegiado? 
* ¿Por qué no se recomienda no utilizarlo y qué es posible hacer con un contenedor privilegiado?
* ¿Es necesario ser un usuario privilegiado (*root*) o cualquier usuario dentro de un contenedor privilegiado es peligroso?
* ¿Existe alguna manera de evitar que se lancen contenedores privilegiados?

## ¿Qué es el modo privilegiado?

Los contenedores se inician con una serie de capacidades de Linux por defecto. Además de las que vienen por defecto, hay muchas otras que se pueden añadir a nuestro contenedor con la opción `--cap-add=`. La lista completa de las capacidades y lo que hacen se puede ver en la [documentación oficial](https://docs.docker.com/engine/reference/run/#runtime-privilege-and-linux-capabilities){:target="_blank"}. Al iniciar el contenedor en modo privilegiado, se le otorgan todas las capacidades, además de acceso a todos los dispositivos del *host* y se hacen ciertos cambios a AppArmor o SELinux, todo esto para darle al contenedor un acceso similar al que tienen el resto de procesos en el *host*.

<p align="center">
    <img src="/assets/images/2020-09-01-deberias-utilizar-contenedores-privilegiados/no-devices.png">
</p>

<label style="text-align: center; display: block;">Lista de dispositivos de un contenedor</label>

<p align="center">
    <img src="/assets/images/2020-09-01-deberias-utilizar-contenedores-privilegiados/devices.png">
</p>

<label style="text-align: center; display: block;">Lista de dispositivos de un contenedor **en modo privilegiado**</label>

## ¿Por qué no se recomienda no utilizarlo y qué es posible hacer con un contenedor privilegiado?

Por definición, un contenedor debe estar aislado del anfitrión donde se está ejecutando. Esto implica que debe tener un árbol de directorios diferente, usuarios y grupos propios, dispositivos propios..., hasta los recursos *hardware* de la máquina pueden ser diferentes. Todo esto para que un proceso ejecutándose en un contenedor no sepa que existe un anfitrión, y que ese contenedor y sus procesos no dependan del anfitrión.

Al ejecutar un contenedor privilegiado, rompemos este aislamiento, ya que el contenedor consigue acceso a los recursos y dispositivos del anfitrión, y además tiene todos los permisos posibles para tratar con ellos. Esto permite, entre otras cosas, realizar acciones como:
* Modificar el sistema de ficheros del anfitrión.
* Control sobre los procesos del anfitrión.
* Permisos para asignación de recursos del anfitrión.

## ¿Es necesario ser un usuario privilegiado (*root*) o cualquier usuario dentro de un contenedor privilegiado es peligroso?

En principio, todas las acciones que hemos listado requieren de privilegios de administrador dentro del contenedor para realizarse. Esto hace que, en teoría, un usuario no privilegiado dentro de un contenedor privilegiado no sea capaz de romper este aislamiento. 

Sin embargo, es común encontrarse imágenes (y crearlas) donde el usuario por defecto es un usuario con privilegios (normalmente *root*). Muchas veces esto es así por desconocimiento del creador de la imágen, porque el creador prefiere delegar la responsabilidad de modificar el usuario, o porque la imagen necesita ejecutar un proceso con un usuario privilegiado.

<p align="center">
    <img src="/assets/images/2020-09-01-deberias-utilizar-contenedores-privilegiados/top5.png" height="420">
</p>

<label style="text-align: center; display: block;">Las cinco imágenes más populares de Docker Hub tienen un usuario privilegiado por defecto</label>

Además, también se han encontrado vulnerabilidades ([CVE-2019-5736 detectado en febrero de 2019](https://blog.dragonsector.pl/2019/02/cve-2019-5736-escape-from-docker-and.html){:target="_blank"}) donde un usuario sin privilegios es capaz de explotar las capacidades de un contenedor privilegiado y acceder al anfitrión. Aunque mucho menos común que el caso de los usuarios privilegiados, es un riesgo a tener en cuenta, porque si ha habido una, pueden detectarse más.

## ¿Existe alguna manera de evitar que se lancen contenedores privilegiados?

Existen *plugin*s que se instalan en el Docker daemon que permiten extender las funcionalidades del proceso. Para este caso en concreto, nos interesan los [*plugin*s de autorización](https://docs.docker.com/engine/extend/plugins_authorization/){:target="_blank"}. Como dicen en la documentación de Docker, la autorización por defecto de `dockerd` es "todo o nada", es decir, o se tiene acceso al daemon y es posible hacer cualquier cosa, o no se tiene acceso a él.

> Nota: Docker daemon o `dockerd` es un proceso que se ejecuta en el anfitrión y que se encarga de gestionar los contenedores del mismo.

Con los *plugin*s de autorización tenemos la libertad de definir políticas que permiten regular el acceso de manera granular, dando permiso, por ejemplo, a un usuario en concreto a realizar ciertas acciones que otros no pueden. Y, ¿qué tiene esto que ver con los privilegios de un contenedor?

Bien, cada *plugin* trabaja de una manera diferente, pero todos acaban haciendo lo mismo: interceptan la llamada a la API del daemon y comprueban si esa llamada tiene permiso de ser ejecutada o no, según las políticas que hayamos definido. Es decir, podremos **permitir que solo se ejecuten las llamadas que NO intenten lanzar contenedores privilegiados**.

Para hacer una demostración hemos escogido el *plugin* [opa-docker-authz](https://github.com/open-policy-agent/opa-docker-authz){:target="_blank"}, que permite de manera sencilla y muy visual definir esta regla en concreto.

```rego
 package docker.authz

 default allow = false

 allow {
     not deny
 }

 deny {
     privileged
 }

 privileged {
     input.Body.HostConfig.Privileged == true
 }
```

El documento `input` corresponde al cuerpo de la llamada hecha a la API de Docker. Es decir, si este cuerpo contiene un atributo llamado `Body.HostConfig.Privileged` con valor `true`, denegaremos la llamada. Esto es solo un ejemplo, se pueden crear políticas mucho más elaboradas para cada caso en concreto.

Como hemos visto antes, el mayor riesgo de seguridad viene al permitir utilizar el modo privilegiado de los contenedores, por lo que con un *plugin* como este podríamos securizar nuestra instalación en gran medida. 

> Deberíamos añadir esto?: Instalar un *plugin* así en un Docker daemon en un cluster Kubernetes puede ser más complicado, por lo que podéis ver un ejemplo en este [repositorio](https://github.com/UrkoLekuona/unprivilegedDinD){:target="_blank"}, donde creo dos imágenes, una con el daemon ya configurado y otra con un cliente (servidor jenkins con docker cli instalado) que utiliza el docker daemon.

## Conclusiones

**Utilizar un usuario privilegiado o darle capacidades de Linux a un contenedor es siempre poco recomendable**. Dicho esto, hay ocasiones en las que no queda alternativa. Hay que intentar otorgar el mínimo número de prioridades posibles a un contenedor, las suficientes para que cumpla su función y ninguna más. 

El modo privilegiado de un contenedor debería usarse lo menos posible, en entornos cerrados donde sabemos qué personas van a tener acceso a ese contenedor y confiamos en ellas. En caso de que haya riesgo de que un usuario en el que no confiemos acceda al contenedor, deberíamos descartar el modo privilegiado, para prevenir problemas. Si es necesario otorgar permisos a un usuario para crear contenedores, se recomienda securizar el `dockerd` del anfitrión con un plugin de autorización.
