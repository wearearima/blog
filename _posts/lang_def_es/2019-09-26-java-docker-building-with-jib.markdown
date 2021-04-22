---
layout: post
title:  "Java en contenedores Docker con Jib"
date:   2019-09-26 9:00:00
author: telle
lang: es
categories: mediator feature
tags: spring-boot, docker, jib, maven
header-image:	2017-01-15-view-rendering-performance/post-header2.jpg
---

Generalmente cuando se quiere empaquetar una aplicación Java en un contenedor Docker, se crea un 
fichero Dockerfile en el proyecto para especificar las propiedades de la imagen Docker, tales como: 
en qué imagen se basa, cuál es el entrypoint, qué puerto se expone, etc. 

Una alternativa al fichero Dockerfile es definir esa información en el pom.xml mediante el plugin de 
[Jib](https://github.com/GoogleContainerTools/jib){:target="_blank"} para Maven o Gradle. Las ventajas que nos aporta este proyecto son:

 - No requiere configurar un fichero Dockerfile en el proyecto ni tener Docker instalado en el equipo para crear imágenes Docker. 
 - Logramos que el building de la imagen sea más rápido ya que JIB separa en diferentes capas el código del proyecto y 
 sus dependencias. Dado que las dependencias no cambian habitualmente, JIB puede reutilizar la capa de dependencias y sólo
 hacer el building de la capa de código. 
 - Simplificamos el flujo de construcción de la imagen y de publicación en un repositorio. Como ilustra la siguiente imagen,
 este flujo antes implicaba varios comandos y con jib lo resolvemos a la ejecución de un único comando. 

![jib-flow](/assets/images/2019-09-26-java-docker-building-with-jib/jib-flow.png)

En [este proyecto de Spring Boot](https://github.com/wearearima/spring-boot-jib-docker){:target="_blank"} hemos configurado el plugin Jib para Maven de esta manera:

```
<plugin>
    <groupId>com.google.cloud.tools</groupId>
    <artifactId>jib-maven-plugin</artifactId>
    <version>1.5.1</version>
</plugin>
```

Sólo con esto y ejecutando el comando `./mvnw compile jib:dockerBuild` ya es suficiente para crear una imagen Docker de nuestra aplicación Java.

Con objeto de reducir configuración de Docker, a partir de la información del proyecto Jib ha inferido la configuración que mejor se ajusta. Por ejemplo, no hemos especificado la imagen base que incluirá la JDK. Jib no lo ha necesitado porque a partir de la configuración del pom, `<java.version>1.8</java.version>`, ha detectado que se necesita Java 8 y para este tipo de proyecto la imagen base que emplea Jib es `gcr.io/distroless/java:8`, una imagen [distroless de Google](https://github.com/GoogleContainerTools/distroless){:target="_blank"}. 

Asimismo, aunque carecemos del fichero Dockerfile, seguimos teniendo el control sobre los parámetros de configuración de la imagen Docker. En el siguiente ejemplo veremos cómo podemos configurar algunos de estos parámetros:

```
<plugin>
    <groupId>com.google.cloud.tools</groupId>
    <artifactId>jib-maven-plugin</artifactId>
    <version>1.5.1</version>
    <configuration>
        <from>
            <image>adoptopenjdk/openjdk8:alpine-slim</image>
        </from>
        <to>
            <image>${project.groupId}/${project.artifactId}</image>
        </to>
        <container>
            <jvmFlags>
                <jvmFlag>-Djava.security.egd=file:/dev/./urandom</jvmFlag>
            </jvmFlags>
        </container>
    </configuration>
</plugin>
```

En esta configuración se ha especificado:
 - AdoptOpenJDK como imagen base mediante `<form>`
 - Tag de la imagen mediante `<to>`
 - Flags de JVM mediante `<jvmFlags>`

Si inspeccionamos la imagen recien creada observamos que la imagen fue creada hace ¡49 años! 

```
$ docker image ls | grep spring-boot-jib-docker
spring-boot-jib-docker                                           0.0.1-SNAPSHOT          fe30b0d3f8d6        49 years ago        142MB
```

No se trata de un bug, no hay que asustarse. Jib por defecto elimina la fecha de creación para mantener la [reproducibilidad](https://reproducible-builds.org/){:target="_blank"} de la imagen. Un building reproducible es aquel que siempre devuelve el mismo resultado, incluso la misma fecha de creación. Por este motivo Jib lo elimina, aunque se puede [modificar este comportamiento](https://github.com/GoogleContainerTools/jib/blob/master/docs/faq.md#why-is-my-image-created-48-years-ago){:target="_blank"}. 