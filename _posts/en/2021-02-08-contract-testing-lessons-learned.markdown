---
layout: post
title: Lessons learned about Contract Testing
date: 2021-02-08 8:00:00
author: jessica
lang: en
categories: testing, software quality, QA
tags: testing, calidad, software quality, QA, contract testing, consumer-driven contract testing, consumer driven contract testing, provider-driven contract testing, provider driven contract testing
header-image: 2021-02-08-contract-testing/header.jpg
---
Over the course of several posts, we have seen how, as a result of the evolution of application architectures, new needs arise in the field of testing. We have focused on a specific one: as important as testing the functionalities in _consumer_ and _producer_ independently is, so also is ensuring that [the interaction between them is correct](https://blog.arima.eu/en/2020/09/03/contract-testing.html){:target="_blank"}. We have seen that we have **Contract Testing** within our reach, with [different approaches and tools](https://blog.arima.eu/en/2020/10/09/contract-testing-approach.html){:target="_blank"} that allow us to address this specific need. Also using the **producer driven** approach and [**Spring Cloud Contract**](https://spring.io/projects/spring-cloud-contract){:target="_blank"} we have [put into practice](https://blog.arima.eu/en/2020/10/29/playing-with-spring-cloud-contract.html){:target="_blank"} everything learned. 

I was thinking of ending this series of posts with a compilation of lessons learned ... Something like a mini-post summarizing everything we've seen so far in four or five headlines.
While reflecting on this, I remembered that in my learning process there was a lesson that stood out from the rest. There may be those for whom it’s obvious, but there’s sure to be someone out there who finds themself in the same alley as I did at the time ... So, for that "someone" 😉 here’s my two cents:
> Doing Contract Testing **does not** exempt you from doing Unit Testing or Integration Testing. 

Okay, I know that this is what it says on all the sites, that I'm not saying anything new ... but hey, I was tempted to do it ... maybe you who are reading this too ... and you know my mantra: _understand by doing_ 😊.
We are going to start from the example in which we used Spring Cloud Contract. We already know what it’s about and we can check the example. 

Looking at the _consumer_ tests, we might think ...

💡 Hey! It would be great to have all the possible cases that I need for my logic represented in the stub so it would save me the unit test where I have all those situations mocked up

What a good idea!

🤔 Sure, but the _producer_ doesn’t have to know my different scenarios and is the one who created the contract.
  
Hmm, it's true ... how could I have come up with that? What was I thinking .....? 

💡 Wait! What I need is _consumer driven contracts_!

I can create the contracts from the _consumer_ with the information I need and make the contracts available in the _producer_ via pull-request (for example). As the _producer_ tests are generated automatically, no-one is going to find out ... Perfect! In the bag! Let's get to work! 

If we take a look at the _consumer_ tests we see that basically, we want to test three situations: when the duration of the worklogs is 8 hours, more than 8 hours and less than 8 hours.

We therefore generate the new contracts and leave them so that they are accessible from the _producer_. The following code shows how we might do this (the complete code of all the steps that we will take, along with the .json, is in [Github](https://github.com/wearearima/time-report-ContractTesting-03){:target="_blank"}).

#### worklogsForWorkerAndDay.yaml
```yml
description: Given a worker's username and a day it returns worklogs with 8 hours
name: worklogsForWokerAndDay_with_8hours_worklogs
request:
   url: /worklogs/worker/JESSI
   queryParameters:
      day: "2020-05-01"
   method: GET
   matchers:
    url:
      regex: /worklogs/worker/([a-zA-Z]*)    
response:
   status: 200
   headers:
      Content-Type: "application/json"
   bodyFromFile: worklogs_8hours.json

---   
description: Given a worker's username and a day it returns worklogs that sum more than 8 hours
name: worklogsForWokerAndDay_with_moreThan8hours_worklogs
request:
   url: /worklogs/worker/JESSI
   queryParameters:
      day: "2020-05-05"
   method: GET
   matchers:
    url:
      regex: /worklogs/worker/([a-zA-Z]*)    
response:
   status: 200
   headers:
      Content-Type: "application/json"
   bodyFromFile: worklogs_moreThan8hours.json
   
---   
description: Given a worker's username and a day it returns worklogs that sum less than 8 hours
name: worklogsForWokerAndDay_with_lessThan8hours_worklogs
request:
   url: /worklogs/worker/JESSI
   queryParameters:
      day: "2020-05-10"
   method: GET
   matchers:
    url:
      regex: /worklogs/worker/([a-zA-Z]*)    
response:
   status: 200
   headers:
      Content-Type: "application/json"
   bodyFromFile: worklogs_lessThan8hours.json
```

We have generated the 3 situations that we wanted.  
With the contract defined, it's time to generate the stub in the _producer_. We run `./mvnw clean install` and we see that although we have changed the contract with Spring Cloud Contract, the tests are autogenerated, so everything goes according to plan and we don't have to touch anything in the _producer_.

As we already have the stub accessible with the possible cases generated from the _consumer_, we could now delete our unit tests and implement them by making calls to the stub directly. The code would be: 

#### Consumer | ReportsServiceTest.java
```java
@ExtendWith(SpringExtension.class)
@SpringBootTest(properties = { "server.url=http://localhost:8083" })
@AutoConfigureStubRunner(ids = { "eu.arima.tr:timeReports-producer:+:stubs:8083" })
public class ReportsServiceTest {

  @Autowired
  private ReportsService reportsService;

  @Test
  @DisplayName("Given a worklog with 8 hours duration the status is RIGHT_HOURS")
  void when_the_worklog_for_the_resquested_day_is_8_hours_the_status_is_RIGHT_HOURS() throws InterruptedException {
    LocalDate day = LocalDate.of(2020, 05, 01);
    String username = "JESSI";

    DayStatusSummary result = reportsService.getDayStatusSummaryForWorkerAndDay(username, day);

    assertStatusEquals(RIGHT_HOURS, result);

  }

  @Test
  @DisplayName("Given a list of worklogs with more than 8 hours duration the status is MISSING_HOURS")
  void when_the_worklogs_for_resquested_day_are_more_than_8_hours_the_status_is_MISSING_HOURS()
      throws InterruptedException {
    LocalDate day = LocalDate.of(2020, 05, 05);
    String username = "JESSI";

    DayStatusSummary result = reportsService.getDayStatusSummaryForWorkerAndDay(username, day);

    assertStatusEquals(DayStatus.EXTRA_HOURS, result);

  }

  @Test
  @DisplayName("Given a list of worklogs with less than 8 hours duration the status is MISSING_HOURS")
  void when_the_worklogs_for_resquested_day_are_less_than_8_hours_the_status_is_MISSING_HOURS()
      throws InterruptedException {
    LocalDate day = LocalDate.of(2020, 05, 10);
    String username = "JESSI";

    DayStatusSummary result = reportsService.getDayStatusSummaryForWorkerAndDay(username, day);

    assertStatusEquals(MISSING_HOURS, result);

  }

  @Test
  @DisplayName("Given the username of a worker the status result has that username")
  void the_status_result_belongs_to_the_requested_worker() throws InterruptedException {
    LocalDate day = LocalDate.of(2020, 05, 01);
    String username = "JESSI";

    DayStatusSummary result = reportsService.getDayStatusSummaryForWorkerAndDay(username, day);

    assertEquals(username, result.getWorkerUserName());

  }

  @Test
  @DisplayName("Given a date the status result has that date")
  void the_status_result_belongs_to_the_requested_day() throws InterruptedException {
    LocalDate day = LocalDate.of(2020, 05, 01);
    String username = "JESSI";

    DayStatusSummary result = reportsService.getDayStatusSummaryForWorkerAndDay(username, day);

    assertEquals(day, result.getDate());

  }
}

```
Great! Everything is much cleaner. How could it not have occurred to me before!?

But what would happen if we modify the logic of our _consumer_?
For example, suppose we consider the case of summer, when instead of 8-hour days we have 7-hour days.
To introduce this change, as a minimum we would have to:

1. Modify the contract and add more scenarios, so that depending on the input parameters, it returns different data
2. Send the contract to the _producer_ (for example PR)
3. Regenerate _producer_ elements such as tests and the stub (`./mvnw clean install`)
4. Modify the tests in the _consumer_ to add the new scenarios
 
We are modifying the contract when in reality there have been no changes in the "agreement" between _consumer_ and _producer_. We are taking advantage of Spring Cloud Contract to use it as a “mock” data generation method for our business logic ... Something doesn't seem right. If we had not made the change, we would only have to do step 4. It seems that it wasn’t such a good idea after all.
So, can we do it? Yes. However **just because you can doesn’t mean you should**.

Having put it into practice, we are forced to return to our original conclusion highlighted at the beginning: Contract testing replaces neither unit tests, nor integration tests, nor other tests that we may have in our projects. Contract testing is one more tool, a complement to the previous ones, the objective of which is NOT to verify/ensure the proper functioning of the business logic (neither of consumers nor of producers) - for that there are the unit or integration tests. Its objective IS to ensure that the agreements between _consumer_ and _producer_ are complied with, as they make sure that the interaction between _consumer_ and _producer_ is correct.
 
The truth is that we have a tendency to discover a tool, and if we like it and it suits us, to use it indiscriminately. As we have seen, when we are applying them, it might seem that we could do without our unit tests, but if we look further, we see that what we thought was a brilliant discovery is not such a good idea, in fact quite the opposite. 

# Lessons learned
Well, the time for the summary has come. Let's see what we have learned throughout these posts.

- We have one more tool that helps us to test (micro)services applications, which does not apply to monolithic applications.

- As with all the other test types/techniques, it is necessary to find a balance and be clear about their objective - in this case, to test the agreement (contract or pact) between _consumer_ and _producer_ (neither more nor less) and not use them indiscriminately.

- In projects where the _producer_ works across several _consumers_ (where development is not linked between them) and/or public users, the _producer_-driven approach seems more appropriate, where it is the _producer_ who defines the nature of the agreement to be complied with in the communication.

- In projects where the _producer_ has no reason to exist without the _consumer_, and where developments are more linked, the _consumer_-driven approach seems more appropriate as it will be the _consumer(s)_ who will indicate their needs to the _producer_ by establishing the agreement to be fulfilled in the communication.

- How to implement/organize testing will depend on the selected approach and the nature of the project: there is no single universal recipe for good testing. 
