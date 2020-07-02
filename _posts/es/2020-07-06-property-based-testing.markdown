---
layout: post
title:  "Otra forma de hacer tests: property based testing"
date:   2020-07-07 9:00:00
author: jessica
lang: es
categories: testing, software quality, QA
tags: testing, property based testing, PBT, calidad, software quality, QA, junit
header-image:	post-headers/property-based-testing.jpg
---

## ¿Qué es property based testing?
*Property based testing* (en adelante PBT) es una alternativa (más) para el desarrollo de tests, cuyo eje principal en lugar de ser un ejemplo/caso concreto pasa a ser una propiedad del caso de uso, entendiendo que una propiedad viene a ser algo así como:

> para cualquier entrada (x,y,....)  
> que cumpla la precondición pre(x,y….) se cumple que  
> la propiedad(x,y….) es verdad

Normalmente las propiedades no son demasiado detalladas, únicamente verifican alguna característica general que debe cumplirse.

Por ejemplo, para testear un método custom de sumas, en caso de estar haciendo _example based testing_, podríamos tener varios tests como estos:
<pre>
<code>- dados los números 10 y 1 la suma será 11
- dados los números 10 y 20 la suma será 30
  . . . . </code></pre>

  
Sin embargo, si estuviésemos haciendo PBT, formularíamos un test más general, por ejemplo como el que se muestra a continuación:
<pre>
<code>para cualquier número entero a y b que estén entre que 1 y 20
la suma de  a y b será mayor que a</code></pre>

  
Veamos qué implicaciones tiene un test como este.
### Para cualquier entrada (_a, b_)
> <pre style="margin-bottom: 0px">
> <code><b>para cualquier número entero a y b</b> que estén entre que 1 y 20
la suma de a y b será mayor que a</code></pre>  

Se ejecutarán varios sets de prueba con combinaciones de valores random para `a` y `b` (el número exacto de ejecuciones depende del framework/librería utilizado y suele ser configurable).

### Que cumpla la precondición (_entre 1 y 20_)
> <pre style="margin-bottom: 0px">
> <code>para cualquier número entero <b>entre 1 y 20 (a, b)</b>
la suma de a y b será mayor que a</code></pre>

Estamos indicando una precondición de que tanto `a` como `b` deben estar comprendidos entre `1` y `20`. Si los valores random que se generan para un test (una ejecución de un test, si somos puristas) no la cumplen se descarta como test válido y se continúa con otros valores.

### La propiedad (_a+b > a_) es verdad
> <pre style="margin-bottom: 0px">
> <code>para cualquier número entero entre 1 y 20 (a, b)
<b>la suma de a y b será mayor que a</b></code></pre>

Comprobación que se ejecutará cada vez.

## De la teoría a la práctica
Vale y ¿esto como aplica a mis caso de uso? Repaso mis tests, definidos en [GetDayStatusSummaryForWorkerAndDayTests.java](https://github.com/wearearima/time-report-pbt/blob/feature/01_tests_jqwik_property_test/src/test/java/eu/arima/tr/reports/reportsServiceImpl/GetDayStatusSummaryForWorkerAndDayTests.java){:target="_blank"} y pienso en si alguno de ellos podría escribirse en base a propiedades del método sin importar los valores “exactos” de los parámetros.
Me doy cuenta de que tengo dos tests que en realidad están escritos en estos términos:
```java
@Test
@Displayname (“Given the username of a worker the status result has that username”)
void the_status_result_belongs_to_the_requested_worker() {
  DayStatusSummary result = reportsService.getDayStatusSummaryForWorkerAndDay(USERNAME, DAY);
  assertEquals(USERNAME, result.getWorkerUserName());

}

@Test
@Displayname (“Given a date the status result has that date”)
void the_status_result_belongs_to_the_requested_day() {
 LocalDate day = DAY;
 DayStatusSummary result = reportsService.getDayStatusSummaryForWorkerAndDay(USERNAME, day);
 assertEquals(day, result.getDate());
}
```
En ambos estoy haciendo tests basados en ejemplos concretos, pero en realidad si leemos lo que se pretende probar, es bastante más genérico: ¿quizás podríamos aplicar aquí PBT?

Para Java hay varias herramientas, las más populares son:
* [junit-quickcheck](https://pholser.github.io/junit-quickcheck/site/0.9.1/#){:target="_blank"}
* [jqwik](https://jqwik.net/){:target="_blank"}

A priori la primera de ellas no soporta JUnit 5, así que vamos a probar con **jqwik**. 

Añadimos la dependencia en el pom.xml
```xml
<dependency>
  <groupId>net.jqwik</groupId>
  <artifactId>jqwik</artifactId>
  <version>1.3.1</version>
  <scope>test</scope>
</dependency>
```
Y pasamos a reformular nuestros tests en "formato" PBT:
```java
public class GetDayStatusSummaryForWorkerAndDayPropertyTests {

  ReportsServiceImpl reportsService;

  @BeforeProperty
  void setup() {
    reportsService = new ReportsServiceImpl(mock(WorklogRepository.class));
  }

  @Property
  @Label("Given the username of a worker and a date the status result has that username and date")
  boolean the_status_result_belongs_to_the_requested_worker(@ForAll String username, @ForAll("localdates") LocalDate date) {

    DayStatusSummary result = reportsService.getDayStatusSummaryForWorkerAndDay(username, date);
    
    return result.getDate().equals(date) && result.getWorkerUserName().equals(username);
}

  @Provide
  Arbitrary<LocalDate> localdates() {
    Arbitrary<Integer> years = Arbitraries.integers().between(1900, 2099);
    Arbitrary<Integer> months = Arbitraries.integers().between(1, 12);
    Arbitrary<Integer> days = Arbitraries.integers().between(1, 31);
  
    return Combinators.combine(years, months, days).as(LocalDate::of).ignoreException(DateTimeException.class);
  }

}
```
Voila! Nuestro test se ejecuta 1000 veces con una batería de parámetros de entrada diferente cada vez (es como si hubiésemos generado y ejecutado 1000 tests diferentes). Si mostramos por consola ambos parámetros veremos las 1000 combinaciones que se ejecutan. El número de ejecuciones por defecto varía en función de la herramienta seleccionada y normalmente es configurable. Si lo ejecutamos una segunda vez, se ejecutará 1000 veces con otra batería de parámetros diferente.

Nota: Este ejemplo al completo está disponible en [Github](https://github.com/wearearima/time-report-pbt/tree/feature/01_tests_jqwik_property_test){:target="_blank"}. Para personalizar/configurar diferentes parámetros consultar la documentación de [jqwik](https://jqwik.net/){:target="_blank"}.

## En resumen
Hasta aquí un caso muy simple que nos ha servido para entender el concepto de _property based testing_. Leyendo la documentación y revisando el estado del arte, parece que en casos más complejos hacer PBT es más complicado: tanto a la hora de formular/identificar los tests como a la hora de implementarlos.

Está claro que como otras muchas herramientas/tendencias en testing, no hay nada blanco o negro. No hay un tipo de test mejor que otro, al menos no de forma absoluta: depende del contexto (funcionalidad/proyecto…) al que aplique.

En base a esto y a lo investigado, las ideas con las que me quedaría son:
* Con _property based testing_ podemos reemplazar varios tests basados en ejemplo por uno sólo, testeando el método con múltiples combinaciones de inputs (que variarán en cada ejecución). Es más complicado identificarlos dada su genericidad.

* Con _example based testing_ las combinaciones serán las elegidas por el desarrollador (fijas en todas las ejecuciones) y los tests serán muy concretos. Son sencillos de desarrollar y de entender. No son tan exhaustivos.

A primera vista, se me ocurre: y ¿por qué no usar `@ParameterizedTests` con un método que genere los parámetros de forma aleatoria? ¿Qué ofrece PBT que no pueda lograr con tests parametrizados?

Básicamente, nos ofrece la posibilidad de tener no sólo valores para los inputs aleatorios, sino que además diferentes combinaciones entre ellos (algo que de otro modo tendríamos que implementar de alguna forma).

Por ejemplo, en [Github](https://github.com/wearearima/time-report-pbt/tree/feature/02_tests_jqwik_combinedValues){:target="_blank"} hemos añadido un `System.out.println` para los parámetros del test anterior y además hemos creado una clase `JqwikPropertiesTests.java` cuyo objetivo únicamente es ver las combinatorias:
```java
@Property(edgeCases = EdgeCasesMode.FIRST, tries = 30)
void printCombinedValuesOfTwoParams(@ForAll @IntRange(min = 0, max = 10) int a, @ForAll @IntRange(min = 0, max = 10) int b) {
  String parameters = String.format("%s, %s", a, b);
    System.out.println(parameters);
}

@Property(edgeCases = EdgeCasesMode.FIRST, tries = 30)
void printCombinedValuesOfThreParams(@ForAll @IntRange(min = 0, max = 10) int a, @ForAll @IntRange(min = 10, max = 20) int b, @ForAll @IntRange(min = 20, max = 30) int c) {
  String parameters = String.format("%s, %s, %s", a, b, c);
  System.out.println(parameters);
}
```
Este código genera un output de combinaciones, como por ejemplo:
<table>
<tr>
<th>Combinación de parámetros generados para primer ejemplo</th>
<th>Combinación de parámetros generados para segundo ejemplo</th>
</tr>
<tr>
<td>0, 0<br/>
0, 2<br/>
0, 1<br/>
0, 10<br/>
2, 0<br/>
2, 2<br/>
2, 1<br/>
2, 10<br/>
1, 0<br/>
1, 2<br/>
1, 1<br/>
1, 10<br/>
10, 0<br/>
10, 2<br/>
10, 1<br/>
10, 10<br/>
8, 0<br/>
1, 5<br/>
7, 2<br/>
10, 4<br/>
9, 3<br/>
1, 3<br/>
8, 4<br/>
10, 6<br/>
4, 10<br/>
5, 9<br/>
2, 0<br/>
0, 5<br/>
6, 8<br/>
3, 5</td>
<td>0, 10, 20<br/>
0, 10, 30<br/>
0, 20, 20<br/>
0, 20, 30<br/>
2, 10, 20<br/>
2, 10, 30<br/>
2, 20, 20<br/>
2, 20, 30<br/>
1, 10, 20<br/>
1, 10, 30<br/>
1, 20, 20<br/>
1, 20, 30<br/>
10, 10, 20<br/>
10, 10, 30<br/>
10, 20, 20<br/>
10, 20, 30<br/>
0, 12, 21<br/>
1, 11, 29<br/>
9, 17, 24<br/>
1, 10, 27<br/>
4, 20, 29<br/>
0, 19, 23<br/>
0, 10, 27<br/>
7, 11, 20<br/>
2, 10, 22<br/>
4, 10, 23<br/>
7, 14, 28<br/>
8, 20, 25<br/>
7, 20, 22<br/>
10, 17, 30</td>
</tr>
</table>

Además de las combinatorias, nos ofrece diferentes herramientas para la generación de esos parámetros y configuraciones, para casuísticas más complejas.

El peaje: cambiar el enfoque de los tests, aprender un nuevo framework para la implementación de los mismos y el tiempo de ejecución.

Mi feeling es que estos tests terminan siendo bastante más complejos si se les quiere sacar chicha a tope, y aunque veo sus beneficios, lo que no termino de tener claro es ¿existen proyectos reales que usen este tipo de testing? ¿Se usa de forma intensiva en ellos o solamente en algunas de las funcionalidades que no requieren de configuración/personalización extra? ¿Qué características debería tener mi proyecto para invertir en este tipo de testing más que en example based testing?

---
---

<br/>
A continuación añado algunas referencias que he utilizado y que me han ayudado a entender el concepto de _property based testing_
* [Introduction to Property Based Testing](https://medium.com/criteo-labs/introduction-to-property-based-testing-f5236229d237){:target="_blank"} - _por Nicolas Dubien_
* [Property-based testing](https://www.erikschierboom.com/2016/02/22/property-based-testing/){:target="_blank"} - _por Erik Schierboom_
* [Property based testing](https://felginep.github.io/2019-03-20/property-based-testing){:target="_blank"} - _por Pierre Felgines_ 
* [Improve your software quality with Property-Based Testing](https://medium.com/@yoan.thirion/improve-your-software-quality-with-property-based-testing-70bd5ad9a09a){:target="_blank"} - _por Yoan Thirion_
* [Property-based Testing Patterns](https://blog.ssanj.net/posts/2016-06-26-property-based-testing-patterns.html){:target="_blank"} - _Sanjiv Sahayam_