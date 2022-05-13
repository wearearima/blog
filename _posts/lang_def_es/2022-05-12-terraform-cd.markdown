---
layout: post
title:  "¿Deberíamos usar Terraform como herramienta de Despliegue Continuo?"
date:   2022-05-12 9:00:00
author: urko
lang: es
categories: terraform, cd, cicd
tags: terraform, cd, cicd
header-image: 2022-05-12-terraform-cd/header.jpg
---

En ARIMA, desde hace unos años, hemos apostado por Kubernetes y el ecosistema *cloud native* que lo rodea. Nos hemos hecho miembro de la [Cloud Native Computing Foundation](https://www.cncf.io/) y hemos promovido el uso de muchos de sus proyectos en nuestros clientes. Desde Helm y kustomize para gestionar los despliegues de un *cluster*, pasando por ArgoCD o Flux que nos ayudan a automatizar estos despliegues y a seguir el patrón [GitOps](https://www.weave.works/technologies/gitops/), o Prometheus y Grafana para monitorizar las métricas de nuestras aplicaciones. Todos estos son solo algunos ejemplos de los proyectos *open source* que forman parte de un ecosistema cada vez más popular y en constante crecimiento.

Aunque ya hemos usado [Terraform](https://www.terraform.io/) previamente en varios proyectos, recientemente nos surgió una pregunta que a primeras parece inocente, pero tiene su miga: ¿Deberíamos usar Terraform como herramienta de Despliegue Continuo? Para el que no lo conozca, Terraform es una herramienta de gestión de infrastructura que nos permite crear y actualizar componentes tanto en entornos *cloud* como *on-premise*, utilizando para ello las APIs de los distintos proveedores. Se basa en el concepto de *infrastructure as code*, que consiste en definir en código la estructura de la infraestructura, que permite almacenarlo en un sistema de control de versiones y que todos los miembros del equipo conozcan lo que está desplegado, entre otras ventajas.

Terraform, para el usuario, provee únicamente un CLI, que sirve para inicializar el proyecto local y para aplicar la configuración, principalmente. Para que este CLI se comunique con las diferentes APIs, Terraform ofrece también una extensa lista de *providers* (creados por la comunidad) que son los que interpretan nuestros ficheros de configuración y contactan con las APIs para crear la infraestructura definida. Al ser un proyecto con varios años desde su publicación y al tener bastante popularidad dentro de la comunidad *cloud-native*, la lista de *providers* es muy extensa (más de 2000) y prácticamente cualquier arquitectura en *cloud* se puede desarrollar utilizando Terraform.

### Nuestro proyecto

Sin entrar en demasiados detalles, nuestro proyecto contenía un cluster de Kubernetes donde desplegamos nuestros servicios. Al usar AWS, el cluster tenía que ser desplegado con EKS y decidimos utilizar perfiles de Fargate para minimizar el coste y evitar tener que provisionar los nodos a medida que crece el cluster.

Además, nos interesaba instalar algún tipo de herramienta de Despliegue Continuo, para que los desarrolladores pudieran ver sus cambios cada vez que los aplicasen en su respectiva rama del repositorio. Para esto, decidimos utilizar [ArgoCD](https://argo-cd.readthedocs.io/en/stable/), ya que habíamos trabajado con esta herramienta anteriormente, es sencilla de instalar, y nos encajaba para que los desarrolladores pudieran consultar el estado de los despliegues.

Sin embargo, durante el desarrollo del plan de Terraform, nos dimos cuenta que al igual que desplegábamos ciertos componentes de Kubernetes para instalar Argo con el CLI de Terraform, podíamos definir los componentes de nuestros despliegues en el plan y desplegarlos desde el pipeline del repositorio para automatizarlo. De esta manera, podíamos evitar usar ArgoCD en el proyecto y aprovechar Terraform para satisfacer nuestras necesidades.

En este momento nos surgió una duda que no nos habíamos planteado antes: ¿deberíamos usar Terraform como herramienta de Despliegue Continuo? ¿cuáles son sus ventajas/desventajas?

### ¿Qué nos ofrece Terraform?

Al usar Terraform como herramienta de despliegue de nuestros servicios, obtendríamos ciertas ventajas que nos hicieron plantearnos esta alternativa:
* Eliminariamos la necesidad de usar ArgoCD en el proyecto, simplificando la arquitectura y reduciendo el coste de mantener sus contenedores activos. 
* Unificaríamos el despliegue de la infraestructura con el despliegue de nuestros servicios en una sola pieza: el plan de Terraform. Conocer el estado de la arquitectura consistiría en consultar el plan únicamente, ya que estaría todo centralizado en él.
* Minimizariamos el número de tecnologías que habría que conocer para trabajar con el proyecto.

### ¿Qué implicaciones tiene utilizar Terraform para automatizar los despliegues?

En esencia, Terraform no está pensado para utilizarlo como sustituto de ArgoCD. Su forma de interactuar con los componentes desplegados tiene implicaciones subyacentes que son importantes de identificar antes de tomar una decisión.

* En vez de usar un operador de Kubernetes como hace ArgoCD para sincronizar el repositorio con el cluster, Terraform hará la sincronización de manera externa, desde la máquina que ejecute el pipeline. Esto tiene ciertas implicaciones de seguridad, porque habrá que crear un usuario y rol para que el pipeline pueda efectuar cambios, además de exponer el cluster a modificaciones desde fuera.
* El CLI de Terraform está pensado para ser utilizado manualmente. Cada vez que se intenta aplicar una actualización del plan, el CLI notifica al usuario de los cambios que tendrá que efectuar en la infraestructura, ya sea añadir, modificar, y/o eliminar componentes. En ocasiones puede darse el caso de que los cambios propuestos por Terraform no sean correctos, porque alguna llamada a las APIs haya fallado o se hayan actualizado las APIs y los *providers* aún no. En estos casos, Terraform puede intentar aplicar unos cambios erróneos que un usuario debería identificar y denegar. Al ejecutarlo desde un pipeline, perdemos esta capacidad de supervisión sobre los cambios de Terraform y nos exponemos al riesgo de cambios inesperados sobre la infraestructura. Un ejemplo que nos ha ocurrido es que Terraform intente constantemente intentar eliminar una instancia de RDS y recrearla, cuando no ha habido ningún cambio en el plan relacionado con ella.
* En caso de querer gestionar múltiples entornos o proyectos en la misma infraestructura, ArgoCD nos aporta utilidades para hacerlo de manera sencilla, mientras que diseñar un plan de Terraform para que sea flexible es más complicado y propenso a errores.
* La interfaz gráfica de Argo hará que los desarrolladores puedan conocer el estado de sus despliegues sin conocer las herramientas que se han usado para ello. Trabajar directamente con descriptores YAML de K8s o Charts de Helm es más sencillo y llevadero que gestionar esos mismos recursos desde Terraform. En general, la experiencia de usuario empeorará si prescindimos de ArgoCD.

### Conclusiones

En nuestro proyecto, después de sopesar ambas opciones, nos acabamos decantando por utilizar Terraform para desplegar la infraestructura, pero instalando ArgoCD para que gestionase los despliegues de Kubernetes. Esto no quiere decir que creamos que esta es la mejor decisión, sino que era la que más se ajustaba a las características de nuestro proyecto.

En definitiva, porque una herramienta sea capaz de cumplir múltiples roles no significa que sea la herramienta más adecuada para cada una de esas funciones.