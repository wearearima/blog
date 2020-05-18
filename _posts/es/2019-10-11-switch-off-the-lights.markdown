---
layout: post
title:  "[CSS] Switch off the lights"
date:   2019-10-11 9:00:00
author: alberto
lang: es
categories: css
tags: css, dark, light, claro, oscuro
header-image:	post-headers/lights-header.jpg
---

El "modo oscuro" en las interfaces de usuario se ha puesto de moda el último año. Antes eran pocas las aplicaciones (nativas o webapps) que tenían una interfaz alternativa a la de colores blancos/claros que utilizan la mayoría de UIs por defecto. Y las que lo ofrecían (por ejemplo, Youtube) lo tienen escondido de tal forma que hay que activarlo como opción en los menús de configuración de la propia aplicación. Es decir, había pocas aplicaciones que lo ofrecían y además se necesitaba bucear entre las opciones para ver si lo ofrecían y en caso afirmativo activarlo en cada una de ellas: cocktail perfecto para que en la práctica no lo utilizase prácticamente nadie y, en consecuencia a su vez, no existiese ningún aliciente para ofrecer ese modo oscuro.

Sin embargo macOS estrenó con su versión Mojave/10.14 (septiembre de 2018) una configuración global para poner todo el sistema operativo en modo oscuro (menús, el Finder, etc.) y ofrecer a las aplicaciones nativas esta información (si el usuario ha elegido un tema claro u oscuro) para poder integrarse en el sistema operativo automáticamente. A partir de ahí muchas aplicaciones nativas se han ido actualizando para respetar esta configuración (por ejemplo Firefox y Chrome han lanzado estos últimos meses interfaces oscuras del propio navegador para los que tenemos el modo oscuro activado), ha llegado también a Windows, y ha dado el salto a móviles implementándose oficialmente en Android 10 e iOS 13 (aunque desde Android 9 ya se podía activar en muchos móviles) donde además tiene el aliciente del ahorro de batería en pantallas AMOLED, etc.

Y, lo que nos interesa, es que esta configuración ha saltado también a CSS. La propuso WebKit implementándola en Safari 12.1 y ya se ha lanzado también en Firefox (67+) y Chrome de escritorio (77+), aunque por alguna razón aún no en Chrome de Android (caniuse). Estamos hablando de la media query _prefers-color-scheme_ (MDN).

Esto permite ejecutar CSS específico según las preferencias de tema del usuario en su sistema operativo (de escritorio o móvil). En la práctica, podemos hacer algo así:

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

Con esto tendríamos un tema oscuro para quien así tenga configurada la preferencia en su sistema operativo, y un tema tradicional claro para todos los demás (incluidos aquellos navegadores que aún no soporten esta nueva media query).

Podéis probarlo con la versión de cualquier navegador de escritorio esta mini demo que he hecho: [https://typescript-rf4g1k.stackblitz.io/](https://typescript-rf4g1k.stackblitz.io/){:target="_blank"}

![demo](/assets/images/2019-10-11-switch-off-the-lights/demo.gif){: .center }

Si jugáis, como en el GIF, con la configuración System Preferences -> General -> Appearance, al cambiar entre el modo Light y Dark cambiará no solo la interfaz de macOS y la UI del navegador, sino también nuestra propia web. Yay!

Y, de hecho, con el CSS puro actual podemos jugar aún más: podríamos utilizar variables CSS y conseguir algo así:

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

Definir todos los colores que utilicemos en nuestra UI como variables y reescribir el tema oscuro con esta nueva media query. Y esto funcionaría igual que lo anterior, out of the box sin ningún pre-tratamiento necesario de Sass/PostCSS/etc.