---
layout: post
title:  "Exprimiendo tu Data Lake (Parte I, Hudi)"
date:   2020-10-20 9:00:00
author: juan
lang: es
categories: big data, data lake, apache hudi
tags: big data, data lake, apache hudi, docker, data warehouse, parquet, avro, orc, delta lake, iceberg
header-image: 2020-10-20-exprimiendo-tu-data-lake-parte-I-hudi/post-header.jpg
---

Desde que surgieron las primeras bases de datos en los años 70, siempre se ha buscado la forma de explotar esa información tratando de extraer indicadores que ayuden en la toma de decisiones. Así es como nacieron las herramientas conocidas como Data Warehouse que estaban dirigidas a almacenar y explotar la información. Muchas de estas herramientas están compuestas por [bases de datos columnares](https://en.wikipedia.org/wiki/Column-oriented_DBMS){:target="_blank"} que permiten realizar consultas analíticas de una forma mucho más eficiente que las bases de datos orientadas a fila utilizadas habitualmente en las bases de datos operacionales.

Con el tiempo, las necesidades y volúmenes de información con las que las empresas trabajan han crecido de forma exponencial. En los últimos 15 años, hemos visto a empresas como Google, Microsoft, Amazon, Facebook, Uber, Netflix o Twitter manejando inmensas cantidades de volúmenes de datos y tráfico. Los Data Warehouse tradicionales no eran capaces de manejar estos volúmenes en un periodo de tiempo razonable y en muchos casos necesitaban de varios días para poder ejecutar las consultas.

Esta situación forzó a estas empresas a liderar un cambio lanzando papers y nuevas herramientas que les permitieran analizar ingentes cantidades de información de manera más eficiente. El pistoletazo de salida lo dió Google publicando los papers [Google File System](https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf){:target="_blank"} (2003) y [Map Reduce](https://static.googleusercontent.com/media/research.google.com/en//archive/mapreduce-osdi04.pdf){:target="_blank"} (2004). Pocos años después (2006), Yahoo hizo público el proyecto open source Hadoop que estaba basado en los papers de Google mencionados. Hadoop cambió la industria de la analítica de datos tal y como la conocíamos hasta entonces y dió inicio al movimiento denominado “Big Data”.

El stack Hadoop básicamente permitía almacenar ([HDFS](https://hadoop.apache.org/docs/r1.2.1/hdfs_design.html){:target="_blank"}) y procesar ([Map Reduce](https://static.googleusercontent.com/media/research.google.com/en//archive/mapreduce-osdi04.pdf){:target="_blank"}) la información de forma distribuida. Esto aumentaba la capacidad de procesamiento ya que se podía escalar horizontalmente añadiendo más máquinas al sistema.

El disponer de un sistema de archivos distribuido como HDFS, posibilitó que muchas organizaciones comenzasen a almacenar datos que antes tenían que desechar. Esta tendencia se hizo todavía más notoria con el nacimiento de productos como Amazon S3 que permiten almacenar cualquier tipo de información de forma económica en la nube. Esta nueva realidad, llevó a James Dixon (fundador de Pentaho) a acuñar el concepto Data Lake en 2010. Los Data Lake se presentaban como almacenes de datos en los que se puede encontrar la información en crudo tal cual ha sido recibida y sin ningún tipo de procesamiento. De esta forma, se podía empezar a almacenar información con la expectativa de que algún día se pudiera explotar de alguna manera.

Esta aproximación que resultó atractiva para muchas organizaciones, entrañaba también un peligro evidente. Almacenar la información sin ningún criterio puede provocar que nuestro Data Lake se convierta en un cajón de sastre, donde encontrar y organizar la información sea bastante complicado y por lo tanto, nunca se llegue a sacar ningún provecho de la misma.

<p align="center">
    <img src="/assets/images/2020-10-20-exprimiendo-tu-data-lake-parte-I-hudi/messy-room.png">
</p>

Otro de los inconvenientes de Hadoop, es que era necesario tener conocimientos de programación para poder realizar operaciones analíticas sobre los datos almacenados en el sistema de archivos distribuido. Esto hacía que para algunos perfiles directivos o analistas fuese imposible realizar las exploraciones por sí mismos sin la ayuda de un(a) programador(a). Por este motivo, empezaron a surgir multitud de proyectos como Apache Hive que añadían capas SQL sobre este tipo de sistemas de archivos distribuidos. Estas capas SQL vinieron acompañadas de nuevos formatos de almacenamiento que eran más eficientes y se asemejaban a las utilizadas en bases de datos tradicionales ya que algunos estaban orientados a fila (Avro) y otros a columna (Parquet, ORC).

<p align="center">
    <img src="/assets/images/2020-10-20-exprimiendo-tu-data-lake-parte-I-hudi/parquet-orc-avro.png">
</p>

Disponer de Data Lakes capaces de almacenar información de manera eficiente y accesible mediante SQL, puede llevarnos a pensar que estos pueden reemplazar completamente los Data Warehouse más tradicionales. A pesar de que la línea que los separa es cada vez más fina, hay ciertas características que los Data Lakes no tienen y que con el tiempo se ha visto que son necesarias:

* Poder realizar actualizaciones de manera eficiente. Formatos como Parquet, por defecto, no están preparados para ser actualizados y requieren de procesos manuales que son pesados y poco eficientes.
* Transacciones ACID con las que poder asegurar la atomicidad, consistencia, aislamiento y durabilidad de las operaciones.
* <i>Lineage</i> o seguimiento, para saber qué modificaciones han tenido los datos a lo largo del tiempo.
* Evolución del esquema o estructura.

En los últimos años han aparecido algunas soluciones que pretenden cubrir estas necesidades, como por ejemplo:

* Apache hudi
* Delta Lake
* Apache Iceberg

En este artículo vamos a hablar sobre Apache Hudi, pero probablemente hablaremos sobre Delta Lake y Iceberg en futuras entradas.

<p align="center">
    <img src="/assets/images/2020-10-20-exprimiendo-tu-data-lake-parte-I-hudi/apache-hudi.png">
</p>

<i>Apache Hudi</i> es un proyecto open source destinado a crear data lakes eficientes y a almacenar grandes conjuntos de datos en sistemas de archivos HDFS o sistemas de archivos en la nube como S3. El propio nombre del proyecto es una declaración de intenciones de las características que proporciona: Hudi (<b>H</b>adoop <b>U</b>psert <b>D</b>elete and <b>I</b>ncremental).

<i>Hudi</i> por tanto, permite aplicar actualizaciones de forma eficiente sobre archivos Parquet almacenados en sistemas de archivos distribuidos ocupándose de aspectos como la compactación y otorgando capacidades ACID. Además, permite hacer consultas incrementales de forma que se pueden obtener todas las modificaciones que se hayan llevado a cabo desde un momento determinado. Esto abre la puerta a poder realizar analíticas en streaming sin tener que implantar infraestructuras complejas como las propuestas en la [arquitectura lambda](http://lambda-architecture.net){:target="_blank"}.

Hudi tiene dos modos de funcionamiento, siendo cada uno de ellos más indicado en función de la frecuencia con la que se lleven a cabo lecturas o escrituras sobre los datos:

* Copy on Write (CoW) 
* Merge on Read (MoR) 

Las diferencias entre estos dos modos se pueden encontrar en la [documentación oficial](https://hudi.apache.org/docs/concepts.html#table-types--queries){:target="_blank"}.

En el [siguiente](https://github.com/wearearima/hudi-exercise){:target="_blank"} repositorio de Github tenemos implementado un ejemplo en el que se puede ver cómo se utiliza Hudi, así como algunas de sus capacidades. En él se procesan entradas de la Wikipedia con Apache Spark, identificando aquellas que se corresponden con celebridades. El resultado se almacena en HDFS con formato Parquet haciendo uso de la herramienta Hudi. Una vez se ha completado esta operación se llevan a cabo nuevos procesos que provocan actualizaciones sobre los datos. En ellos veremos como HUDI gestiona automáticamente la creación y compactación de los nuevos archivos Parquet, guardando <i>commits</i> en cada una de la operaciones con las que se puede comprobar el <i>lineage</i> de lo datos.

Utilizaremos el módulo `hudi-spark` que ofrece una <i>API Datasource</i> con el que se puede escribir (y leer) un Dataframe de Spark en una tabla Hudi, de la siguiente manera:

```python
df.write.format("hudi") \
.options(**hudi_options).mode("overwrite").save(basePath)
```

No obstante, dispone de otro módulo llamado <i>DeltaStreamer</i> con el que se puede trabajar con fuentes de streaming, como puede ser Apache Kafka. Más información [aquí](https://hudi.apache.org/docs/writing_data.html){:target="_blank"}.


## Conclusiones

En este artículo hemos visto cuál fue la motivación que llevó al nacimiento de los almacenes de datos conocidos como Data Lake. Hemos mencionado también algunas de las carencias e inconvenientes que tienen las mismas y cómo han aparecido herramientas que pretenden paliarlas. ¿Significa esto que los Data Lake van a evolucionar lo suficiente como para poder convertirse en nuestra única fuente de datos? Quizás es pronto para hacer una afirmación así pero lo que sí parece seguro es que estamos en un momento de cambios en el ecosistema big data y que los próximos años se presentan apasionantes en este sector.