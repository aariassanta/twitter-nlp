# BOEs-NLP
Commits:
* ~~Separar boletines en scripts Python separados~~
* ~~Separar búsqueda de Tags en BBDD ASECORP en script separado~~
    + Hacer que se compruebe modificación de la BBDD, y si no no se modifican Tags encontrados no se ejecuta de nuevo el Script
    + Buscar más patrones REGEX en filas en las que no se han encontrado Tags
    + Hacer que los patrones REGEX se compartan para sólo actualizarlos en un lugar
* Incluir extracción Tags en contenido PDFs
* Evaluar librería **Schedule**

## BOE
---
* ~~Considera Secciones: 'I. Disposiciones generales', y 'III. Otras disposiciones'~~
* ~~Sólo considera ámbito de BBDD_ASECORP España~~
* ~~Intentar incluír también Sección Anuncios, con código similar a :~~

    ```el = doc.xpath("//div[contains(@class, 'channel') or (contains(@class, 'disabled'))]")```

* En reunión del 5/03/2021 con ASECORP se proponen la siguientes modificaciones:
    + Incluír secciones: III, V. A, y Tribunal Constitucional
    + Eliminar disposiciones referidas a comunidades 

## DOGC
---
* No implementado ^[This is a footnote.]

## DOUE
---
* De momento sólo incorpora sección L
* ~~Revisar que ámbito de BBDD_ASECORP incluya Europa~~

## DOCM (Diario Oficial de Castilla la Mancha)
---
* Incopora todas las secciones
    * Considerar eliminar algunas secciones
* En reunión del 5/03/2021 con ASECORP se proponen la siguientes modificaciones:
    * Eliminar sección II. Autoridades y personal
    * Eliminar disposiciones referidas a proyectos
    * Eliminar si tiene número de expediente
    * Eliminar Sanciones
