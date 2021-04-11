---
layout: post
title:  "Java Docker edukiontzietan exekutatzea bideragarria al da?"
date:   2020-02-11 9:00:00
author: telle
lang: eu
categories: docker, containers, java
tags: docker, containers, java, contenedores
header-image: 2020-02-11-java-en-contenedores-docker/fondo-cafe-min.jpg
---

Gure inguruan enpresa asko daude Java erabili izan dutenak beraien aplikazioak garatzeko. Horretarako Spring, Tomcat, Weblogic eta JPA bezelako tresnak erabili ohi dira. Azpiegitura hau nahiko egonkorra izan da beti eta aldaketa gutxi jasan ditu. 

Azkenaldian, Kubernetes-en oinarrituta dauden "cloud" infraestuktura berriak plazaratu dira ([Azure](https://azure.microsoft.com/en-us/free/kubernetes-service/){:target="_blank"}, [Openshift](https://www.redhat.com/es/technologies/cloud-computing/openshift){:target="_blank"}, [Amazon EKS](https://aws.amazon.com/es/eks/){:target="_blank"}, etab.). Enpresa asko Kubernetes ebaluatzen hasten direnean zalantza ugari izaten dituzte, adibidez, orain arte erabilitako teknologiak "cloud"-era joateko egokiak al dira?

Beti gertatzen den bezala, zalantzak argitzeko egiten dugun lehenengo gauza Google-i galdetzea da eta emaitzak aztertuz gero, bildurra ematen duten artikuluak aurkitu ditzakegu. Adibidez, [Nobody puts Java in a container](https://jaxenter.com/nobody-puts-java-container-139373.html){:target="_blank"} edo [Nobody puts Java in the container](https://vimeo.com/181900266){:target="_blank"}.

![Nobody puts java in containers](/assets/images/2020-02-11-java-en-contenedores-docker/no-body-puts-java-in-a-container.png)

Hau ikusita, hurrengo galdera egiten diogu gure buruari: Java docker edukiontzitan exekutatzea bideragarria da?

## Java Ergonomics

Java plataforma, 1995 urtean sortu zen eta hortik gutxira, web zerbitzariak eta aplikazioen zerbitzariak zabaldu ziren web aplikazioak Java lengoaian garatu ahal izateko. Garai horretan, oraindik ez zen [edukiontzien](https://www.docker.com/resources/what-container){:target="_blank"} kontzeptua existitzen ezta ["Cloud Native"](https://www.cncf.io/){:target="_blank"} mugimendua ere. Normalean Java web aplikazioak (war-ak edo ear-ak), zerbitzari batean exekutatzen ziren beste hainbat aplikazioekin batera.

<p align="center">
    <img src="/assets/images/2020-02-11-java-en-contenedores-docker/servidor-java-ee.png">
</p>

Java mota horretako azpiegituratan exekutatzeko diseinatua izan zen, hau da, JVM bakarra duen zerbitzari bat. Hori kontutan hartuta, JVM-ak [Java Ergonomics](https://docs.oracle.com/javase/8/docs/technotes/guides/vm/gctuning/ergonomics.html){:target="_blank"} prozesua exekutatzen du. Java Ergonomics-aren lana, JVM-aren konfigurazio parametroak kalkulatzea da eta horretarako erabilgarri dauden hardwarearen errekurtsoak aintzat hartzen ditu. Adibidez, Java Ergonomics-ak, JVMaren heap-aren tamaina maximoa ezartzeko zerbitzariak guztira duen RAMaren laurden bat erabiltzen du. Hau da, zerbitzari batek 64GB RAM baditu, lehenetsitako heap-aren tamaina maximoaren balioa 16GBtakoa izango da.

JVM bakoitzeko zerbitzari bat erabiltzen badugu, aurreko planteamenduarekin ez dago inongo arazorik, baino, zer gertatzen da Java Ergonomics Docker edukiontzi batean exekutatzen denean?

## Lehenengo esperientziak Java eta Docker-ekin

Java aplikazio bat edukiontzi batean exekutatzen dugunean, Java Ergonomics prozesuak JVMaren parametroak edukiontziaren baliabideen arabera kalkulatzea interesatzen zaigu. Adibidez, edukiontzi bat 4GBekin exekutatzen badugu, Java Ergonomics-ak 1GBeko heap maximoa ezartzea esperoko genuke.

Tamalez, Java aplikazioak edukiontzitan exekutatzen hasi ginenean, gauzak horrela ez zirela ikusi genuen. Java Ergonomics-ak, heap maximoaren kalkulua zerbitzariaren baliabideen arabera egiten zuen, ez edukiontziaren baliabideen arabera. Hortaz, zerbitzariak 64GB RAM bazituen, heap-aren tamaina maximoa 16GBtan ezartzen zen eta ez guk espero genuen 1GBean. Hori dela eta, aplikazio bat eskalatzean (5 edukiontzitara adibidez), zerbitzariaren memoria agortu egiten zen edukiontzi guztien heap-aren baturak zerbitzariaren memoria gainditzen zuelako (16GB * 5 > 64GB).

Hau konpontzeko, Java Ergonomics-en flag batzuk erabili ohi genituen (-Xmx, -Xms, etab.). Hala ere, enpresa askok ez zuten guzti honen berri eta konturatu zirenerako, produkzioan zeuzkaten aplikazioetan memoria arazoak (OOMKilled erroreak) eta erorketak jasaten ari ziren. Arazo hauen eraginez, artikulu asko idatzi ziren Java aplikazioak edukiontzitan exekutatzeko zeuden arriskuak jakinarazteko helburuarekin.

## Java Container Aware

Oracle-k arazo hauei [erantzuna eman zien](https://blogs.oracle.com/java-platform-group/java-se-support-for-docker-cpu-and-memory-limits){:target="_blank"} eta Java 8u131 eta Java 9 bertsioetan aplikazioak edukiontziekin bateragarriak egin zituzten nahiz eta modu espermientalean eta zenbait gabeziekin izan. Java 8u191 eta Java 10 bertsioetan arazo guzti hauek konpondu egin ziren

Bertsio berri hauetatik aurrera, Java Ergonomics prozesuak JVMaren konfigurazioa kalkulatzeko, edukiontziaren baliabideak automatikoki aintzat hartzen ditu. Java bertsio ezberdinen arteko ezberdintasunak probatu nahi badituzue, Git biltegi [honetan](https://github.com/wearearima/docker-java-cpu-memory-limit){:target="_blank"} dagoen kodearekin frogak egin ditzakezue.

Aldaketa hauekin batera, JVMan edukiontzitara zuzendutako konfigurazio aukera berriak gehitu ziren: `InitialRAMPercentage`, `MaxRAMPercentage` y `MinRAMPercentage`. 

Aldaketa guzti hauei esker, **Java "Container Aware" dela esaten da Java 8u191 eta Java 10 bertsioetatik aurrera**.

## Ondorioak

Java 1995. urtean sortu zenean, inorrek ezin zuen aurreikusi Docker eta Kubernetes bezalako teknologiak sortuko zirela. Hori kontutan izanda, Java aplikazioak edukiontzitan exekutatzea bideragarria al da?

Erantzuna baiezkoa da, Java komunitatea teknologia berrietara moldatzen ari da. Lehenengo oztopoa Java Ergonomics-ekin erlazionatuta zegoen eta dagoeneko konponduta dago. Hala eta guztiz ere, badaude beste alor batzuk hobetzeko, adibidez, JVMak duen tamaina. Horren inguruan, gertutik jarraitu beharreko tresna eta framework ugari agertzen hasi dira ([Graal Native Image](https://www.graalvm.org/docs/reference-manual/native-image/){:target="_blank"}, [Micronaut](https://micronaut.io/){:target="_blank"}, [Quarkus](https://quarkus.io/){:target="_blank"}, etab.).
