---
layout: post
title:  "Another way of doing tests: property-based testing"
date:   2020-07-06 9:00:00
author: jessica
lang: en
categories: testing, software quality, QA
tags: testing, property based testing, PBT, calidad, software quality, QA, junit
header-image:	post-headers/property-based-testing.jpg
---

## What is property-based testing?
*Property-based testing* (from now on PBT) is another alternative for development tests where the main focus, instead of being a specific example/case, becomes a property of the the use case, understanding that a property becomes something like:

> for all input (x,y,....)  
> where precondition (x,y…) is met   
> the property (z,k....) is true

Normally the properties are not too detailed, they only verify some general characteristic that must be met.

For example, to test an addition custom method, if we were doing _example-based testing_, we could have several tests like these:
<pre>
<code>- given the numbers 10 and 1 the sum will be 11
- given the numbers 10 and 20 the sum will be 30
   . . . . </code></pre>

However, if we were doing PBT, we would formulate a more general test, for example like the one shown below:
<pre>
<code>for any integer a and b that are between 1 and 20
the sum of a and b will be greater than a</code></pre>


Let's look at the implications of a test like this.
### For all input (_a, b_)
> <pre style="margin-bottom: 0px">
> <code><b>for any integer a and b</b> that are between 1 and 20
the sum of a and b will be greater than a</code></pre>

Several sets of tests will be run with combinations of random values ​​for `a` and `b` (the exact number of runs depends on the framework/library used and is usually configurable).

### Where precondition is met (_a and b between 1 and 20_)
> <pre style="margin-bottom: 0px">
> <code>for any integer a and b <b>that are between 1 and 20</b>
the sum of a and b will be greater than a</code></pre>

We are indicating a precondition that both `a` and `b` must be between `1` and` 20`. If the random values ​​that are generated for a test (test execution, if we are purists) do not comply, it is discarded as a valid test and continues with other values.

### Property (_a+b> a_) is true
> <pre style="margin-bottom: 0px">
> <code>for any integer a and b that are between 1 and 20
<b>the sum of a and b will be greater than a</b></code></pre>

This check is to be executed every time.

## From theory to practice
Ok and how does this apply to my use case? I review my tests, defined in [GetDayStatusSummaryForWorkerAndDayTests.java](https://github.com/jaguado-arima/time-report-pbt/blob/feature/01_tests_jqwik_property_test/src/test/java/eu/arima/tr/reports/ reportsServiceImpl/GetDayStatusSummaryForWorkerAndDayTests.java){:target="_blank"} and I think about whether any of them could be written based on method properties regardless of the "exact" values ​​of the parameters.
I realize that I have two tests that are actually written in these terms:
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
In both I am doing tests based on concrete examples, but actually if we read what is intended to be tested, it is much more generic: perhaps we could apply PBT here?

For Java there are several tools, the most popular are:
* [junit-quickcheck](https://pholser.github.io/junit-quickcheck/site/0.9.1/#){:target="_blank"}
* [jqwik](https://jqwik.net/){:target="_blank"}

It seems that the first one doesn’t support JUnit 5, so we’re going to try it with **jqwik**.

We add the dependency in the pom.xml
```xml
<dependency>
  <groupId>net.jqwik</groupId>
  <artifactId>jqwik</artifactId>
  <version>1.3.1</version>
  <scope>test</scope>
</dependency>
```
And then we reformulate our tests to PBT "format":
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
Voila! Our test runs 1,000 times with a different set of input parameters each time (it's as if we had generated and run 1,000 different tests). If we show both parameters on the console, we will see the 1000 combinations that are executed. The default number of executions varies depending on the selected tool and is normally configurable. If we run it a second time, it will run 1000 times with a different set of parameters.

Note: This full example is available at [Github](https://github.com/jaguado-arima/time-report-pbt/tree/feature/01_tests_jqwik_property_test){:target="_blank"}. To personalize/configure different parameters, consult the [jqwik documentation](https://jqwik.net/){:target="_blank"}.

## In summary
So far a very simple case has helped us understand the concept of _property-based testing_. Reading the documentation and reviewing the state of the art, it seems that in more complex cases, doing PBT is more complicated: both when formulating/identifying the tests and when implementing them.

It is clear that like many other testing tools/trends, there is nothing black or white. There is no one type of test better than another, at least not absolutely: it depends on the context (functionality/project...) to which it applies.

Based on this and the research, the ideas I would stay with are:
* With _property-based testing_, we can replace several example-based tests with only one, testing the method with multiple combinations of inputs (which will vary with each execution). It is more difficult to identify them given their generic nature.

* With _example-based testing_ the combinations will be ones chosen by the developer (fixed in all executions) and the tests will be very specific. They are easy to develop and understand. They are not that exhaustive.

At first glance it occurs to me: and why not use `@ParameterizedTests` with a method that generates the parameters randomly? What does PBT offer that you cannot achieve with parameterized tests?

Basically, it offers us the possibility of having not only values ​​for random inputs, but also different combinations between them (something that we would otherwise have to implement in some other way).

For example, in [Github](https://github.com/jaguado-arima/time-report-pbt/tree/feature/02_tests_jqwik_combinedValues){:target="_blank"} we have added a `System.out.println` for the parameters of the previous test and we have also created a class `JqwikPropertiesTests.java` whose sole objective is to look at the combinations:
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
This code generates an output of combinations, such as:
<table>
<tr>
<th>Combination of parameters generated for the first example</th>
<th>Combination of parameters generated for the second example</th>
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


In addition to combinations, it offers us different tools for generating those parameters and configurations for more complex cases.

The price: change the focus of the tests, learn a new framework for their implementation, plus the execution time.

My feeling is that these tests end up being much more complex if you want to get the most out of them, and although I see their benefits, what I’m not sure of is whether there are any real projects that use this type of testing. Is it used intensively throughout or only in some of the functionalities that do not require extra configuration/customization? What should the characteristics of my project be to invest in this type of testing rather than example-based testing?

---
---

<br/>
Below I’ve added some references that I’ve used and that have helped me understand the concept of _property-based testing_
* [Introduction to Property Based Testing](https://medium.com/criteo-labs/introduction-to-property-based-testing-f5236229d237) - _por Nicolas Dubien_
* [Property-based testing](https://www.erikschierboom.com/2016/02/22/property-based-testing/) - _por Erik Schierboom_
* [Property based testing](https://felginep.github.io/2019-03-20/property-based-testing) - _por Pierre Felgines_ 
* [Improve your software quality with Property-Based Testing](https://medium.com/@yoan.thirion/improve-your-software-quality-with-property-based-testing-70bd5ad9a09a) - _por Yoan Thirion_
* [Property-based Testing Patterns](https://blog.ssanj.net/posts/2016-06-26-property-based-testing-patterns.html) - _Sanjiv Sahayam_