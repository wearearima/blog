---
layout: post
title:  "Buenas prácticas para escribir un Dockerfile"
date:   2020-04-21 9:00:00
author: urko
lang: es
categories: docker
tags: docker, dockerfile
header-image: 2020-04-21-buenas-practicas-para-escribir-un-dockerfile/skyline.jpg
---

A la hora de escribir un Dockerfile, las posibilidades son infinitas. Se pueden crear imágenes con el mismo propósito, que funcionen similar, pero que estén estructuradas de una manera muy diferente. Empezando por elegir una imagen de partida (FROM), pasando por el orden de los comandos que ejecutamos al construir la imagen, o creando imágenes intermedias (*multistage builds*), escribir un Dockerfile es un mundo.

En este documento se recogen algunas de las pautas más importantes que hay que seguir si queremos optimizar al máximo el tiempo que tardamos en crear la imagen, la seguridad de la misma y el tamaño que ocupa.

### 1. El orden de los comandos importa

Por la manera en la que funciona el caché a la hora de construir una imagen, Docker es capaz de detectar si el comando que queremos ejecutar se ha ejecutado antes o no (en una *build* anterior) y reutilizar el resultado desde la caché para hacerlo más rápido. El problema es que, si uno de los comandos ha cambiado, los comandos que le suceden no pueden ser sacados de caché porque puede que alguno se haya visto afectado y el resultado sea diferente. 

Es por esto que se recomienda ordenar los comandos según la frecuencia que tienen de ser cambiados. Si estuviésemos creando una imagen que contiene una aplicación, por ejemplo, las modificaciones más comunes serían las del código, las de los recursos serían las siguientes, y por último irían las dependencias. Por eso, deberíamos ordenarlas en order ascendente para asegurarnos de que optimizamos el uso de caché.

### 2. Junta los comandos en capas

En un Dockerfile, cada comando representa una capa de la imagen final. Es importante juntar las capas que compartan la misma lógica (instalación de dependencias, por ejemplo) para mejorar el uso de caché y para hacer el Dockerfile más mantenible.

Sin embargo, hay que tener en cuenta que, si realizamos demasiadas acciones en el mismo comando, si en algún momento queremos cambiar algo del comando la caché ya no servirá y habrá que volver a ejecutarlo entero. Por esto, es importante estudiar cada escenario y evaluar cuál es la mejor forma de hacerlo.

**MAL** &#10060;
```Dockerfile
FROM ubuntu
RUN apt update && apt install openjdk-8-jdk -y
RUN apt update && apt install vim -y
```
**BIEN** &#9989;
```Dockerfile
FROM ubuntu
RUN apt update && apt install openjdk-8-jdk vim -y
```

### 3. Elimina la caché que no necesites

La caché es buena sí, ¿pero cuál? Hay que entender que a la hora de construir una imagen existen dos tipos de caché: 1. la que genera docker con las capas de nuestra imagen y 2. la que generan nuestros comandos dentro de la propia imagen. La primera es buena para mejorar el tiempo de construcción, pero la segunda probablemente no.

El segundo tipo de caché se suele generar al instalar dependencias o durante el proceso de compilación de una aplicación, y es muy poco probable que vayas a utilizarlo y lo más seguro es que solo esté ahí ocupando espacio.

Fíjate en la última línea del siguiente Dockerfile:
```Dockerfile
FROM maven:3.6.3-jdk-11
ENTRYPOINT ["java", "-jar", "target/*.jar"]
COPY pom.xml .
COPY src ./src
RUN mvn -e -B clean package && rm -rf /root/.m2
```

Tiene que quedar claro que, para borrar un fichero de la imagen, es necesario que el fichero se cree y se borre en el mismo comando. Si se hace en diferentes comandos, el fichero aparentemente habrá desaparecido, pero seguirá estando en la *layer* en la que lo hemos creado y seguirá consumiendo espacio.

Este fichero sigue existiendo:
```Dockerfile
FROM busybox
RUN touch a
RUN rm a
```

Este no:
```Dockerfile
FROM busybox
RUN touch a && rm a
```
Si el objetivo es reducir el espacio que ocupa la imagen final y no podemos eliminar este tipo de ficheros en el mismo comando en el que lo creamos, podemos utilizar la opción `--squash` a la hora de crear la imagen para juntar todas las capas en una sola, donde sí que eliminaríamos el fichero. Pero, !cuidado! La opción `--squash` tiene más implicaciones, como borrar la historia de la imagen, úsala solo cuando sea extrictamente necesario.

### 4. Elige bien la imagen base

A la hora de elegir una imagen desde la que partir, lo primero que se nos puede ocurrir es escoger una imagen que no tenga más que lo básico (un sistema operativo) e instalar encima todo lo que necesitemos. Esto puede funcionar, pero lo que es mucho mejor a nivel de seguridad, mantenibilidad y espacio, es utilizar una imagen de algún proveedor de confianza que ya nos lo dé hecho.

Por ejemplo, supongamos que necesitamos una imagen con Python 3.6 instalado. Podríamos utilizar `alpine` como base e instalar Python con el gestor de paquetes, o utilizar la imagen `python:3.6-alpine`, que ya trae Python instalado y está mantenido por los desarrolladores de Python (además de otras cosas).

El exponente que mejor cumple con este punto puede que sea [Google Distroless Docker Images](https://github.com/GoogleContainerTools/distroless){:target="_blank"}, que es una imagen base que solo contiene las dependencias necesarias para ejecutar tu aplicación y elimina todo el resto de elementos (como gestores de paquetes, shells, y otros comandos) y por lo tanto, reduce la superficie de ataque de nuestros contenedores. Estas imagenes son específicas para cada lenguaje y puede que el que necesites no esté soportado, pero si lo está, no encontrarás una imagen más segura desde donde partir.

### 5. Especifica la versión de la imagen base

Si te has fijado, para escoger la imagen de Python hemos utilizado un *tag*. Esto también es importante. Para que una imagen sea reproducible, deberemos elegir un *tag* para esa imagen que sepamos que no va a cambiar en el tiempo (*tag*s como `latest` o `slim` sí lo hacen, ¡ojo!).

{% raw %}
En realidad, no es posible garantizar que un *tag* que escojamos se vaya a mantener siempre igual, independientemente de si es uno genérico como `latest` o uno específico como `3.6.8-alpine-slim`. La mejor práctica de todas sería escoger la versión concreta de una imagen que queramos utilizar, y utilizar su identificador. Este identificador se puede conseguir con el comando:
```
docker images --format "{{.Repository}}:{{.Tag}} {{.ID}}"
```

Por ejemplo, si quisiese el identificador de la imagen `busybox` que acabo de añadir a mi registro local, ejecuto: 

```
$ docker images --format "{{.Repository}}:{{.Tag}} {{.ID}}" |grep busybox
busybox:latest 83aa35aa1c79
```
{% endraw %}
Ahora, podría utilizar el identificador como `FROM` de mi Dockerfile:

```Dockerfile
FROM 83aa35aa1c79
CMD ["echo", "Hola!"]
```

### 6. El potencial de las *multistage build*s

Cuando creamos una imagen, podemos generar imágenes intermedias que utilizamos para un propósito en concreto (como generar un artefacto) y que se acaban eliminando y no forman parte de la imagen final (aunque el artefacto que hemos generado sí). Esto se llama *multistage build*, y es muy útil en casos donde haya que compilar una aplicación, por ejemplo.

Utilizar *multistage builds* hará que nuestra imagen final sea menos pesada, y probablemente más segura. Fíjate cómo en el siguiente Dockerfile compilamos la aplicación en una imagen que no se acaba usando y generamos un JAR que ejecutamos en la imagen final, donde no tenemos ni JDK ni Maven.

```Dockerfile
FROM maven:3.6.3-jdk-11 as builder
WORKDIR /app
COPY pom.xml .
RUN mvn -e -B dependency:go-offline
COPY src ./src
RUN mvn -e -B clean package

FROM adoptopenjdk:8u242-b08-jre-hotspot
COPY --from=builder /app/target/*.jar /app.jar
ENTRYPOINT ["java", "-jar", "/app.jar"]
```

### 7. Usuario sin privilegios

Se considera una buena práctica en un Dockerfile modificar el usuario final de la imagen a uno que disponga los privilegios justos para cumplir con el propósito de la imagen y nada más. Esto hará que nuestra imagen sea más segura y evite que un usuario administrador en el contenedor gane acceso al *host*.

Para esto, lo mejor es agregar un nuevo usuario (y un grupo) y darle los permisos que necesite. Por ejemplo:

```Dockerfile
FROM ubuntu
RUN groupadd -r usergroup && useradd -r -g user usergroup
ENTRYPOINT ["sh", "myScript.sh"]
COPY ./myScript.sh /myScript.sh
RUN chown user /myScript.sh
USER user
```

### 8. Mantén tus secretos ocultos

Es muy habitual que en una imagen necesitemos utilizar credenciales, *token*s de acceso o ficheros con información que no queremos compartir. Si pasamos estos elementos a la imagen mediante comandos como `COPY` o `ADD`, estarán visibles en la imagen y cualquiera que tenga acceso a ella podrá verlos.

Existe una forma de añadir esta información a nuestros contenedores, llamada `docker secret`. La forma de implementarla es un poco compleja como para explicarla en este documento, ya que depende de la manera en la que vayas a desplegar la imagen (`docker-compose`, `kubernetes`, ...). [Introduction to Docker Secrets](https://dzone.com/articles/introduction-to-docker-secrets){:target="_blank"} o [Distribute Credentials Securely Using Secrets](https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/){:target="_blank"} pueden ser un buen punto de partida.

### 9. Copia solo lo que necesites

La imagen que generemos debería contener única y exclusivamente los ficheros que necesite. Es común ver comandos del estilo de `COPY . /app`, que copiará todo el contexto al directorio `/app`. Y esto puede no estar mal, depende del contexto y de lo que pretendamos hacer, pero en muchos casos podemos estar copiando archivos que no vamos a utilizar o que tienen información confidencial.

Hay dos formas de evitar esto:
1. Copiar únicamente los ficheros que vayamos a utilizar, aunque si son muchos y no los tenemos estructurados en directorios, puede crear demasiadas *layer*s.
2. Usar `.dockerignore`. En este fichero con la misma sintaxis que `.gitignore` podremos decidir qué ficheros o directorios queremos evitar añadir al contexto. [Más información](https://docs.docker.com/engine/reference/builder/#dockerignore-file){:target="_blank"}.

### 10. Copia, no añadas

Existen dos comandos en Dockerfile muy similares: `COPY` y `ADD`. El primero sirve para copiar una serie de ficheros o directorios desde el *host* a la imagen. El segundo hace lo mismo, pero además es capaz de descargar elementos desde URLs o repositorios y descomprime ficheros comprimidos. Para mas información sobre `ADD`, ver [la documentación](https://docs.docker.com/engine/reference/builder/#add){:target="_blank"}.

Puede que viendo que hacen lo mismo y `ADD` sea más potente, solo quieras usar este, pero deberías evitarlo. Utiliza `COPY` para la mayoría de situaciones, que será copiar desde el *host*, y únicamente utiliza `ADD` cuando necesites algo que no puedas conseguir con `COPY`. Utilizar `ADD` sin tener en cuenta la diferencia puede conllevar riesgos de seguridad como [*zip bomb*s](https://en.wikipedia.org/wiki/Zip_bomb){:target="_blank"}.

## Conclusión

Aunque escribir un Dockerfile pueda parecer algo sencillo, es importante seguir ciertas recomendaciones que harán que nuestro proceso de *building* se ejecute más rápido, y que la imagen resultante sea más pequeña y segura.

En este artículo hemos repasado algunos de los puntos más importantes, que a la vez son muy sencillos de seguir en la mayoría de los casos. Puedes encontrar más consejos de este tipo en la [documentación oficial](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/){:target="_blank"}.