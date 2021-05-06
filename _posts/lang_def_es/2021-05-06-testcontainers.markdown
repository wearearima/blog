---
layout: post
title:  "Testcontainers: contenedores al servicio del testing"
date:   2021-05-04 8:00:00
author: jessica
lang: es
categories: testing, software quality, QA
tags: testing, calidad, software quality, QA, testContainers, test integración
header-image: 2021-05-06-testcontainers/header.jpg
---

Siempre he sido más fan de los test unitarios que de los tests de integración, sobre todo por un motivo: no necesito nada externo para poder pasarlos. No necesito tener una base de datos arrancada, un servicio externo al que conectarme o un Kafka funcionando para poder pasar los tests y por tanto para poder desarrollar.
Y eso en el entorno de desarrollo, si hablamos ya del entorno de integración ya ni te cuento.  
Por ejemplo, en el caso de las bases de datos tenemos la opción de hacer los tests con H2. Pero también es cierto que dependiendo del tipo de proyecto, puede darse la situación de que algo que funciona perfectamente en H2 no lo haga en la base de datos para la que estamos desarrollando: 
Tan cierto como que frecuentemente hemos caído en el  
> “Venga va... con h2, por no arrancar la bd...”  

lo es la situación  
> “¡Pero si está testeado! ¿Entonces por qué ...? Ups...”

Yo siempre he sido de las que necesitaba tener todo instalado: Mysql, Postgres, Kafka,.... todo lo que fuese necesario para ejecutar el proyecto. Así, dependiendo del proyecto me tenía que asegurar de tener todo instalado y unos servicios u otros levantados... hasta que mis compañeros me descubrieron los contenedores, bueno Docker. 
Nunca he sido muy hábil con estas cosas, pero la verdad es que gracias a ellos, no tengo la necesidad de tener millones de cosas instaladas: tengo las imágenes de los servicios que necesito y no tengo más que poner en marcha los que necesito y ya.  
Bueno al grano. Es cierto que ahora para ejecutar las aplicaciones lo tengo todo mucho más organizado, pero en realidad para desarrollar, sigo estando un poco en las mismas: si quiero pasar tests de integración tengo que acordarme de levantar la base de datos (por ejemplo) así que no termina de ser tan transparente como lo es H2.  

<small>Como alguno ya habrá imaginado todo esto también tiene aplicación en CI, pero me voy a centrar en el día a día del desarrollador y en cómo nos ayuda esta herramienta en el trabajo diario.</small>

> "Tiene que haber algo que una ambos mundos y que haga que los tests sean autosuficientes simulando un entorno real"

Con esta idea en la cabeza y tras una conversación con un compi descubrí que así era: ¡existía algo llamado [**TestContainers**](https://www.testcontainers.org/){:target="_blank"}!

Por ejemplo, imaginemos algunas situaciones del día que nos hacen suspirar (o resoplar más bien): ¡nuevo miembro en el equipo! o ¿si queremos pedir ayuda a algún compi con un caso de uso o bug? o ¿si volvemos a un proyecto en el que hace meses que no trabajamos?  
Ante situaciones como estas (y otras) cuántas veces no habremos pensado: ¿no sería posible descargar todo y poder lanzar los tests y ponerme a desarrollar sin hacer absolutamente nada más? 
Hace un tiempo, viendo una presentación de [@kiview](https://twitter.com/kiview){:target="_blank"}, me di cuenta que no estaba sola. Al principio de su presentación decía algo así como:
> ...una experiencia de onboarding exitosa en un proyecto sería que el desarrollador sólo tuviese que clonar el repositorio, hacer el build y que con eso ya tuviesesmos el build hecho incluyendo los tests unitarios y los tests de integración...  

Es decir, seguir estos pasos:
```
> git clone https://github.com/wearearima/school-library-testcontainers-01.git
> cd school-library-testcontainers-01
> ./mvnw install
```
¡Y ya!  
Los ojos me hicieron 😍. La charla se titulaba [Integration Testing with Docker and Testcontiners](https://www.youtube.com/watch?v=Lv1evJe2MRI){:target="_blank"}, exacto: **TestContainers**. Bueno, pues ¡good news! Parece que trabajar con **TestContainers** nos facilitan el acercarnos a ese objetivo y nos simplifica el trabajo para que nos podamos centrar en el desarrollo propiamente dicho (obviamente, implícitamente en los tests).

# Ejemplo de Database container (Postgres Module)
Así contado, todo suena muy bien pero (como bien sabréis quienes me leáis de vez en cuando) para entender los conceptos tengo que ponerlos en práctica, así que hemos preparado un ejemplo en [Github](https://github.com/wearearima/school-library-testcontainers-01){:target="_blank"}. 
Lo más común probablemente es la situación en la que hacemos tests contra base de datos y Testcontainers nos ofrecen diferentes _módulos_ para diferentes bases de datos. Por ello, hemos preparado un ejemplo sencillo, de una aplicación Spring Boot, que se conecta a una base de datos Postgres.  
Nuestro ejemplo:  
    Supongamos una biblioteca de un cole. Tenemos una funcionalidad que servirá para ir dando de alta los ejemplares que vayamos recibiendo. Uno de los métodos que podríamos tener, podía ser el de "añadir una copia de un libro" (entendiendo "libro" como el concepto y "copia" la representación de cada uno de los ejemplares que podamos tener). 
<small>En un futuro seguiremos evolucionando este ejemplo e iremos añadiendo código.</small>


Como hemos dicho, utilizaremos el módulo que hay para [Postgres](https://www.testcontainers.org/modules/databases/postgres/){:target="_blank"}. La implementación de los tests utilizando este container es muy sencilla, ¡vamos allá!

## Instalar Docker
Lo primero que necesitamos es instalar [Docker Desktop](https://www.docker.com/products/docker-desktop){:target="_blank"} (en caso de no tenerlo). A continuación dejo también, la sección de la documentación donde podemos encontrar los requerimientos de Docker: [General Docker requirements](https://www.testcontainers.org/supported_docker_environment/){:target="_blank"}.


## Añadir las dependencias necesarias
Para empezar con el código, lo primero que tendremos que hacer será añadir las dependencias necesarias al proyecto (en nuestro caso en el pom.xml).

En nuestro caso hemos generado el proyecto utilizando Spring Initializr, desde donde hemos añadido la dependencia

![Imagen de cómo se añade la depedencia de testscontainer utilizando springinitializr](/assets/images/2021-05-06-testcontainers/spring-initializr.png){: .center }

En caso de hacerlo manualmente, en la [documentación](https://www.testcontainers.org/quickstart/junit_5_quickstart/#1-add-testcontainers-as-a-test-scoped-dependency){:target="_blank"} se detalla cómo añadir las dependencias.

Además, como vamos a utilizar el módulo de Postgres añadimos esa dependencia:

#### pom.xml
```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>postgresql</artifactId>
    <scope>test</scope>
</dependency>
```

Bueno, y del mismo modo que haríamos si no estuviesemos utilizando Testcontainers, incluiremos la dependencia de Postgres.

#### pom.xml
```xml
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <scope>runtime</scope>
</dependency>
```

## Start coding!
¡Y listo! Ya podemos implementar nuestro caso de uso. Vamos a implementar más de un test (disponibles en [Github](https://github.com/wearearima/school-library-testcontainers-01/blob/master/src/test/java/eu/arima/schoolLibrary/bookStore/BooksServiceTest.java){:target="_blank"}. ), aquí veremos el código para uno de ellos. Será un test que haremos que comprobará que cuando añadamos una copia a un libro cuyo ISBN ya exista, se añadirá una copia al mismo. ¿Sencillo verdad?

#### BooksServiceTest.java
```java
@SpringBootTest
@Transactional
class BooksServiceTest {

    @Autowired
    private BooksService booksService;
    @Autowired
    private BooksRepository booksRepository;
    @Autowired
    private CopiesRepository copiesRepository;

    @Test
    @DisplayName("addCopy for a book that exists with the provided isbn adds a new copy to it")
    void addCopy_if_book_exist_adds_new_copy() {
        String isbn = "9780745168197";
        Book existingBook = booksRepository.findBookByIsbnEquals(isbn).orElseThrow();
        int existingNumCopies = existingBook.getCopies().size();

        Copy createdCopy = booksService.addCopy(existingBook.getTitle(), existingBook.getAuthors(), isbn);

        Book updatedBook = booksRepository.findById(existingBook.getId()).orElseThrow();
        assertAll(
                () -> assertEquals(existingNumCopies + 1, updatedBook.getCopies().size()),
                () -> assertRelationBetweenBookAndCopyIsCorrect(createdCopy, updatedBook));

    }

}
```

Pero si ejecutamos el test sin más, veremos que falla por no poder levantar el contexto: le falta la información de la base de datos.
Es cierto que podríamos ir a application.properties y setear ahí los valores.... pero eso requeriría que si ese nuevo desarrollador que llegar (o tú que te vas a descargar el ejemplo) levantase la base de datos etc. Ya no sería el "ideal" que buscamos. ¿La solución?

### @Testcontainers
Efectivamente una anotación `@Testcontainers` y unas líneas más y lo tendremos:

#### BooksServiceTest.java
```java
@SpringBootTest
@Transactional
@Testcontainers
class BooksServiceTest {

    @Container
    private final static PostgreSQLContainer postgresContainer = new PostgreSQLContainer(DockerImageName
            .parse("postgres:13"));

    @DynamicPropertySource
    static void databaseProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgresContainer::getJdbcUrl);
        registry.add("spring.datasource.username", postgresContainer::getUsername);
        registry.add("spring.datasource.password", postgresContainer::getPassword);
    }

}
```
¿Qué hemos hecho?
- Hemos añadido la anotación `@Testcontainers` a la clase de test. 
- Hemos creado una instancia de un contenedor con Postgres utilizando la anotación `@Container` y especificando la versión. 
- Y por último hemos seteado la información del datasource a partir del contenedor creado mediante `@DynamicPropertySource`.

Como podéis ver la implementación es muy sencilla, el beneficio es instantáneo: podéis descargaros el ejemplo y ejecutarlo directamente en vuestros equipos sin nada más que tener Docker instalado (¿recordáis los 3 comandos de antes? Podéis probarlo.)

### Patrón Singleton
Hay otra forma de implementar todo esto, más eficiente, que sería utilizando el patrón Singleton. De esta forma utilizaríamos el mismo contenedor en más de una clase. 
De hecho, en la documentación se recomienda esta aproximación. En este ejemplo donde aún sólamente tenemos un clase de test no parece útil, pero probablemente no será la única funcionalidad de nuestro proyecto ¿verdad? Llegado ese momento, entonces sí, pasaríamos al patrón Singleton, como se explica [aquí](https://www.testcontainers.org/test_framework_integration/manual_lifecycle_control/#singleton-containers){:target="_blank"}.

Veamos cómo sería:

#### BooksServiceTest.java
```java
@SpringBootTest
@Transactional
class BooksServiceTest extends PostgresContainerBaseTest {
    //Ya no es necesario @Container ni @DynamicPropertySource porque lo gestionaremos en PostgresContainerBaseTest
}
```

#### PostgresContainerBaseTest.java
```java
public abstract class PostgresContainerBaseTest {

    static final PostgreSQLContainer postgresContainer;

    static {
        postgresContainer = new PostgreSQLContainer<>(DockerImageName.parse("postgres:13"));
        postgresContainer.start();
    }

    @DynamicPropertySource
    static void databaseProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgresContainer::getJdbcUrl);
        registry.add("spring.datasource.username", postgresContainer::getUsername);
        registry.add("spring.datasource.password", postgresContainer::getPassword);
    }
}
```

### Testcontainers y Pitest
Como hemos visto, tampoco esta forma supone a penas esfuerzo. Además de ser la recomendada, tenemos que decir, que tiene una ventaja frente a la anterior si estamos [midiendo la calidad de nuestros tests con PIT](https://blog.arima.eu/es/2020/05/25/mutation-testing.html){:target="_blank"}.

¿[PIT](https://pitest.org/){:target="_blank"}?¿Qué tienen que ver esto con PIT? Bueno pues si bien es cierto que PIT está directamente orientado a **tests unitarios** (sobre todo por cuestión de tiempos/eficiencia) también es cierto, que hasta ahora no nos habíamos encontrado con ningún problema a la hora de poner a prueba nuestros **tests de integración**.

Sin embargo, al intentar pasarlo sobre unos tests implementados como en el primer ejemplo, nos encontraremos un error: no hay forma de pasar los tests.
En su momento [reportamos el error](https://github.com/hcoles/pitest/issues/827){:target="_blank"}. El origen del problema parece estar en el cacheo del contexto de testing de Spring.
Detectamos que podían ir por ahí los tiros, al ver que utilizando `@DirtiesContext` el error desaparecía. Obviamente, la solución no es utilizar esta anotación ya que estaríamos condicionando nuestros tests por un factor externo a los mismos (al hecho de tener otra herramienta para medir su calidad).
Dado que la aproximación de utilizar el patrón singleton es la recomendada y además no presenta problemas nos decidimos por asumir dicha solución. Sin embargo, en el hilo hubo quien hizo una [extensión de JUnit para tal propósito](https://github.com/StefanPenndorf/pitTestcontainers/tree/sprint-test-context-cleanup-poc){:target="_blank"} (por si alguien estuviese interesado en utilizarla).


Hasta aquí una pequeña introducción a **Testcontainers**, con un ejemplo de aplicación en el caso de una base de datos. Como hemos mencionado anteriormente, Testcontainers nos ofrece otros muchos módulos. E incluso, en caso de que por nuestras necesidades necesitemos algo más concreto también dispone de soporte para que tengamos nuestro propio `docker-compose.yml` como se explica en la [documentación](https://www.testcontainers.org/modules/docker_compose/). 
En futuros posts, iremos evolucionando nuestra aplciación de forma que podamos introducir algunos ejemplos de otros casos de uso en los que utilizar Testcontainers (para ver de forma práctica su facilidad de uso y sus ventajas).



