---
layout: post
title:  "Testcontainers: containers for testing"
date:   2021-05-06 8:00:00
author: jessica
lang: en
categories: testing, software quality, QA
tags: testing, calidad, software quality, QA, testContainers, test integración
header-image: 2021-05-06-testcontainers/header.jpg
---

I've always been more of a fan of unit tests than integration tests, mainly for one reason: I don't need anything external to be able to run them. I don't need to have a database started, an external service to connect to or a Kafka running to be able to run the tests and therefore to be able to develop.
That’s in the development environment, but if we’re talking about the integration environment, then I won't even start.
For example, in the case of databases we have the option of doing the tests with H2. But it is also true that depending on the type of project, it could be that something which works perfectly in H2 does not work in the database for which we are developing:
As sure as we have often relied on
> “Let’s go ... with h2, so as not to start the db ..."

so is the situation 
> “But it has been tested! Then why ...? Oops ... " 

I have always been one of those who needed to have everything installed: Mysql, Postgres, Kafka, .... everything that was necessary to execute the project. So, depending on the project, I had to make sure I had everything installed and some services or others called up ... until through my colleagues, I discovered containers. Well, Docker.
I have never been very good with these things, but the truth is that thanks to them, I don't need to have millions of things installed: I have the images of the services I need and I only have to start the ones I need, and that's all.
OK up to a point. It’s true that now to run the applications I have everything much more organized, but to actually develop, I’m still in pretty much the same situation: if I want to run integration tests, I have to remember to build the database (for example), so it ends up not being as transparent as H2.  

<small>As some may have already been thinking, all this makes sense in CI too, but I am going to focus on the day-to-day of the developer and how this tool helps us in our everyday work.<small>

> "There must be something that unites both worlds and makes the tests self-sufficient by simulating a real environment"

With this idea in mind and after a conversation with a colleague, I discovered that it was so: there was something called [**TestContainers**](https://www.testcontainers.org/){:target="_blank"}!
 
For example, let's imagine some situations in the day that make us sigh (or rather huff): a new member on the team! Or if we want to ask a colleague for help with a use case or a bug? Or if we go back to a project that we haven't worked on for months?
In situations like these (and others) how many times have we thought: wouldn't it be possible to download everything and be able to run the tests and start developing without doing absolutely anything else?
Some time ago, while watching a presentation from [@kiview](https://twitter.com/kiview){:target="_blank"}, I realized that I was not alone. At the beginning of his presentation he said something like:
> ... a successful onboarding experience in a project would be that the developer only had to clone the repository, do the build and with that we would already have the build done including unit and integration tests ... 

In other words, to follow these steps:

```
> git clone https://github.com/wearearima/school-library-testcontainers-01.git
> cd school-library-testcontainers-01
> ./mvnw install
```

That’s it!
My eyes were popping 😍. The talk was titled [Integration Testing with Docker and Testcontainers](https://www.youtube.com/watch?v=Lv1evJe2MRI){:target="_blank”}, exactly: **TestContainers**. So, good news! It seems that working with **TestContainers** makes it easier for us to get closer to that goal and simplifies our work so that we can focus on the development itself (implicitly, on the tests). 

# Database container example (Postgres Module)
Told this way, everything sounds very good, but (as those who read me from time to time will know well) to understand the concepts, I have to put them into practice, so we have prepared an example in [Github](https://github.com/wearearima/school-library-testcontainers-01){:target="_blank"}.
The most common is probably the situation in which we do tests against databases and Testcontainers offer us different _modules_ for different databases. Therefore, we have prepared a simple example of a Spring Boot application that connects to a Postgres database.  
Our example:  
    _Let’s take the case of a school library. We have a functionality that will serve to register the book copies that we receive. One of the methods that we could use, would be to "add a copy of a book" (understanding "book" as the concept and "copy" the representation of each printed copy that we have)._  
<small>In the future we will continue to develop this example and add code.</small> 

As we have said, we will use the module that exists for [Postgres](https://www.testcontainers.org/modules/databases/postgres/){:target="_blank"}. The implementation of the tests is very simple using this container. Let's go!

## Install Docker
The first thing we need to do is to install [Docker Desktop](https://www.docker.com/products/docker-desktop){:target="_blank"} (in case we don’t have it). This is the documentation section where we can find the Docker requirements: [General Docker requirements](https://www.testcontainers.org/supported_docker_environment/){:target="_blank"}.

## Add the necessary dependencies
To start with the code, the first thing we will have to do is add the necessary dependencies to the project (in our case in the pom.xml).

In our case we have generated the project using [Spring Initializr](https://start.spring.io/){:target="_blank"}, from where we have added the dependency 

![Imagen de cómo se añade la depedencia de testscontainer utilizando springinitializr](/assets/images/2021-05-06-testcontainers/spring-initializr.png){: .center }

If doing it manually, in the [documentation](https://www.testcontainers.org/quickstart/junit_5_quickstart/#1-add-testcontainers-as-a-test-scoped-dependency){:target="_blank"} it details how to add the dependencies.

Also, since we are going to use the Postgres module, we add the dependency: 

#### pom.xml
```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>postgresql</artifactId>
    <scope>test</scope>
</dependency>
```

So, in the same way we would if we weren't using Testcontainers, we will include the Postgres dependency. 

#### pom.xml
```xml
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <scope>runtime</scope>
</dependency>
```

## Start coding!
And we’re ready! We can now implement our use case. We are going to implement more than one test (available in [Github](https://github.com/wearearima/school-library-testcontainers-01/blob/master/src/test/java/eu/arima/schoolLibrary/bookStore/BooksServiceTest.java){:target="_blank"}. ), and here we will see the code for one of them. It’s a test that we will do to verify that when we add a copy to a book whose ISBN already exists, the copy will be added to the same one. Simple right?
 
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

But if we run the test without doing anything else, we will see that it fails due to not being able to raise the context: it is missing the information from the database.
It is true that we could go to `application.properties` and set the values ​​there ... but that would require any new developer (or you who is going to download the example) to raise the database etc. It would no longer be the "ideal" we are looking for. The solution?

### @Testcontainers
Effectively an annotation `@Testcontainers` and a few more lines and we have it:

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
So what have we done?
- We have added the annotation `@Testcontainers` to the test class.
- We have created a container instance with Postgres using the `@Container` annotation and specifying the version.
- And finally we have set the datasource information from the container created by `@ DynamicPropertySource`.

As you can see, the implementation is very simple and the benefit is instantaneous: you can download the example and run it directly on your equipment with nothing more than having installed Docker (do you remember the 3 commands from before? You can try it.) 

### Singleton pattern
There is another way to implement all this more efficiently, by using the singleton pattern. In this way we would use the same container in more than one class.
In fact, the documentation recommends this approach. In this example where we only have one test class, it doesn't seem useful, but it probably won't be the only functionality of our project, right? When that moment arrives, then yes, we would move to the singleton pattern, as explained [here](https://www.testcontainers.org/test_framework_integration/manual_lifecycle_control/#singleton-containers){:target="_blank"}.

Let's see how it would work: 

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

## Tip relating to Pitest
[PIT](https://pitest.org/){:target="_blank"}? What do **Testcontainers** have to do with **PIT**? Let's remember that we discovered that we could [measure the quality of our tests with PIT](https://blog.arima.eu/es/2020/05/25/mutation-testing.html){:target="_blank"}. It is true that PIT is directly oriented to **unit tests** (mainly due to time/efficiency), but it is also true that until now we had not encountered any problem when testing our **integration tests**. 

However, if you try to run Pitest on tests implemented using `@Testcontainers` you will find that they fail. On the other hand, if the tests are implemented using the singleton pattern, you will be able to perform the Pit coverage analysis without problems.

_If anyone wants to know the reason for all this, in addition to testing a solution proposed by a contributor, they can do so in the [issue](https://github.com/hcoles/pitest/issues/827){:target="_blank"} that we opened when detecting the problem._

So for now, a short introduction to **Testcontainers**, with an application example in the case of a database. As we have mentioned before, Testcontainers offer us many other modules. And even if for our requirements we need something more specific, they also dispose of support for us to have our own `docker-compose.yml` as explained in the [documentation](https://www.testcontainers.org/modules/docker_compose/). 
 
In future posts, we will develop our application so that we can introduce some examples of other use cases in which to use Testcontainers (to see in a practical way their ease of use and their advantages). 


