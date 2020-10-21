---
layout: post
title:  "Jugando con Spring Cloud Contract"
date:   2020-10-13 8:00:00
author: jessica
lang: es
categories: testing, software quality, QA
tags: testing, calidad, software quality, QA, contract testing, provider driven contract testing, spring cloud contract
header-image: 2020-10-15-playing-with-spring-cloud-contract/header.jpg
---
En un [post anterior](https://blog.arima.eu/es/2020/09/03/contract-testing.html){:target="_blank"} hemos visto cómo surgen nuevas necesidades en el ámbito del testing derivadas de la evolución de las arquitecturas de las aplicaciones.  

Mediante un ejemplo sencillo hemos asentado conceptos como _consumer_, _producer_, _servicio_ y hemos puesto en evidencia que tan importante como testear las funcionalidades en _consumer_ y _producer_ de forma independiente lo es asegurar que la interacción entre ambos es correcta. 

Hemos introducido el concepto de **Contract Testing**, en el que hemos profundizado en otro [post](https://blog.arima.eu/es/2020/10/09/contract-testing-approach.html){:target="_blank"} lo que nos ha permitido conocer los diferentes enfoques y herramientas.

Ahora, con toda la información en nuestras manos es hora de materializar todas esas ideas en código. Lo haremos paso a paso, partiendo del ejemplo del primer post, cuyo código podemos descargar de [aquí](https://github.com/wearearima/time-report-contractTesting){:target="_blank"}. Recordemos que con él pusimos en evidencia el problema que podríamos encontrarnos: una aplicación que falla en producción pese a tener todos los tests unitarios y de integración pasando.  

Hemos elegido el enfoque **producer driven** y como herramienta utilizaremos [**Spring Cloud Contract**](https://spring.io/projects/spring-cloud-contract){:target="_blank"}. El código está disponible en [Github](https://github.com/wearearima/time-report-contractTesting-02){:target="_blank"} ¡Vamos allá!

# 1. Definir el contrato

Empezaremos definiendo el acuerdo: escribiremos la especificación que tienen que cumplir _consumer_ y _producer_ para que la comunicación funcione correctamente. En Spring Cloud Contract se utiliza el término **contrato**. Se puede definir de diferentes formas (groovy, yaml, java, kotlin), nosotros hemos elegido `yaml` porque para este ejemplo nos parecía que podría resultar fácil de leer.

Para nuestro caso de uso definimos el siguiente contrato:

##### worklogsForWorkerAndDay.yaml

```yaml
description: Given a worker's username and a day it returns the worklog info for that worker and day
name: worklogsForWokerAndDay_success
request:
   urlPath: /worklogs/worker/JESSI
   queryParameters:
      day: "2020-05-05"
   method: GET
   matchers:
    url:
      regex: /worklogs/worker/([a-zA-Z]*)
    queryParameters:
      - key: day
        type: matching
        value: "(\\d\\d\\d\\d)-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])"
response:
   status: 200
   headers:
      Content-Type: "application/json"
   bodyFromFile: worklogsForJessiOn20200505Response.json
```

En este caso estamos estableciendo el siguiente acuerdo:  
  _Para una **petición** con: un nombre de usuario y una fecha (cuyo formato también especificamos), la **respuesta** será: `status 200` y un `JSON` (cuyo contenido establecemos mediante un [fichero](https://github.com/wearearima/time-report-contractTesting-02/blob/master/timeReports-producer/src/test/resources/contracts/worklogs/worklogsForJessiOn20200505Response.json){:target="_blank"})._

Este contrato debe estar accesible para el _producer_. En este caso y por simplificar estará en la carpeta `/test/resources/contracts/worklogs` del _producer_.

Una vez que hemos definido el contrato tendremos que hacer la implementación que lo cumpla y los tests necesarios que lo verifiquen. En este ejemplo ya partíamos de la implementación, así que ¡vamos con los test!

# 2. Producer: configurar las dependencias en el pom.xml

Modificamos el `pom.xml` para añadir la dependiencia de Spring Cloud Contract Verifier y el plugin `spring-cloud-contract-maven-plugin`. Con este último conseguiremos que de forma automática:

- Se generen los tests que verifiquen que nuestro _producer_ cumple el contrato
- Se cree un stub que permitirá al _consumer_ generar un [WireMock](http://wiremock.org/){:target="_blank"} (que cumplirá el contrato) contra el que ejecutar sus tests

#### Producer | pom.xml

```xml
...
<dependencies>
  ...
  <!-- Spring Cloud Contract Verifier -->
  <dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-contract-verifier</artifactId>
    <scope>test</scope>
  </dependency>
</dependencies>
...
<build>
  <plugins>
    ...
    <plugin>
      <groupId>org.springframework.cloud</groupId>
      <artifactId>spring-cloud-contract-maven-plugin</artifactId>
      <version>3.0.0-SNAPSHOT</version>
      <extensions>true</extensions>
      <configuration>
        <testFramework>JUNIT5</testFramework>
        <packageWithBaseClasses>eu.arima.tr</packageWithBaseClasses>
      </configuration>
    </plugin>
  </plugins>
</build>

<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>org.springframework.cloud</groupId>
      <artifactId>spring-cloud-dependencies</artifactId>
      <version>${spring-cloud.version}</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>
...
```

Como se muestra en el `pom.xml`además de las dependencias hemos configurado algunas de las propiedades del plugin:
-  Hemos indicado que el framework de test será JUnit 5
-  Hemos indicado que el paquete que contendrá la _clase base de test_ será `eu.arima.tr`

¿Qué es esto de la _clase base de test_? Según la especificación debemos generar una clase base que los test autogenerados extenderán. Esta clase debe contener toda la información necesaria para ejecutarlos (por ejemplo, podríamos configurar mocks de algunos beans, popular la base de datos con datos específicos para los tests...).  
Para este ejemplo hemos creado una clase base muy sencilla cuya única responsabilidad será levantar el contexto. El contrato lo hemos definido en la carpeta `contracts/worklogs`, por lo tanto (en base a la documentación que indica que el nombre se infiere en base a los nombres de las dos últimas carpetas), la clase se llama `WorklogsBase.java`.

#### Producer | WorklogsBase.java

```java
package eu.arima.tr;

@ExtendWith(SpringExtension.class)
@SpringBootTest
public abstract class WorklogsBase {
  @Autowired
  WebApplicationContext context;

  @BeforeEach
  public void setup() {
    RestAssuredMockMvc.webAppContextSetup(this.context);
  } 
} 
```

El plugin admite la configuración de otros parámetros como se explica en la [documentación del plugin](https://cloud.spring.io/spring-cloud-contract/spring-cloud-contract-maven-plugin/index.html){:target="_blank"}, como por ejemplo: dónde están los contratos, cómo generar los diferentes elementos, etc.


# 3. Producer: crear y ejecutar los tests

Como mencionábamos en el apartado anterior, con este plugin podemos generar automáticamente los tests que aseguren que el _producer_ cumple el conrato. Para ello hacemos `./mvnw clean test` y vemos que:

- Se generan las clases de test del _producer_
- Se ejecutan los tests
- Además se crea un `.jar` (que de momento dejamos aparcado)

¿Cómo son los tests que se autogeneran? Están en la carpeta `generated-test-sources`. En este caso en concreto, como tenemos una única carpeta, se genera una única clase:

#### Producer | WorklogsTest.java

```java
@SuppressWarnings("rawtypes")
public class WorklogsTest extends WorklogsBase {

 @Test
 public void validate_worklogsForWokerAndDay_success() throws Exception {
  // given:
   MockMvcRequestSpecification request = given();


  // when:
   ResponseOptions response = given().spec(request)
     .queryParam("day","2020-05-05")
     .get("/worklogs/worker/JESSI");

  // then:
   assertThat(response.statusCode()).isEqualTo(200);
   assertThat(response.header("Content-Type")).isEqualTo("application/json");

  // and:
   DocumentContext parsedJson = JsonPath.parse(response.getBody().asString());
   assertThatJson(parsedJson).array().contains("['id']").isEqualTo(4);
   assertThatJson(parsedJson).array().field("['worker']").field("['id']").isEqualTo(1);
   assertThatJson(parsedJson).array().field("['worker']").field("['userName']").isEqualTo("JESSI");
   assertThatJson(parsedJson).array().field("['worker']").field("['new']").isEqualTo(false);
   assertThatJson(parsedJson).array().field("['task']").field("['id']").isEqualTo(1);
   assertThatJson(parsedJson).array().field("['task']").field("['name']").isEqualTo("Daily meeting");
   assertThatJson(parsedJson).array().field("['task']").field("['new']").isEqualTo(false);
   assertThatJson(parsedJson).array().contains("['day']").isEqualTo("2020-05-05");
   assertThatJson(parsedJson).array().contains("['fromTime']").isEqualTo("08:30:00");
   assertThatJson(parsedJson).array().contains("['toTime']").isEqualTo("09:30:00");
   assertThatJson(parsedJson).array().contains("['description']").isEqualTo("Daily meeting");
   assertThatJson(parsedJson).array().contains("['new']").isEqualTo(false);
   assertThatJson(parsedJson).array().contains("['id']").isEqualTo(8);
   assertThatJson(parsedJson).array().field("['task']").field("['id']").isEqualTo(3);
   assertThatJson(parsedJson).array().field("['task']").field("['name']").isEqualTo("Implement the use case Create report for user and day");
   assertThatJson(parsedJson).array().contains("['fromTime']").isEqualTo("09:30:00");
   assertThatJson(parsedJson).array().contains("['toTime']").isEqualTo("16:30:00");
   assertThatJson(parsedJson).array().contains("['description']").isEqualTo("Create database and queries");
   assertThatJson(parsedJson).array().contains("['id']").isEqualTo(9);
   assertThatJson(parsedJson).array().contains("['toTime']").isEqualTo("11:00:00");
   assertThatJson(parsedJson).array().contains("['description']").isEqualTo("Create de frontend form for selecting user and date");
 }

}
```

Como vemos hay un método de test para la definición del contrato. Si tuviésemos más de una, en ese caso tendríamos un test por cada uno de ellos.  

En el test que se ha generado vemos como se hace un `assert` para comprobar que el `statusCode` de la response es el esperado. Además vemos cómo se verifica que el tipo de respuesta sea un `json` y cómo se ha parseado el fichero `.json` (al que hacíamos referencia en la especificación) para hacer los `assert`s necesarios que aseguran que la respuesta es la esperada.

**¿Y desde eclipse?**  

Personalmente utilizo eclipse en mis desarrollos, así que me interesa poder ejecutarlos desde el IDE. Obviamente primero necesitamos que se generen, esto ya hemos visto cómo debemos hacerlo mediante `./mvnw clean test`. Pero si no he cambiado el contrato y no hace falta que se regeneren los test y además estoy desarrollando y quiero pasar todos los tests, ¿cómo lo hago? Como son clases autogeneradas, es necesario añadir las carpetas de `generated-test-sources` al buildpath. Por ejemplo, en este caso:

![Configuración del buildpath para ejecutar los tests desde eclipse](/assets/images/2020-10-15-playing-with-spring-cloud-contract/buildpath_config.png){: .center }

# 4. Consumer: configurar las dependencias

A diferencia del _producer_, los tests en el _consumer_ relacionados con el contrato no se generan de forma automática. Pero no estamos solos: recordemos que al mismo tiempo que se han creado los tests del _producer_ también se ha generado un `.jar` con el stub que nos permitirá simular las llamadas al _producer_ desde los tests del _consumer_. 

En nuestro caso, el jar es: `timeReports-producer-0.0.1-SNAPSHOT-stubs.jar` que podemos encontrarlo en la carpeta `target `del _producer_.

En este caso, al tener ambos proyectos en local, si en lugar de hacer `./mvnw clean test` (en el _producer_) hacemos `./mvnw clean install` tendremos dicho jar directamente en nuestro repositorio local de maven, con lo cual, podremos configurar nuestro _consumer_ para que acceda a él.

Para poder tener acceso a él añadimos la siguiente dependencia en el `pom.xml`:

#### Consumer | pom.xml

```xml
...
  <dependencies>
  ...
    <!-- PRODUCER STUB -->
    <dependency>
        <groupId>eu.arima.tr</groupId>
        <artifactId>timeReports-producer</artifactId>
        <classifier>stubs</classifier>
        <version>0.0.1-SNAPSHOT</version>
        <scope>test</scope>
        <exclusions>
            <exclusion>
                <groupId>*</groupId>
                <artifactId>*</artifactId>
            </exclusion>
        </exclusions>
    </dependency>
  ...
  </dependencies>
...  
```

Además, no debemos olvidarnos de dependencia de Spring Cloud Contract para poder ejecutar el stub añadido. 

#### Consumer | pom.xml

```xml
...
  <dependencies>
  ...
    <!-- SPRING CLOUD CONTRACT -->
    <dependency>
      <groupId>org.springframework.cloud</groupId>
      <artifactId>spring-cloud-starter-contract-stub-runner</artifactId>
      <scope>test</scope>
    </dependency>
  ...
  </dependencies>

  <dependencyManagement>
    <dependencies>
      <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-dependencies</artifactId>
        <version>${spring-cloud.version}</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
   </dependencies>
 </dependencyManagement>
...  
```

# 5. Consumer: crear y ejecutar los tests

Una vez añadidas las dependencias ya podemos crear el WireMock basado en ese stub y crear nuestros tests. Un ejemplo podría ser:

##### Consumer | ReportsServiceContractTest.java

```java
@ExtendWith(SpringExtension.class)
@SpringBootTest(properties = { "server.url=http://localhost:8083" })
@AutoConfigureStubRunner(ids = { "eu.arima.tr:timeReports-producer:+:stubs:8083" })
public class ReportsServiceContractTest {

  @Autowired
  private ReportsService reportsService;

  @Test
  void test_getDayStatusSummaryForWorkerAndDay() {
    LocalDate dateFromProducerTest = LocalDate.now();
    String workerFromProducerTest = "TestUser";
    DayStatusSummary result = reportsService.getDayStatusSummaryForWorkerAndDay(workerFromProducerTest,
				dateFromProducerTest);
    assertEquals(workerFromProducerTest, result.getWorkerUserName());
    assertEquals(dateFromProducerTest, result.getDate());
  }

}
```

Con esto ya tendríamos la comunicación entre ambos testeada, asegurándonos que si en algún momento en alguno de los dos componentes hubiese una modificación en el contrato los tests del otro fallarían. ¿Lo vemos?

# ¿Somos capaces de desplegar en producción con la certeza de que todo funciona? 

Este era el problema que nos encontramos en el [post anterior](https://blog.arima.eu/es/2020/09/03/contract-testing.html){:target="_blank"}: pese a tener testeados _consumer_ y _producer_, no éramos capaces de saber que algo no iba bien hasta llegar a producción. ¿Seremos capaces de detectarlo ahora?

Supongamos, que realizamos el mismo cambio que proponíamos en aquel post:

##### Producer | WorklogController.java

```diff
@RestController
@RequestMapping("/worklogs")
public class WorklogController {

  ...

  @GetMapping("/worker/{workerUserName}")
  public List<Worklog> getReportForWorkerAndDay(
                       @PathVariable("workerUserName") String workerUserName, 
-                      @RequestParam("day") LocalDate day) {
+                      @RequestParam("date") LocalDate day) {    
    return reportsService.getWorklogsForWorkerAndDay(workerUserName, day);
  }

}
```

Pasamos los tests y efectivamente fallan: tanto el unitario que tenemos como el autogenerado. ¿Y esto por qué? Porque en realidad hemos modificado el contrato. Actualizamos el contrato y corregimos los tests que fallan:

##### worklogsForWorkerAndDay.yaml
```diff
request:
   urlPath: /worklogs/worker/JESSI
   queryParameters:
-      day: "2020-05-05"
+      date: "2020-05-05"
   method: GET
   matchers:
    url:
      regex: /worklogs/worker/([a-zA-Z]*)
    queryParameters:
-      - key: day
+      - key: date
        type: matching
        value: "(\\d\\d\\d\\d)-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])"
```

Hacemos `./mvnw clean test` y ahora ya pasan todos nuestros tests. ¡Bien! Vemos cómo ha cambiado el test autogenerado. 

##### Producer | WorklogsTest.java

```diff
@Test
public void validate_worklogsForWokerAndDay_success() throws Exception {
  // given:
  MockMvcRequestSpecification request = given();

  // when:
  ResponseOptions response = given().spec(request)
-	      .queryParam("day","2020-05-05")
+	      .queryParam("date","2020-05-05")
        .get("/worklogs/worker/JESSI");
```

Como hemos cambiado el contrato debemos hacer llegar al _consumer_ la actualización, así que hacemos `./mvnw clean install` en el _producer_ y pasamos los tests del _consumer_ con `./mvnw clean test`. 

¿Qué sucede? Si bien los tests unitarios que teníamos siguen pasando correctamente, el nuevo test añadido falla: nos hace ver que algo ha cambiado en el contrato, así que la aplicación no va a funcionar. ¡Bien! **Objetivo conseguido: hemos detectado el problema antes del despliegue en producción**.

Modificamos la implementación del _consumer_:

#### Consumer | ReportsService.java

```diff
public DayStatusSummary getDayStatusSummaryForWorkerAndDay(String workerUserName, LocalDate date) {
  // retrieve worklogs for worker and day
  List<WorklogInfo> worklogsForDay = webClient.get().uri(uriBuilder -> uriBuilder
-	    .path("/worklogs/worker/{workerUserName}").queryParam("day", date).build(workerUserName)).retrieve()
+	    .path("/worklogs/worker/{workerUserName}").queryParam("date", date).build(workerUserName)).retrieve()
      .bodyToFlux(WorklogInfo.class).collectList().block();

  int totalDuration = worklogsForDay.stream().mapToInt(WorklogInfo::getDuration).sum();
```

Pasamos los tests, y vemos que al cambiar la implementación los tests unitarios también han dejado de funcionar (lógicamente). Sólo nos quedará por lo tanto, corregirlos.

Como hemos visto en el ejemplo, es importante que cuando cambia el contrato tanto _consumer_ como _producer_ estén al tanto del cambio.  

En este caso como es desde el _producer_ desde donde se realiza el cambio, es importante que el _consumer_ reciba la nueva especificación a través del stub (si no, los test seguirán pasando). En nuestro ejemplo es sencillo porque lo tenemos todo en local. Nos sirve para explicar el concepto de forma sencilla pero no nos olvidamos de que no refleja la realidad, donde muchas veces diferentes personas están trabajando en uno o en el otro sin necesidad de tener los proyectos en local.  
Existen muchas formas de organizar el código y por lo tanto existen diferentes soluciones, que habría que analizar en función del proyecto y sus necesidades. Las preguntas más importantes a las que habría que dar respuesta sería:

- **¿Dónde ubicamos los contratos?** ¿Podrían estar en el propio proyecto (como en el ejemplo) o quizás seríamejor que estuviesen en su propio repositorio de github?
- **¿Cómo gestionamos el stub del _producer_?** ¿Podríamos desplegarlo en un repo de maven?
- **¿Cómo gestionamos el versionado?** ¿Será el mismo que el del _producer_ o será independiente?

No vamos a entrar a valorar estas y otras muchas cosas, que habría que tener en cuenta a la hora de ponerlo en práctica porque la respuesta será *depende*. Depende del proyecto, de la organización de los equipos,... En la documentación de Spring Cloud Contract hay diferentes recomendaciones y ejemplos que pueden sernos de utilidad.
