---
layout: post
title:  "[CSS] Switch off the lights"
date:   2019-10-11 9:00:00
author: alberto
lang: eu
categories: css
tags: css, dark, light, claro, oscuro, iluna
header-image:	post-headers/lights-header.jpg
---

Azkenaldian, erabiltzaileen interfazeetan "modu iluna" erabiltzea bogan dago. Lehen aplikazio gutxi ziren interfazeetan kolore argiak erabiltzen ez zituztenak eta aldatzeko aukera ematen zutenak (Youtube adibidez), izkutuan zegoen konfigurazio baten bitartez izaten zen. Hau da, aplikazio gutxi ziren aukera hori eskaintzen zutenak eta aukera ematekotan, aplikazioz aplikazio ezarri beharreko konfigurazio bat zen. Hori dela eta, praktikan oso gutxi erabiltzen zen.

2018 urtean publikatu zen MacOS sistema eragilearen eguneraketan (10.14/Mojave), sistema eragilea modu ilunean ezartzea ahalbidetzen zuen konfigurazio orokor bat gehitu zen: finder-a, menua, etab. Horri esker, aplikazio natiboek konfigurazio hau erabili dezakete bere burua "modu ilunean" erakusteko ere. Hori da hain zuzen ere, hainbat aplikazio egiten hasi zirena: Firefox, Chrome etab. Joera hau Windows eta mugikorretan (Android 10 eta iOS 13) ikusi genuen ere eta gainera, mugikorretan bateria aurreztu dezakegu AMOLED pantailak dituzten gailuetan.

Gaur egun, konfigurazio hau CSS orrietan aplikatu dezakegu ere. WebKit izan zen ezaugarri hau inplementatu zuen lehenengo nabigatzailea Safariren 12. bertsioan. Webkit-en atzetik Firefox (67+ bertsioetan) eta Chrome (77+ bertsioetan) etorri ziren. _prefers-color-scheme_ "media query"-aren bitartez, kolore ezberdinak aplikatu ditzakegu erabiltzaileak sistema eragilean konfiguratutako moduaren (argia/iluna) arabera. Praktikan, horrelako zerbait egin dezakegu:


```
body {
  background: #eee;
  color: #111;
}

@media (prefers-color-scheme: dark) {
  body {
    background: #111;
    color: #eee;
  }
}
```

CSS horren bitartez, kolore ilunak erabiliko lirateke modu iluna konfiguratuta duten erabiltzaileentzat eta kolore argiagoak beste guztientzat (media query berri hori oraindik onartzen ez duten nabigatzaileek ere modu argia erakutsiko lukete defektuz).

Ezaugarri berri hau probatu nahi badezute, garatu deten hurrengo demoa ikusi dezakezute: [https://typescript-rf4g1k.stackblitz.io/](https://typescript-rf4g1k.stackblitz.io/){:target="_blank"}

![demo](/assets/images/2019-10-11-switch-off-the-lights/demo.gif){: .center }

Aurreko animazioan ikusten den bezala, sistema eragilearen konfigurazioa "light"-etik "dark"-era  aldatuz gero, macOS interfazea aldatzeaz gain, gure webgunearen itxura aldatzen dela ikusi dezakegu. CSS aldagaiei esker, gauza aurreratuagoak egin ditzakegu:

```
:root {
    --background-color: #eee;
    --text-color: #111;
}

@media (prefers-color-scheme: dark) {
    :root {
        --background-color: #111;
        --text-color: #eee;
    }
}

body {
  background: var(--background-color);
  color: var(--text-color);
}
```

Gure interfazeetan erabiliko ditugun kolore guztiak aldagaietan zehaztu ditzakegu eta media query berri honen bitartez, aldagaien balioak ilunagoak diren koloreekin berridatzi. Modu horretan, modu iluna erabiltzen duten erabiltzaileei automatikoki aplikazio guztiaren itxura aldatuko zaie beste inongo aldaketarik egin gabe.