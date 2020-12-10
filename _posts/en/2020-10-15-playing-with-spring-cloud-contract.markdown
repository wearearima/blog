---
layout: post
title:  Playing with Spring Cloud Contract
date:   2020-10-29 8:00:00
author: jessica
lang: en
categories: testing, software quality, QA
tags: testing, calidad, software quality, QA, contract testing, provider driven contract testing, spring cloud contract
header-image: 2020-10-15-playing-with-spring-cloud-contract/header.jpg
---
In a [previous post](https://blog.arima.eu/en/2020/09/03/contract-testing.html){:target="_blank"} we saw how new needs arose in the field of testing derived from the evolution of application architectures.
  
Through a simple example we established concepts such as _consumer_, _producer_, _service_ and showed that just as important as testing the functionalities in _consumer_ and _producer_ independently is, so also is ensuring that the interaction between them both is right.

We introduced the concept of **Contract Testing**, which we delved into in another [post](https://blog.arima.eu/en/2020/10/09/contract-testing-approach.html){:target="_blank"} which allowed us to get familiar with the different approaches and tools.

Now, with all the information to hand, it's time to put all those ideas into code. We will do it step by step, starting from the example in the first post, which we can download from [here](https://github.com/wearearima/time-report-contractTesting){:target="_blank"}. Remember that here we highlighted the problem that we might encounter: an application that fails in production despite all the unit and integration tests pass.

We have chosen the **producer driven** approach and as a tool we will use [**Spring Cloud Contract**](https://spring.io/projects/spring-cloud-contract){:target="_blank"}. The code is available on [Github](https://github.com/wearearima/time-report-contractTesting-02){:target="_blank"}. Let's go!

# 1. Define the contract

We will start by defining the agreement: we will write the specification that _consumer_ and _producer_ have to comply with for the communication to work properly. In Spring Cloud Contract the term **contract** is used. It can be defined in different ways (groovy, yaml, java, kotlin) and we have chosen `yaml` because for this example, we thought it would be easy to read.

For our use case we define the following contract:

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

In this case we are establishing the following agreement:
_For a **request** with: a username and a date (whose format we also specify), the **response** will be: `status 200` and a `JSON` (whose content we establish through a [file](https://github.com/wearearima/time-report-contractTesting-02/blob/master/timeReports-producer/src/test/resources/contracts/worklogs/worklogsForJessiOn20200505Response.json){:target="_blank"})._

This contract must be accessible to the _producer_. In this case, and for simplicity, it will be in the _producer_ folder `/test/resources/contracts/worklogs`.

Once we have defined the contract, we will have to complete the implementation that complies with it and the necessary tests to verify it. In this example we were already starting from the implementation, so let's get on with the tests!

# 2. Producer: configure dependencies in the pom.xml

We modify the `pom.xml` by adding the Spring Cloud Contract Verifier dependency and the `spring-cloud-contract-maven-plugin`. With the latter we will automatically achieve:

- Generation of tests that verify that our _producer_ complies with the contract
- Creation of a stub that will allow the _consumer_ to generate a [WireMock](http://wiremock.org/){:target="_blank"} (which will comply with the contract) against which to run its tests

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

As shown in the `pom.xml` in addition to the dependencies, we have configured some of the plugin properties:
- We have indicated that the test framework will be JUnit 5
- We have indicated that the package that will contain the _test base class_ will be `eu.arima.tr`

What's this about the _test base class_? According to the specification, we must generate a base class for the autogenerated tests to extend. This class must contain all the information necessary for executing the tests (for example, we could configure mocks of some beans, populate the database with specific data for tests ...).
For this example we have created a very simple base class whose only responsibility will be to establish the context. We have defined the contract in the `contracts/worklogs` folder, therefore (based on the documentation that indicates that the name is inferred from the names of the last two folders), the class is called `WorklogsBase.java`.

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

The plugin supports the configuration of other parameters as explained in the [plugin documentation](https://cloud.spring.io/spring-cloud-contract/spring-cloud-contract-maven-plugin/index.html){:target="_blank"}, such as: where the contracts are, how to generate the different elements, etc.

# 3. Producer: create and run tests

As we mentioned in the previous section, with this plugin we can automatically generate the tests that ensure that the _producer_ complies with the contract. To do this we execute the command `./mvnw clean test` and we see that:

- The _producer_ test classes are generated
- The tests are run
- In addition, a `.jar` is created (which for now we leave parked)

What about the self-generated tests? They are in the `generated-test-sources` folder. In this specific case, as we have a single folder, a single class is generated:

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

As we can see, there is a test method for the definition of the contract. If we had more than one, then we would have a test for each of them.  

In the test that has been generated, we see how an `assert` is made to check that the response `statusCode` is as expected. We also see how it is verified that the type of response is a `json` and how the `.json` file has been parsed (which we referenced in the specification) to make the necessary `asserts` that ensure the response is as expected.

**And since eclipse?**

I personally use eclipse in my development, so I am interested in being able to run it from the IDE. Obviously we need it to be generated first and we have already seen how we should do it through `./mvnw clean test`. But if I have not changed the contract and it is not necessary to regenerate the tests and I am also developing and I want to pass all the tests, how do I do it? As they are autogenerated classes, it is necessary to add the `generated-test-sources` folders to the buildpath. For example, in this case:

![Configuration of the buildpath to run the tests from eclipse](/assets/images/2020-10-15-playing-with-spring-cloud-contract/buildpath_config.png){: .center }

# 4. Consumer: configure dependencies

Unlike the _producer_, the tests in the _consumer_ related to the contract are not generated automatically. But we are not alone: ​​remember that at the same time that the _producer_ tests were created, a `.jar` was also generated with the stub that will allow us to simulate the calls to the _producer_ from the _consumer_ tests.

In our case, the jar is: `timeReports-producer-0.0.1-SNAPSHOT-stubs.jar` which we can find in the _producer_ `target `folder.

In this case, having both projects locally, if instead of executing the command `./mvnw clean test` (in the _producer_) we run `./mvnw clean install` we will have the said jar directly in our local maven repository, with which we can configure our _consumer_ to access it.

In order to have access to it, we add the following dependency in the `pom.xml`:


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
    </dependency>
  ...
  </dependencies>
...  
```

Also, we must not forget the Spring Cloud Contract dependency to be able to execute the added stub.

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

# 5. Consumer: create and run tests

Once the dependencies are added, we can create the WireMock based on that stub and create our tests. We will do it with the annotation `@AutoConfigureStubRunner` where we indicate our stub so it will be downloaded and registered automatically in the Wiremock. An example might be:

##### Consumer | ReportsServiceContractTest.java

```java
@ExtendWith(SpringExtension.class)
@SpringBootTest
@AutoConfigureStubRunner(ids = { "eu.arima.tr:timeReports-producer:+:stubs:" })
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
With this, we would already have the communication between the two tested, making sure that if at any time there was a modification of the contract in either of the two components, the tests of the other would fail.

## Are we able to deploy in production with the certainty that everything works?

This was the problem we encountered in the [previous post](https://blog.arima.eu/en/2020/09/03/contract-testing.html){:target="_blank"}: despite having tested _consumer_ and _producer_, we were not able to know if anything was wrong until we reached production. Will we be able to detect it now?

Suppose we make the same change that we proposed in that post:


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

We run the tests and indeed they fail: both the unitary one we have and the self-generated one. And why is this? Because we have actually modified the contract. We update the contract and correct the tests that fail:

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

We run `./mvnw clean test` and now all our tests pass. Right! Let's see how the autogenerated test has changed.

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

As we have changed the contract, we must send the update to the _consumer_, so we execute `./mvnw clean install` in the _producer_ and run the _consumer_ tests with `./mvnw clean test`.

What's going on? Although the unit tests from before continue to work correctly, the new added test fails: it shows us that something has changed in the contract, so the application will not work. Right! **Goal achieved: we have detected the problem before deployment to production**.

We modify the _consumer_ implementation:

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

We run the tests, and we see that when changing the implementation, the unit tests have also stopped working (logically). Therefore, all we need to do is correct them.

As we have seen in the example, it is important that when the contract changes, both _consumer_ and _producer_ are aware of that change. 

In this case, as it is from the _producer_ where the change is made, it is important that the _consumer_ receives the new specification through the stub (if not, the tests will continue to pass). In our example it is simple because we have everything locally. It helps us to explain the concept in a simple way, but we should not forget that it does not reflect reality, where often, different people are working on one or the other, without needing to have projects locally.
There are many ways to organize the code and therefore there are different solutions, which should be analyzed depending on the project and its requirements. The most important questions to be answered would be:

- **Where do we place the contracts?** Could they be in the project itself (as in the example) or maybe it would be better if they were in their own github repository?
- **How do we manage the _producer_ stub?** Could we deploy it in a maven repo?
- **How do we manage versioning?** Will it be the same as that of the _producer_ or will it be independent?

We are not going to go into evaluating these and many other things, which should be taken into account when putting it into practice because the answer will be *it depends*. It depends on the project, on the organization of the teams, ... In the Spring Cloud Contract documentation there are different recommendations and examples that could be useful.
