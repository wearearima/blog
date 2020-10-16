---
layout: post
title:  "Lecciones aprendidas sobre Contract Testing"
date:   2020-10-09 8:00:00
author: jessica
lang: es
categories: testing, software quality, QA
tags: testing, calidad, software quality, QA, contract testing, consumer-driven contract testing, consumer driven contract testing, provider-driven contract testing, provider driven contract testing
header-image: 2020-10-20-contract-testing/header.jpg
---
A lo largo de varios posts, hemos ido viendo cómo a consecuencia de la evolución de las arquitecturas de las aplicaciones surgen nuevas necesidades en el ámbito del testing. Nos hemos centrado en una concreta: tan importante como testear las funcionalidades en _consumer_ y _producer_ de forma independiente lo es asegurar que [la interacción entre ambos es correcta](https://blog.arima.eu/es/2020/09/03/contract-testing.html){:target="_blank"}. Hemos visto que tenemos a nuestro alcance **Contract Testing**, con [diferentes enfoques y herramientas](https://blog.arima.eu/es/2020/10/09/contract-testing-approach.html){:target="_blank"} que nos permiten abordar esta necesidad en concreto. Además utilizando el enfoque **producer driven** y [**Spring Cloud Contract**](https://spring.io/projects/spring-cloud-contract){:target="_blank"} hemos [llevado a la práctica](//TODO){{:target="_blank"}} todo lo aprendido.

Estaba pensando en cómo terminar esta serie de posts, con una recopilación de lecciones aprendidas... Algo así como un minipost resumiendo todo lo que hemos visto hasta ahora en cuatro o cinco titulares.  
Haciendo este ejercicio de reflexión, he recordado que en mi proceso de aprendizaje hubo una lección que destacó frente al resto. Puede que haya gente para la que resulte obvia pero seguro que hay alguien por ahí que puede meterse en el mismo callejón que me metí yo en su momento... Así que, para ese "alguien" 😉 aquí mi granito de arena:
> Hacer Contract Testing **no** te exime de hacer Unit Testing o Integration Testing.

Vale, ya se que esto es lo que pone en todos los sitios, que no estoy diciendo nada nuevo.... pero bueno, yo estuve tentada de hacerlo... quizás tú que me lees también.... y ya sabéis mi mantra: _materializar para entender_ 😊.  
Vamos a partir del ejemplo en el que hemos utilizado Spring Cloud Contract. Ya sabemos de qué va y controlamos el ejemplo. Viendo los tests del _consumer_, podríamos pensar...

💡 Ey! Sería genial tener las casuísticas que necesito para mi lógica representadas en el stub así no me ahorraría el test unitario donde las tengo mockeadas

¡Qué buena idea!

🤔 Ya pero el _producer_ no tiene por qué conocer mis casuísticas y es quien ha creado el contrato.
  
Es verdad….. ¿cómo se me habrá ocurrido? 

💡 Wait! ¡Lo que necesito son consumer-driven contracts! 

Puedo crear los contratos desde el _consumer_ con la información que necesito y hacer que los contratos estén disponibles en el _producer_ mediante pull-request (por ejemplo). Como los tests del _producer_ son autogenerados no se va a enterar... ¡Perfecto!¡Manos a la obra!

Si echamos un vistazo a los tests del _consumer_ vemos que básicamente queremos probar tres situaciones: cuando la duración de los worklogs es de 8 horas, de más de 8 horas y de menos de 8 horas.

Generamos por tanto los nuevos contratos y los dejamos accesibles por el _producer_. A continuación mostramos un fragmento de cómo podría ser (el código completo está en [Github](//TODO){:target="_blank"}).

#### worklogsForWorkerAndDay.yaml
```yml
//TODO
```

En él hemos generado las 3 situaciones que queríamos. Es hora de generar el stub en el _producer_. Hacemos `./mvnw clean install` y vemos que aunque hemos cambiado el contrato con Spring Cloud Contract se autogeneran los tests, así que todo va según lo previsto y no tenemos que tocar nada del _producer_.

Como ya tenemos accesible el stub con las casuísticas generadas, en el _consumer_ podríamos borrar nuestros tests unitarios e implementarlos haciendo llamadas al stub directamente. El código quedaría

```Java
//TODO
```
¡Genial! Todo queda mucho más limpio ¿¡Cómo no se me habrá ocurrido antes!?

Pero ¿qué sucedería si modificamos la lógica de nuestro consumer? 
Por ejemplo, supongamos que contemplamos la casuística del verano, cuando en lugar de jornadas de 8 horas tenemos jornadas de 7 horas, o sin más, que hemos decidido tener jornadas de 7 horas de ahora en adelante. Para introducir este cambio, como mínimo tendríamos que: 
1. Modificar el contrato y añadir más casuísticas para que en función de los parámetros de entrada nos devuelva otros datos
1. Hacer llegar al producer el contrato (por ejemplo pull-request)
1. Regenerar elementos del producer como los tests y el stub (`./mvnw clean install`)
1. Modiicar los tests en el consumer para añadir las nuevas casuísticas

Estamos modificando el contrato cuando en realidad no ha habido cambios en el “acuerdo” consumer-producer.Estamos utilizando las bondades de Spring Cloud Contract como un método de generación de datos “mock” para nuestra lógica de negocio... Algo no suena bien. Si no hubiésemos hecho el cambio, únicamente tendríamos que hacer el paso 4. Parece que no ha sido tan buena idea ¿no?
¿Poder se puede? Sí. Sin embargo, un gran poder conlleva una gran responsabilidad... y **que se pueda no quiere decir que se deba**. 

Con esto llegamos a la conclusión que hemos destacado al principio: Contract testing no sustituye ni a los tests unitarios, ni a los de integración, ni otros tests que podamos tener en nuestros proyectos. Contract testing es una herramienta más, un complemento a los anteriores cuyo objetivo NO ES verificar/asegurar el buen funcionamiento de la lógica de negocio (ni de consumidores ni de proveedores) para eso están los test unitarios o de integración de cada uno de ellos. Su objetivo ES asegurar que existen acuerdos entre consumer y producer para  por los acuerdos que hacen que la interacción entre consumer y producer sea correcta.
 
La verdad es que somos propensos a descubrir una herramienta y si nos gusta y nos encaja utilizarla de forma indiscriminada. Como hemos visto, cuando estamos aplicándolos podría parecernos que podríamos llegar a prescindir de nuestros test unitarios, pero si seguimos indagando, vemos que ese que nos parecía el descubrimiento del día no es tan buena idea, todo lo contrario.

# Lecciones aprendidas
Bueno pues ya llega el momento del resumen. Vamos a ver qué hemos aprendido a lo largo de estos posts.

- Tenemos una herramienta más que nos sirve para el testeo de aplicaciones de (micro)servicios y que no aplica en aplicaciones monolíticas.

- Como con el resto de tipos/técnicas de tests, hay que buscar el equilibrio y tener claro el objetivo de los mismos, en este caso: testear el acuerdo (contrato o pacto) entre consumer y producer (ni más ni menos) y no utilizarlos de forma indiscriminada.

- En proyectos donde el producer sea transversal a varios consumers (cuyo desarrollo no esté acoplado entre sí)  y/o público parece más apropiada la aproximación o el enfoque producer driven, donde es el producer quien define cómo será el acuerdo a cumplir en la comunicación.

- En proyectos donde el producer no tiene razón de ser sin el consumer, y cuyo desarrollos está acoplados, parece más apropiado el enfoque de consumer driven, donde será el (o los) consumer(s) quienes indicarán al producer sus necesidades estableciendo el acuerdo a cumplir en la comunicación

- Cómo implementar/organizar el testing dependerá del enfoque seleccionado y de la naturaleza del proyecto: no existe una receta única y universal para hacer buen testing.
