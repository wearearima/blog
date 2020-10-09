---
layout: post
title:  "Introduction to Contract Testing, setting the context "
date:   2020-09-03 8:00:00
author: jessica
lang: en
categories: testing, software quality, QA
tags: testing, calidad, software quality, QA, contract testing, consumer-driven contract, consumer driven contract
header-image: 2020-09-03-contract-testing/header_recortado.png
---

Application development has evolved, and therefore new needs have arisen when it comes to testing and new tools to deal with them. Let's take a look!

We have gone from having monolithic architectures to applications based on (micro) services. Why do I say (micro) services instead of microservices? Because although the literature talks about the evolution of development from monolithic applications to applications based on microservices, in reality we often find ourselves with the integration of services (as is, without the need for them to be micro). The concept at hand applies equally well to the concept of microservices as it does to services, so from here on we will simplify using the term services.

Let's imagine an application for managing worklogs, tasks, worklog reports…. The scheme of this said service-based application could be reflected in the following scheme.

![Example for service based applicactions scheme](/assets/images/2020-09-03-contract-testing/01_schema_apps.jpg){: .center }

The example shown in the previous image is quite simple. We would have two applications (one for the generation of reports and another for managing tasks and worklogs) and both would have on one side their implementation of a web application and their mobile application. The 4 services would consume a common service in charge of the overall management of tasks and worklogs. We could have more complex examples, where a service consumes another that in turn is consumed by a third party, etc. but in order to better understand the concept, instead of adding complexity, we are going to simplify it even more by zooming in on the previous image.

![Zoom of a portion of the scheme](/assets/images/2020-09-03-contract-testing/02_schema_app_simplificado.jpg){: .center }

As shown in the image, we have reduced the example to a web application that is responsible for making work log reports and that accesses a REST API to obtain information. We are going to establish the terminology that we will use from here on:
- **CONSUMER**: We will refer to the web application or equivalent service in its role of consuming another service
- **PRODUCER**: With this term we will refer to the REST API or equivalent service in its role of offering its functionality.

Having clarified these two concepts, we’ll make the most of using **SERVICE** to refer to each one of the functionalities offered by the _producer_.

Let's see some possible code snippets of each:

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
The _consumer_ makes a request to `/worklogs/worker/username?day=date` with a specific username and date and calculates the status based on the worklogs received.

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
The _producer_ has an entry point for the url `/worklogs/worker/username?day=date` and makes a database query to retrieve the user’s worklogs on a specific date and returns them.

This complete code, as well as the rest that we use in the different examples, is available at [Github](https://github.com/wearearima/time-report-contractTesting){:target="_blank"}.

## Back to testing

So far then, a little introduction or snapshot of the evolution of application architecture and a context to define some concepts that we will use throughout the article. Now let's go back to what interests us: quality and testing. How would we test our application? What testing “tools” do we have at our disposal to test an application of this type?

As we have said, the _consumer_ remains a web application that accesses another application, which offers us its services through a REST API, the _producer_. We have a backpack full of tools and resources that can help us to test each of these two components in a watertight way: unit tests, integration tests, parameterized tests, JUnit 5, TestContainers, Mockito, [Pitest](https://blog.arima.eu/en/2020/05/25/mutation-testing.html){:target="_blank"}...

For example, in the _consumer_ we could test the services that include the calls to the REST API by mocking/stubbing the responses from the server. Let's see what some of those tests might look like.

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

This is just an example of a test that we could do. We have used the example to test [MockWebServer](https://github.com/square/okhttp/tree/master/mockwebserver){:target="_blank"}, but we could have directly mocked Webclient or used one of the other alternatives which exist such as [Wiremock](http://wiremock.org/){:target="_blank"}, [TestContainers](https://www.testcontainers.org/modules/mockserver/){:target="_blank"}....(in the not too distant future we’ll meet them again for sure ;)).

In the _producer_ we could also test the REST API using the tools offered by SpringBoot. Let's look at it too through an example.

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
  @DisplayName("When no date is requested it returns status 400")
  void response_400_for_request_with_no_date() throws Exception {

    mvc.perform(get("/worklogs/worker/" + USERNAME).contentType(APPLICATION_JSON))
        .andExpect(status().isBadRequest());

	}

  ...
}
``` 

With these (and other tests) we could have a well-tested _consumer_ and _producer_, but we are missing an important part: ensuring that they work together correctly. What might happen if there were a change in the _producer_? Let's suppose something as simple as changing the name of a parameter (for example, instead of **day** it is renamed **date**).

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

We would make the necessary corrections to the tests for our _producer_.


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

And perfect! the tests will continue to work on one component as well as the other.

Try it yourself. Download the [code](https://github.com/wearearima/time-report-contractTesting){:target="_blank"} and make the above modifications. You will see that the tests again work correctly in both the _consumer_ and _producer_.
But try something else... start the application and try [request the report for a user and a date](http://localhost:8080/reports/report-worker-day){:target="_blank"} from the application. Whoops! Error. The application crashes. What does this mean? That we will only be able to detect that something has broken when the application crashes 😱 ? Too late, don't you think? 😖

It is obvious that we must avoid this, but can we? If we go back to look in our backpack (which I like to call _testing toolbox_) we find the functional tests or end-to-end tests. If we had added some of these tests to all of the above, then we would have tested the integration of the entire system and we would be able to detect the previous problem before reaching production.

Although this is a solution, reality shows us that this type of test is not easy to carry out/maintain because it is more complex, forcing us to have _consumer_ and _producer_ running (which entails the start-up of the entire system) or it forces us to have 100% implemented the functionalities in both components to be able to carry out the tests. And while that’s simple in this example, in a more complex one... So, isn’t there some way of simplifying the communication test between _consumer-producer_? The business logic of each of them is tested in a watertight manner, therefore, it would actually be necessary (and sufficient) to ensure that both meet a particular specification... to verify that there is an **agreement** between _consumer_ and _producer_ and that both keep to it, nothing more (and nothing less). Do we have anything to help us do this? Of course! We have a tool whose objective is just this, called **Contract Testing**. Soon we will publish a new post with a practical example. Stay tuned!