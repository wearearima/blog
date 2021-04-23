---
layout: post
title:  "Cómo preparé y aprobé el Certified Kubernetes Application Developer (CKAD)"
date:   2020-04-28 6:00:00
author: fernando
lang: es
categories: certificaciones
tags: certificaciones, examenes, Kubernetes, CNCF, CKAD, CKA
header-image:	2020-04-22-examen-ckad/header-image.jpg
---

En este post voy a explicar un poco mi experiencia de cómo preparé y aprobé el Certified Kubernetes Application Developer (CKAD).

[The Linux Foundation](https://www.linuxfoundation.org/){:target="_blank"} y [Cloud Native Computing Foundation](https://www.cncf.io/){:target="_blank"} 
ofrecen dos variantes en la certificación de Kubernetes, CKAD y CKA. En pocas palabras:

- [CKAD](https://www.cncf.io/certification/ckad/){:target="_blank"} está diseñado para desarrolladores de software que deseen desarrollar e implementar sus aplicaciones en Kubernetes. 

- [CKA](https://www.cncf.io/certification/cka/){:target="_blank"} está diseñado para los administradores de sistemas que administran los clústeres de Kubernetes.

En general, CKA cubre un temario más amplio que CKAD. Puedes ver información sobre las similitudes y diferencias entre los dos exámenes [aquí](https://medium.com/faun/cka-vs-ckad-1dd45527505){:target="_blank"}.

![CKAD / CKA](/assets/images/2020-04-22-examen-ckad/ckad-cka.png){: .center }

Como he dicho, CKAD es uno de los dos programas diseñados por la CNCF y The Linux Foundation para certificar a los usuarios que pueden "diseñar, construir, configurar y exponer aplicaciones nativas en la nube para Kubernetes".

Si eres un desarrollador que usas la infraestructura centrada en Kubernetes a diario, CKAD es un gran método para medir tus habilidades con los últimos estándares de la industria.

Cabe destacar que Kubernetes es una herramienta con la que yo ya había trabajado con anterioridad y por lo tanto, estaba familiarizado con la mayoría de conceptos.

## ¿Por qué deberías hacer este examen?

A pesar de que en [ARIMA](https://arima.eu/){:target="_blank"} por lo general no somos muy partidarios de medir los conocimientos de las personas u organizaciones en función de los certificados que puedan poseer, hay ocasiones en las que disponer de un certificado emitido por un tercero sí que puede ayudar como carta de presentación a la hora de ofrecer soluciones que giran en torno a una herramienta como Kubernetes. Más aún cuando se trata de una organización del prestigio de la CNCF y de un certificado que tiene un cierto grado de dificultad como puede ser el CKAD.

## Prerequisitos

No hay prequisitos oficiales para este examen, pero recomiendo tener experiencia práctica en **Docker** y **Linux**.

Al trabajarse constantemente con contenedores, uno debe comprender qué es una imagen de Docker, cómo ejecutar los contenedores, extraer y trabajar con imágenes, etc.

Linux también es esencial para este examen, ya que el examen al ser 100% práctico necesitas tener bastante agilidad a la hora de editar ficheros, cambiar permisos, ejecutar comandos, etc. 


## Sobre el examen

Este es un examen **totalmente práctico**, no tiene preguntas de opción múltiple.

Se te dará un conjunto de problemas que tienes que ir solventando desde una línea de comandos desplegada en una aplicación web y se espera que tardes aproximadamente dos horas en completarlo.

Debes resolver **19 preguntas** en **2 horas** y cada pregunta tiene un valor diferente, desde **2% a 13%**, pero la mayoría de las preguntas están entre **8% y 5%**. La puntuación no corresponde al nivel de dificultad.

**Para aprobar el examen es necesario sacar al menos el 66%.** En mi caso, conseguí un 88% en el primer intento y me dio tiempo justo a acabar las 19 preguntas a pesar de que fui bastante rápido en la resolución de los problemas. **El tiempo es todo en este examen.**

El precio de este examen es de **$300 USD**, y dispones de otro intento gratuito si suspendes el examen. El examen incluye preguntas de los siguientes temas:

- Core Concepts (13%)
- Configuration (18%)
- Multi-Container Pods (10%)
- Observability (18%)
- Pod Design (20%)
- Services & Networking (13%)
- State Persistence (8%)

En el examen, se te proporcionan **4 clústeres** por los cuales tendrás que ir trabajando hasta completar todos los ejercicios. El sistema operativo que usan es un **Ubuntu 16.04**.

![Clusters](/assets/images/2020-04-22-examen-ckad/clusters.png){: .center }

Al comienzo de cada pregunta, se te proporciona el comando que debes ejecutar para ir al clúster en concreto. Por ejemplo:

    $ kubectl config use-context k8s

### Tipos de preguntas

Las preguntas van desde preguntas relativamente cortas, como las que aparecen en la lista de  [ejercicios CKAD de Dgkanatsios](https://github.com/dgkanatsios/CKAD-exercises){:target="_blank"}, hasta preguntas más largas de unas 6 o 7 líneas.

Tienes que sentirte cómodo creando *pods*, *developments*, *jobs*, *cronjobs*, *services*, etc. También habrá ejercicios de *rolling updates* and *rollbacks*. Básicamente preguntan todo el temario que entra en el examen.

### Recursos oficiales del examen

Estos son los recursos que la propia CNCF pone a disposición de los estudiantes:

- Certified Kubernetes Application Developer: [https://www.cncf.io/certification/ckad/](https://www.cncf.io/certification/ckad/){:target="_blank"}
- Curriculum Overview: [https://github.com/cncf/curriculum](https://github.com/cncf/curriculum){:target="_blank"}
- Candidate Handbook: [https://training.linuxfoundation.org/go/cka-ckad-candidate-handbook)](https://training.linuxfoundation.org/go/cka-ckad-candidate-handbook){:target="_blank"}
- Exam Tips: [http://training.linuxfoundation.org/go/Important-Tips-CKA-CKAD](http://training.linuxfoundation.org/go/Important-Tips-CKA-CKAD){:target="_blank"}
- FAQ: [http://training.linuxfoundation.org/go/cka-ckad-faq](http://training.linuxfoundation.org/go/cka-ckad-faq){:target="_blank"}


### Dónde registrarse

Primero deberás registrarte en **The Linux Foundation** desde [aquí](https://identity.linuxfoundation.org/user/login){:target="_blank"}. Después, podrás registrarte para el examen desde [aquí](https://identity.linuxfoundation.org/pid/813){:target="_blank"}, donde se te mostrará la siguiente pantalla:

![Checkout](/assets/images/2020-04-22-examen-ckad/checkout.png){: .center }

Una vez que hayas hecho el pago para el examen, recibirás un correo electrónico y podrás iniciar sesión desde [este](https://training.cncf.io/portal){:target="_blank"} enlace al portal donde debes seguir una serie de pasos antes de programar y hacer el examen, tales  como verificar los requisitos de tu máquina, leer información importante sobre el examen, etc.

![Checkout](/assets/images/2020-04-22-examen-ckad/cncf-checklist.png){: .center }

## Cómo preparar el examen

### Cursos

Como he dicho antes, de cara a prepararme el examen realicé los dos siguientes cursos de [Udemy](https://www.udemy.com/){:target="_blank"}:

1. [Kubernetes for the Absolute Beginners - Hands-on](https://www.udemy.com/course/learn-kubernetes/){:target="_blank"}
2. [Kubernetes Certified Application Developer (CKAD) with Tests](https://www.udemy.com/course/certified-kubernetes-application-developer/){:target="_blank"}

El primero, aunque ya tenía nociones básicas de Kubernetes, lo realicé para comprobar que mi base en Kubernetes era la adecuada. No aprendí practicamente nada nuevo en ese curso, por lo que si eres una persona que ya ha trabajado con Kubernetes yo pasaría directamente al segundo. Además, en el segundo curso, hacen repaso de los conceptos más importantes que se dan en el primero.

El segundo curso me aportó mucho más, ya que está centrado en el examen en sí, y los ejercicios prácticos que tiene son muy buenos. El entorno de pruebas es muy potente (parecido al que te vas a encontrar en el examen), me ayudó mucho a mejorar la velocidad con la que solventaba los problemas.


### Ejercicios para practicar

Básicamente estos fueron los recursos que use para preparar el examen a parte de los del propio curso, alguno lo hice entero entre 2 y 3 veces, al final tienes que coger la habilidad de poder leer la pregunta y sin dudar un segundo, saber cómo resolver el problema, ya que como repito el tiempo es todo en este examen.

- [https://github.com/bmuschko/ckad-prep](https://github.com/bmuschko/ckad-prep){:target="_blank"}
- [https://github.com/dgkanatsios/CKAD-exercises](https://github.com/dgkanatsios/CKAD-exercises){:target="_blank"}
- [https://codeburst.io/kubernetes-ckad-weekly-challenges-overview-and-tips-7282b36a2681](https://codeburst.io/kubernetes-ckad-weekly-challenges-overview-and-tips-7282b36a2681){:target="_blank"} 

En total, entre realizar los dos cursos, estudiar y hacer los ejercicios prácticos habré dedicado unas **90 horas** para aprobar el examen. Empecé a prepararlo un 30 de marzo e hice el examen el 15 de abril.

## Consejos y trucos útiles

1. **Sé rápido y preciso. Es un examen muy largo y con poco tiempo.** No esperes poder responder con tranquilidad todas las preguntas en 120 minutos, no da tiempo, ni siquiera a repasar. 

    Lo que hice yo en el examen fue que si veía que la pregunta tenía un valor < 3% y el enunciado era muy largo, las dejaba para el final y volví a ellas tras haber completado la mayoría de las preguntas. Si te quedas atascado, pasa de pregunta, tienes que lograr responder a las máximas preguntas posibles.

2. Cuando estés creando recursos en el clúster, **no escribas archivos YAML desde el principio**. Usa los argumentos ``-o yaml --dry-run`` siempre que puedas. Si todavía no sabes lo que es, ya estás tardando en aprenderlo!

3. Si no recuerdas alguna sintaxis al escribir archivos YAML, utiliza ``kubectl explain`` en lugar de la documentación. Es más rápido y tiene buena documentación. Te recomiendo que lo practiques para que te vaya saliendo solo.

    Por ejemplo, si no recuerdas las opciones de ``livenessProbe`` para el contenedor, simplemente escribe ``kubectl explain pod.spec.containers.livenessProbe`` y te dará todas las opciones con una buena documentación.

4. Usa siempre alias, tanto en tu entrenamiento como en el examen, te ahorran tiempo, estos fueron los que usé yo en el examen:

        alias k=kubectl
        alias ks='kubectl config set-context --current --namespace '

5. **Elimina los objetos de Kubernetes rápidamente**. Eliminar los objetos en Kubernetes a veces tarda hasta 30 segundos debido a que tiene un periodo de gracia, en el examen no te interesa que lo haga así, lo mejor es que siempre fuerces la eliminación del recurso. 

        $ kubectl delete pod nginx --grace-period=0 --force

6. **Asegúrate que estás en el contexto y namespace adeacuados**. Vas a tener que estar cambiando de contexto y de namespace constantemente, yo en el examen perdí la cuenta de cuantas veces lo hice, pero es muy importante asegurarse que siempre estás en el clúster y namespace correctos.

7. **¡Usa los marcadores del navegador!** Solo tienes permitido tener una pestaña extra a la del examen con la documentación de Kubernetes, lo que sí permiten son los marcadores. Te dejo [aquí](/assets/extra/2020-04-22-examen-ckad/CKAD-bookmarks.html){:target="_blank"} los marcadores que creé y utilicé yo en el examen, son enlaces directos a ejemplos que te ayudará a resolver los problemas más rápido. 

    ![Marcadores](/assets/images/2020-04-22-examen-ckad/marcadores.png){: .center }

8. **¡Recuerda hacer clic en el botón "Finalizar el examen"!** Estuve durante cinco minutos sin tocar el teclado preguntándome por qué esto no ha terminado todavía hasta que el supervisor del examen me lo recordó. El botón está oculto en el menú de configuración del examen.

9. Antes de comenzar el examen, debes **quitar todo lo que tengas encima de la mesa: lámpara de escritorio, bebidas, alimentos, etc.**, posteriormente debes mostrar tu DNI o pasaporte, tu habitación y escritorio. Utilicé una portátil con un monitor externo, así que asegúrate de que tus cables sean lo suficientemente largos o desconéctalos por completo.

10. No te tapes nunca la boca con la mano o murmures porque el examinador te lo recriminará y al menos a mí me desconcentró. 

11. Usa la misma versión de **Kubectl** y de **Kubernetes** que el examen. En mi caso fue la versión 1.17. Al usar ``Minikube for Mac OS`` en local, cambiar la versión de Kuberenetes es muy sencillo:

        minikube start --kubernetes-version v1.17.0

12. También se permite el **uso de múltiples monitores**, yo tenía la documentación de Kubernetes en un monitor y examen en el otro monitor. Me fue de gran utilidad tener de un vistazo ambas pantallas. Eso sí, se te pedirá en el examen que compartas ambas pantallas.

13. **Practica**. No por ser el último consejo es el menos importante. Practica todo lo que puedas. En el examen lo agradecerás.


## Resultados

Lamentablemente, los resultados no se obtienen de inmediato, tardan hasta 36 horas en darte el resultado. ¡No sabes que larga se me hizo la espera! Pero finalmente llegó, aquí estaba el tan ansiado certificado.

![Certificado](/assets/images/2020-04-22-examen-ckad/certificate.png){: .center }

## Conclusión

No te voy a engañar, no es un examen fácil. Al principio lo verás complicado, pero a medida que vas practicando vas viendo la luz. Tienes que practicar mucho, coger soltura con los comandos ``kubectl``, editando ficheros con ``Vim`` o ``Nano``, saber moverte bien por la documentación de K8s, etc. 

Me ha parecido una experiencia muy buena para completar mis conocimientos de Kubernetes y estar al día de lo que está ofreciendo la plataforma.

¡Buena suerte con tu examen CKAD! 

