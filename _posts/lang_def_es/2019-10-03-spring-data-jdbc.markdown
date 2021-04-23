---
layout: post
title: "Spring Data, JDBC frente a JPA"
date: 2019-10-03 10:00:00
author: ugaitz
lang: es
categories: base de datos,spring,jdbc, JPA
tags: base de datos,spring,jdbc, JPA
header-image:	post-headers/data.jpg
---
_Spring Data JDBC_ es una librería para facilitar la creación de repositorios que acceden a bases de datos sin tratar con la complejidad que supone utilizar JPA. El hecho de que JPA ofrezca muchas funcionalidades como caché, carga de relaciones bajo demanda _(Lazy)_, etc. supone que el desarrollador tenga que tener en cuenta cierta complejidad.

Hemos creado [este proyecto de github][github-project]{:target="_blank"} para realizar pruebas con Spring Data JDBC y JPA. En la rama [jpa][github-project-jpa]{:target="_blank"} se pueden encontrar test de los siguientes casos.

- Si hay un modelo cargado en la aplicación y se vuelve a hacer una búsqueda, la instancia del objeto nuevo y el viejo será misma y no se habrá vuelto a ejecutar una consulta. Para forzar una nueva consulta habrá que hacer un _entityManager.clear()_. (test [reloadModel1][jpa-reload-model-1]{:target="_blank"} y [reloadModel2][jpa-reload-model-2]{:target="_blank"})
- Las relaciones de una entidad se cargan bajo demanda, si por alguna razón se cierra la conexión a la base de datos y después se intenta acceder a una relación, este método fallará. (test [lazyLoad][jpa-lazy-load]{:target="_blank"})
- JPA se encarga de los UPDATE, no solo no es necesario hacer un _repositorio.save()_ para actualizar un modelo, sino que el hacerlo no asegura que se vaya a actualizar en ese momento. Cuando se vaya a cerrar la conexión, JPA hará un _flush_ y será entonces cuando se realizará el guardado. El haber pasado por el setter de la propiedad de un modelo es la razón para actualizarlo, por eso hay que tener mucho cuidado con los cambios que se le hacen a un objeto cargado desde JPA. (test [update][jpa-update-1]{:target="_blank"} y [update2][jpa-update-2]{:target="_blank"})

_Spring Data JDBC_ es una solución más simple, sin uso de cachés ni proxys, sin _"magia"_ por detrás con automatizaciones pero que hace lo que se le indica en cada comando.

Hemos creado otros test en la rama _master_ del [mismo proyecto][github-project]{:target="_blank"} donde se pueden ver los siguientes casos:
- Cada vez que se realiza una búsqueda, se ejecuta una consulta y la instancia del objeto devuelto es distinta. (test [reloadModel][jdbc-reload-model]{:target="_blank"})
- Obtiene las relaciones del modelo en el mismo instante en el que se obtiene el propio modelo. (test [notLazyLoad][jdbc-not-lazy-load]{:target="_blank"})
- La actualización del modelo en la base de datos se realiza explícitamente, cambiar el objeto no implica el cambio en base de datos. (test [update][jdbc-update]{:target="_blank"})


## Algunas limitaciones de Spring Data JDBC
Spring Data JDBC simplifica muchas acciones, pero también tiene ciertas limitaciones, sobre todo en acciones con modelos relacionados.
- Como la instancia de un modelo no tiene ningún proxy, no puede saber que propiedades se han añadido o borrado de un objeto, por lo que al ejecutar un guardado de un modelo con tablas relacionadas, estas siempre se borran y se vuelven a insertar. (test updateWithRelations)
- Así como JPA acepta relaciones _OneToMany_, _ManyToOne_ o _ManyToMany_, Spring Data JDBC acepta solo relaciones _OneToMany_.
- Aún no está implementada la interfaz _PagingAndSortingRepository_, lo que implica que la paginación hay que hacerla de manera manual, como por ejemplo, haciendo uso de _@Query_. Hay una tarea en el [jira de Spring][jira-pagination]{:target="_blank"}, pero es de prioridad _minor_.

[github-project]: https://github.com/wearearima/spring-data-jdbc-demo
[github-project-jpa]: https://github.com/wearearima/spring-data-jdbc-demo/tree/jpa
[jpa-reload-model-1]: https://github.com/wearearima/spring-data-jdbc-demo/blob/b4224ffb83561e88598c23b5047885cb6ee86369/src/test/java/eu/arima/springdatajdbcdemo/CountryRepositoryTests.java#L43
[jpa-reload-model-2]: https://github.com/wearearima/spring-data-jdbc-demo/blob/b4224ffb83561e88598c23b5047885cb6ee86369/src/test/java/eu/arima/springdatajdbcdemo/CountryRepositoryTests.java#L51
[jpa-update-1]: https://github.com/wearearima/spring-data-jdbc-demo/blob/b4224ffb83561e88598c23b5047885cb6ee86369/src/test/java/eu/arima/springdatajdbcdemo/CountryRepositoryTests.java#L71
[jpa-update-2]: https://github.com/wearearima/spring-data-jdbc-demo/blob/b4224ffb83561e88598c23b5047885cb6ee86369/src/test/java/eu/arima/springdatajdbcdemo/CountryRepositoryTests.java#L83
[jpa-lazy-load]: https://github.com/wearearima/spring-data-jdbc-demo/blob/b4224ffb83561e88598c23b5047885cb6ee86369/src/test/java/eu/arima/springdatajdbcdemo/CountryRepositoryTests.java#L60
[jdbc-reload-model]: https://github.com/wearearima/spring-data-jdbc-demo/blob/cf888e3b0ff6fb6a1a08dbddf1ca0722654f0352/src/test/java/eu/arima/springdatajdbcdemo/CountryRepositoryTests.java#L42
[jdbc-not-lazy-load]: https://github.com/wearearima/spring-data-jdbc-demo/blob/cf888e3b0ff6fb6a1a08dbddf1ca0722654f0352/src/test/java/eu/arima/springdatajdbcdemo/CountryRepositoryTests.java#L50
[jdbc-update]: https://github.com/wearearima/spring-data-jdbc-demo/blob/cf888e3b0ff6fb6a1a08dbddf1ca0722654f0352/src/test/java/eu/arima/springdatajdbcdemo/CountryRepositoryTests.java#L59
[jira-pagination]: https://jira.spring.io/browse/DATAJDBC-101