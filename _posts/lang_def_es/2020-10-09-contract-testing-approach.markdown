---
layout: post
title:  "Estrategia de Contract Testing: Producer driven o Consumer driven"
date:   2020-10-09 8:00:00
author: jessica
lang: es
categories: testing, software quality, QA
tags: testing, calidad, software quality, QA, contract testing, consumer-driven contract, consumer driven contract, pact, spring cloud contract
header-image: 2020-10-09-contract-testing/header_recortado.jpg
---
En un [post anterior](https://blog.arima.eu/es/2020/09/03/contract-testing.html){:target="_blank"} hemos visto cómo surgen nuevas necesidades en el ámbito del testing derivadas de la evolución de las arquitecturas de las aplicaciones. En él, hablamos de cómo con el paso de los años hemos pasado de desarrollar aplicaciones basadas en una arquitectura monolítica a aplicaciones basadas en (micro)servicios. Donde antes teníamos tests centralizados en una única aplicación, ahora pasamos a tenerlos divididos en varias, de forma que tendremos testeadas cada una de ellas de forma independiente y estanca.


Hemos presentado un ejemplo sencillo de una aplicación, que nos ha servido para establecer algunos conceptos (como _consumer_, _producer_, _servicio_) y que nos ha permitido poner en evidencia una nueva necesidad: tan importante como testear las funcionalidades en _consumer_ y _producer_ de forma independiente lo es asegurar que la interacción entre ambos es correcta. Esta necesidad podemos abordarla mediante test _end-to-end_, pero si bien estos tests ya resultan complejos de implementar/ejecutar en aplicaciones monolíticas en aquellas que no los son la complejidad es mayor. 

En este punto surge una idea: podría ser suficiente con verificar entre _consumer_ y _producer_  que existe un acuerdo que ambos cumplen. Aquí es donde descubrimos un nuevo concepto: **Contract Testing**.

Y ¿qué es **Contract Testing**? En la documentación de Pact encontramos la siguiente [definición](https://docs.pact.io/#what-is-contract-testing){:target="_blank"}
> Es una técnica que nos permite probar la integración de varias aplicaciones, verificando en cada una de ellas que los mensajes que envía o recibe (dependiendo de su rol _consumer/producer_) se ajustan a un acuerdo que está documentado en un contrato.

Este concepto podríamos desgranarlo y traducirlo (a nivel práctico) en los siguientes puntos:
- Existirá un acuerdo concreto definido al que tanto _consumer_ como _producer_ tendrán acceso.
- En el _consumer_, tendremos tests donde las peticiones se harán a un “stub” del _producer_ que cumplirá el acuerdo definido. 
- En el _producer_, tendremos tests donde se realizarán peticiones basadas en el acuerdo definido.

Dependiendo de la herramienta/framework que tomemos como referencia, el concepto de “acuerdo entre _consumer_ y _producer_” recibe el nombre de **pacto** o **contrato**. Pero no dejan de ser diferentes nombres para el mismo concepto: una especificación de cómo deben ser las llamadas y respuestas para consumir los servicios ofertados por el _producer_.

Volviendo al mismo ejemplo que hemos utilizado en el post anterior esta idea podríamos representarla como sigue: 

![Ejemplo del esquema de una aplicacion con consumer-producer donde se resalta la parte en la que se centra el Contract Testing](/assets/images/2020-10-09-contract-testing/01_schema_app_simplificado_agreement.jpg){: .center }

Una vez presentado el concepto detrás de _Contract Testing_ en términos generales, vamos a profundizar un poco más viendo los enfoques y herramientas existentes. 

# Enfoques
En la literatura principalmente encontramos la relación **_Contract Testing_** &rarr; **_Consumer Driven Contract Testing_**. Esto al principio hizo que me resultase más difícil comprender el concepto subyacente. Tras leer varios post, documentación.... llegué a la conclusión de que el motivo de esta asociación parte de la idea de que un _servicio_ de un _producer_ carece de sentido si no hay alguna aplicación utilizándolo (_consumer_). Por tanto, parece lógico que quien establezca qué acuerdo debe cumplirse sea el _consumer_, mientras que en el _producer_ debería recaer la responsabilidad de satisfacer las necesidades fijadas por _consumer_ (de ahí la coletilla de "Consumer Driven").

Vale, bien, pero en los proyectos que he conocido de cerca, la casuística no ha sido precisamente esa. El escenario ha sido el de un _producer_ transversal a varias aplicaciones, que no conoce a sus _consumers_, y a quienes les oferta unos servicios determinados.

Así que, no me terminaba de encajar. Tuve que dar un paso atrás y verlo en perspectiva para llegar a entender que, en realidad, podríamos encontrarnos con dos situaciones en función del proyecto que tuviésemos entre manos (diferentes en forma pero iguales en concepto) y así dependiendo de quién sea el que define el acuerdo podríamos tener dos enfoques:

- **_Consumer Driven_ Contract Testing**
- **_Producer Driven_ Contract Testing**

¿Por qué no? El nombre no deja lugar a dudas: en un caso la definición del contrato nace en el _consumer_ y en el otro del _producer_. La verdad es que hubo un momento en que _Producer Driven Contract Testing_ parecía que fuese invención mía (no hay más que ver la búsqueda en Google de este término o de provider-driven...), pero encontré una referencia a ese término (como veremos un poquito más adelante) lo cual me dió pie a continuar con mi esquema mental.

El concepto base, en ambos casos, no deja de ser el mismo. Sin embargo dependiendo del enfoque que encaje mejor con nuestro proyecto podremos decantarnos por uno u otro. Lo mismo sucede a la hora de elegir las herramientas para hacerlo: dependiendo de nuestras necesidades podremos elegir entra las diferentes herramientas existentes.

# Herramientas

Basándonos en el ejemplo presentado al inicio (y sabiendo que es un proyecto Spring Boot gestionado con Maven), las herramientas más populares que hemos encontrado que podríamos utilizar en nuestro proyecto son:

- **Pact**

  Esta herramienta está fuertemente acoplada con _Consumer Driven Contract Testing_, básicamente porque los pactos estarán siempre en la parte _consumer_. En la [documentación](https://docs.pact.io/#consumer-driven-contracts){:target="_blank"} podemos leer: 
  
  > Pact is a code-first consumer-driven contract testing tool, .... 
  The contract is generated during the execution of the automated consumer tests
  

- **Spring Cloud Contract**

  Aunque en su [descripción](https://spring.io/projects/spring-cloud-contract){:target="_blank"} dice:
  > Spring Cloud Contract is an umbrella project holding solutions that help users in successfully implementing the Consumer Driven Contracts approach. Currently Spring Cloud Contract consists of the Spring Cloud Contract Verifier project. 

  Puede utilizarse tanto en un sentido como en otro. De hecho, en la documentación [Pact](https://docs.pact.io/getting_started/comparisons/#how-does-pact-differ-from-spring-cloud-contract){:target="_blank"} indican que Spring Cloud Contract nació con el enfoque provider-driven.
  > Pact has always been a consumer-driven contract testing framework whereas Spring Cloud Contract started as provider-driven.

  ¡Parece que no me he inventado el término!, tampoco estaré tan desencaminada ¿no?  

 Hasta aquí el proceso que seguí hasta llegar a comprender que detrás **Contract Testing** hay más de un enfoque y múltiples herramientas. Como siempre, dependerá del proyecto que tengamos entre manos para elegir lo que más nos encaje.  
 Mucha chapa y poco código, ¿verdad? Yo soy de las que para aprender/entender realmente algo tengo que ponerlo en práctica.... así que si te pasa lo mismo que a mí, no te preocupes, aquí no terminamos: en breve publicaré un pequeño ejemplo utilizando **Spring Cloud Contract**.