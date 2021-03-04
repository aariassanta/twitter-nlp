
from lxml import etree, html
from lxml.html.clean import clean_html
import pandas as pd
from datetime import date, datetime
import requests
import re
import os
import shutil
from ASECORP_BBDD import tagea_BBDD_ASECORP


# # # Recoge resumen diario del BOE de hoy
# 
today = date.today()
# 
# # dd/mm/YYYY
hoy = today.strftime("%Y%m%d")
print("Fecha de Hoy =", today.strftime("%d/%m/%Y"))
# 
# # dd
# d = today.strftime("%d")
# print("dia =", d)
# 
# # mm
# m = today.strftime("%m")
# print("mes =", m)
# 
# # YYYY
# Y = today.strftime("%Y")
# print("año =", Y)
# 
# print(today.strftime("%d/%m/%Y"))

## Crea función que convierte lista a string en todas las columnas de tabla_analisis
## para evitar en presentación final los caracteres [' '] propios de las listas
def list2Str(lst):
    if type(lst) is list: # apply conversion to list columns
        return", ".join(lst)
    else:
        return lst

def save_html(html, path):
    with open(path, 'wb') as f:
        f.write(html)

# Define expresiones REGEX para búsqueda de leyes, decretos, etc. referenciadas anteriormente
pattern = ['Ley [0-9]+\/[0-9]+','Real Decreto [0-9]+\/[0-9]+','Real Decreto Legislativo [0-9]+\/[0-9]+','Real Decreto-ley [0-9]+\/[0-9]+','Orden [A-Z]+\/[0-9]+\/[0-9]+','Orden Circular [0-9]+\/[0-9]+','Reglamento \(UE\) [0-9]+\/[0-9]+', 'Reglamento de Ejeución \(UE\) [0-9]+\/[0-9]+' ,'Sentencia de [0-9]+ de [a-z]+ de [0-9]+','Sentencia [0-9]+\/[0-9]+','Orden de [0-9]+ de [a-z]+ de [0-9]+', 'Resolución de [0-9]+ de [a-z]+ de [0-9]+','Resolución [a-z]+\/[0-9]+\/[0-9]+', 'Nota de Servicio [0-9]+\/[0-9]+', 'Acuerdo multilateral M\-[0-9]+', 'Circular [0-9]+\/[0-9]+', 'Decisión \(UE\) [0-9]+\/[0-9]+', 'Decisión de Ejecución \(UE\) [0-9]+\/[0-9]+']

# --------------------------------------------------------------------------------------
# DOUE
# --------------------------------------------------------------------------------------

URL_HTML_resumen =  "https://eur-lex.europa.eu/oj/direct-access.html?locale=es"

## carga página HTML y genera árbol

print('Accediendo a página del boletín')

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
response = requests.get(URL_HTML_resumen, headers=headers)
tree = html.fromstring(response.text)

## Recoge Nombre Secciones Sumario

secciones = tree.xpath('//*[@class="table table-striped table-hover table-condensed OJTable AllBordersTable"]')
#print(secciones)

print('Accediendo a página resumen de disposiciones')

source_dir = './DOUEs'
target_dir = './DOUEs_Anteriores'
    
file_names = os.listdir(source_dir)
    
for file_name in file_names:
    # Evita que de error si el fichero que se mueve ya existe en dir destino
    try:
        os.remove(os.path.join(target_dir, file_name))
        shutil.move(os.path.join(source_dir, file_name), target_dir)
    except OSError:
        shutil.move(os.path.join(source_dir, file_name), target_dir)


## Recoge Valores para formar URLs Secciones Sumario

df_secciones_sumarios = pd.DataFrame()
for seccion in secciones:
    seccion_name = seccion.xpath('./tbody/tr[1]/td[2]/a/text()')
    seccion_URL = seccion.xpath('./tbody/tr[1]/td[2]/a/@href')
    #seccion = re.sub('(\\r|\\n|\\t)+', '', seccion)
    #print(seccion_name)
    #print(seccion_URL)


### Si no hay disposiciones hay que gestionar el error y salir del script
#if len(seccion_name) == 0:
#    print('No hay disposiciones')
#    # exit()

for row in range(len(seccion_name)):
    df_secciones_sumarios = df_secciones_sumarios.append({'Seccion': seccion_name[row],
                                                            'Seccion_link' : 'https://eur-lex.europa.eu' + seccion_URL[row][4:]},
                                                            ignore_index=True)


#if len(df_secciones_sumarios['Seccion'][0]) == 0:
#    print('No hay disposiciones')


DOUE_sumarios = pd.DataFrame()

print('Accediendo a página detalle de disposiciones')

for URL in df_secciones_sumarios['Seccion_link']:
    
    ### Recoge Items en Seccion Legislación

    #print(URL)
    response = requests.get(URL)
    sumario_HTML = html.fromstring(response.text)

    documentos_Name = sumario_HTML.xpath('//*[@class="oj-ti-doc-dur"]/a[1]/text()[1]')
    documentos_URL = sumario_HTML.xpath('//*[@class="oj-ti-doc-dur"]/a[1]/@href')

    for row in range(len(documentos_Name)):
        DOUE_sumarios = DOUE_sumarios.append({'Seccion': 'L' + documentos_URL[row][-7:-4],
                                        'Item_Title': documentos_Name[row],
                                        'Item_Link': 'https://eur-lex.europa.eu' + documentos_URL[row][10:],
                                        #'Item_Tag': documentos_URL[row][-45:-29],
                                        'Item_Doc_Name': '',
                                        'Fecha_publicacion': '',
                                        'PDF_Link': '',
                                        'Tags': '',
                                        'Match_ASECORP_BBDD': []},
                                        ignore_index=True)


def save_txt(txt, path):
    with open(path, 'w') as f:
        f.write(txt)

documentos_FileName = sumario_HTML.xpath('//*[@class="DocumentTitle pull-left"]/text()')

print('Generando Tags de patrones encontrados en disposiciones')

row = 0
for link in DOUE_sumarios['Item_Link']:
    sumario_Text = []
    ### Recoge PDF link en Items Legislación

    response = requests.get(link)
    sumario_HTML = html.fromstring(response.text)

    PDF_Link = sumario_HTML.xpath('//*[@id="format_language_table_PDF_ES"]/@href')
    DOUE_sumarios['PDF_Link'][row] = 'https://eur-lex.europa.eu' + PDF_Link[0][10:]

    Item_Doc_Name = sumario_HTML.xpath('//*[@class="DocumentTitle pull-left"]/text()')[0][9:]
    DOUE_sumarios['Item_Doc_Name'][row] = Item_Doc_Name

    #Item_Fecha = str(sumario_HTML.xpath('//*[@class="oj-hd-date"]/text()'))
    #Item_Fecha = datetime.strptime(str(raiz.xpath('//*[@class="oj-hd-date"]/text()'))[0:-2],"%d.%m.%Y")
    Item_Fecha = re.findall('[0-9]+\.[0-9]+\.[0-9]+', str(sumario_HTML.xpath('//*[@class="oj-hd-date"]/text()')))
    DOUE_sumarios['Fecha_publicacion'][row] = datetime.strptime(str(Item_Fecha)[2:-2],"%d.%m.%Y").date()

    ### Recoge Texto de Items
    
    Item_Text = sumario_HTML.xpath('//*[@class="oj-normal"]/text()')
    
    #[ sumario_Text.append(re.sub('(\\r||\\n\\t|\\xa0)+', '', item)) for item in Item_Text ]
    [ sumario_Text.append(item) for item in Item_Text ]
   
    ### Sustituye caracteres 'n.' por 'n.º' ya que al importar de HTML se pierde el caracter º

    sumario = "".join(sumario_Text).replace(' n.',' n.º')
    #print(sumario)
    ### Busca tags en texto

    DOUE_sumarios['Tags'][row] = list(set(re.findall('|'.join(pattern), sumario, flags=re.IGNORECASE)))

    ### Salva texto de Items en formato TXT

    save_txt(sumario, './DOUEs/Resumen-DOUE-' + Item_Doc_Name + '.txt')
    #print(sumario)
    #print('./DOUEs/Resumen-DOUE-' + Item_Doc_Name + '.txt')
    #print(Item_Doc_Name)

    #print(list(set(re.findall('|'.join(pattern), sumario, flags=re.IGNORECASE))))

    row += 1


# Elimina Tags duplicados
for i, row in DOUE_sumarios.iterrows():
    DOUE_sumarios['Tags'][i] = list(set(DOUE_sumarios['Tags'][i]))
    #print(DOUE_sumarios['Tags'][i])


### Ordena Columnas
DOUE_sumarios = DOUE_sumarios[['Seccion', 'Item_Doc_Name', 'Fecha_publicacion', 'PDF_Link', 'Item_Title', 'Item_Link', 'Tags', 'Match_ASECORP_BBDD']]
DOUE_sumarios


### Crea lista plana de Tags sin duplicados
DOUE_flat_list = list(set([item for row in DOUE_sumarios['Tags'] for item in row ]))

print('Generando Tags de patrones encontrados en BBDD ASECORP')

# Inicializa datos de BBDD_ASECORP
boletin_ASECORP_flat_list = []
ASECORP_BBDD = pd.DataFrame()
ambitos = []

# Incluir en llamada a función el ambito territorial como lista
# si no se especifica ámbito los incluye todos
boletin_ASECORP_flat_list, ASECORP_BBDD, ambitos = tagea_BBDD_ASECORP(['España','Europa'])

## Busca coincidencias entre lista boletines BOEs explorados y lista boletines de BBDD ASECORP
list(set(DOUE_flat_list) & set(boletin_ASECORP_flat_list))

print('Realizando Matching entre Tags encontrados en disposiciones y en BBDD ASECORP')

for i, row_to_compare in DOUE_sumarios.iterrows():
    for j, row_comparing in ASECORP_BBDD.iterrows():
        if set(row_to_compare['Tags']) & set(row_comparing['Tags']):
            DOUE_sumarios['Match_ASECORP_BBDD'][i].append (ASECORP_BBDD['Codigo'][j])
            #print(str(set(row_to_compare['Tags']) & set(row_comparing['Tags'])) + ' ' + str(row_comparing['Codigo']))


## Aplica función de conversión de listas a strings
DOUE_sumarios = DOUE_sumarios.apply(lambda x: [list2Str(i) for i in x])


DOUE_sumarios_CSV = pd.DataFrame()
DOUE_sumarios_CSV = DOUE_sumarios

# Compone y genera enlace a PDF del DOUE correspondiente
DOUE_sumarios_CSV['PDF_Link'] = '=HIPERVINCULO(' + '"' + DOUE_sumarios['PDF_Link'] + '";' + '"' + "Doc: " + DOUE_sumarios['Item_Doc_Name'] + '")'

print('Guardando resultados en fichero')

### Genera fichero CSV

DOUE_sumarios_CSV.to_csv("./ASECORP/Resultados_Matching_DOUE_" + today.strftime("%Y%m%d") + ".csv", index=False) 


