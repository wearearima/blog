---
layout: post
title:  "Contract Testing en acción"
date:   2020-09-07 8:00:00
author: jessica
lang: es
categories: testing, software quality, QA
tags: testing, calidad, software quality, QA, contract testing, consumer-driven contract, consumer driven contract
header-image: 2020-07-15-contract-testing/header_recortado.png
---

En un [post anterior](https://blog.arima.eu/es/2020/09/03/contract-testing.html){:target="_blank"} hemos visto cómo surgen nuevas necesidades en el ámbito del testing derivadas de la evolución de las arquitecturas de las aplicaciones. En él, hablamos de cómo con el paso de los años hemos pasado de desarrollar aplicaciones basadas en una arquitectura monolítica a aplicaciones basadas en (micro)servicios. Donde antes teníamos tests centralizados en una única aplicación, ahora pasamos a tenerlos divididos en varias de forma que tendremos testeadas cada una de ellas de forma idenpendiente y estanca. 
Hemos presentado un ejemplo sencillo de una aplicación, que nos ha servido para establecer algunos conceptos (como _consumer_, _producer_, _servicio_) y que nos ha permitido poner en evidencia una nueva necesidad: tan importante como testear las funcionalidades en _consumer_ y _producer_ de forma independiente lo es asegurar que la interacción entre ambos es correcta. Esta necesidad podemos abordarla mediante test end-to-end, pero si bien estos tests ya resultan complejos de implementar/ejecutar en aplicaciones monolíticas en aquellas que no los son la complejidad es mayor. En este punto surge una idea: podría ser suficiente con verificar entre _consumer_ y _producer_  que existe un acuerdo que ambos cumplen. Aquí es donde descubrimos un nuevo concepto: **Contract Testing**.

¿Qué es Contract Testing? En la documentación de Pact encontramos la siguiente [definición](https://docs.pact.io/#what-is-contract-testing){:target="_blank"}
> Es una técnica que nos permite probar la integración de varias aplicaciones, verificando en cada una de ellas que los mensajes que envía o recibe (dependiendo de su rol consumer/producer) se ajustan a un acuerdo que está documentado en un contrato.

Este concepto podríamos desgranarlo y traducirlo (a nive práctico) en los siguientes puntos:
- En el consumer, en los test en lugar de hacer las llamadas a un “MockServer” (como veíamos [aquí](//TODO){:target="_blank"}), las peticiones se hacen a un “stub” del “producer” que cumple con un acuerdo concreto preestablecido y que ambos conocen. 
- En el producer, las llamadas que se realizan se basarán de igual modo en dicho acuerdo.
Dependiendo de la herramienta/framework utilizada, el concepto de “acuerdo entre consumer y producer” recibe el nombre de pacto o contrato. Pero no dejan de ser diferentes nombres para el mismo concepto: una especificación de cómo deben ser las llamadas y respuestas para consumir los servicios ofertados por el producer.

Volviendo al mismo ejemplo que hemos utilizado en el post anterior esta idea podríamos representarla como sigue: 

![Ejemplo del esquema de una aplicacion con consumer-producer donde se resalta la parte en la que se centra el Contract Testing](/assets/images/2020-09-07-contract-testing/01_schema_app_simplificado_agreement.jpg){: .center }

Una vez presentado la técnica de Contract Testing en términos generales, vamos a profundizar un poco más viendo los enfoques y herramientas existentes. Posteriormente y como para mi la única forma de aprender/entender es haciendo, veremos cómo materializar la teoría mediante un pequeño ejemplo. 

# Enfoques y herramientas
En la literatura principalmente encontramos la relación **_Contract Testing_** &rarr; **_Consumer Driven Contract Testing_**, algo que en un inicio me hizo más complejo entender el concepto subyacente. Entiendo que el motivo es que un _servicio_ de un _producer_ carece de sentido si no va a haber alguna aplicación utilizándolo (_consumer_). Por tanto, parece lógico que quien establezca qué acuerdo debe cumplirse sea el _consumer_, mientras que en el _producer_ debería recaer la responsabilidad desatisfacer las necesidades fijadas por _consumer_ (de ahí la coletilla de "Consumer Driven").

Sin embargo, y en base al tipo de proyectos que tenía en mente, no me terminaba de encajar. Se me hizo necesario verlo en perspectiva, y dar un paso atrás para primero entender el concepto que hay detrás (y que ya hemos explicado). Después de leer y profundizar un poco llegué a la conclusión de que en realidad podríamos encontrarnos con dos situaciones en función del proyecto que tuviésemos entre manos (diferentes en forma pero iguales en concepto) y así dependiendo de quién sea el que define el acuerdo podríamos tener dos enfoques:

- Consumer Driven Contract Testing
- Producer Driven Contract Testing

¿Por qué no? El nombre no deja lugar a dudas: en un caso la definición del contrato nace en el _consumer_ y en el otro del _producer_. La verdad es que hubo un momento en que _Producer Driven Contract Testing_ parecía que fuese invención mía (no hay más que ver la búsqueda en Google de este término o de provider-driven...), pero encontré una referencia a ese término (como veremos un poquito más adelante) lo cual me dió pie a continuar con mi esquema mental.

El concepto base en ambos casos no deja de ser el mismo, sin embargo dependiendo del enfoque que se ajuste mejor a nuestro proyecto habrá herramientas del mercado que se ajusten más o menos, y que nos ofrezcan las alternativas que cubran nuestras necesidades. Basándonos en el ejemplo presentado al inicio (y sabiendo que es un proyecto Spring Boot gestionado con Maven), las herramientas más populares que hemos encontrado que podríamos utilizar en nuestro proyecto han resultado ser:

- **Pact**

  Esta herramienta está fuertemente acoplada con _Consumer Driven Contract Testing_, básicamente porque los pactos estarán siempre en la parte consumer: 
  
  Pact is a code-first consumer-driven contract testing tool, .... 
  The contract is generated during the execution of the automated consumer tests
  https://docs.pact.io/getting_started/#consumer-driven-contracts

- **Spring Cloud Contract**

  Aunque en su descripción dice:
  > Spring Cloud Contract is an umbrella project holding solutions that help users in successfully implementing the Consumer Driven Contracts approach. Currently Spring Cloud Contract consists of the Spring Cloud Contract Verifier project. 

  Puede utilizarse tanto en un sentido como en otro. De hecho, en la documentación Pact indican que esta nació con el enfoque provider-driven contract (¡parece que no me he inventado el término!, tampoco estaré tan desencaminada ¿no?)
  Esta será la herramienta que utilizaremos en nuestros ejemplo. Ya veremos cómo nos ofrece ambas posibilidades.

Personalmente me ha resultado más sencillo utilizar un enfoque _Producer Driven_ para llegar comprender bien el concepto, e incluso para entender mejor un escenario _Consumer Driven_. Es decir, que sea quien ofrece los servicios quien defina el acuerdo. 
Probablemente sea porque en los proyectos que ha me han tocado de cerca, la casuística ha sido la de un _producer_ transversal a varias aplicaciones, que no conoce a sus _consumers_, y a quienes les oferta unos servicios determinados. 
Lo más común es encontrar ejemplos _Consumer Driven_ pero puede haber gente a la que como a mí, le más sea útil la aproximación _Producer Driven_ para comprender esta herramienta. Así que para toda esa gente (y para mi yo del futuro) utilizando la aplicación sobre los partes de horas (que siempre utilizo como ejemplo), vamos a implementar un pequeño ejemplo de cómo hacer Contract Testing utilizando **Spring Cloud Contract**.

# Ejemplo utilizando Spring Cloud Contract

## Definición del contrato
Definimos el acuerdo: escribiremos la especificación que tienen que cumplir _consumer_ y _producer_ para que la comunicación funcione correctamente. En Spring Cloud Contract se utiliza el término **contrato**. Se puede definir de diferentes formas (groovy, yaml, java, kotlin), para este ejemplo hemos elegido yaml porque nos parece fácil de escribir/leer. 

Un ejemplo de los contratos que podríamos tener, puede ser el siguiente:

##### worklogsForWorkerAndDay.yaml
```yaml
description: Given a worker's username and a day it returns the worklog info for that worker and day
name: worklogsForWokerAndDay_success
request:
   url: /worklogs/worker/JESSI
   queryParameters:
      day: "2020-05-05"
   method: GET
   matchers:
    url:
      regex: /worklogs/worker/([a-zA-Z]*)
    queryParameters:
      - key: day
        type: matching
        value: iso_date
response:
   status: 200
   headers:
      Content-Type: "application/json"
   bodyFromFile: worklogsForJessiOn20200505Response.json   

---
description: Given a worker's username if no date is provided it returns bad request 400
name: worklogsForWokerAndDay_wihtout_date_bad_request
request:
   url: /worklogs/worker/JESSI
   method: GET
response:
   status: 400
```
En este caso, caso en concreto estamos estableciendo dos situaciones. Si se hace una petición con el nombre de usuario y una fecha (establecemos el formato de cada uno de los parámetros aceptados), la respuesta será `status 200` y además devolverá un `JSON`. En este caso concreto establecemos cuál va a ser la respuesta mediante un [fichero](/src/test/resources/contracts/worklogs/worklogsForJessiOn20200505Response.json){:target="_blank"}. 

Este contrato debe estar accesible para el producer (independientemente que sea él quien lo defina o el consumer ;) ). En este caso y por simplificar estará en la carpeta `/test/resources/contracts/worklogs` del producer.

## Producer: configurar las dependencias en el pom.xml
Modificamos el pom.xml para añadir la dependiencia de Spring Cloud Contract Verifier y el plugin spring-cloud-contract-maven-plugin. Con este último conseguiremos que de forma automática:
- Se generen los tests que verifiquen que nuestro producer cumple el contrato
- Se cree un stub que permitirá al consumidor generar un wiremock (que cumplirá el contrato) contra el que ejecutar sus tests

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
Además de las dependencias, hay que crear una clase base de test para que la extiendan los tests autogenerados del producer y añadirla en la configuración del plugin en el pom.xml. Además de la clase base de test, se pueden personalizar diferentes aspectos como se explica en la [documentación del plugin](https://cloud.spring.io/spring-cloud-contract/spring-cloud-contract-maven-plugin/index.html){:target="_blank"}, como por ejemplo sobre dónde están los contratos, cómo generar los diferentes elementos etc.
En nuestro ejemplo, lugar de especificar una clase base para los tests  concreta, hemos configurado el paquete en el que deben estar todas las clases "base" (podría haber diferentes). 

Nuestra clase deberá estar en el paquete eu.arima.tr (porque así lo hemos configurado). Además, como el contrato lo hemos definido en la carpeta "contracts/worklogs", por lo tanto (en base a la documentación que indica que el nombre se infiere en base a los nombres de las dos últimas carpetas), la clase deberá llamarse WorklogsBase.java.

A continuación mostramos cómo es la clase de base, que es la que hemos utilizado en nuestro ejemplo:

#### Producer | WorklogsBase.java
```java
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
## Producer: crear y ejecutar los tests
Como mencionabamos en el apartado anterior, con este plugin podemos generar automáticamente los tests que aseguren que el produce cumple el conrato. Vamos a verlo. Para ello hacemos `./mvnw clean test` (en el producer) y vemos que:
- Se generan las clases de test del producer
- Se ejecutan los tests
- Además se crea un .jar (que de momento dejamos aparcado)

¿Cómo son los tests que se autogeneran? Está en la carpeta generated-test-sources. En este caso en concreto, como tenemos una única carpeta, se genera una única clase con los tests:

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

 @Test
 public void validate_worklogsForWokerAndDay_wihtout_date_bad_request() throws Exception {
  // given:
   MockMvcRequestSpecification request = given();


  // when:
   ResponseOptions response = given().spec(request)
     .get("/worklogs/worker/JESSI");

  // then:
   assertThat(response.statusCode()).isEqualTo(400);
 }

}
```
Como vemos hay un método de test por cada definición del contrato. En ambos vemos como se hace un assert para comprobar que el statusCode de la response es la esperada. Además en la primera de ellas vemos cómo se verifica que el tipo de respuesta sea un json y cómo se ha parseado el fichero .json (al que hacíamos referencia en la especificación) para hacer los asserts necesarios que aseguran que la respuesta es la esperada.

**¿Y desde eclipse?**
Yo utilizo eclipse en mis desarrollos, así que me interesa poder ejecutarlos desde el IDE. Obviamente primero necesitamos que se generen, esto ya hemos visto cómo debemos hacerlo mediante clean test. Pero si no he cambiado el contrato y no hace falta que se regeneren los test y además estoy desarrollando y quiero pasar todos los tests, ¿cómo lo hago? Como son clases autogeneradas, es necesario añadir las carpetas de generated-test-sources al buildpath. En nuestro ejemplo lo hacemos como sigue.

![Configuración del buildpath para ejecutar los tests desde eclipse](/assets/images/2020-09-07-contract-testing/02_buildpath_config.png){: .center }

## Consumer: configurar las dependencias
A diferencia del producer, los tests en el consumer no se generan de forma automática, sin embargo, desde el producer hemos generado un .jar con el stub que nos permitirá simular las llamadas al producer. En nuestro caso, el jar es: timeReports-producer-0.0.1-SNAPSHOT-stubs.jar que podemos encontrarlo en la carpeta target del producer.
En nuestro ejemplo, al tener ambos proyectos en local, si en lugar de hacer ./mvnw clean test (en el producer) hacemos ./mvnw clean install tendremos dicho jar directamente en nuestro repositorio local de maven, con lo cual, podremos configurar nuestro consumer para que acceda a él.

Para acceder a él añadimos la siguiente dependencia en el pom.xml:

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

## Consumer: crear y ejecutar los tests

Una vez añadidas las dependencias ya podemos crear el wiremock basado en ese stub y crear nuestros tests. Un ejemplo podría ser:

```java

```
Con esto ya tendríamos la comunicación entre ambos testeada, asegurándonos que si en algún momento en alguno de los dos componentes hubiese una modificación en el contrato los tests del otro fallarían.

¿Ya conocemos el qué pero y el cómo?
En nuestro ejemplo lo tenemos todo en local pero ¿cómo organizamos todo esto? Existen muchas formas de organizar el código. En nuestro ejemplo tenemos todo en “local” (es decir, el contrato en el propio proyecto) porque para explicar el concepto de contract testing es la forma más sencilla. Pero existen diferentes soluciones, que habría que analizar en función del proyecto y sus necesidades. Habría que decidir:
dónde ubicar los contratos (como en este ejemplo en el propio proyecto o sería mejor que estuviesen en su propio repositorio de github?)
qué hacer con el stub del producer (lo desplegamos en un repo de maven?)
qué versionado seguir
...
Todo esto, y otras muchas cosas, que habría que tener en cuenta a la hora de ponerlo en práctica queda fuera del objetivo de este artículo, además dependerá del proyecto en el que se esté trabajando. 

Lo que pretendía no era otra cosa que dejar lo más claro posible el concepto de contract testing para dar a conocer una más de las herramientas que pueden sernos de utilidad en el camino para dotar de calidad a nuestros proyectos.
