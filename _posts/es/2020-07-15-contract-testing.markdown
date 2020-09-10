---
layout: post
title:  "Introducción a Contract Testing, estableciendo el contexto "
date:   2020-10-03 8:00:00
author: jessica
lang: es
categories: testing, software quality, QA
tags: testing, calidad, software quality, QA, contract testing, consumer-driven contract, consumer driven contract
header-image: 2020-07-15-contract-testing/header_recortado.png
---

El desarrollo de aplicaciones ha evolucionado, y por tanto han surgido nuevas necesidades a la hora de hacer testing y nuevas herramientas para hacerles frente ¡Vamos a verlo!

Hemos pasado de tener arquitecturas monolíticas a aplicaciones basadas en (micro)servicios. ¿Por qué digo (micro)servicios en lugar de microservicios? Porque aunque la literatura habla de la evolución del desarrollo desde aplicaciones monolíticas a aplicaciones basadas en microservicios, en la realidad nos encontramos muchas veces con la integración de servicios (tal cual, sin necesidad de que sean micro). El concepto que nos ocupa aplica igual de bien al concepto de microservicios que al de servicios, así que de aquí en adelante simplificaremos utilizando el término servicios.

Imaginemos una aplicación para la gestión de partes de horas, las tareas, los informes de partes de horas…. El esquema de dicha aplicación basada en servicios podría verse reflejado en el siguiente esquema.

![Ejemplo del esquema para aplicaciones basadas en servicios](/assets/images/2020-07-15-contract-testing/01_schema_apps.jpg){: .center }

El ejemplo que se muestra en la imagen anterior, es bastante sencillo. Tendríamos 2 aplicaciones (una para la generación de informes y otra para la gestión de tareas y partes de horas) y ambas tendrían por un lado su implementación de aplicación web y su aplicación móvil. Los 4 servicios consumirían un servicio transversal encargado de la gestión en bruto de tareas y worklogs. Podríamos tener ejemplos más complejos, donde un servicio consumiese otro que a su vez fuese consumido por un tercero, etc.  Pero para poder entender mejor el concepto, en lugar de añadir complejidad, vamos a simplificar aún más la foto haciendo zoom sobre la imagen anterior. 

![Zoom de una parte del esquema](/assets/images/2020-07-15-contract-testing/02_schema_app_simplificado.jpg){: .center }

Como se muestra en la imagen, hemos reducido el ejemplo a una aplicación web que se encarga de hacer informes sobre los partes de horas y que accede a un API REST para obtener información. Vamos a establecer la terminología que utilizaremos de aquí en adelante:
- **CONSUMER**: Nos referiremos así a la aplicación web o lo que es lo mismo, el servicio en su papel de consumir otro servicio
- **PRODUCER**: Con este término haremos referencia al API REST o lo que es lo mismo, el servicio en su papel de ofrecer su funcionalidad.

Utilizaremos los nombres en inglés ya que su traducción al castellano (consumidor y productor o proveedor) no me termina de convencer.

Teniendo claros estos dos conceptos, aprovecharemos para denominar **SERVICIO** a cada una de las funcionalidades ofertadas por el _producer_.

Vamos a ver unos fragmentos de código de cómo podrían ser ambos:

##### Consumer | ReportsService.java
```java
@Service
public class ReportsService {

  ...

  public DayStatusSummary getDayStatusSummaryForWorkerAndDay(String workerUserName, LocalDate date) {
    // retrieve worklogs for worker and day
	List<WorklogInfo> worklogsForDay = webClient.get().uri(uriBuilder -> uriBuilder
      .path("/worklogs/worker/{workerUserName}").queryParam("day", date).build(workerUserName)).retrieve()
      .bodyToFlux(WorklogInfo.class).collectList().block();

    int totalDuration = worklogsForDay.stream().mapToInt(WorklogInfo::getDuration).sum();

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

}
```
El _consumer_ hace una petición a `/worklogs/worker/username?day=fecha` con un nombre de usuario y una fecha concretos y en base a los worklogs recibidos calcula el estado.

##### Producer | WorklogController.java
```java
@RestController
@RequestMapping("/worklogs")
public class WorklogController {

  ...

  @GetMapping("/worker/{workerUserName}")
  public List<Worklog> getReportForWorkerAndDay(@PathVariable("workerUserName") String workerUserName, 
                                                @RequestParam("day") LocalDate day) {
    return reportsService.getWorklogsForWorkerAndDay(workerUserName, day);
  }

}
```
El _producer_ tiene un entry point para la url `/worklogs/worker/username?day=fecha` y hace una consulta a base de datos para recuperar los partes de horas del usuario en una fecha fecha y los devuelve.

Este código al completo, así como el resto que utilicemos en los diferentes ejemplos está disponible en [Github](https://github.com/wearearima/time-report-contractTesting){:target="_blank"}.

## Back to testing

Hasta aquí una pequeña introducción o fotografía sobre la evolución de arquitectura de las aplicaciones y una puesta en contexto para definir algunos conceptos que utilizaremos a lo largo del artículo. Volvamos a lo que nos interesa: calidad y testing. ¿Cómo testearíamos nuestra aplicación? ¿Qué “herramientas” de testing tenemos a nuestro alcance para testear una aplicación de este tipo? 

Como hemos dicho el _consumer_ no deja de ser una aplicación web que accede a otra aplicación, que nos ofrece sus servicios mediante un API REST, el _producer_. Tenemos la mochila llena de herramientas y recursos que nos pueden servir para testear de forma estanca cada uno de estos dos componentes: test unitarios, tests de integración, [tests parametrizados](https://blog.arima.eu/2020/07/01/parameterized-tests.html){:target="_blank"}, JUnit 5, TestContainers, Mockito, [Pitest](https://blog.arima.eu/2020/05/25/mutation-testing.html){:target="_blank"}...

Por ejemplo, en el _consumer_ podríamos testear los servicios que incluyen las llamadas al API REST mockeando/stubbeando las respuestas del servidor. Vamos a ver cómo podría ser alguno de los tests que podríamos tener.

##### Consumer | ReportsServiceWithMockWebServerTest.java
```java
public class ReportsServiceWithMockWebServerTest {
  ...

  private MockWebServer mockWebServer;
  private ReportsService reportsService;

  @BeforeEach
  public void setup() throws IOException {
    this.mockWebServer = new MockWebServer();
    this.mockWebServer.start();
    this.reportsService = new ReportsService(WebClient.builder().baseUrl(mockWebServer.url("/").toString()).build());
  }

  @Test
  @DisplayName("Given a worklog with 8 hours duration the status is RIGHT_HOURS")
  void when_the_worklog_for_the_resquested_day_is_8_hours_the_status_is_RIGHT_HOURS() throws InterruptedException {
    MockResponse mockResponse = new MockResponse().addHeader("Content-Type", "application/json; charset=utf-8")
        .setBody("[{\"fromTime\": \"08:30:00\", \"toTime\": \"16:30:00\"}]");
    mockWebServer.enqueue(mockResponse);

    DayStatusSummary result = reportsService.getDayStatusSummaryForWorkerAndDay(USERNAME, DAY);

    assertWebClientRequestEquals("/worklogs/worker/" + USERNAME + "?day=" + DAY);
    assertStatusEquals(RIGHT_HOURS, result);

  }

  @Test
  @DisplayName("Given a list of worklogs with 5,1,1 hours duration the status is MISSING_HOURS")
  void when_the_worklogs_for_resquested_day_are_5_1_1_hours_the_status_is_MISSING_HOURS() throws InterruptedException {
    MockResponse mockResponse = new MockResponse().addHeader("Content-Type", "application/json; charset=utf-8")
        .setBody("[{\"fromTime\": \"08:30:00\", \"toTime\": \"13:30:00\"},"
                + "{\"fromTime\": \"14:30:00\", \"toTime\": \"15:30:00\"},"
                + "{\"fromTime\": \"15:30:00\", \"toTime\": \"16:30:00\"}]");
    mockWebServer.enqueue(mockResponse);

    DayStatusSummary result = reportsService.getDayStatusSummaryForWorkerAndDay(USERNAME, DAY);

    assertWebClientRequestEquals("/worklogs/worker/" + USERNAME + "?day=" + DAY);
    assertStatusEquals(MISSING_HOURS, result);

  }

}
```

Este no es más que un ejemplo de test que podríamos hacer. Hemos aprovechado el ejemplo para probar [MockWebServer](https://github.com/square/okhttp/tree/master/mockwebserver){:target="_blank"}, pero podríamos haber mockeado directamente Webclient o utilizar alguna de las otras alternativas que existen como [Wiremock](http://wiremock.org/){:target="_blank"}, [TestContainers](https://www.testcontainers.org/modules/mockserver/){:target="_blank"}.... (en un futuro no muy lejano seguro que nos volvemos a encontrar con ellas ;)).

En el _producer_ podríamos testear el API REST también mediante las herramientas que nos ofrece SpringBoot. Veámoslo también mediante un ejemplo.

##### Producer | WorklogControllerMockedTests.java
```java
@WebMvcTest
public class WorklogControllerMockedTests {

  private static final LocalDate DAY = LocalDate.now();
  private static final String USERNAME = "USU";

  private static final String CORRECT_URL = "/worklogs/worker/" + USERNAME + "?day=" + DAY;

  @MockBean
  WorklogServiceImpl worklogService;

  @Autowired
  private MockMvc mvc;

  @Test
  @DisplayName("It returns a list with existing worklogs for requested worker and day")
  void worklog_list_for_existing_user() throws Exception {
    Worklog worklog1 = createWorklogWithDescription(1, "Description");
    Worklog worklog2 = createWorklogWithDescription(2, "Another description");
    when(worklogService.getWorklogsForWorkerAndDay(USERNAME, DAY)).thenReturn(Arrays.asList(worklog1, worklog2));

    mvc.perform(get(CORRECT_URL).contentType(APPLICATION_JSON)).andExpect(status().isOk())
        .andExpect(jsonPath("$", hasSize(2))).andExpect(jsonPath("$[0].id", is(worklog1.getId())))
        .andExpect(jsonPath("$[0].description", is("Description")))
        .andExpect(jsonPath("$[0].day", is(DAY.toString())))
        .andExpect(jsonPath("$[1].id", is(worklog2.getId())))
        .andExpect(jsonPath("$[1].description", is("Another description")))
        .andExpect(jsonPath("$[1].day", is(DAY.toString())));
  }

  @Test
  @DisplayName("When the user doesn't have worklogs it returns an empty list")
  void no_worklogs_for_user() throws Exception {

    when(worklogService.getWorklogsForWorkerAndDay(USERNAME, DAY)).thenReturn(emptyList());

    mvc.perform(get(CORRECT_URL).contentType(APPLICATION_JSON)).andExpect(status().isOk())
        .andExpect(jsonPath("$", hasSize(0)));

  }

  @Test
  @DisplayName("When no date is request it returns status 400")
  void response_400_for_request_with_no_date() throws Exception {

    mvc.perform(get("/worklogs/worker/" + USERNAME).contentType(APPLICATION_JSON))
        .andExpect(status().isBadRequest());

	}

  ...
}
```

Con estos (y otros tests) podríamos tener un _consumer_ y un _producer_ bien testeados, pero nos falta una parte importante: asegurar que juntos funcionan correctamente. ¿Qué sucedería si hay un cambio en el _producer_? Supongamos algo tan sencillo como el cambio del nombre de un parámetro (por ejemplo en lugar de **day** que se renombrase a **date**). 

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

Corregiríamos los tests que fuese necesario de nuestro _producer_.

```diff
@WebMvcTest
public class WorklogControllerMockedTests {

  private static final LocalDate DAY = LocalDate.now();
  private static final String USERNAME = "USU";

-  private static final String CORRECT_URL = "/worklogs/worker/" + USERNAME + "?day=" + DAY;
+  private static final String CORRECT_URL = "/worklogs/worker/" + USERNAME + "?date=" + DAY;
    ...
}
```

Y ¡perfecto! los tests seguirán funcionando tanto en un componente como en el otro.

Pruébalo tu mismo. Descarga el [código](https://github.com/wearearima/time-report-contractTesting){:target="_blank"} y haz las modificaciones anteriores. Verás que los tests vuelven a funcionar correctamente tanto en el _consumer_ como en el _producer_.
Pero prueba algo más... pon en marcha la aplicación y prueba a [solicitar el informe para un usuario y una fecha](http://localhost:8080/reports/report-worker-day){:target="_blank"} desde la aplicación. ¡Ups! Error. La aplicación falla. ¿Esto qué quiere decir?, que ¡sólo seremos capaces de detectar que algo se ha roto cuando la aplicación falle 😱 ! Demasiado tarde, ¿no crees? 😖

Es obvio que esto debemos evitarlo, ¿podemos? Si volvemos a revisar nuestra mochila (a la que me gusta llamar _testing toolbox_) encontramos los tests funcionales o test end-to-end. Si a todo lo anterior, añadimos unos tests de este tipo ya tendríamos testeada la integración de todo el sistema y seríamos capaces de detectar el problema anterior antes de llegar a producción.

Aunque esta es una solución, la realidad nos hace ver que este tipo de tests no son sencillos de realizar/mantener porque son más complejos, porque nos obligan a tener _consumer_ y _producer_ en marcha (con lo que conlleva la puesta en marcha de todo el sistema) o incluso porque nos obliga a tener 100% implementadas las funcionalidades en ambos componentes para poder realizar las pruebas. Y eso en este ejemplo que es sencillo, en uno más complejo... Entonces, ¿no hay alguna forma de simplificar el testeo de la comunicación entre _consumer-producer_? La lógica de negocio de cada uno de ellos está testeada de forma estanca, por lo tanto, en realidad sería necesario (y suficiente) asegurarnos que ambos cumplen una especificación concreta... verificar que existe un **acuerdo** entre _consumer_ y _producer_ y que ambos lo cumplen, nada más (y nada menos). ¿Tenemos algo que nos ayude en este propósito? ¡Cómo no! Tenemos una herramienta cuyo objetivo es este, su nombre **Contract Testing**. En breve publicaremos un nuevo post con un ejemplo práctico, stay tuned!
