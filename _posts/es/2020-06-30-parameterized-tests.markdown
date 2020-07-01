---
layout: post
title:  "Descubriendo JUnit 5: Tests Parametrizados"
date:   2020-06-30 9:00:00
author: jessica
lang: es
categories: testing, software quality, QA
tags: testing, calidad, software quality, QA, junit, junit 5, parameterized test
header-image:	2020-06-30-parameterized-tests/header.jpg
---

Estaba preparando el ejemplo de tests para el post [Mutation testing systems, mejorando la calidad de los tests](https://blog.arima.eu/2020/05/25/mutation-testing.html){:target="_blank"} y me surgió una duda sobre si podría probar de forma más exhaustiva el método under test, ya que era consciente de que me dejaba algunos ejemplos sin probar.

El método de ejemplo a testear es:
```java
@Override
public DayStatusSummary getDayStatusSummaryForWorkerAndDay(String workerUserName, LocalDate date) {

  List<Worklog> worklogsForDay = this.worklogRepository.findByUsernameAndDate(workerUserName, date);

  int totalDuration = worklogsForDay.stream().mapToInt(Worklog::getDuration).sum();

  DayStatusSummary status = new DayStatusSummary(date, workerUserName);

  if (totalDuration == 8) {
    status.addDayStatus(RIGHT_HOURS);
  } else if (totalDuration > 8) {
    status.addDayStatus(EXTRA_HOURS);
  } else {
    status.addDayStatus(MISSING_HOURS);
  }

  return status;
}
```

Básicamente lo que hace es a partir de un conjunto de worklogs se encarga de sumar las duraciones y comprobarlas “contra” la jornada estándar de 8 horas. Si la suma es > 8 debe indicar que hay horas extras, si es < 8 faltarán por imputar horas y si es 8 todo estará OK.

Este caso es bastante trivial, pero si lo extrapolamos a métodos más complejos, no es la primera situación de estas características que me encuentro, y normalmente termino creando varios tests con diferentes combinaciones finitas, de casos de ejemplo acotados, que normalmente podría sacar de una tabla de este tipo:


| | | 1 único worklog | lista de n worklogs (n<1) |
| ------ | ------ | ------ | ------ |
| caso 1 | suma = 8 | test | test |
| caso 2 | suma = a (a<8) | test | test |
| caso 3 | suma = b (b>8) | test | test |

Así a priori mi batería de tests para este método podría ser la siguiente[^1]:

[^1]: Código fuente para ejemplo de primera versión de los tests disponible [aquí](https://github.com/wearearima/time-report-parameterized/tree/feature/01_tests_first_approach/src/test/java/eu/arima/tr/reports/reportsServiceImpl/GetDayStatusSummaryForWorkerAndDayTests.java){:target="_blank"}

![Primera aproximación del set de tests](/assets/images/2020-06-30-parameterized-tests/01_test_set.png){: .center }

Teniendo en cuenta que `n`, `a` y `b` los fijaré (en este caso `n = 3`, `a = 7` y `b = 9`) siempre me quedo con la duda de que estoy testeando algunos ejemplos pero no otros: `suma = 7` pero no `suma = 0`o `suma = 9` pero no `suma = 10`, o listas de 1 y 3 elementos pero no de 0 o más de 3....

En este caso en el que los casos 1 y 2 son muy acotados podría liarme la manta a la cabeza y hacer tests exhaustivos que probasen todos los casos… Por ejemplo[^2]:

![Segunda aproximación del set de tests](/assets/images/2020-06-30-parameterized-tests/02_test_set.png){: .center }

[^2]: Código fuente para ejemplo de tests exhaustivos disponible [aquí](https://github.com/wearearima/time-report-parameterized/tree/feature/02_tests_exhaustive/src/test/java/eu/arima/tr/reports/reportsServiceImpl/GetDayStatusSummaryForWorkerAndDayTests.java){:target="_blank"}

Pero nunca me ha parecido algo apropiado porque pensando en esfuerzo vs beneficio parece que no compensa, y porque aumentar tanto la clase de test con métodos tan “redundantes” probablemente haga que mi clase de tests termine siendo infumable. El ejemplo anterior ratificaría esta idea... y ni siquiera cubrimos todos los ejemplos que se nos podrían ocurrir... ¡sólo hemos cubierto ejemplos del _caso 2_ con _un único worklog_!

¡Otra idea!, ¿por qué no iterar `n` veces la ejecución del método SUT junto el assert asociado, y personalizar el mensaje de error utilizando el parámetro de la iteración?

Algo así como el siguiente ejemplo[^3]:

[^3]: Código fuente para ejemplo de tests iterando SUT disponible [aquí](https://github.com/wearearima/time-report-parameterized/tree/feature/03_tests_tricky_exhaustive/src/test/java/eu/arima/tr/reports/reportsServiceImpl/GetDayStatusSummaryForWorkerAndDayTests.java){:target="_blank"}

```java
@Test
void when_the_worklog_for_the_resquested_day_is_less_than_8_hours_the_status_is_MISSING_HOURS() {
  Worklog wl = mock(Worklog.class);

  for (int i = 0; i < 8; i++) {
    when(wl.getDuration()).thenReturn(i);
    when(worklogRepository.findByUsernameAndDate(ArgumentMatchers.anyString(),
        ArgumentMatchers.any(LocalDate.class))).thenReturn(Arrays.asList(wl));

    DayStatusSummary result = reportsService.getDayStatusSummaryForWorkerAndDay(USERNAME, DAY);

    List<Integer> durations = Arrays.asList(i);
    List<DayStatus> resultStatusList = result.getStatusList();
    assertEquals(1, resultStatusList.size(), "Statuslist size failed for worklogs with duration " + durations);
    assertEquals(MISSING_HOURS, resultStatusList.get(0), "Daystatus failed for with duration " + durations);
  }
}
```

En este caso estaré ejecutando un único test, pero si falla para algún valor de `i`, el mensaje de error me indicará el ejemplo que falla.

Vale, con esto cubro los casos más acotados….. y ¿para los menos acotados? Se me ocurre generar varios valores random y aplicar el mismo patrón[^4]:

[^4]: Código fuente para ejemplo de tests iterando SUT con valores random disponible [aquí](https://github.com/wearearima/time-report-parameterized/tree/feature/03_tests_tricky_exhaustive/src/test/java/eu/arima/tr/reports/reportsServiceImpl/GetDayStatusSummaryForWorkerAndDayTests.java){:target="_blank"}

```java
@Test
void when_the_worklog_for_the_resquested_day_is_more_than_8_hours_the_status_is_EXTRA_HOURS() {
  Worklog wl = mock(Worklog.class);
  List<Integer> worklogDurations = (new Random().ints(10, 9, Integer.MAX_VALUE)).boxed()
      .collect(Collectors.toList());
  for (Integer d : worklogDurations) {
    when(wl.getDuration()).thenReturn(d);
    when(worklogRepository.findByUsernameAndDate(ArgumentMatchers.anyString(),
        ArgumentMatchers.any(LocalDate.class))).thenReturn(Arrays.asList(wl));

    DayStatusSummary result = reportsService.getDayStatusSummaryForWorkerAndDay(USERNAME, DAY);

    List<Integer> durations = Arrays.asList(d);
    List<DayStatus> resultStatusList = result.getStatusList();
    assertEquals(1, resultStatusList.size(), "Statuslist size failed for worklogs with duration " + durations);
    assertEquals(EXTRA_HOURS, resultStatusList.get(0), "Daystatus failed for with duration " + durations);

  }
}
```

Pues sí, reconozco que alguna vez (en alguno de mis sideprojects) he hecho alguna de estas “chapucillas”🤫😰. Digo chapucilla, porque a priori no suena muy bien hacer estas triquiñuelas... (pero bueno, hay tests, hay cobertura de mutantes, estoy trasteando, así practico testing.....). Excusas y más excusas. Intento engañarme a mí misma y no duermo tranquila. Amanezco, pensando en cómo podría cubrir estos “vacíos” aparentes. Es un caso sencillo... ¿no hay nada que pueda ayudarme en esto?

La respuesta es que sí, y ¡encima lo ofrece JUnit 5 por sí mismo!: no me hace falta ninguna herramienta nueva, sólo sacarle más chicha a la que tengo. La solución: [Parameterizered Tests](https://junit.org/junit5/docs/current/user-guide/#writing-tests-parameterized-tests){:target="_blank"}. Están en modo experimental para la última versión de JUnit 5, pero lo cierto es que están disponibles desde la versión 5.0 ¡y yo sin conocerlos! Vamos a probarlo.

Lo primero es añadir en el `pom.xml` la dependencia correspondiente:
```xml
<!-- https://mvnrepository.com/artifact/org.junit.jupiter/junit-jupiter-params -->
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter-params</artifactId>
    <scope>test</scope>
</dependency>
```

A continuación, modificamos el primer test utilizando la anotación y queda como sigue:

```java
@ParameterizedTest(name = "Given a worklog for the requested day with {0} duration the status is MISSING_HOURS")
@ValueSource(ints = { 0, 1, 2, 3, 4, 5, 6, 7 })
void worklog_duration_for_requested_day_less_than_8(Integer duration) {
  Worklog wl = mock(Worklog.class);
  when(wl.getDuration()).thenReturn(duration);
  when(worklogRepository.findByUsernameAndDate(ArgumentMatchers.anyString(),
      ArgumentMatchers.any(LocalDate.class))).thenReturn(Arrays.asList(wl));

  DayStatusSummary result = reportsService.getDayStatusSummaryForWorkerAndDay(USERNAME, DAY);

  assertStatusEquals(MISSING_HOURS, result);
}
```

Tras esta modificación no estamos ejecutando un sólo test, **estamos ejecutando 8 tests**:

![Ejemplo de parameterized](/assets/images/2020-06-30-parameterized-tests/03_test_parameterized.png){: .center }

Además, si por ejemplo, quisiéramos hacer lo mismo con el método que utilizaba valores random, podríamos conseguir algo similar haciendo:

```java
@ParameterizedTest(name = "Given a worklog for the requested day {0} the status is EXTRA_HOURS")
@MethodSource
void worklog_duration_for_requested_day_more_than_8(Worklog wl) {
  when(worklogRepository.findByUsernameAndDate(ArgumentMatchers.anyString(),
      ArgumentMatchers.any(LocalDate.class))).thenReturn(Arrays.asList(wl));

  DayStatusSummary result = reportsService.getDayStatusSummaryForWorkerAndDay(USERNAME, DAY);

  assertStatusEquals(EXTRA_HOURS, result);
}

static Stream<Worklog> worklog_duration_for_requested_day_more_than_8() {
  // since 24h/day --> max value is 24
  Stream<Integer> randomDurations = (new Random().ints(10, 9, 24)).boxed();
  return randomDurations.map(d -> {
    Worklog wl = mock(Worklog.class);
    when(wl.toString()).thenReturn(String.format("[with %d duration]", d)); // mock info in test description
    when(wl.getDuration()).thenReturn(d);
    return wl;
  });
}
```

En este caso en vez de devolver una lista de enteros con las duraciones hemos probado a hacer el ejemplo devolviendo directamente diferentes worklogs.

![Ejemplo de parameterized con valores ramdom](/assets/images/2020-06-30-parameterized-tests/04_test_parameterized_random.png){: .center }

Nota: Este ejemplo está disponible al completo [en Github](https://github.com/wearearima/time-report-parameterized/tree/feature/04_tests_parameterizedTest){:target="_blank"}.

Otra cosa que siempre he echado de menos de mis tiempos en Grails ha sido la posibilidad de utilizar nombres más “legibles” para los tests. Y ya que estoy de suerte, y con la anotación `@ParameterizedTest` puedo poner un nombre... seguro que hay algo para los tests “normales”... ¡Bingo! Otra anotación al rescate: `@Displayname`.

Pues nada, ahora tengo unos tests mejores, más fáciles de entender y de mantener que los de los ejemplos 2 y 3, y más completos que los del ejemplo 1. 

## Descubriendo JUnit 5
Nos acostumbramos a hacer las cosas de determinada manera y a veces nos cuesta levantar la mirada y ver si hay herramientas que nos faciliten la vida (que con poco esfuerzo vengan a cubrir carencias que habíamos detectado en nuestro propio código). En este caso, hemos descubierto unas anotaciones que nos ayudarán en nuestro día a día a hacer que nuestros tests sean mejores.

`@ParameterizedTest` para poder crear múltiples ejemplos para una misma situación de un SUT. Los parámetros de entrada pueden ser tan sencillos como una lista de valores (si sólo se necesita uno utilizando `@ValueSource`) o más complejos, desde múltiples parámetros para cada test, hasta tipos de parámetros más complejos (utilizando por ejemplo `@MethodSource`). Toda la información puede encontrarse [en esta sección](https://junit.org/junit5/docs/current/user-guide/#writing-tests-parameterized-tests){:target="_blank"} de la documentación de JUnit 5.

Además `@DisplayName` para poder poner nombres más legibles a los tests, algo muy útil especialmente cuando fallan: poder leer lo que está pasando de forma sencilla. Toda la información puede encontrarse [en esta sección](https://junit.org/junit5/docs/current/user-guide/#writing-tests-display-names){:target="_blank"} de la documentación de JUnit 5.


## Más allá…
Sin embargo, sigo notando cierto run run: ¿qué pasa con esos casos que no puedo atacar de forma exhaustiva? ¿Podría usar `@ParameterizedTest`s y pasar random values de diferentes listas?
Parece que sí, pero... en este caso que es sencillo no parece que tenga problemas. Sin embargo y ¿si tuviese más parámetros de entrada o más complejos? ¿Tendría que desarrollar mi propio “generador” de combinaciones aleatorias? ¿Cómo de frágiles serían mis tests? ¿Es posible hacer tests que no estén basados en ejemplo? 
Investigando un poco me encuentro con un concepto que parece que puede encajar: **Property Based Testing**, donde en base a unos parámetros de características determinadas se verifica una propiedad/comportamiento concreto del SUT.

No tengo claro si encajaría en este ejemplo, pero ¿quizás deba profundizar más en el tema para ver si hay algo que podamos aprender y que nos permita mejorar nuestros tests? ¡Por supuesto, allá vamos!
