---
layout: post
title:  "AWS Lambda Funtzioak"
date:   2021-04-30 9:00:00
author: urko
lang: eu
categories: aws, serverless, cloud
tags: aws, serverless, cloud, faas, java
header-image: 2021-04-30-aws-lambda/cloud.jpg
---

Duela gutxi, *serverless* hitza gero eta gehiago agertzen da postetan, foroetan edo softwarearekin lotutako edozein baliabidetan. Ez badakizu zer den, *serverless* gure aplikazioa exekutatzen den makinaz ez arduratzea eta haren **hedapena** hutsaltzea inplikatzen du. Kontzeptua ulertzea ez da hain erreza, beraz, aurrerago beste post batean sakonduko dugu.

Post honetan AWS Lambdaz hitz egin nahi dut, AWSek ematen digun *serverless* funtzio (FaaS) soluzioaz. Funtzio bat **gertaera** baten bidez aktibatzen den eta eginkizun jakin bat egiten duen edozein aplikazio bat bezala ikus daiteke.

AWS Lambda gauza hauetaz arduratzen da:
* Gure aplikazioa **gertakaria** **abiatzen** denean pizteaz, eta exekuzioa amaitu eta berehala hiltzeaz. Honek ere barne hartzen du gure aplikazioa exekutatzen den makina hornitzea, eta dena denbora errekorrean egiten du. Aurrerago ikusiko dugu adibideren bat.
* Funtzioaren exekuzioaren denboragatik soilik kobratzea. Honen ondoriak kostuak txikiaraztea eta baliabideen erabilera optimizatzea da.
* Behar izanez gero, aplikazio instantzia gehio aldi berean pizteaz. Horrela, gure funtzioa trafiko-tontorrera egokitzea lortuko dugu, eta erabiltzen ditugun baliabideak soilik ordainduko ditugu. Agur esan lan egiten ez duten makinei eta baliabiderik gabe geratzeari!

### Nola funtzionatzen du


Esan dugun bezala, funtzioa **gertakari** bat aiegatzen delako pizten da. Lambdaren kasuan, gertaera bat honako arrazoi hauengatik etor daiteke:
* AWSeko baliabide batetik sortu da.
* AWSekoa ez den baliabide batetik sortu da, Kafka errenkada bat adibidez.
* HTTP eskaera bat egin da.
* Beste batzuk.

![Lambda funtzio baten adibidea](/assets/images/2021-04-30-aws-lambda/lambda_example.png){: .center }
<label style="text-align: center; display: block;">Lambda funtzio baten adibidea ([iturria](https://aws.amazon.com/lambda/){:target="_blank"})</label>

Gure aplikazioak AWS sistematik iristen den gertaera tratatu ahal izateko, lehenik eta behin Amazonek ematen duen SDKa erabili behar da (edo Lambdarekin bateragarria den liburutegi bat, [Spring Cloud Function](https://spring.io/projects/spring-cloud-function){:target="_blank"} bezala) gertaeraz arduratuko den *handler* bat inplementatzeko.

Post honetan AWS SDKarekin eginiko Spring Boot aplikazio bat erabiliko dut. Aplikazio honen kodea ikus daiteke [gordailu honetan](https://github.com/wearearima/serverlessDemoAWSHandler){:target="_blank"}. **Gordailuak** funtzioa sortzeko jarraibideak ere baditu.

Lamdak funtzioa zehatzago konfiguratzeko aukera ematen digu, honako konfigurazio hauek aukeratu ahal izango ditugu: erabili nahi dugun instantzia bakoitzaren memoria, exekuzioaren gehieneko denbora, gure aplikaziorako ingurune-aldagaiak definitzea (hemendik, adibidez, JVMaren propietateak konfiguratu daitezke), etab.

Behin hau eginda, funtzioa erabiltzeko prest dago. Ez dugu makinaren sistema eragilea aukeratu behar, Java aplikazioak exekutatu ahal izateko konfiguratu behar, ezta sekurizatu ere. Ez naiz makinaren egoerari buruz kezkatu behar, ezta autoeskalatzeko sistemarik ezarri behar ere, beharrezkoa balitz. Lambda arduratzen da honetaz guztiaz.

Hurrengo irudian, funtzioaren exekuzioaren emaitzak ikusi ditzakegu. Ezkerrean lehen exekuzioaren edo hasiera hotzaren emaitzak erakusten dira (*cold-startup*), eta eskuinean bigarren exekuzioaren edo hasiera beroaren emaitzak (*warm-startup*). Ikusi dezakegu ezberdintasun handia dagoela exekuzio-denboran, eta are nabarmenagoa izango litzatekeela gure aplikazioa lehen aldiz hasteko denbora gehiago beharko balu (adibidez, datu-base batekin konexioen *pool* bat sortu beharko balu).

![Exekuzioen emaitzak (cold / warm)](/assets/images/2021-04-30-aws-lambda/results.png){: .center }
<label style="text-align: center; display: block;">Exekuzioen emaitzak (cold / warm)</label>

*Cold-startup*ren ohikoa da *serverless* ereduan, etengabe ari baikara instantzia berriak sortzen. Hurrengo post batean, hori saihesteko moduak aztertuko ditugu. Oraingoz, aipatuko dut Lambdak *provisioned concurrency* izeneko aukera eskaintzen duela, aukera ematen digula aukeratzen ditugun instantzien kopurua aktibo mantentzeko (ordainduz, noski).


### Hausnarketak:

Zerbitzu honi buruz irakurtzean, kontuan hartzeko garrantzitsuak iruditzen zaizkidan muga tekniko batzuk aurkitu ditut.

1. Funtzioak paralelizagarria izan behar du. Eskaera bat iristen bada beste eskaera bat prosesatzen dagoen bitartean, beste instantzia bat sortu egingo da. Horrek esan nahi du funtzioa aldi berean exekutatzean arazorik ez dagoela ziurtatu beharko dugula. Adibide bat datu-base baten erregistro bat eguneratzen duen funtzio bat izan liteke.
2. Funtzioari gehienez 10GB-ko memoria esleitu ahal diogu. Gainera, esleitutako vCPUen kopurua aukeratutako memoriarekiko proportzionala da (gehienez 6 vCPU). Honek, bi baliabideetako bat gainhornitzera behartu ahal gaitu, edo baita nahikoak ez izatea ere, ez baitira oso muga altuak.
3. Amazon nos deja elegir entre varios entornos de ejecución para la mayoría de lenguajes principales. Si estos no nos sirven (porque nuestro lenguaje no está o porque necesitamos una versión específica), es posible configurar uno personalizado o utilizar una imagen para que se lance un contenedor (hablaremos sobre esta opción en otro post).
4. Exekuzio bakoitzeko gehieneko denbora 15 minutu dira. Gure negoziorako nahikoa ez bada edo funtzioa denbora luzez exekutatzen ari bada (denbora fakturagarria), agian beste *serverless* mota bat aukeratu beharko genuke.
   
### Ondorioak

AWS Lambda zerbitzu ahaltsua da, eta oso ondo integratzen da gainerako AWS ingurunearekin. *Serverles* munduan, bere abaintala guztiekin, sartzen gaitu, eta aplikazio baten hedatzea inoiz baino errazagoa eta merkeagoa bihurtzen du.

Hala ere, ez da arazo guztien konponbidea. Beti bezala, kasu zehatz bakoitzak bere xehetasunak ditu eta ikerketa bat egin beharko da Lambda egokitzen den edo irtenbide tradizionalago bat hobe den ikusteko. Lambda oso garestia izan daiteke eskaera asko aldi berean eta etengabe egiten badira. Nolanahi ere, niri, pertsonalki, begiak irekitzeko eta FaaS funtzioetan barneratzeko balio izan dit, eta iraganean hartutako erabaki batzuk birplantearazi dizkit.