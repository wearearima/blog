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

Integrazio-testak baino gustokoago izan ditut beti unitate-testak, batez ere arrazoi honengatik: ez dut kanpoko ezer behar hauek pasa ahal izateko. Ez dut behar datu-base bat, kanpo-zerbitzu bat edo Kafka bat martxan izatea testak pasatu ahal izateko, eta ondorioz, garatu ahal izateko.
Eta hori garapen-inguruneari dagokionez, zeren eta integrazio-ingurunea hartzen badugu kontutan, hare gehiago.
Adibidez, datu-baseen kasuan, testak H2rekin egiteko aukera dugu. Baina kontutan eduki behar da proiektu motaren arabera, gerta daitekeela H2n primeran funtzionatzen duen zerbaitek, garatzen ari garen datu-basean ez funtzionatzea.   
Askotan 
> “Tira... H2rekin egingo dugu, datu-basea martxan ez jartzeagatik...”  

pentsatu dugun bezain egia da beste egoera hau:
> “Baino... testatuta dago! Orduan zergatik...? Ups...”

Ni beti izan naiz dena instalatuta eduki behar duen horietakoa: MySQL, Postgres, Kafka... Proiektua martxan jartzeko behar den guztia. Horrela, proiektuaren arabera, dena instalatuta eta zerbitzu guztiak martxan ditudala ziurtatu behar izan dut beti. Baina hau nire lankideek edukiontziak aurkeztu zizkidatenean bukatu zen, tira, Docker aurkeztu zizkidatenean.
Inoiz ez naiz izan oso trebea gauza hauekin,. Baina egia esan, hauei esker ez dut hamaika gauza instalatuta edukitzeko beharrik: behar ditudan zerbitzuen irudiak ditut, eta behar ditudanak martxan jarri besterik ez dut egin behar, eta kito.
Goazen harira. Egia da orain aplikazioak martxan jartzeko dena askoz ere antolatuago daukadala, baina egia esan, garatzerako orduan oraindik ere gutxi gorabehera berdin nago: integrazio-testak pasatu nahi baditut, datu-basea martxan jartzeaz gogoratu behar naiz (adibidez), beraz, oraindik ez da H2 bezain gardena.  

<small>Baten batek imajinatuko zuen bezala, honek guztiak ere badu CIn aplikazioa. Baina post honetan, tresna honek garatzailearen eguneroko lanean nola lagunduko digun jarriko dugu harreta.</small>

> "Bi munduak batzen dituen eta testak autosufizienteak egiten dituen zerbait egon behar du, benetako ingurune bat simulatuz"

Ideia hori buruan nuela eta lankide batekin hitz egin ondoren, hala zela jakin nuen: ¡[**TestContainers**](https://www.testcontainers.org/){:target="_blank"} izeneko zerbait existitzen da!

Adibidez, imajina ditzagun buruhausteak eragiten dizkigun eguneko egoera batzuk: kide berri bat taldean! edo, laguntza eskatu nahi badiogu lankide bati erabilera-kasu edo bug kasu bati buruz? edo, hilabetetan lanik egin ez dugun proiektu batetara itzultzen bagara?
Horrelako egoeren aurrean (eta beste batzuen aurrean), zenbat aldiz pentsatuko genuen "ez al da posible izango dena deskargatu, testak pasa eta garatzen hastea beste ezer egin gabe?".
Denbora igaro da bakarrik ez negoela konturatu nintzela. [@kiview](https://twitter.com/kiview){:target="_blank"}ren aurkezpen bat ikusten ari nintzela konturatu nintzen. Aurkezpenaren hasieran honelako zerbait esaten zuen:
> ...proiektu baten onboarding-esperientzia arrakastatsua ondorengoa izango litzateke: garatzaile batek proiektu baten biltegia klonatzea, buildinga egitea eta horrekin proiektua eraikita izatea, unitate eta integrazio-testak barne...

Hau da, ondorengo pauso hauek jarraitzea:
```
> git clone https://github.com/wearearima/school-library-testcontainers-01.git
> cd school-library-testcontainers-01
> ./mvnw install
```
Eta listo!  
Begiek 😍 egin zidaten. Hitzaldiaren izenburua [Integration Testing with Docker and Testcontiners](https://www.youtube.com/watch?v=Lv1evJe2MRI){:target="_blank"} zen, hau da,  **TestContainers** hain zuzen. Berri onak orduan! Badirudi **TestContainers**ekin lan egiteak helburu horretara hurbiltzea errazten digula eta lana sinplifikatzen digula, garapen propioan zentratu ahal izateko (eta jakina, testetan ere).

# Adibidea: Database container (Postgres Module)
Horrela esanda, denak oso itxura ona du, baina (noizbehinka irakurtzen nauzuenok jakingo duzuenez) kontzeptuak ulertzeko praktikan jarri behar ditut, beraz, adibide bat prestatu dugu [Github](https://github.com/wearearima/school-library-testcontainers-01){:target="_blank"}en. 
Ohikoena, seguruenik, datu-baseen aurka egiten ditugun testen egoera da, eta Testcontainersek datu-base desberdinetarako _moduloak_ eskaintzen dizkigu. Horregatik, adibide sinple bat prestatu dugu, Postgres datu-base batera konektatzen den Spring Boot aplikazio batena.  
Gure adibidea:  
    _Demagun eskola bateko liburutegia. Jasotzen ditugun aleei alta ematen joateko balioko duen funtzionalitate bat dugu. Izan genezakeen metodoetako bat "liburu baten kopia gehitzea" izan zitekeen ("liburua" kontzeptua dela ulertuta, eta "kopia", berriz, izan dezakegun ale bakoitzaren errepresentazioa)._  
<small>Etorkizunean adibide hau eboluzionatzen eta kodea gehitzen joango gara.</small>


Esan bezela,[Postgres](https://www.testcontainers.org/modules/databases/postgres/){:target="_blank"}erako dagoen modulua erabiliko dugu. Kontainer hau erabiliz testak egitea oso erraza da, goazen ba!

## Docker instalatu
Lehenik eta behin, [Docker Desktop](https://www.docker.com/products/docker-desktop){:target="_blank"} instalatu behar dugu (eduki ezean). Ondoren, Docker instalatu ahal izateko behar diren eskakizunak azaltzen dituen dokumentazioaren esteka utziko dut: [General Docker requirements](https://www.testcontainers.org/supported_docker_environment/){:target="_blank"}.


## Gehitu behar diren dependentziak
Kodearekin hasteko, lehenik eta behin, proiektuak behar dituen dependentziak gehitu beharko ditugu (gure kasuan, pom.xml-an).

Guk [Spring Initializr](https://start.spring.io/){:target="_blank"} erabiliz sortu dugu proiektua eta bertan gehitu dugu dependentzia

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
Listo! Gure erabilera-kasua inplementatu dezakegu. Test bat baino gehiago egingo dugu (hemen eskuragarri: [Github](https://github.com/wearearima/school-library-testcontainers-01/blob/master/src/test/java/eu/arima/schoolLibrary/bookStore/BooksServiceTest.java){: target = "_blank"}), baina hemen adibide gisa bakarra ikusiko dugu. Testak ondorengoa egingo du: lehendik existitzen den ISBN bati liburu baten kopia bat gehitzen diogunean, liburu horri kopia bat gehitu zaiola egiaztatuko dugu. Erraza, ezta?

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
Baina testa besterik gabe exekutatzen badugu, ikusiko dugu kontextua altxatu ezin duelako huts egiten duela: datu-baseari buruzko informazioa falta zaio.
Egia da application.properties fitxategian jarri ditzakegula balioak... baina horrek eskatuko luke iritsi berri den garatzaile horrek (edo zuk, adibidea deskargatuko duzunak) datu-basea altxatuko beharko lukeela... Ez litzateke izango bilatzen dugun egoera ezin hobe hori. Soluzioa?

### @Testcontainers
Hain zuzen, `@Testcontainers` anotazioa, lerro gutxi batzuk, eta listo:

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
- Postgres duen kontainer baten instantzia bat sortu dugu `@Container` anotazioa erabiliz eta bertsioa zehaztuz.
- Azkenik, datasourcearen datuak ezarri ditugu `@DynamicPropertySource` bidez, sortutako kontainerretik balioak hartuz.

Ikus dezakezuenez, inplementazioa oso erraza da, eta onura berehalakoa: adibidea deskargatu eta zuen ekipoetan testak pasa dezakezue zuzenean, Docker instalatuta besterik eduki gabe (gogoratzen al dituzue lehengo 3 komandoak? Proba ditzakezue).

### Singleton patroia
Badago hori guztia inplementatzeko beste modu bat, eraginkorragoa: Singleton eredua. Horrela, kontainer bera test klase batean baino gehiagotan erabili ahalko genuke.
Dokumentazioan hurbilketa hori egitea gomendatzen da hain zuzen. Test klase bakarra besterik ez dugun adibide honetan, ez dirudi erabilgarria. Baina seguruenik ez da gure proiektuaren funtzionalitate bakarra izango, ezta? Kasua hori izango balitz, orduan bai, Singleton eredura pasatuko ginateke, [hemen](https://www.testcontainers.org/test_framework_integration/manual_lifecycle_control/#singleton-containers){:target="_blank"} azaltzen den bezala.

Ikus dezagun nolakoa izango litzatekeen:

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

## Pitest-i buruzko tip-a
[PIT](https://pitest.org/){:target="_blank"}? Zer zerikusi du **Testcontainers**ek **PIT**rekin? Gogoan izan [gure testen kalitatea neurtu ahal dugula PIT erabiliz](https://blog.arima.eu/eu/2020/05/25/mutation-testing.html){: target = "_blank"}. Egia da PIT zuzenean bideratuta dagoela **unitateko test**etara (batez ere denbora/efizientzia dela eta). Baina egia da, halaber, orain arte ez dugula inolako arazorik aurkitu gure **integrazio-test**ak frogatzerakoan.

Hala ere, `@Testcontainers` erabiliz egindako testekin Pitest exekutatzen saiatzen bazarete, ez direla pasatzen ikusiko duzue. Aldiz, testak Singleton eredua erabiliz inpelementatuta badaude, Piten estaldura-analisia arazorik gabe egin ahal izango duzue.

_Norbaitek horren guztiaren zergatia jakin nahi badu eta norbaitek proposatutako irtenbide bat probatu nahi badu, arazoarekin topo egitean ireki genuen [issue](https://github.com/hcoles/pitest/issues/827){:target="_blank"}n egin dezake._


Honaino **Testcontainers**i buruzko sarreratxo bat, datu-base baten adibide batekin. Lehen aipatu bezala, Testcontainersek beste modulu asko eskaintzen dizkigu. Are gehiago, gure beharrengatik zerbait zehatzagoa behar badugu, gure 'docker-compose.yml' propioa izateko aukera ere badu, [dokumentazioan](https://www.testcontainers.org/modules/docker_compose/){: target = "_blank"} azaltzen den bezala.
Etorkizuneko postetan, gure adibidea garatuko dugu, Testcontainers erabiltzeko beste erabilera-kasu batzuen adibide batzuk sartuz (erabiltzeko erraztasuna eta abantailak modu praktikoan ikusteko).



