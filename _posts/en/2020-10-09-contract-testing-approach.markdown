---
layout: post
title:  "Contract Testing strategy: Producer driven or Consumer driven"
date:   2020-10-09 8:00:00
author: jessica
lang: en
categories: testing, software quality, QA
tags: testing, calidad, software quality, QA, contract testing, consumer-driven contract, consumer driven contract, pact, spring cloud contract
header-image: 2020-10-09-contract-testing/header_recortado.jpg
---

In a [previous post](https://blog.arima.eu/en/2020/09/03/contract-testing.html){:target="_blank"} we saw how new needs arise in the field of testing derived from the evolution of application architectures. We talked about how over the years we have gone from developing applications based on a monolithic architecture to applications based on (micro) services. Where before we had centralized tests in a single application, we now have them divided between several, so we have to ensure that each of them is tested independently and securely.

We presented a simple example of an application, which helped us to establish some concepts (such as _consumer_, _producer_, _service_) and which allowed us to highlight a new need: as important as testing the functionalities in _consumer_ and _producer_ independently is, so it is to ensure that the interaction between the two is right. We can address this need by means of _end-to-end_ tests, but while these tests are already complex to implement/execute in monolithic applications, they are even more so in other types of applications. 

At this point an idea comes up: it could be enough to verify between _consumer_ and _producer_  that there is an agreement they both keep to. This is where we discover a new concept: **Contract Testing**.

And what is **Contract Testing**? In the Pact documentation we find the following [definition](https://docs.pact.io/#what-is-contract-testing){:target="_blank"}
> It is a technique that allows us to test the integration of several applications, verifying in each one of them that the messages sent or received (depending on their role _consumer/producer_) conform to an agreement that is documented in a contract.

We could explain this concept and translate it (at a practical level) through the following points:
- There will be a specific agreement defined to which both _consumer_ and _producer_ will have access.
- In the _consumer_, we will have tests where the requests will be made to a "stub" of the _producer_ which will comply with the defined agreement.
- In the _producer_, we will have tests where requests based on the defined agreement will be made.

Depending on the tool/framework that we take as a reference, the concept of "agreement between _consumer_ and _producer_" is called **pact** or **contract**, but they are just different names for the same concept: a specification of what the requests and responses should be like to consume the services offered by the _producer_.

Going back to the same example we used in the previous post, this idea could be represented as follows:

![Example of the scheme of an application with consumer-producer where the part in which the Contract Testing is focused is highlighted](/assets/images/2020-10-09-contract-testing/01_schema_app_simplificado_agreement.jpg){: .center }

Having presented the concept behind _Contract Testing_ in general terms, let's dig a little deeper by looking at the existing approaches and tools.

# Approaches
In the literature we mainly find the connection **_Contract Testing_** &rarr; **_Consumer Driven Contract Testing_**. This at first made it more difficult for me to understand the underlying concept. After reading several posts, documentation.... I came to the conclusion that the reason for this association starts from the idea that a _service_ from a _producer_ is meaningless if there is no application using it (_consumer_). Therefore, it seems logical that it is the _consumer_ who establishes which agreement must be complied with, while the _producer_ should be responsible for satisfying the requirements set by the _consumer_ (hence the tagline "Consumer Driven").

Okay, fine, but in the projects that I have been closely involved with, this has not exactly been the case. The scenario has been that of a _producer_ across several applications, unaware of its _consumers_ and to whom it offers certain services.

So, I couldn't quite make it fit together. I had to take a step back and see it in perspective to understand that, in reality, we could encounter two different situations, according to the project that we had in hand (different in form but the same in concept) and depending on who it is that defines the agreement, there might be two approaches:

- **_Consumer Driven_ Contract Testing**
- **_Producer Driven_ Contract Testing**

And why not? The name leaves no room for doubt: in one case the definition of the contract comes from the _consumer_ and in the other from the _producer_. The truth is that there was a moment when _Producer Driven Contract Testing_ seemed like it was my own invention (just look at the Google search for this term or provider-driven...), but I found a reference to the term (as we'll see a little later) which gave me the base to continue with my mental schema.

The basic concept, in both cases, is still the same. However, depending on the approach that best fits our project, we can choose one or the other. The same applies when choosing the tools: depending on our needs, we can choose between the various existing ones.

# Tools

Based on the example presented at the beginning (and knowing that it is a Spring Boot project managed with Maven), the most popular tools we have come across that we could use are:

- **Pact**

   This tool is strongly connected to _Consumer Driven Contract Testing_, basically because the pacts will always be in the _consumer_ part. In the [documentation](https://docs.pact.io/#consumer-driven-contracts){:target="_blank"} we can read:
  
   > Pact is a code-first consumer-driven contract testing tool, ....
   The contract is generated during the execution of the automated consumer tests
  
- **Spring Cloud Contract**

  Although in its [description](https://spring.io/projects/spring-cloud-contract){:target="_blank"} it says...
  > Spring Cloud Contract is an umbrella project holding solutions that help users in successfully implementing the Consumer Driven Contracts approach. Currently Spring Cloud Contract consists of the Spring Cloud Contract Verifier project.

  ...it can be used in both ways. In fact, in the documentation [Pact](https://docs.pact.io/getting_started/comparisons/#how-does-pact-differ-from-spring-cloud-contract){:target="_blank"} it indicates that Spring Cloud Contract originated from the provider-driven approach.
  > Pact has always been a consumer-driven contract testing framework whereas Spring Cloud Contract started as provider-driven.

  So it seems that I didn’t invent the term after all!

So far, this is the process I followed until I understood that behind **Contract Testing** there is not only one approach, there are also multiple tools. As always, choosing what suits us best will depend on the project we have in hand.
But this is all just a load of talk, right? And if, like me, to really learn/understand something, you need to put it into practice, don’t worry, as we’re not finished here: shortly I’m going to publish a brief example using **Spring Cloud Contract**.