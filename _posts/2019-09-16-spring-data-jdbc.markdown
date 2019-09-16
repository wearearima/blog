---
layout: post
title: "Spring Data, JDBC frente a JPA"
date: 2019-09-16 5:00:00
author: ugaitz
categories: base de datos,spring,jdbc
tags: 
header-image:	headers/data.jpg
---
_Spring Data JDBC_ es una librería para facilitar la creación de repositorios que acceden a bases de datos sin tratar con la complejidad que supone utilizar JPA. El hecho de que JPA ofrezca muchas funcionalidades como caché, carga de relaciones bajo demanda _(Lazy)_, etc. supone que el desarrollador tenga que tener en cuenta ciertas características.

En la rama _jpa_ de [este proyecto de github][github-project]{:target="_blank"} se pueden encontrar test de los siguientes casos.
- Si hay un modelo cargado en la aplicación y se vuelve a hacer una búsqueda, la instancia del objeto nuevo y el viejo será misma y no se habrá vuelto a ejecutar una consulta. Para forzar una nueva consulta habrá que hacer un _entityManager.clear()_. _(test reloadModel y reloadModel2)_
- Las relaciones de una entidad se cargan bajo demanda, si por alguna razón se cierra la conexión a la base de datos y después se intenta acceder a una relación, este método fallará. _(test lazyLoad)_
- JPA se encarga de los UPDATE, no solo no es necesario hacer un _repositorio.save()_ para actualizar un modelo, sino que el hacerlo no asegura que se vaya a actualizar en ese momento. Cuando se vaya a cerrar la conexión, JPA hará un _flush_ y será entonces cuando se realizará el guardado. El haber pasado por el setter de la propiedad de un modelo es la razón para actualizarlo, por eso hay que tener mucho cuidado con los cambios que se le hacen a un objeto cargado desde JPA. _(test update y update2)_

Una solución que utilice _Spring Data JDBC_ es una solución más simple, sin uso de caches ni proxys, sin _"magia"_ por detrás con automatizaciones pero que hace lo que se le indica en cada comando.

En la rama _master_ del [mismo proyecto][github-project]{:target="_blank"} se pueden ver los siguientes casos:
- Cada vez que se realiza una búsqueda, se ejecuta una consulta y la instancia del objeto devuelto es distinta. (test reloadModel)
- Obtiene las relaciones del modelo en el mismo instante en el que se obtiene el propio modelo. (test notLazyLoad)
- La actualización del modelo en la base de datos se realiza explícitamente, cambiar el objeto no implica el cambio en base de datos. (test update)


## Algunas limitaciones de Spring Data JDBC
Spring Data JDBC simplifica muchas acciones, pero también tiene ciertas limitaciones, sobre todo en acciones con modelos relacionados.
- Como la instancia de un modelo no tiene ningún proxy, no puede saber que propiedades se han añadido o borrado de un objeto, por lo que al ejecutar un guardado de un modelo con tablas relacionadas, estas siempre se borran y se vuelven a insertar. (test updateWithRelations)
- Así como JPA acepta relaciones _OneToMany_, _ManyToOne_ o _ManyToMany_, Spring Data JDBC acepta solo relaciones _OneToMany_.
- Aún no está implementada la interfaz _PagingAndSortingRepository_, lo que implica que la paginación hay que hacerla de manera manual, como por ejemplo, haciendo uso de _@Query_. Hay una tarea en el [jira de Spring][jira-pagination]{:target="_blank"}, pero es de prioridad _minor_.

[github-project]: https://github.com/wearearima/spring-data-jdbc-demo
[jira-pagination]: https://jira.spring.io/browse/DATAJDBC-101