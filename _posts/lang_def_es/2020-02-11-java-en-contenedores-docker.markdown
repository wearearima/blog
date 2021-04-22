---
layout: post
title:  "¿Es viable ejecutar Java en contenedores Docker?"
date:   2020-02-11 9:00:00
author: telle
lang: es
categories: docker, containers, java
tags: docker, containers, java, contenedores
header-image: 2020-02-11-java-en-contenedores-docker/fondo-cafe-min.jpg
---

En nuestro alrededor existen muchas empresas que llevan años trabajando sobre Java utilizando un stack tecnológico tradicional (Spring, Tomcat, Weblogic, JPA, etc). Esta infraestructura ha sido bastante estable en el tiempo y ha sufrido pocos cambios.

Sin embargo, reciemente han surgido nuevas infraestructuras cloud basadas en Kubernetes ([Azure](https://azure.microsoft.com/en-us/free/kubernetes-service/){:target="_blank"}, [Openshift](https://www.redhat.com/es/technologies/cloud-computing/openshift){:target="_blank"}, [Amazon EKS](https://aws.amazon.com/es/eks/){:target="_blank"}, etc) y estas empresas ahora se encuentran en proceso de evaluación o transición a Kubernetes. En este proceso, surgen dudas y se cuestiona por ejemplo, si el stack tecnológico empleado hasta ahora sigue siendo valido en estos nuevos entornos  cloud. 

En estos casos, como suele ser habitual, solemos echar mano de Google para consultar cómo es la transición de los proyectos Java a Kubernetes. Sorprendentemente nos encontramos artículos y presentaciones que nos pueden asustar a dar el salto a Kubernetes. Por ejemplo, [Nobody puts Java in a container](https://jaxenter.com/nobody-puts-java-container-139373.html){:target="_blank"} o [Nobody puts Java in the container](https://vimeo.com/181900266){:target="_blank"}. 

![Nobody puts java in containers](/assets/images/2020-02-11-java-en-contenedores-docker/no-body-puts-java-in-a-container.png)

Visto esto, a todos nos viene la misma pregunta a la cabeza: ¿es viable ejecutar Java en contenedores Docker?

## Java Ergonomics

La plataforma Java se creó en el año 1995 y un poco más tarde vinieron los servidores web y servidores de aplicación para desarrollar aplicaciones Web sobre Java. En aquel entonces no existía el concepto de [contenedor](https://www.docker.com/resources/what-container){:target="_blank"} ni tampoco el movimiento [cloud native](https://www.cncf.io/){:target="_blank"}. Lo habitual era que el servidor de aplicaciones Java se ejecutara en una máquina dedicada y en dicho servidor se desplegaban múltiples aplicaciones Web (wars o ears). 

<p align="center">
    <img src="/assets/images/2020-02-11-java-en-contenedores-docker/servidor-java-ee.png">
</p>

Java fue diseñado para ejecutarse sobre este tipo de infraestructuras, una única JVM en un servidor. En base a esto, la JVM ejecuta el proceso [Java Ergonomics](https://docs.oracle.com/javase/8/docs/technotes/guides/vm/gctuning/ergonomics.html){:target="_blank"} que calcula los parámetros de configuración de JVM en función de los recursos HW disponibles en la máquina. Por ejemplo, Java Ergonomics establece el tamaño de heap máximo de JVM como la cuarta parte de la RAM del servidor. Es decir, en un servidor con 64GB de RAM el tamaño máximo del Heap es 16GB por defecto. 

Todo bien hasta ahora. Un servidor para cada JVM y Java Ergonomics configura la JVM en base a los recursos del servidor. Pero, ¿qué ocurre si ejecutamos Java Ergonomics en un contenedor Docker?

## Primeras experiencias de Java en Docker

Cuando ejecutamos una aplicación Java en un contenedor, nos interesa que Java Ergonomics calcule los parámetros de JVM en función de los recursos del propio contenedor. Por ejemplo, si arrancamos un contenedor con 4GB de memoria, esperamos que Java Ergonomics establezca 1GB de heap máximo. 

Sin embargo, las primeras experiencias de Java en contenedores demostraron que eso no era así. Java Ergonomics continuaba configurando la JVM en base a los recursos del servidor en lugar de los recursos del contenedor. Es decir, si el servidor tiene 64GB de RAM, se establecía 16 GB de heap máximo, en lugar de 1GB que se esperaba. Esto hacía que al escalar una aplicación, por ejemplo a 5 contenedores, se agotara toda la memoria del servidor porque la suma del heap de todos los containers superaba la memoria del servidor (16GB * 5 > 64GB). 

La manera de solventar esto consistía en utilizar los flags de configuración de Java Ergonomics (-Xmx, -Xms, etc), pero algunos se dieron cuenta demasiado tarde, cuando la aplicación que tenían en producción estaba sufriendo caídas y problemas de memoria OOMKilled. Este tipo de problemas motivaron los artículos antes citados que advertían del riesgo que implicaba ejecutar Java en contenedores. 

## Java Container Aware

Conocidos los problemas de Java Ergonomics con los contenedores Docker, [Oracle reaccionó](https://blogs.oracle.com/java-platform-group/java-se-support-for-docker-cpu-and-memory-limits){:target="_blank"} e implementó un soporte de contenedores experimental en las versiones Java 8u131 y Java 9. Sin embargo, este soporte experimental tenía carencias que finalmente fueron resueltas en las versiones Java 8u191 y Java 10. 

A partir de estas versiones, Java Ergonomics calcula automáticamente la configuración de JVM en base a los recursos del contenedor. Si queréis probar las diferencias entre versiones diferentes de Java en contenedores, podéis jugar con este [repositorio](https://github.com/wearearima/docker-java-cpu-memory-limit){:target="_blank"}. 

Asimismo, también se añadieron nuevas opciones de configuración en la JVM para ajustar mejor la configuración del heap en un contenedor: `InitialRAMPercentage`, `MaxRAMPercentage` y `MinRAMPercentage`. 

Con todos estos cambios, ya se considera que **Java es Container Aware a partir de las versiones Java 8u191 y Java 10**.

## Conclusiones

Cuando se creó Java en 1995 nadie se imaginaba que surgirían las tecnologías Docker, Kubernetes, etc. Entonces, ¿es viable ejecutar Java en contenedores? 

La respuesta es que sí. La comunidad Java está reaccionando y se está adaptando a los cambios que suponen estas nuevas tecnologías cloud y contenedores. Uno de los primeros obstáculos fue solventar la compatibilidad entre Java Ergonomics y los contendores. Ese escollo ya está resuelto con las versiones superiores de Java y no nos tendremos que volver a preocupar.

De todos modos, hay otros aspectos de la plataforma Java como puede ser el peso de la máquina virtual que la comunidad está tratando de mejorar. En este sentido, también hay mucho movimiento y están surgiendo nuevas herramientas y frameworks que hay que vigilar ([Graal Native Image](https://www.graalvm.org/docs/reference-manual/native-image/){:target="_blank"}, [Micronaut](https://micronaut.io/){:target="_blank"}, [Quarkus](https://quarkus.io/){:target="_blank"}, etc).
