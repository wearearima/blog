---
layout: post
title:  "My experiencia con el examen CKA"
date:   2021-04-12 8:00:00
author: urko
lang: es
categories: kubernetes, certifications, cloud
tags: kubernetes, certifications, cloud, exams, CKA
header-image: 2021-04-12-my-cka-exam-experience/header.jpg
---

El pasado Lunes 22 de Marzo me examiné del certificado [CKA](https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/){:target="_blank"} de Linux Foundation, y he venido a contaros mi experiencia sobre cómo lo preparé y lo que podemos esperar en este examen. Os recomiendo encarecidamente que leáis también un [post que hizo mi compañero Fernando hace unos meses sobre el examen CKAD]({{ site.baseurl }}/es/2020-04-22-examen-ckad){:target="_blank"}, que habla mucho más en detalle sobre los aspectos de estos exámenes y sirve de ayuda para aprobarlos. !Leyendo su post aprendí algunos consejos cruciales!

### Experiencias previas con Kubernetes

Sinceramente, hace exactamente un año no sabía nada de Kubernetes, no es que nunca hubiera trabajado con ello, sino que ni siquiera tenía claro el concepto de "contenedor". Es verdad que este último año he estado trabajando con esta herramienta frecuentemente (lo cual sin duda me ha ayudado al preparar el examen), pero opino que no es necesario más que un poco de experiencia previa.

### Cómo preparé el examen

Pese al conocimiento que ya tenía de los recursos de K8s, del uso de `kubectl` o de administrar clusters, consideramos que era necesario que me apuntase a este curso en Udemy: [enlace](https://www.udemy.com/course/certified-kubernetes-administrator-with-practice-tests){:target="_blank"}. Empieza explicando los conceptos más básicos tanto de la administración como de los recursos de Kubernetes, que puede ayudar a las personas con menos experiencia, y en poco tiempo empieza ya a explicar contenido más avanzado. 

Sin embargo, en el examen muchas preguntas son sobre el contenido más básico, así que recomiendo personalmente prestar atención a estas lecciones también. El curso está compuesto por vídeos y laboratorios prácticos, e incluso tiene algunos examenes al final con preguntas muy similares al del examen de verdad.

![Ejemplo de ejercicio de los laboratorios](/assets/images/2021-04-12-my-cka-exam-experience/exercise.jpg){: .center }
<label style="text-align: center; display: block;">Ejemplo de ejercicio de los laboratorios</label>

En resumen, el curso hace las cosas tan bien que da la sensación de que el temario es incluso fácil. En mi opinión, la dificultad examen no radica en su los conocimientos, sino en la soltura a la hora de operar el cluster y en saber gestionar bien el tiempo. Haciendo restrospectiva, diría que el curso es muy completo y lo recomendaría a cualquiera que se quiera sacar la certificación.

### El examen

La prueba consiste de 17 preguntas que habrá que realizar en 2 horas. La dificultad de las preguntas varía entre algunas muy básicas, como arrancar un Pod con múltiples contenedores o crear un Rol con ciertos permisos, pasando por otras más complicadas, como crear un NetworkPolicy que restrinja el tráfico de un Pod de cierta manera, e incluso hay un par de preguntas que pondrán de verdad a prueba nuestros conocimientos. Un ejemplo de estas preguntas fue un cluster que tenía un nodo caído y tuve que identificar el problema, sin ningún tipo de pista.

Como ya he dicho, la dificultad reside en lo familiarizados que estemos con las herramientas que vamos a utilizar. Por esto mismo, quiero recalcar algunos de los consejos que nos ofrece Fernando en [su post]({{ site.baseurl }}/es/2020-04-22-examen-ckad){:target="_blank"}:

* Practica usando los subcomandos de `kubectl`. Crear descriptores a partir de `run` o `create <tipo> --dry-run=client -o yaml`, o utilizar `explain` para entender la estructura de un recurso nos pueden ahorrar mucho tiempo.
* En caso de no poder crear estos recursos mediante `kubectl`, saber navegar por la documentación y encontrar los ejemplos de los descriptores que necesitamos también es una buena opción. Por esto, crea marcadores en tu navegador que te lleven directamente a las zonas de la documentación que más vayas a utilizar.
* Personalmente, utilicé `alias k=kubectl` y, ¡me pareció una maravilla!
* Aprende a usar la terminal de bash y práctica con sus comandos. Lo mismo con el editor que vayamos a usar (yo usé `vim`). Ser productivos en estos aspectos nos aportará mucho tiempo extra para ocuparlo en tareas más importantes.

### Conclusión

Estoy contento de haber podido obtener esta certificación, y de poder pasar a ser un usuario reconocido por la CNCF. La mayoría de la materia del temario es sencilla de interiorizar y con una buena preparación estoy seguro de que los usuarios que trabajen con K8s en su día a día podrán obtener esta certificación. Es cuestión de práctica.

Yo obtuve una puntuación de 87/100, por lo que asumo que fallé en una o dos preguntas. Me quedo satisfecho porque sé que soy capaz de resolver cualquiera de los ejercicios del examen, que para mí acaba siendo lo importante: poder entender la materia y aplicar el conocimiento obtenido a casos en la vida real.

![Certificación](/assets/images/2021-04-12-my-cka-exam-experience/certification.png){: .center }
<label style="text-align: center; display: block;">Certificación</label>
