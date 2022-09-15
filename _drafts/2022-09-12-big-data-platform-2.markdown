---
layout: post
title:  "Construyendo una plataforma Big Data open-source desde cero (II): Orquestador de flujos de trabajo"
date:   2022-09-08 9:00:00
author: dana
lang: es
categories: bigdata
tags: bigdata, argo-workflows, kubernetes, orquestador, etl
header-image: TODO
---

Un caso de uso común en los proyectos de Big Data son los procesos ETL (*extract, transform, load*),
 a través de los cuales obtenemos datos, los limpiamos y transformamos, 
 y los volcamos en la base de datos de análisis. 
 Pero, si lo pensamos, la mayoría de tareas de análisis de datos se componen de
 pasos dependientes entre sí.

Un orquestador de flujos de trabajos (o *workflow engine*, o *workflow orchestrator)* 
es un software que nos ayuda a crear, gestionar y ejecutar la serie de pasos 
interdependientes que componen una tarea concreta. 
Tal vez el orquestador de trabajos más popular en este momento sea Apache Airflow. Nosotros hemos escogido Argo Workflows, no solo por ser una herramienta nativa de Kubernetes, 
sino por los motivos que explicaremos a continuación:

## 1. Paralelismo

Argo Workflows funciona como una extensión de Kubernetes y, por ello, 
las tareas se ejecutan en contenedores. 
Esto le permite una capacidad mayor de paralelismo que Airflow, 
que está limitado por el número de workers activos. 
Con Argo Workflows, por el contrario, se pueden llegar a ejecutar decenas de 
miles de contenedores al mismo tiempo.

## 2. Flexibilidad de uso

Otro punto en el que Argo Workflows aventaja a Airflow es la flexibilidad. 
Airflow está pensado como un orquestador de tareas programadas y predefinidas,
y es difícil salirse del patrón de ejecución de un mismo *job* 
 en un momento prederminado.

Por el contrario,  Argo Workflows está diseñado para ser flexible. Por un lado,
parametrizar *workflows* es extremadamente sencillo, de forma que podamos ejecutar
el mismo trabajo con distintas variables de entrada cada vez. Además, a través de
[Argo Events](https://argoproj.github.io/argo-events/) podemos programar el
lanzamiento de trabajos a partir de eventos externos.

## 3. Definición de *workflows*

Tanto Airflow como Argo usan DAGs (*directed acyclic graphs*) como forma de especificar las interdependencias entre los pasos de un flujo de trabajo. Un DAG es un grafo
 acíclico dirigido como el que podemos observar en la imagen.

![dag](../assets/images/2022-09-08-big-data-platform-2/dag.jpeg)

- Es **dirigido** porque la relación entre dos pasos tiene dirección 
  (de una tarea anterior a una posterior) y,
- es **acíclico** porque no contiene ciclos: partiendo de un nodo (tarea) y siguiendo
  el camino que marcan los vérticos, nunca podremos llegar al nodo inicial. Si esto
  sucediese, es *job* nunca se acabaría.

Con Airflow, la definición se hace mediante scripts de Python. Argo implementa un CRD (*custom resource definition*) de Kubernetes, por lo que instanciamos los DAGs en simples ficheros YAML.

Pero no siempre necesitamos un DAG para representar nuestro flujo de trabajo. 
En muchos casos, una simple lista de pasos consecutivos podría bastar. 
Y Argo nos lo pone muy fácil en este caso, ya que también permite definir flujos de trabajos como listas de pasos

## En resumen

En nuestra misión por construir una plataforma *open-source* capaz de dar soporte a todo tipo de proyectos de Big Data, hemos añadido una pieza esencial: el orquestador de flujos de trabajo. Hemos escogido Argo Workflows no solo por ser un orquestador nativo de Kubernetes, sino por ser más flexible, más potente y, creemos, más sencillo, que otras alternativas.

En [Github]() encontrarás los pasos para instalar las herramientas que hemos
presentado hasta ahora, y también ver algunos ejemplos de definiciones de *workflows*.



