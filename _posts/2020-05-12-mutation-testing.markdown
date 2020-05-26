---
layout: post
title:  "Mutation testing systems, mejorando la calidad de los tests"
date:   2020-05-25 9:00:00
author: jessica
categories: testing, software quality, QA
tags: testing, mutation testing systems, pit, pitest, calidad, software quality, QA, cobertura, coverage, junit
header-image:	2020-05-12-mutation-testing/header.jpg
---

Profesionalmente me etiqueto como _desarrolladora_, aunque no me gustan mucho las etiquetas y me gusta más decir que la razón de ser de mi trabajo es: crear software de calidad. Pero ¿qué es **software de calidad**? A mi me gusta definirlo como sigue:

> Software de calidad es aquel que satisface las necesidades del usuario de forma eficiente y sin errores.

Podría añadir más adjetivos, entrar en detalle de por qué necesidades y no requerimientos... pero para mi ese sería el titular. Ahora bien, difícilmente se puede tener un software de calidad si este no está escrito con código de calidad. 

> Software de calidad &rarr; código de calidad

Afortunadamente, los desarrolladores no nos encontramos solos en esta tarea. Existen herramientas para análisis de código de forma estática (Checkstyle, PMD, FindBugs, SonarQube...) y diferentes recomendaciones de buenas prácticas (personalmente destacaría Clean Code y The Pragmatic Programmer). Y ahí entre propuestas, siglas y métricas, no hay desarrollador que no asocie directamente el término _**calidad**_ con el término _**testing**_ (¿verdad?)

> Código de calidad &rarr; tests de calidad

## Testing: el camino hacia la calidad

>**Tests are as important to the health of a project as the production code is.**
><p align="right" markdown="1">**Clean Code.** Chapter 9: Unit Tests</p>  

Hay varios tipos de test (unitarios, de integración, de aceptación...). Los más extendidos son los tests unitarios y los tests de integración. Con ellos se consigue una cierta percepción de seguridad, ya que si bien no sabemos si el código hace lo que debe, al menos hace lo que dice. 

¿Pero es esto así? Paradójicamente esta práctica consiste en generar más código, es decir, seguimos programando, ¿quién vela porque este código hace lo que dice?, es decir ¿quién vela por la calidad de los tests? De nuevo otra asociación de términos: **tests de calidad** son aquellos que ofrecen un % de **cobertura** del código alto.

> Tests de calidad &rarr; % cobertura elevado de nuestro código

A mayor porcentaje de cobertura de código mejores tests y código más fiable. Esto no es nada nuevo. Si hablo de mi experiencia personal, hace algunos años (allá por inicios del 2000) ya formaba parte de las especificaciones de entrega de algunos proyectos el % de cobertura mínimo que debía tener un proyecto. “_Este entregable debe tener una batería de tests que aseguren un mínimo de 70% de cobertura de código_”, como sinónimo de código libre de errores y calidad probada en un 70% del código al menos.

Tomando como ejemplo una aplicación para controlar los partes de horas trabajados, vamos a imaginar que estamos desarrollando un método que dados un trabajador y un día, comprueba el estado de los partes de horas de ese trabajador en ese día (si ha cumplido o no las horas, si hay partes solapados....).

##### ReportsServiceImpl.java [ver todo](https://github.com/wearearima/time-report-app/blob/feature/01_tests_for_project_requirements/src/main/java/eu/arima/tr/reports/ReportsServiceImpl.java){:target="_blank"}

```java
@Override
public DayStatusSummary getDayStatusSummaryForWorkerAndDay(String workerUserName, LocalDate date) {
  DayStatusSummary status = new DayStatusSummary();
  status.setDate(date);
  status.setWorkerUserName(workerUserName);

  List<Worklog> worklogsForDay = worklogRepository.findByUsernameAndDate(workerUserName, date);
  int totalDuration = 0;
  for (Worklog worklog : worklogsForDay) {
    totalDuration = totalDuration + worklog.getDuration();
  }
  if (totalDuration == 8) {
    status.getStatusList().add(DayStatus.RIGHT_HOURS);
  }
  if (totalDuration > 8) {
    status.getStatusList().add(DayStatus.EXTRA_HOURS);
  }
  if (totalDuration < 8) {
    status.getStatusList().add(DayStatus.MISSING_HOURS);
  }
  return status;
}
```

Vamos a ver un ejemplo de tests que entregábamos por aquel entonces:

##### GetDayStatusSummaryForWorkerAndDayTests.java [ver todo](https://github.com/wearearima/time-report-app/blob/92fd1b537de787bc2a5d10dc85c9ee80295350d8/src/test/java/eu/arima/tr/reports/reportsServiceImpl/GetDayStatusSummaryForWorkerAndDayTests.java){:target="_blank"}

```java
@Test
public void get_status_summary_for_worker_and_day() {
  reportsService.getDayStatusSummaryForWorkerAndDay("USU", LocalDate.now());
  assertTrue(true);
}

@Test
public void calculates_the_status_based_on_worker_and_date_worklogs() {
  List<Worklog> partes = new ArrayList<Worklog>();
  Worklog wl = new Worklog();
  wl.setFromTime(LocalTime.of(8,0,0));
  wl.setToTime(LocalTime.of(19,0,0));
  partes.add(wl);
  Mockito.when(worklogRepository.findByUsernameAndDate(ArgumentMatchers.anyString(), ArgumentMatchers.any(LocalDate.class))).thenReturn(partes);

  LocalDate fecha = LocalDate.now();
  reportsService.getDayStatusSummaryForWorkerAndDay("USU", fecha);

  Mockito.verify(worklogRepository).findByUsernameAndDate("USU", fecha);
}
```

Hemos configurado [JaCoCo](https://www.eclemma.org/jacoco/){:target="_blank"} para obtener el informe de la cobertura de nuestros tests, y el resultado ha sido el siguiente.  

![JaCoCo report general](/assets/images/2020-05-12-mutation-testing/01jacocoreport.png){: .center }

Tenemos una cobertura de un 92% de líneas y 87% de ramas: objetivo cumplido. Pero...si nos fijamos: el primer test no fallará (casi) nunca porque siempre termina con `assert true`, el segundo es un poco “más completo” porque al menos está verificando que se recuperan los partes... [^1]

[^1]: Si quieres probar todo esto puedes descargarte el código de [aquí](https://github.com/wearearima/time-report-app/tree/feature/01_tests_for_project_requirements){:target="_blank"}

Pues esta era mi realidad, y mucho me temo que LA realidad, de aquella época en muchos proyectos (y quien sabe si en algunos de hoy en día). Los proyectos cumplían los requerimientos de cobertura de código, lo que distaba mucho de tener un software de calidad.  

Es cierto que el ejemplo que he puesto es extremo, pero es real. En mi opinión, el problema está en el enfoque: se ha dado la vuelta a la tortilla y en él los tests nacen como una mera herramienta para asegurar uno de los requerimientos del proyecto.

> % cobertura mínimo por requerimiento &rarr; test = "pérdida de tiempo"

Volvamos al enfoque original. Quedaría:

> Software de calidad &rarr; código de calidad &rarr; tests de calidad &rarr; % cobertura de código

En este escenario, los tests nacen bajo la premisa de tener un código de mayor calidad y el % de cobertura se convierte en un indicador más. Vamos a ver un fragmento de un ejemplo de test mejor, de esos de los que hacemos por convicción y no por cumplir un requerimiento sin más (supongo que más parecidos a los que podemos encontrarnos en los proyectos actuales que los anteriores...).

##### GetDayStatusSummaryForWorkerAndDayTests.java [ver todo](https://github.com/wearearima/time-report-app/blob/feature/02_tests_for_testing_purposes/src/test/java/eu/arima/tr/reports/reportsServiceImpl/GetDayStatusSummaryForWorkerAndDayTests.java){:target="_blank"}

```java
@Test
public void if_the_worklog_for_the_resquested_day_is_less_than_8_hours_the_status_is_MISSING_HOURS() {
  Worklog worklog = Mockito.mock(Worklog.class);
  Mockito.when(worklog.getDuration()).thenReturn(7);
  Mockito.when(worklogRepository.findByUsernameAndDate(ArgumentMatchers.anyString(), ArgumentMatchers.any(LocalDate.class))).thenReturn(Arrays.asList(worklog));

  DayStatusSummary resultado = reportsService.getDayStatusSummaryForWorkerAndDay("USU", LocalDate.now());

  assertEquals(DayStatus.MISSING_HOURS, resultado.getStatusList().get(0));
}

@Test
public void if_the_worklog_for_the_resquested_day_is_equal_to_8_hours_the_status_is_RIGHT_HOURS() {
  Worklog worklog = Mockito.mock(Worklog.class);
  Mockito.when(worklog.getDuration()).thenReturn(8);
  Mockito.when(worklogRepository.findByUsernameAndDate(ArgumentMatchers.anyString(), ArgumentMatchers.any(LocalDate.class))).thenReturn(Arrays.asList(worklog));

  DayStatusSummary resultado = reportsService.getDayStatusSummaryForWorkerAndDay("USU", LocalDate.now());

  assertEquals(DayStatus.RIGHT_HOURS, resultado.getStatusList().get(0));
}

@Test
public void if_the_worklog_for_the_resquested_day_is_more_than_8_hours_the_status_is_EXTRA_HOURS() {
  Worklog worklog = Mockito.mock(Worklog.class);
  Mockito.when(worklog.getDuration()).thenReturn(10);
  Mockito.when(worklogRepository.findByUsernameAndDate(ArgumentMatchers.anyString(), ArgumentMatchers.any(LocalDate.class))).thenReturn(Arrays.asList(worklog));

  DayStatusSummary resultado = reportsService.getDayStatusSummaryForWorkerAndDay("USU", LocalDate.now());

  assertEquals(DayStatus.EXTRA_HOURS, resultado.getStatusList().get(0));
}
```

En este caso el porcentaje de cobertura es del 100% de líneas de código y ramas. Y además parece que los tests ya tienen más sentido. Ahora ya sí, nos sentiríamos seguros con ellos, ¿verdad? Es así, o ¿es sólo una percepción?

Si alguien modificase algo del método, por su puesto, antes de comitear y pushear pasaría los tests. Si no hubiese ningún test en rojo, vía libre: no se ha "roto" nada.  

¿Seguro?

Supongamos que lo que se modifica en el método de ejemplo es:

##### ReportsServiceImpl.java

```java
  for (Worklog worklog : worklogsForDay) {
    totalDuration = totalDuration + worklog.getDuration();
  }
```

por

```java
  for (Worklog worklog : worklogsForDay) {
    totalDuration = worklog.getDuration();
  }
```

Nuestros tests seguirán pasando[^2]. Además seguimos con un % de cobertura alto... ¡Todo perfecto!

[^2]: Pruébalo tu mismo, el código está disponible [aquí](https://github.com/wearearima/time-report-app/tree/feature/02_tests_for_testing_purposes){:target="_blank"}

> Test &rarr; **sensación** de seguridad

## Mutation testing systems: asegurando el camino

>**Because we can’t write perfect software, it follows that we can’t write perfect test software either. We need to test the tests.**
><p align="right" markdown="1">**The Pragmatic Programmer.** Chapter 8: Pragmatic projects</p>

Parece que los tests que hemos creado no son tan buenos como creíamos, no tienen calidad suficiente como para asegurar la calidad (valga la redundancia) de nuestro método. Nos han ofrecido una falsa sensación de seguridad.  

Está claro que conseguir % altos de cobertura no es sencillo y si escribir tests es costoso, escribir buenos tests lo es aún más y lo que obtenemos es una sensación de seguridad que no es real. ¿No podríamos hacer que esta sensación fuese más cercana a la realidad? ¿No podríamos detectar situaciones, como la que hemos visto, de forma automática?

Pues bien, para abordar este tipo de situaciones surgen los denominados _Mutation Testing Systems_. La idea que hay detrás de ellos no es otra que la que hemos expuesto en el último ejemplo: simular cambios en el código fuente que se está probando y verificar que efectivamente, algún test fallará tras haber realizado la modificación.  

> Software de calidad &rarr; código de calidad &rarr; tests de calidad &rarr; % cobertura mutation tests

Los conceptos básicos son los siguientes:

* Cada cambio que se genera en el código es un **mutante** (mutant).
* Cada cambio (o mutante) que nuestros tests son capaces de detectar se denomina **matar un mutante** (killed mutant).
* Cada cambio (o muntante) que nuestros tests no son capaces de detectar son **mutantes vivos** (lived)
* Los cambios en el código se generan mediante **operadores mutantes** (mutators / mutation operators), que se agrupan en diferentes categorias dependiendo del tipo de cambio que realicen en el código.

Personalmente no había oído hablar de este concepto hasta hace relativamente poco sin embargo, la realidad es que ya llevan varios años entre nosotros. Existen múltiples alternativas para los diferentes stacks tecnológicos. Por ejemplo:

* [Stryker](https://stryker-mutator.io/){:target="_blank"} para JavaScript, TypeScript, C# y Scala
* [Mutode](https://thesoftwaredesignlab.github.io/mutode/){:target="_blank"} para JavaScript y Node.js
* [Cosmic Ray](https://cosmic-ray.readthedocs.io/en/latest/){:target="_blank"} para Python
* [mutmut](https://pypi.org/project/mutmut/){:target="_blank"} para Python
* [Mutant](https://github.com/mbj/mutant){:target="_blank"} para Ruby

Y volviendo a Java algunos de los sistemas de mutación son (o han sido):

* [PIT](https://pitest.org/){:target="_blank"}
* [Jumble](http://jumble.sourceforge.net/index.html){:target="_blank"}
* [Jester](http://jester.sourceforge.net/){:target="_blank"}
* [muJava](https://github.com/jeffoffutt/muJava){:target="_blank"}

Nosotros hemos utilizado PIT porque:

* Es sencillo de usar
* Se integra fácilmente en los proyectos que los hemos usado (mediante un plugin de maven) así como en el IDE (en nuestro caso Eclipse)
* Admite diferentes configuraciones (algunas que permiten mejorar la eficiencia)
* Aún está activo
* Parece ser la solución más utilizada en la actualidad

Si ejecutamos el informe de _pitest_ en nuestro ejemplo, veremos este resultado.

![Informe _Pit test_ general](/assets/images/2020-05-12-mutation-testing/PitTestCoverageReport01.png){: .center }

Aquí se indica el resultado general: por un lado la cobertura de líneas de código y por otro lado la cobertura de mutación.

![Informe _Pit test_ clase](/assets/images/2020-05-12-mutation-testing/PitTestCoverageReportClass01.png){: .center }

Las líneas marcadas en verde, reflejan código en el que PIT ha introducido cambios y los tests han sido capaces de detectarlo. Las líneas marcadas en rojo, reflejan las líneas de código que nuestros tests no han sabido detectar que había habido cambios. Si nos fijamos la línea 27 es la que nosotros habíamos modificado y nuestros tests habían pasado. Ahora tenemos dos opciones: seguir adelante, asumiendo la fragilidad que puede tener nuestro código o lo más acertado (y lógico) añadir/corregir tests que nos aseguren la fiabilidad frente a los cambios detectados.

En el siguiente [enlace](https://github.com/wearearima/time-report-app/tree/feature/03_tests_improving_quality){:target="_blank"} está disponible el código del ejemplo en el que hemos trabajado, donde hemos mejorado los tests para conseguir una mayor cobertura de mutantes.

Los mutantes que se aplican son configurables, y hay que valorar el equilibrio entre la cantidad/tipo de mutantes configurados y el tiempo de ejecución. A mayor número de tests, mayor número de líneas de código y mayor cantidad de mutantes, más tiempo necesitará Pit en generar el informe correspondiente. Puede llegar un momento en el que sea tan costoso pasar el informe que se hagamos skip, y entonces todo el esfuerzo dedicado a testing se desvanecería. En los ejemplos hemos visto sólo tests unitarios pero lo mismo aplica a los test de integración (muchos de ellos ya costosos en sí mismos).  

En nuestro caso, solemos configurar los que vienen por defecto (DEFAULTS) y añadiendo los del siguiente grupo (NEW_DEFAULTS). En el código de ejemplo hay alguno más configurado, pero [aquí](https://pitest.org/quickstart/mutators/){:target="_blank"} se muestran los "mutadores" (mutators) de Pit, así que prueba a cambiar la configuración y a ver los diferentes resultados.

## Conclusiones

> Software de calidad &rarr; código de calidad &rarr; tests de calidad

Software de calidad require de código calidad que a su vez puede validarse gracias a tests de calidad.  

Generalmente hay más código para testear un método que para implementarlo, lo que conlleva un claro esfuerzo en tiempo: dedicaremos más tiempo al testeo de un método que a su implementación. Necesitamos asegurar que dicho esfuerzo no sea en balde.  

**Mutation testing** es una herramienta que nos permite evaluar y mejorar la calidad de nuestros tests. El precio a pagar es el aumento de tiempo necesario para pasarlos. Teniendo en cuenta que se basa en mutaciones de código y que aplica no sólo a tests unitarios, también a tests de integración, a medida que el código crezca y el número de tests aumente, mayor será el tiempo necesario para ejecutarlos. Es necesario, por tanto, buscar fórmulas que aseguren que en alguna fase de nuestro desarrollo todos los tests pasan: si dejamos de pasarlos porque es demasiado costoso todo el esfuerzo habrá sido en vano.  

Hemos dado un paso firme, pero nos queda recorrido en nuestro camino hacia la calidad: ¿Qué podemos hacer para buscar este equilibrio? ¿Podemos organizar de alguna forma los tests para facilitarlo? ¿Hay herramientas que nos permitan desarrollar/ejecutar tests de forma más eficiente?
