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

Azken aldian  *serverless* hitza gero eta gehiago agertzen da post, foro edo softwarearekin erlazionatutako edozein baliabidetan. Laburbilduz, gure aplikazioa exekutatzen den makinaz ez arduratzea eta horren **hedapen prozesua** arintzea inplikatzen duen kontzeptua da *serverless*. Ez da ulertzeko kontzeptu oso erraza, eta horregatik aurrerago beste post batean sakonduko dugu.

Post honetan AWS Lambdari buruz hitz egin nahi dut, AWSek funtzio moduan (FaaS) eskaintzen digun *serverless* soluzioaz. Funtzio bat **gertaera** baten bidez aktibatzen den eta eginkizun jakin bat duen edozein aplikazio gisa uler daiteke.

AWS Lambda ondorengoaz arduratzen da:
* **Gertaera** gertatzen denean soilik abiarazteaz gure aplikazioa, eta exekuzioa amaitzerakoan berehala hiltzeaz. Exekuzioaz arduratuko den makina hornitzeaz era arduratzen da, dena denbora errekorrean eginez. Aurrerago ikusiko dugu adibideren bat.
* Funtzioa exekutatzen egon den denbora soilik kobratzeaz. Honen ondorioz, kostuak txikitu eta baliabideen erabilera optimizatzen da.
* Behar izanez gero, aplikazioaren instantzia gehiago modu konkurrentean abiarazteaz. Honi esker, gure funtzioa trafiko-tontorrera egokitzea lortuko dugu, erabiltzen ditugun baliabideak soilik ordainduz. Agur esan lan egiten ez duten makinei eta baliabiderik gabe geratzeari!

### Nola funtzionatzen du

Esan dugun bezala, funtzioa **gertaera** bat jazotzen denean abiarazten da. Lambdaren kasuan, **gertaera** bat ondorengo arrazoiengatik gertatu daiteke:
* AWSeko baliabide batetik sortzea.
* AWSekoa ez den baliabide batetik sortzea, adibidez, Kafka errenkada bat.
* HTTP eskaera bat egitea.
* Beste batzuk.

![Lambda funtzio baten adibidea](/assets/images/2021-04-30-aws-lambda/lambda_example.png){: .center }
<label style="text-align: center; display: block;">Lambda funtzio baten adibidea ([iturria](https://aws.amazon.com/lambda/){:target="_blank"})</label>

Gure aplikazioak AWS sistematik iristen den **gertaera** tratatu ahal izateko, lehenik eta behin, Amazonek ematen duen SDKa erabili behar da (edo Lambdarekin bateragarria den liburutegi bat, [Spring Cloud Function](https://spring.io/projects/spring-cloud-function){:target="_blank"} bezala) gertaeraz arduratuko den *handler* bat inplementatzeko.

Post honetan AWSren SDKrekin eginiko Spring Boot aplikazio bat erabiliko dut. Aplikazio honen kodea [biltegi honetan](https://github.com/wearearima/serverlessDemoAWSHandler){:target="_blank"} ikus daiteke. **Biltegiak** funtzioa sortzeko jarraibideak ere baditu.

Lambdak funtzioa modu zehatz batean konfiguratzeko aukera ematen digu, ondorengo konfigurazio hauek ditugularik: erabili nahi dugun instantzia bakoitzaren memoria kantitatea, exekuzioaren denbora maximoa, gure aplikaziorako ingurune-aldagaiak definitzea (adibidez, JVMaren propietateak konfiguratu daitezke honen bidez), etab.

Behin hau eginda, funtzioa erabiltzeko prest dago. Aipatzekoa da ez dugulu makinaren sistema eragilerik aukeratu beharrik izan, ezta aplikazioak exekutatu ahal izateko Java konfiguratu beharrik izan edo ezta sekurizatu beharrik izan ere. Ez dut makinaren egoerari buruz kezkatu beharrik izan, edo autoeskalatzeko sistemarik ezarri behar izan ere, beharrezkoa izango balitz. Honetaz guztiaz Lambda arduratzen da.

Hurrengo irudian, funtzioaren exekuzioaren emaitzak ikus ditzakegu. Ezkerrean, lehen exekuzioaren edo hasiera hotzaren emaitzak daude (*cold-startup*), eta eskuinean bigarren exekuzioaren edo hasiera beroaren emaitzak (*warm-startup*). Ikus dezakegu ezberdintasun handia dagoela exekuzio-denboran, eta ezberdintasuna are nabarmenagoa izango litzateke gure aplikazioa lehen aldiz hasteko denbora gehiago beharko balu (adibidez, datu-base batekin konexioen *pool* bat sortu beharko balu).

![Exekuzioen emaitzak (cold / warm)](/assets/images/2021-04-30-aws-lambda/results.png){: .center }
<label style="text-align: center; display: block;">Exekuzioen emaitzak (cold / warm)</label>

*Cold-startup*aren arazoa ohikoa da *serverless* kasuan, etengabe ari baikara instantzia berriak sortzen. Hurrengo post batean hori saihesteko moduak aztertuko ditugu. Oraingoz, Lambdak *provisioned concurrency* izeneko aukera eskaintzen duela aipatuko dut, eta honek aukera ematen digula aukeratzen ditugun instantzien kopurua aktibo mantentzeko (ordainduz gero, noski).


### Hausnarketak:

Zerbitzu honi buruz irakurtzean, kontuan hartzeko garrantzitsuak iruditzen zaizkidan muga tekniko batzuk aurkitu ditut.

1. Funtzioa paralelizagarria izan behar da. Eskaera bat prozesatzen ari den bitartean beste eskaera bat iristen bada, beste instantzia bat sortuko da. Horrek esan nahi du funtzioa aldi berean exekutatzeko konkurrentzia-arazorik ez dagoela ziurtatu beharko dugula. Adibide bat datu-base batean erregistro bat eguneratzen duen funtzio bat izan daiteke.
2. Funtzioari gehienez 10 GBko memoria esleitu ahal diogu. Gainera, esleitutako vCPUen kopurua aukeratutako memoriarekiko proportzionala da (gehienez 6 vCPU). Honek, bi baliabideetako bat gainhornitzera behartu ahal gaitu, edo baita nahikoak ez izatera ere, ez baitira oso muga altuak.
3. Programazio-lengoai nagusi gehienentzako exekuzio-inguruneak eskaintzen ditu Amazonek. Hauetakoren batek ere ez badigu balio (gure lengoaia ez dagoelako horietakoen artean edo bertsio zehatz bat behar dugulako), ingurune pertsonalizatu bat konfiguratu daiteke, edo bestela, irudi bat erabili daiteke kontenedore bat abiarazteko (honetaz beste post batean hitz egingo dugu).
4. Exekuzio bakoitzaren gehienezko denbora 15 minutu dira. Gure negoziorako nahikoa ez bada edo funtzioa denbora luzez exekutatzen ari bada (denbora fakturagarria), agian beste *serverless* mota bat aukeratu beharko genuke.
   
### Ondorioak

AWS Lambda zerbitzu ahaltsua da, oso ondo integratzen dena gainerako AWS ingurunearekin. *Serverless* munduan sartzen gaitu, bere abaintala guztiekin, eta aplikazio baten hedapena inoiz baino errazagoa eta merkeagoa egiten du.

Hala ere, ez da arazo guztien soluzioa. Beti bezala, kasu zehatz bakoitzak bere xehetasunak ditu, eta ikerketa bat egin beharko da Lambda egokitzen den edo irtenbide tradizionalago bat hobe den ikusteko kasu bakoitzean. Lambda oso garestia izan daiteke eskaera asko aldi berean eta etengabe egiten badira. Nolanahi ere, niri pertsonalki, begiak irekitzeko eta FaaS funtzioetan barneratzeko balio izan dit, eta iraganean hartutako erabaki batzuk birplantearazi dizkit.