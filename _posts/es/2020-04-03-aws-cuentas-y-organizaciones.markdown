---
layout: post
title:  "AWS: Cuentas y Organizaciones"
date:   2020-04-03 9:00:00
author: urko
lang: es
categories: AWS
tags: aws, organizacion, organizaciones, iam, scp, cuenta, cuentas
header-image: 2020-04-03-aws-cuentas-y-organizaciones/rice-fields.jpg
---
En esta entrada quiero hablar sobre las cuentas de [Amazon Web Services](https://aws.amazon.com/) y sobre la arquitectura que hay por detrás. La gestión de cuentas de AWS es un poco compleja y puede ralentizar el tiempo necesario para empezar a usar sus servicios (cada vez que pruebo algo nuevo tengo la intención de ir directo al grano, como en este caso crear un cluster de [EKS](https://aws.amazon.com/eks/), y siempre me acabo dando de frente con la cruda realidad). Espero que al final de esta entrada seáis capaces de entender un poco mejor todos los conceptos que voy a explicaros y que agilice vuestro proceso de introducción en AWS.

Bien, lo primero de lo que hay que hablar es sobre las cuentas. ¿Qué es una cuenta de AWS? Pues no es más que eso, una cuenta, con su identificador único y su email, pero en este caso engloba ciertos conceptos propios de AWS. Cuando creas una cuenta, se crea por defecto un **usuario** root de la cuenta. Estos son los elementos que puede contener una cuenta:

* **Usuario**: Se refiere a cada persona individual que vaya a utilizar los servicios de la cuenta (recomiendan tener uno por cada persona, y no hacer un usuario *developer* o *admin*).
* **Grupo**: Un grupo es un conjunto de usuarios.
* **Rol**: Agrupación de políticas que se pueden asignar a usuarios, grupos o servicios.
* **Política**: Las políticas son agrupaciones de permisos que otorgan o deniegan acceso a diferentes acciones sobre los servicios (como ver las instancias de EC2 de la cuenta, crear nuevas, o borrarlas).
* **Servicio**: Un servicio es una funcionalidad de AWS a la que tenemos acceso, como la gestión de clústers de Kubernetes (EKS), repositorios de ficheros ([S3 buckets](https://aws.amazon.com/s3/)), ... Lo que quiero que quede claro, es que estos servicios son propios de la cuenta en la que estamos, es decir, **no se pueden compartir entre cuentas** (esto no es del todo cierto, se pueden otorgar permisos a otra cuenta para acceder a nuestros servicios, pero esto es rizar el rizo, y, por lo que entiendo, una mala utilización del sistema en la mayoría de los casos).

Esto que he explicado se puede gestionar desde el servicio [IAM](https://aws.amazon.com/iam/) (*Identity and Access Management*).

## Organizaciones

Todo esto probablemente sea todo lo que tenéis que entender para trabajar con AWS a nivel individual, pero cuando trabajas en una empresa las cosas se complican un poco. Para dar mayor poder de gestión, AWS tiene un servicio llamado *Organizations*. Una organización se puede entender como un conjunto de cuentas.

Cuando una cuenta crea una organización, esa cuenta pasa a ser la cuenta master de la organización y tiene acceso total. Aquí es donde se empieza a complicar un poco el asunto. Desde esta organización se pueden crear nuevas cuentas de la organización, que son prácticamente equivalentes a una cuenta creada de manera "normal", como la cuenta master. Hay ciertas restricciones para estas cuentas, como que no pueden crear nuevas organizaciones ni salir de la organización actual (aunque he escuchado que en un futuro próximo puede que sí), pero si se les otorgan los permisos necesarios, pueden llegar a tener tanto poder como la cuenta master. Por último, se puede invitar a nuestra organización a cuentas que no lo sean ya, y estas cuentas sí que pueden ir y venir sin restricción.

Otro concepto que introducen las organizaciones son los OU (*Organizational Unit*). Estos elementos son agrupaciones lógicas de cuentas y de OUs (un OU puede agrupar a cuentas y OUs, hasta 5 niveles de profundidad). Las diferentes cuentas de nuestra organización se pueden mover entre OUs sin problemas, pero hay que recordar que cada cuenta sigue teniendo sus usuarios, grupos, servicios, etc, y que estos **no se pueden sacar de la cuenta**. ¿Que por qué digo esto? Pues porque quiero introducir el último concepto importante sobre las organizaciones. Los [*Service Control Policies*](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scp.html).

Los *Service Control Policies* o SCPs son políticas que se utilizan para gestionar nuestra organización. Son diferentes de las políticas de una cuenta pero asumamos de momento que son iguales. Estas políticas se pueden aplicar a la organización, a un OU, o a una cuenta (o a conjuntos de estos elementos), y cuando se aplica a uno de estos elementos **también se aplican a todos los elementos que contengan**. Es decir, si aplicamos un SCP a un OU *ou1*, y *ou1* contiene un cuenta *c1*, el SCP se aplicará tanto a *ou1* como a *c1*. Si después movemos esta cuenta *c1* a otro OU *ou2*, *ou1* seguirá con el SCP aplicado, pero *c1* ya no. Es decir, si movemos cuentas a nivel jerárquico, tenemos que tener cuidado con los SCPs que haya aplicados tanto en el origen como en el destino.

Hay varias estrategias para estructurar nuestra organización, aquí os dejo algunas que he visto:

* Por entorno de trabajo (*development, testing, production*).
* Por cliente o departamento (Y dentro de cada una de ellos podríamos volver a organizarlo por entorno de trabajo, por ejemplo).
* Por cada entidad a la que tengamos que cobrar (se puede ver el uso de recursos de cada OU).

<p align="center">
    <img src="/assets/images/2020-04-03-aws-cuentas-y-organizaciones/OrganizationHierarchy.png"/>
</p>

<a href="https://es.slideshare.net/AmazonWebServices/wrangling-multiple-aws-accounts-with-aws-organizations-79796025" target="_blank" style="text-align: center; display: block;">Fuente de la imagen</a>

## SCPs vs Políticas de IAM

De momento, hemos hablado los SCPs de las organizaciones y de las políticas del IAM como si fuesen lo mismo, pero no lo son. Siguen siendo conjuntos de permisos, de hecho, muchos de los permisos que se utilizan son los mismos en ambos casos, pero **la diferencia está en el propósito** que tienen.

Mientras que una política de IAM sirve para otorgar permisos (a un usuario, grupo, servicio, ...) para acceder y utilizar un servicio, un SCP pretende otorgarle a una cuenta la habilidad de dar esos permisos. Es decir, para que dentro de una cuenta se use cierto permiso en concreto, un SCP deberá haber habilitado a esa cuenta ese permiso (o no habérselo denegado, según se utilicen estrategias de *whitelist* o *blacklist*).

Esto implica que los permisos resultantes que se le aplican a un usuario, por ejemplo, son **la intersección entre políticas y SCPs**. Un ejemplo práctico de esto sería el siguiente:

1. La cuenta *c1* tiene asignado un SCP que le permite otorgar permisos para listar cubos de S3 y para crear nuevos cubos.
2. Se le aplica a un usuario *u1* de la cuenta *a1* una política de IAM que le permite listar los cubos de S3 y borrarlos.
3. Como la cuenta *a1* no tiene permisos para otorgar el permiso de borrar cubos de S3, a *u1* solo se le aplica el permiso de listar cubos.

<p align="center">
    <img src="/assets/images/2020-04-03-aws-cuentas-y-organizaciones/SCPvsIAM.png">
</p>

## Conclusión

Como habréis podido ver, el servicio para gestionar una organización en AWS es una herramienta potente para poder agrupar cuentas y administrarlas desde una sola, pero tiene cierta complejidad.

Después de todo lo que he dicho, la recomendación que yo os hago es: Piensa antes de actuar:
* ¿Que eres un único usuario y quieres utilizar ciertos servicios de manera individual?, pues olvidate de *Organizations* y empieza a trabajar directamente.
* ¿Que tienes que gestionar una pequeña empresa con diferentes proyectos, departamentos o clientes?, párate a plantearte tu escenario y gestiona las diversas cuentas que necesites con la jerarquía adecuada.
* ¿Que eres una gran organización y tienes que administrar una compleja estructura de cuentas con miles de usuarios?, probablemente deberías contactar con Amazon y pedir la ayuda de uno de sus arquitectos. 

El objetivo de *Organizations* es ayudarte y debería acabar evitándote más problemas de los que te ha causado en un primer momento. 
