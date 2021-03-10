
from lxml import etree, html
from lxml.html.clean import clean_html
import pandas as pd
from datetime import date, datetime
import requests
import re
import os
import shutil
from ASECORP_BBDD import tagea_BBDD_ASECORP, devuelve_patrones

## Crea función que convierte lista a string en todas las columnas de tabla_analisis
## para evitar en presentación final los caracteres [' '] propios de las listas
def list2Str(lst):
    if type(lst) is list: # apply conversion to list columns
        return", ".join(lst)
    else:
        return lst

# # Mueve todos los fichero del directorio de trabajo a otro de archivo

source_dir = './BOEs'
target_dir = './BOEs_Anteriores'
    
file_names = os.listdir(source_dir)
    
for file_name in file_names:
    #shutil.move(os.path.join(source_dir, file_name), target_dir)
    # Evita que de error si el fichero que se mueve ya existe en dir destino
    try:
        os.remove(os.path.join(target_dir, file_name))
        shutil.move(os.path.join(source_dir, file_name), target_dir)
    except OSError:
        shutil.move(os.path.join(source_dir, file_name), target_dir)

# # Recoge resumen diario del BOE de hoy

today = date.today()

# dd/mm/YYYY
hoy = today.strftime("%Y%m%d")
print("Fecha de Hoy =", today.strftime("%d/%m/%Y"))

# dd
d = today.strftime("%d")

# mm
m = today.strftime("%m")

# YYYY
Y = today.strftime("%Y")

URL_XML_resumen =  "https://www.boe.es/diario_boe/xml.php?id=BOE-S-" + str(hoy)

#URL_XML_resumen = 'https://www.boe.es/diario_boe/xml.php?id=BOE-S-20210210'

#URL_XML_resumen

url = URL_XML_resumen
r = requests.get(url)

print('Accediendo a página del boletín')

def save_html(html, path):
    with open(path, 'wb') as f:
        f.write(html)

save_html(r.content, './BOEs/Resumen-BOE-' + hoy + '.xml')

resumen = etree.parse('./BOEs/Resumen-BOE-' + hoy + '.xml')

raiz=resumen.getroot()
raiz.tag
raiz_sumario = raiz

seccion = raiz.findall("sumario/diario/seccion")
#seccion

#for seccion in raiz.xpath('//seccion'):
#    nombre_seccion = seccion.xpath('@nombre')
#    print(nombre_seccion)

print('Accediendo a página resumen de disposiciones')

tabla_resumen = pd.DataFrame()

# Busca en Secciones I y III
for secciones in raiz.xpath('//seccion[contains(@nombre, "I. Disposiciones generales") or\
                                     contains(@nombre, "III. Otras disposiciones") or\
                                     contains(@nombre, "V. Anuncios. - A. Contratación del Sector Público") or\
                                     contains(@nombre, "T.C. Sección del Tribunal Constitucional")]'):

    nombre_seccion = secciones.xpath('@nombre')
    #print(nombre_seccion)
    for seccion in secciones:

        for item in seccion.xpath('.//item'):
            item_id = item.xpath('@id')
            nombre_departamento = item.xpath('.//ancestor::departamento/@nombre')   # Recoge Departamento del item
            nombre_epigrafe = item.xpath('.//ancestor::epigrafe/@nombre')           # Recoge Epigrafe del item
            item_name = item.xpath('.//titulo/text()')
            item_urlXml = "https://www.boe.es" + str(item.xpath('.//urlXml/text()'))[2:-2]
            #print(item_urlXml)
            tabla_resumen = tabla_resumen.append({'Seccion': nombre_seccion, 
                                                  'Departamento': nombre_departamento, 
                                                  'Epigrafe' : nombre_epigrafe,
                                                  'Item_id': item_id, 
                                                  'Item_Nombre' : item_name, 
                                                  'Item_URL_XML' : item_urlXml},
                                                  ignore_index=True)

tabla_resumen.sort_values('Item_id')

# Convierte columnas Departamento y Epigrafe a tipo str para poder realizar búsqueda de palabra Comunidad y variantes
tabla_resumen['Epigrafe'] = tabla_resumen['Epigrafe'].astype(str)
tabla_resumen['Departamento'] = tabla_resumen['Departamento'].astype(str)

# Elimina disposiciones con departamento o epigrafe que contenga las palabras Comunidad y sus variantes
terminos = ['Comunidad', 'Comunitat', 'COMUNIDAD', 'COMUNITAT']
tabla_resumen = tabla_resumen.drop(tabla_resumen.index[tabla_resumen['Epigrafe'].str.contains('|'.join(terminos), na=False)])
tabla_resumen = tabla_resumen.drop(tabla_resumen.index[tabla_resumen['Departamento'].str.contains('|'.join(terminos), na=False)])

# # Descarga ficheros XML asociados

for item_URL in tabla_resumen['Item_URL_XML']:
    r = requests.get(item_URL)
    #f = './BOEs/' + item_URL[-16:] + '.xml'
    ### Separa el número del BOE del resto de la cadena y aplica expresión REGEX 
    #print(item_URL.split('='))
    #print(re.match('BOE\-A\-[0-9]+\-[0-9]+',item_URL.split('=')[1]))
    filename = re.match('BOE\-(A|B)\-[0-9]+\-[0-9]+',item_URL.split('=')[1]).group()
    f = './BOEs/' + filename + '.xml'
    save_html(r.content, f)

# # Importa de nuevo los XML generados

import glob
BOEs = glob.glob('./BOEs/BOE*.xml')
#print (BOEs)

# # Genera DF con datos Análisis de cada XML

tabla_analisis = pd.DataFrame()

print('Accediendo a página detalle de disposiciones')

for BOE in BOEs:
    #print (BOE)
    BOE_XML = etree.parse(BOE)
    raiz=BOE_XML.getroot()

    materias = [materia.text for materia in raiz.findall('analisis/materias/materia')]
    alertas = [alerta.text for alerta in raiz.findall('analisis/alertas/alerta')]
    
    referencias = [str(referencia.xpath('@referencia')).replace("['",'').replace("']",'') for referencia in raiz.findall('analisis/referencias/anteriores/anterior')]
    referencias_palabras = [referencia.text for referencia in raiz.findall('analisis/referencias/anteriores/anterior/palabra')]
    referencias_texto = [referencia.text for referencia in raiz.findall('analisis/referencias/anteriores/anterior/texto')]

    Item_Id = raiz.xpath(".//identificador/text()")
    Item_name = raiz.xpath('.//titulo/text()') 

    Fecha_Publicacion = datetime.strptime(str(raiz.xpath('.//fecha_publicacion/text()'))[2:-2],"%Y%m%d")
    #Fecha_Publicacion = str(raiz.xpath('.//fecha_publicacion/text()'))[2:-2]
 
    tabla_analisis = tabla_analisis.append({'Item_id': Item_Id,
                                            'Item_Name' : Item_name,
                                            'Fecha_publicacion' : Fecha_Publicacion,
                                            'Materias' : materias,
                                            'Alertas' : alertas,
                                            'Referencias' : referencias,
                                            'Referencias_palabra' : referencias_palabras,
                                            'Referencias_texto' : referencias_texto},
                                            ignore_index=True)


tabla_analisis.sort_values('Item_id')

print('Generando Tags de patrones encontrados en disposiciones')

# Crea nueva columna vacía de tipo lista en tabla_analisis
tabla_analisis['Referencias_completas'] = [[] for i in range(len(tabla_analisis))]
tabla_analisis['Tags'] = [[] for i in range(len(tabla_analisis))]
tabla_analisis['Match_ASECORP_BBDD'] = [[] for i in range(len(tabla_analisis))]

# Define expresiones REGEX para búsqueda de leyes, decretos, etc. referenciadas anteriormente
#pattern = ['Ley [0-9]+\/[0-9]+','Ley Orgánica [0-9]+\/[0-9]+','Decreto [0-9]+\/[0-9]+','Real Decreto [0-9]+\/[0-9]+','Real Decreto Legislativo [0-9]+\/[0-9]+','Real Decreto-ley [0-9]+\/[0-9]+','Orden [A-Z]+\/[0-9]+\/[0-9]+','Orden Circular [0-9]+\/[0-9]+','Reglamento \(UE\) [0-9]+\/[0-9]+', 'Reglamento de Ejeución \(UE\) [0-9]+\/[0-9]+' ,'Sentencia de [0-9]+ de [a-z]+ de [0-9]+','Sentencia [0-9]+\/[0-9]+','Orden de [0-9]+ de [a-z]+ de [0-9]+', 'Resolución de [0-9]+ de [a-z]+ de [0-9]+','Resolución [a-z]+\/[0-9]+\/[0-9]+', 'Nota de Servicio [0-9]+\/[0-9]+', 'Acuerdo multilateral M\-[0-9]+', 'Acuerdo Multilateral RID [0-9]+\/[0-9]+', 'Circular [0-9]+\/[0-9]+', 'Decisión \(UE\) [0-9]+\/[0-9]+', 'Decisión de Ejecución \(UE\) [0-9]+\/[0-9]+', 'Instrucción IS\-[0-9]+']
pattern = devuelve_patrones()

# Consolida las columnas Referencias_palabra y Referencias_texto en una única frase
for i, row in tabla_analisis.iterrows():
    for item_list in range(len(row['Referencias'])): 
        row['Referencias_completas'].append(row['Referencias_palabra'][item_list] + ' ' + row['Referencias_texto'][item_list])
        tabla_analisis['Tags'][i] = re.findall('|'.join(pattern), str(row['Referencias_texto']), flags=re.IGNORECASE)
    #print(row['Referencias_completas'])

# Elimina Tags duplicados
for i, row in tabla_analisis.iterrows():
    tabla_analisis['Tags'][i] = list(set(tabla_analisis['Tags'][i]))
    #print(tabla_analisis['Tags'][i])

#tabla_analisis

texto = ''
for refs in tabla_analisis['Referencias_completas']:
    for ref in refs:
        texto = texto + ref + ' '
        #print(ref)


texto = ''
for i, row in tabla_analisis.iterrows():
    #unique_id = i
    #print('\n' + str(row['Item_id']) + str(row['Item_Name']) +'\n')

    antecedente = 1
    for ref in row['Referencias_completas']:
        texto = texto + ref + ' '
        #print('\t' + 'Antecedente ' + str(antecedente) + ': ' + ref + ' ' + str(re.findall('|'.join(pattern), ref, flags=re.IGNORECASE)))
        antecedente += 1


# Aplica expresiones REGEX para búsqueda de leyes, decretos, etc. referenciadas anteriormente
regex_result = re.findall('|'.join(pattern), texto, flags=re.IGNORECASE)

#print(regex_result)

## Elimina duplicados
boletin_flat_list = list(set(regex_result))

#boletin_flat_list

print('Generando Tags de patrones encontrados en BBDD ASECORP')

# ## Importa BBDD ASECORP

# Inicializa datos de BBDD_ASECORP
boletin_ASECORP_flat_list = []
ASECORP_BBDD_BOE = pd.DataFrame()
ambitos = []

# Incluir en llamada a función el ambito territorial como lista
# si no se especifica ámbito los incluye todos
boletin_ASECORP_flat_list, ASECORP_BBDD_BOE, ambitos = tagea_BBDD_ASECORP(['España'])


## Busca coincidencias entre lista boletines BOEs explorados y lista boletines de BBDD ASECORP
set(boletin_flat_list) & set(boletin_ASECORP_flat_list)

#tabla_analisis['Tags'].isin(ASECORP_BBDD_BOE['Tags'])
#for row_to_compare in tabla_analisis['Tags']:
#    for row_comparing in ASECORP_BBDD_BOE['Tags']:
#        if set(row_comparing) & set(row_to_compare):
#            print(set(row_comparing) & set(row_to_compare))

print('Realizando Matching entre Tags encontrados en disposiciones y en BBDD ASECORP')

for i, row_to_compare in tabla_analisis.iterrows():
    for j, row_comparing in ASECORP_BBDD_BOE.iterrows():
        if set(row_to_compare['Tags']) & set(row_comparing['Tags']):
            tabla_analisis['Match_ASECORP_BBDD'][i].append (ASECORP_BBDD_BOE['Codigo'][j])
            #print(str(set(row_to_compare['Tags']) & set(row_comparing['Tags'])) + ' ' + str(row_comparing['Codigo']))


# # Genera Fichero EXCEL de resultados

## Cambia orden de columnas y elimina las no necesarias  
tabla_analisis_final = tabla_analisis[['Item_id','Item_Name','Fecha_publicacion','Materias','Alertas','Referencias','Referencias_completas','Tags','Match_ASECORP_BBDD']]

## Aplica función de conversión de listas a strings
tabla_analisis_final = tabla_analisis_final.apply(lambda x: [list2Str(i) for i in x])

## Generar hyperlink a artículo BOE en CSV "=HYPERLINK("https://www.boe.es/boe/dias/2021/02/02/pdfs/BOE-A-2021-1474.pdf";"BOE-A-2021-1474")"
## https://www.boe.es/diario_boe/xml.php?id=## https://www.boe.es/boe/dias/2021/02/02/pdfs/BOE-A-2021-1474.pdf

tabla_analisis_final_CSV = tabla_analisis_final

# Compone y genera enlace a PDF del BOE correspondiente
tabla_analisis_final_CSV['Item_id'] = '=HIPERVINCULO(' + '"https://www.boe.es/boe/dias/' + tabla_analisis_final_CSV['Fecha_publicacion'].map(lambda x: x.strftime('%Y')) + '/'                                                        + tabla_analisis_final_CSV['Fecha_publicacion'].map(lambda x: x.strftime('%m')) + '/'                                                        + tabla_analisis_final_CSV['Fecha_publicacion'].map(lambda x: x.strftime('%d')) + '/'                                                        + 'pdfs/'                                                        + tabla_analisis_final_CSV['Item_id'] + '.pdf";'                                                        + '"' + tabla_analisis_final_CSV['Item_id'] + '")'

print('Guardando resultados en fichero')

tabla_analisis_final_CSV.to_csv("./ASECORP/Resultados_Matching_BOE_" + today.strftime("%Y%m%d") + ".csv", index=False) 
