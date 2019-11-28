---
layout: post
title:  "Búsquedas de texto completo con PostgreSQL"
date:   2019-11-27 9:00:00
author: ugaitz
categories: sql,postgre,base de datos,bbdd
tags: sql,postgre,base de datos,bbdd,postgresql,fulltext
header-image:	post-headers/data.jpg
---

Hay veces en los que nos encontramos con la necesidad de buscar un registro en una base de datos partiendo de alguna palabra que uno de los campos de la tabla contiene. Si la búsqueda que queremos realizar es muy sencilla, normalmente será suficiente con hacer un _LIKE_ en la consulta. Pero si la consulta que queremos realizar es un poco compleja, veremos que utilizar _LIKE_ no será viable.

En este artículo mostraremos algunas de las limitaciones de _LIKE_ y de que otras opciones disponemos en PostgreSQL. 

Si queremos ejecutar estas consultas y no tenemos un postgre instalado en nuestra máquina local, podremos hacerlo fácilmente docker:

```
docker run -d --name postgres-full-text  postgres
docker exec -it postgres-full-text  psql -U postgres
```
Escribiremos `exit` para salir, y podremos borrar el contenedor con el el comando `docker rm -f postgres-full-text`

## Buscar con _LIKE_
Cuando queremos buscar una sola palabra sobre un texto _natural_, como podría ser el contenido de una noticia, la búsqueda con _LIKE_ se complica ya que hay muchos matices que hay que tener en cuenta:

- Si buscamos utilizando _LIKE '%palabra%'_ la consulta también devolverá palabras que contengan lo que se ha buscado, en este ejemplo se ve que si buscamos _texto_ en _contexto_, nos devuelve true.

```
SELECT 'contexto' LIKE '%texto%' as contiene;
```

![contiene1](/assets/images/2019-10-03-busqueda-textos-postgresql/contiene-1.png){: .center }

- Si le añadimos unos espacios para que sea _LIKE '% palabra %'_, cuando la palabra que buscamos está al final de una frase terminando con un punto _(.)_ o es un texto inicial, no lo encontrará:

```
SELECT 'texto texto.' LIKE '% texto %' as contiene;
```
![contiene2](/assets/images/2019-10-03-busqueda-textos-postgresql/contiene-2.png){: .center }

Para que este tipo de búsqueda de texto funcione correctamente, tendríamos que utilizar una expresión complicada que haría que nuestra consulta tardara más de lo debido. Y además de esta complejidad, ¿Qué pasa con las palabras en singular o plural? ¿Cuánto se nos complicaría la expresión para realizar estas búsquedas correctamente?

## Buscar con _tsvector_ y _tsquery_

Para solucionar este tipo de problemas se suele recurrir a herramientas como _Elastic search_. Pero si tenemos una base de datos _PostgreSQL_ y no necesitamos todo el potencial de este tipo de herramientas, desde PostgreSQL 8.3 nos encontramos con un tipo de dato que podría evitarnos quebraderos de cabeza.

### tsvector

Con la función _to_tsvector_ podemos transformar un texto al tipo de dato _tsvector_ separando las palabras, convirtiendolo en lexemas y creando índices optimizados para las búsquedas de texto. Al realizar esta transformación tiene en cuenta la configuración del idioma del servidor, por ejemplo:

```
SELECT to_tsvector('Grumpy wizards make toxic brew for the evil queen and Jack');
```

![contiene2](/assets/images/2019-10-03-busqueda-textos-postgresql/grumpy-wizard.png){: .center }

En la transformación se puede ver que ha elimado las palabras _for_, _the_ y _and_ y ha transformado otras como _Grumpy_ o _wizards_. En este caso ha funcionado correctamente por que el texto escrito estaba en inglés, que es el mismo idioma en el que está configurado nuestra base de datos. ¿Qué pasaría si pusieramos texto en castellano?

```
SELECT to_tsvector('El veloz murciélago hindú comía feliz cardillo y kiwi');
```
![contiene2](/assets/images/2019-10-03-busqueda-textos-postgresql/murcielagohindu-1.png){: .center }

Cómo el idioma por defecto de PostgreSQL es el inglés, el parseo no ha ido muy bien. Sigue apareciendo _el_ y _y_ que no deberían aparecer, por eso el método _to_tsvector_ acepta el parámetro de idioma, por lo que se podría hacer lo siguiente:

```
SELECT to_tsvector('spanish','El veloz murciélago hindú comía feliz cardillo y kiwi');
```
![contiene2](/assets/images/2019-10-03-busqueda-textos-postgresql/murcielagohindu-2.png){: .center }

Al haber hecho la transformación se puede ver que ha eliminado palabras como _y_ y _el_ y ha modificado otras quitando tildes, generos y conjugación de verbos.

### tsquery

Para crear querys y buscar en _tsvector_ está el tipo de dato _tsquery_. Del mismo modo que _to_tsvector_ tenemos el método _to_tsquery_. Con este método convertiremos querys para buscar palabras o textos a un formato adecuado para buscar en tsvector. Es posible pasar el método de idioma del mismo modo que con _to_tsvector_.

```
SELECT to_tsquery('comer') as english, to_tsquery('spanish','comer') as spanish;
```

![contiene2](/assets/images/2019-10-03-busqueda-textos-postgresql/murcielagohindu-3.png){: .center }

En este caso, el verbo _comer_ lo ha modificado también a _com_, lo que hará que al buscar _comer_ en un texto donde pone _comía_ lo encuentre. Para realizar búsquedas, utilizaremos dos arrobas _(@@)_ entre _tsvector_ y _tsquery_

```
SELECT to_tsvector('spanish','El veloz murciélago hindú comía feliz cardillo y kiwi') @@ to_tsquery('spanish', 'comer') as encontrado;
```

![contiene2](/assets/images/2019-10-03-busqueda-textos-postgresql/encontrado.png){: .center }

Si tuvieramos una tabla _documentos_ con una columna _documento_tsvector_ de tipo _tsvector_ y quisiéramos encontrar solamente los registros con la palabra _comer_, podríamos hacerlo la siguiente forma:

```
SELECT * FROM documentos WHERE documento @@ tsquery('spanish', 'comer');
```

_tsquery_ ofrece múltiples posibilidades a la hora de buscar, aquí ponemos los que nos parecen más relevantes:

- _and (&)_: Si queremos que el texto contenga varias palabras

```
SELECT to_tsvector('spanish','El veloz murciélago hindú comía feliz cardillo y kiwi') @@ to_tsquery('spanish', 'comer & feliz') as encontrado;
```
![encontrado](/assets/images/2019-10-03-busqueda-textos-postgresql/encontrado.png){: .center }

```
SELECT to_tsvector('spanish','El veloz murciélago hindú comía feliz cardillo y kiwi') @@ to_tsquery('spanish', 'comer & triste') as encontrado;
```
![contiene2](/assets/images/2019-10-03-busqueda-textos-postgresql/noencontrado.png){: .center }

- _or_ (\|): Si queremos que el texto contenga una de las palabras

```
SELECT to_tsvector('spanish','El veloz murciélago hindú comía feliz cardillo y kiwi') @@ to_tsquery('spanish', 'comer | triste') as encontrado;
```
![encontrado](/assets/images/2019-10-03-busqueda-textos-postgresql/encontrado.png){: .center }

```
SELECT to_tsvector('spanish','El veloz murciélago hindú comía feliz cardillo y kiwi') @@ to_tsquery('spanish', 'cenar | triste') as encontrado;
```
![no encontrado](/assets/images/2019-10-03-busqueda-textos-postgresql/noencontrado.png){: .center }

- _<->_: Si queremos que tenga dos palabras consecutivas

```
SELECT to_tsvector('spanish','El veloz murciélago hindú comía feliz cardillo y kiwi') @@ to_tsquery('spanish', 'veloz <-> murciélago') as encontrado;
```
![encontrado](/assets/images/2019-10-03-busqueda-textos-postgresql/encontrado.png){: .center }

```
SELECT to_tsvector('spanish','El veloz murciélago hindú comía feliz cardillo y kiwi') @@ to_tsquery('spanish', 'veloz <-> hindú') as encontrado;
```
![no encontrado](/assets/images/2019-10-03-busqueda-textos-postgresql/noencontrado.png){: .center }

- _&lt;N&gt;_: Si buscamos dos palabras que estén a una distancia de _N_

```
SELECT to_tsvector('spanish','El veloz murciélago hindú comía feliz cardillo y kiwi') @@ to_tsquery('spanish', 'veloz <2> hindú') as encontrado;
```
![encontrado](/assets/images/2019-10-03-busqueda-textos-postgresql/encontrado.png){: .center }

```
SELECT to_tsvector('spanish','El veloz murciélago hindú comía feliz cardillo y kiwi') @@ to_tsquery('spanish', 'veloz <3> hindú') as encontrado;
```
![no encontrado](/assets/images/2019-10-03-busqueda-textos-postgresql/noencontrado.png){: .center }

Podemos encontrar más acerca de las posibilidades de _tsquery_ en la [documentación][textsearch-documentation]{:target="_blank"}.

### ts_rank

Por último, comentar que es posible ordenar los artículos por relevancia utilizando _ts_rank_. Este método le asigna un valor numérico a la relevancia de _"acierto"_ de la búsqueda en el texto. Por ejemplo, no es lo mismo que en una búsqueda con _or_ estén las 3 palabras que se buscan, o solo esté una.

```
SELECT ts_rank(to_tsvector('spanish','El veloz murciélago hindú comía feliz cardillo y kiwi'),to_tsquery('spanish', 'veloz | murcielago | hindú'));
```
![no encontrado](/assets/images/2019-10-03-busqueda-textos-postgresql/rank-1.png){: .center }

```
SELECT ts_rank(to_tsvector('spanish','El veloz canguro australiano comía feliz cardillo y kiwi'),to_tsquery('spanish', 'veloz | murcielago | hindú'));
```
![no encontrado](/assets/images/2019-10-03-busqueda-textos-postgresql/rank-2.png){: .center }

Para aplicar _ts_rank_ en una consulta, podríamos hacerlo de la siguiente manera.

```
SELECT * FROM documentos ORDER BY ts_rank(document, tsquery('spanish', 'comer')) DESC;
```

[textsearch-documentation]: https://www.postgresql.org/docs/current/textsearch.html