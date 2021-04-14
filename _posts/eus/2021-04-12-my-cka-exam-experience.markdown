---
layout: post
title:  "Nire esperientzia CKA azterketarekin"
date:   2021-04-12 8:00:00
author: urko
lang: eu
categories: kubernetes, certifications, cloud
tags: kubernetes, certifications, cloud, exams, CKA
header-image: 2021-04-12-my-cka-exam-experience/header.jpg
---

Joan zen Martxoaren 22an Linux Foundation-en parte den [CKA](https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/){:target="_blank"} ziurtagiriaren azterketa egin nuen. Post honen bitartez nire esperientzia kontatu nahi dizuet, nola prestatu nuen eta zer espero daitekeen azalduz. Bide batez, orain dela hilabete batzuk [Fernandok, nire lankideak, idatzitako posta]({{ site.baseurl }}/es/2020-04-22-examen-ckad){:target="_blank"} irakurtzea gomendatzen dizuet. Bertan zehaztasun handiarekin azaltzen du azterketa honetan kontutan eduki beharrekoa eta nire ustez, froga gainditzeko benetan lagungarria da. Niri behintzat bere posta irakurtzea baliagarria gertatu zitzaidan!

### Aldez aurreko esperientzia Kubernetesekin

Egia esateko, duela urtebete Kubernetesi buruz ez nekien ezer. Gai honetan aurreko esperientziarik ez edukitzeaz gain, container-en oinarrizko kontzeptuak ere ez nituen menperatzen.

Bestalde, ordutik hona Kubernetesekin erlazionatuta dauden arlo desberdinetako proiektuetan buru-belarri aritu naiz  eta azterketa prestatzeko esperientzia honek asko lagundu dit. Hala eta guztiz ere, froga gainditzeko Kubernetesen oinarrizko esperientzia izatea nahikoa dela iruitzen zait.

### Nola prestatu nuen azterketa

Nahiz eta Kubernetes errekurtsoei buruzko ezagutza izan, kubectl komandoetara ohituta egon edota klusterrak kudeatzen esperientzia izan, [Udemyko kurtso honetan](https://www.udemy.com/course/certified-kubernetes-administrator-with-practice-tests){:target="_blank"} apuntatzea ere beharrezkoa iruditu zitzaigun. Hasieran Kubernetesen oinarrizko kontzeptuak eta bere kudeaketa azaltzen ditu. Atal hauek komenigarriak izan daitezke esperientzia gutxi duten pertsonentzat. Ondoren, konplexatun handiagoko edukiak azaltzen dira. 

Hala ere, azterketaren galdera asko oinarrizko kontzeptuei buruzkoa da, beraz oinarrizko ikasgaiak ere arreta handiz jarraitzea gomendagarria iruditzen zait. Aipatutako ikastaroa bideo eta laboratorio praktikoez osaturik dago, eta amaieran norberaren maila neurtzeko froga batzuk ere badaude, hauek benetako azterketako galderen oso antzekoak izanik. 

![Laborategiko ariketen adibide bat](/assets/images/2021-04-12-my-cka-exam-experience/exercise.jpg){: .center }
<label style="text-align: center; display: block;">Laborategiko ariketen adibide bat</label>

Laburbilduz, ikastaroa bukatu nuenean ikasgaiak errazak iruditzen zitzaizkidan. Azterketaren zailtasuna, berez, ez dago menperatu behar den edukian, klustera kudeatzeko trebezian eta azkartasunean baizik. Beraz, gorago aipatutako ikastaroa oso konpletoa dela iruditzen zait eta azterketarako prestatu nahi duen edozeini gomendatuko nioke. 

### Azterketa

CKA azterketa bi ordutan bete beharreko 17 galderez osaturik dago. Mota guztietako galderak aurkitu daitezke: Batzuk oso oinarrizkoak, adibidez Container anitzekin Pod bat nola hasieratu edo nola sortu Rol bat bere baimenekin. Beste batzuk ordea konplexugoak dira, Pod baten trafikoa mugatzen duen Network Policy bat nola sortu, esaterako. 

Lehen esan bezala, azterketaren benetako erronka erremintak ongi ezagutzea eta erreztasunez erabiltzea da. Horregatik Fernandok [bere postean]({{ site.baseurl }}/es/2020-04-22-examen-ckad){:target="_blank"} azaltzen dituen aholku batzuk azpimarratzen ditut:

- Praktikatu `kubectl`-ren subkomandoak erabiltzen. Yaml descriptoreak sortu `run` edo `create <mota> --dry-run=client -o yaml`, edo erabili `explain` errekurtso baten egitura hobeto ulertzeko. Horrela azterketan denbora asko aurreztu dezakezu. 
- Errekurtsoak `kubectl` bitartez sortu ezin direnean, dokumentazioan zehar azkar nabigatzen jakitea baliagarria izango zaizu, yaml deskriptoreen adibideak bertan aurkituko baitituzu. Horregatik, gehien erabiliko dituzun dokumentazioaren atalen estekak aldez aurretik nabigatzailean gordeta edukitzea gomendarria da. 
- Pertsonalki, nik alias hau erabili nun, `alias k=kubectl`, eta zoragarria iruditu zitzaidan!
- Ikasi bash terminala erabiltzen eta praktikatu bere komandoekin. Baita azterketan erabiliko dezun editoreakin ere (nik `vim` erabili nuen). Tresna hauekin produktiboa bazara, azterketako beste eragiketa baliotsuagoetan erabiltzeko denbora dexente aurreztuko duzu. 

### Ondorioak

Pozik nago ziurtagiri hau lortzeagatik, eta CNCFk onartutako erabiltzailea izatera pasa naizelako. Ikasi beharreko materiaren zati handiena erraz barneratzen da eta aldez aurretik ondo prestatuz gero, egunero Kubernetesekin lan egiten duten erabiltzaileek azterketa gainditu dezaketela ziur nago. 

Nik lortutako emaitza 87/100 izan zen. Beraz galdera bat edo bi gaizki erantzun nituela ondorioztatzen dut. Azterketako edozein ariketa ondo erantzuteko gai naizela jakiteak pozten nau, eta niretzako garrantzitsuena hau da: azterketako edukia ondo ulertzea eta ezagutza hori nire egunerokotasunean aplikatzea. 

![Ziurtagiria](/assets/images/2021-04-12-my-cka-exam-experience/certification.png){: .center }
<label style="text-align: center; display: block;">Ziurtagiria</label>

