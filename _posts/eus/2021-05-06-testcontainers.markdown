---
layout: post
title:  "Testcontainers: edukiontziak testing-aren zerbitzura"
date:   2021-05-06 8:00:00
author: jessica
lang: eu
categories: testing, software quality, QA
tags: testing, calidad, software quality, QA, testContainers, test integración
header-image: 2021-05-06-testcontainers/header.jpg
---
Integrazio testak baino gehiago gustoko izan ditut beti unitateko testak, batez ere arrazoi batengatik: ez dut kanpoko ezer behar pasa ahal izateko. Ez dut behar datu-base bat, kanpo-serbitzu bat edo Kafka bat martxan izatea testak pasatu ahal izateko eta horrez gero garatu ahal izateko.
Eta hori garapen-ingurunean, integrazio-ingurunean esan beharrik ez.
Adibidez, datu-baseen kasuan, testak H2-rekin egiteko aukera dugu. Baina egia da, halaber, proiektu motaren arabera, gerta daitekeela H2-n primeran funtzionatzen duen zerbait, garatzen ari garen datu-basean ez funtzionatzea.   
Askotan 
> “Tira... H2-rekin egingo dugu, datu basea martxan ez jartzeagatik...”  

pentsatu dugula bezain egia da egoera hau:
> “Baino... testatuta dago! Orduan zergatik...? Ups...”

Ni beti izan naiz dena instalatuta eduki behar nuen horietakoa: MySQL, Postgres, Kafka... Proiektua martxan jartzeko behar zen guztia. Horrela, proiektuaren arabera, ziurtatu behar nuen dena instalatuta eta zerbitzu batzuk edo beste batzuk altxatuta neuzkala. Hau bukatu zen nire lankideek edukiontziak aurkeztu zizkidatenean, bueno, Docker.
Inoiz ez naiz oso trebea izan gauza horiekin, baina, egia esan, horiei esker, ez dut milioika gauza instalatuta edukitzeko beharrik: behar ditudan zerbitzuen irudiak ditut, eta behar ditudanak martxan jarri besterik ez dut egin behar, eta kito.   
Goazen harira. Egia da orain aplikazioak martxan jartzeko dena askoz ere antolatuago daukadala, baina, egia esan, garatzeko, oraindik ere pixka bat bertan nago: integrazio-testak pasatu nahi baditut, datu-basea altxatzeaz gogoratu behar naiz (adibidez), beraz, ez da H2 bezain gardena.  

<small>Baten batek imajinatuko zuen bezala, horrek guztiak CI-n ere badu aplikazioa, baina garatzailearen egunerokotasunean eta tresna horrek eguneroko lanean nola laguntzen digun moduan jarriko dugu post honetan.</small>

> "Zerbait egon behar da bi munduak batzen dituena eta testak autosufizienteak izatea eragiten duena, benetako ingurunea simulatuz"

Ideia hori buruan nuela eta lankide batekin hitz egin ondoren, hala zela jakin nuen: ¡bada [**TestContainers**](https://www.testcontainers.org/){:target="_blank"} izeneko zerbait!

Adibidez, imajina ditzagun eguneko egoera batzuk, hasperen eginarazten digutenak (edo, hobeto esanda, arnasa harrarazten digutenak): kide berria taldean! edo laguntza eskatu nahi badiogu lankide bati erabilera kasu edo bug kasu batekin? edo hilabeteak daramatzagun proiektu batera itzultzen bagara?
Horrelako egoeren aurrean (eta beste batzuen aurrean), zenbat aldiz ez dugu pentsatu: ez litzateke posible izango dena deskargatzea, testak pasatzea eta garatzen hastea beste ezer egin gabe? 
Duela denbora bat, bakarrik ez negoela konturatu nintzen. [@kiview](https://twitter.com/kiview){:target="_blank"}-ren aurkezpen bat ikusten izan zen. Aurkezpenaren hasieran honelako zerbait esaten zuen:
> ...proiektu batean arrakasta izango lukeen onboarding-esperientzia izango litzateke garatzaileak repositorioa klonatzea eta builda jaurtitzea besterik ez behar izatea, eta horrekin build osoa edukitzea, unitateko eta integrazioko testak barne ...

Hau da, hurrengo pauso hauek jarraitzea:
```
> git clone https://github.com/wearearima/school-library-testcontainers-01.git
> cd school-library-testcontainers-01
> ./mvnw install
```
¡Eta listo!  
Begiek 😍 egin zidaten. Hitzaldiaren izenburua [Integration Testing with Docker and Testcontiners](https://www.youtube.com/watch?v=Lv1evJe2MRI){:target="_blank"} zen, hala da: **TestContainers**. Ba, berri onak! Badirudi **TestContainers**-ekin lan egiteak helburu horretara hurbiltzea errazten digula eta lana sinplifikatzen digula, garapen propioan zentratu ahal izateko (eta jakina, testetan ere).

# Adibidea: Database container (Postgres Module)
Horrela esanda, dena oso itxura ona du, baina (noizbehinka irakurtzen nauzuenok jakingo duzuenez) kontzeptuak ulertzeko praktikan jarri behar ditut, beraz adibide bat prestatu dugu [Github](https://github.com/wearearima/school-library-testcontainers-01){:target="_blank"}-en. 
Ohikoena, seguruenik, datu-baseen aurkako testak egiten ditugun egoera da, eta Testcontainers datu-base desberdinetarako _moduloak_ eskaintzen dizkigute. Horregatik, adibide sinple bat prestatu dugu, Postgres datu-base batera konektatzen den Spring Boot aplikazio batena.
Gure adibidea:  
   Demagun eskola bateko liburutegia. Jasotzen ditugun aleei alta ematen joateko balioko duen funtzionalitate bat dugu. Izan genezakeen metodoetako bat "liburu baten kopia gehitzea" izan zitekeen ("liburua" kontzeptua dela ulertuta, eta "kopia", berriz, izan dezakegun ale bakoitzaren irudikapena). 
<small>Etorkizunean ere adibide hau haunditzen eta kodea gehitzen joango gara.</small>


Esan bezela,[Postgres](https://www.testcontainers.org/modules/databases/postgres/){:target="_blank"}-rako dagoen modulua erabiliko dugu. Kontainer hau erabiliz testak egitea oso erraza da, goazen ba!

## Docker instalatu
Lehenik eta behin, [Docker Desktop](https://www.docker.com/products/docker-desktop){:target="_blank"} instalatu behar dugu (eduki ezean).
Lo primero que necesitamos es instalar [Docker Desktop](https://www.docker.com/products/docker-desktop){:target="_blank"} (en caso de no tenerlo). Ondoren, dokumentazioaren atala utziko dut, non Dockerren errekerimenduak aurki ditzakegun: [General Docker requirements](https://www.testcontainers.org/supported_docker_environment/){:target="_blank"}.


## Gehitu behar diren dependentziak
Kodearekin hasteko, lehenik eta behin, proiektuan beharrezkoak diren dependentziak gehitu beharko ditugu (gure kasuan, pom.xml-an).

Guk [Spring Initializr](https://start.spring.io/){:target="_blank"} erabiliz sortu dugu proiektua eta hortik gehitu dugu dependentzia

![Nola gehitu Testcontainers Spring Initializr erabiliz](/assets/images/2021-05-06-testcontainers/spring-initializr.png){: .center }

Eskuz eginez gero, [dokumentazioan](https://www.testcontainers.org/quickstart/junit_5_quickstart/#1-add-testcontainers-as-a-test-scoped-dependency){:target="_blank"} dependentziak nola gehitu zehazten da.

Gainera, Postgres modulua erabiliko dugunez, dependentzi hori ere gehituko dugu:

#### pom.xml
```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>postgresql</artifactId>
    <scope>test</scope>
</dependency>
```

Eta Testcontainers erabiltzen ari ez bagina egingo genukeen bezala, Postgresen dependentzia ere gehituko dugu.

#### pom.xml
```xml
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <scope>runtime</scope>
</dependency>
```

## Start coding!
¡Listo! Gure erabilera-kasua inplementatu dezakegu. Test bat baino gehiago egingo ditugu (hemen eskuragarri: [Github] (https://github.com/wearearima/school-library-testcontainers-01/blob/master/src/test/java/eu/arima/schoolLibrary/bookStore/BooksServiceTest.java) {: target = "_blank"}, hemen adibide gisa bakarra egingo dugu. Egingo duguna ISBN lehendik duen liburu bati kopia bat gehitzen diogunean, liburu horri kopia bat gehituko zaiola egiaztatuko dugu. Erraza ez da?

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
Baina testa besterik gabe pasatzen badugu, ikusiko dugu huts egiten duela kontextua altxatu ezin duelako: datu-baseko informazioa falta zaio.
Egia da application.properties fitxategian jarri ditzakegula baloreak... baina horrek eskatuko luke iritsi berri den garatzaile horrek (edo zuk adibidea deskargatuko duzun horrek) datu-basea altxatuko beharko lukeela... Ez litzateke izango bilatzen dugun egoera ezin hobe hori. Erantzuna?

### @Testcontainers
Hain zuzen ere, `@Testcontainers` anotazioa eta beste lerro gutxi batzuk, eta izango dugu:

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
Zer egin dugu?
- `@Testcontainers` anotazioa erantsi diogu test klaseari.
- Postgres duen edukiontzi baten instantzia bat sortu dugu `@Container` anotazioa erabiliz eta bertsioa zehaztuz.
- Azkenik, datasource-aren datuak ezarri ditugu `@DynamicPropertySource` bidez, sortutako edukiontzitik balioak hartuz.

Ikus dezakezuenez, inplementazioa oso erraza da, onura berehalakoa da: adibidea deskargatu eta zuen ekipoetan testak pasa dezakezue zuzenean, Docker instalatuta eduki besterik gabe (gogoratzen al dituzue lehengo 3 komandoak? Proba ditzakezue).

### Singleton patroia
Badago hori guztia inplementatzeko beste modu bat, eraginkorragoa, Singleton patroia erabiliz. Horrela, edukiontzi bera test klase batean baino gehiagotan erabiliko genuke.
Izan ere, dokumentazioan hurbilketa hori egitea gomendatzen da. Test klase bakarra besterik ez dugun adibide honetan ez dirudi erabilgarria, baina seguru asko ez da gure proiektuaren funtzionalitate bakarra izango, ezta? Une horretara iritsita, orduan bai, Singleton patroira pasatuko ginateke, [aquí](https://www.testcontainers.org/test_framework_integration/manual_lifecycle_control/#singleton-containers){:target="_blank"} azaltzen den bezala.

Ikus dezagun nolakoa izango litzateke:

#### BooksServiceTest.java
```java
@SpringBootTest
@Transactional
class BooksServiceTest extends PostgresContainerBaseTest {
    //@Container eta @DynamicPropertySource ez dira behar PostgresContainerBaseTest klasean ditugulako
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

## Tip Pitest-ti buruz
¿[PIT](https://pitest.org/){:target="_blank"}? Zer zerikusi du** Testcontainers** ** PIT** rekin? Gogoan izan [gure testen kalitatea neurtu ahal dugula PIT erabiliz](https://blog.arima.eu/eu/2020/05/25/mutation-testing.html){: target = "_blank"}. Egia da PIT zuzenean bideratuta dagoela **unitateko test**-etara (batez ere denbora/efizientzia dela eta), baina egia da, halaber, orain arte ez dugula inolako arazorik aurkitu gure **integrazio test**-ak frogatzerakoan.

Hala ere, `@Testcontainers` erabiliz egindako testekin Pitest exekutatzen saiatzen bazarete, ez direla pasatzen aurkituko duzue. Aldiz, testak Singleton patroia erabiliz inpelementatuta badaude, Piten estaldura-analisia arazorik gabe egin ahal izango duzue.

_Norbaitek horren guztiaren zergatia jakin nahi badu eta baten batek proposatutako irtenbide bat probatu nahi badu, arazoarekin topo egitean ireki genuen [issue](https://github.com/hcoles/pitest/issues/827){:target="_blank"}-n egin dezake._


Honaino **Testcontainers**-i buruzko sarreratxo bat, datu-base baten adibide batekin. Lehen aipatu bezala, Testcontainers beste modulu asko eskaintzen dizkigu. Are gehiago, gure beharrengatik zerbait zehatzagoa behar badugu, gure 'docker-compose.yml' propioa izateko aukera ere badu, [dokumentazioan](https://www.testcontainers.org/modules/docker_compose/){: target = "_blank"} azaltzen den bezala.
Etorkizuneko postetan, gure adibidea garatuko dugu, Testcontainers erabiltzeko beste erabilera-kasu batzuen adibide batzuk sartu ahal izateko (erabiltzeko erraztasuna eta abantailak modu praktikoan ikusteko).



