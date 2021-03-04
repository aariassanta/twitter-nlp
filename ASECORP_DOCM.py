
from lxml import etree, html
from lxml.html.clean import clean_html
import pandas as pd
from datetime import date, datetime
import requests
import re
import os
import shutil
from ASECORP_BBDD import tagea_BBDD_ASECORP
from selenium import webdriver

from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

## Crea función que convierte lista a string en todas las columnas de DOCM_sumarios
## para evitar en presentación final los caracteres [' '] propios de las listas
def list2Str(lst):
    if type(lst) is list: # apply conversion to list columns
        return", ".join(lst)
    else:
        return lst

def pdf2txt(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text

# # Mueve todos los fichero del directorio de trabajo a otro de archivo

source_dir = './DOCMs'
target_dir = './DOCMs_Anteriores'
    
file_names = os.listdir(source_dir)
    
for file_name in file_names:
    #shutil.move(os.path.join(source_dir, file_name), target_dir)
    # Evita que de error si el fichero que se mueve ya existe en dir destino
    try:
        os.remove(os.path.join(target_dir, file_name))
        shutil.move(os.path.join(source_dir, file_name), target_dir)
    except OSError:
        shutil.move(os.path.join(source_dir, file_name), target_dir)

# # Recoge resumen diario del DOCM de hoy


today = date.today()

# dd/mm/YYYY
hoy = today.strftime("%Y%m%d")
print("Fecha de Hoy =", today.strftime("%d/%m/%Y"))

URL_HTML_resumen =  "https://docm.jccm.es/portaldocm/cambiarBoletin.do?fecha=" + str(hoy)


#URL_HTML_resumen

print('Accediendo a página del boletín')

# carga página HTML y genera árbol

response = requests.get(URL_HTML_resumen)
sumario_HTML = html.fromstring(response.text)

## Recoge Nombre Secciones Sumario

secciones = sumario_HTML.xpath('//*[@class="cabeceraCategoria"]/text()')
secciones = [ re.sub('\r|\n|\t','', seccion) for seccion in secciones ]

def save_html(html, path):
    with open(path, 'wb') as f:
        f.write(html)

save_html(response.content, './DOCMs/Resumen-DOCM-' + hoy + '.html')

for seccion in sumario_HTML.xpath('//*[@class="cabeceraCategoria"]'):
    nombre_seccion = seccion.xpath('./text()')
    nombre_seccion = str(nombre_seccion[0]).strip()
    #print(nombre_seccion)

print('Accediendo a página resumen de disposiciones')

DOCM_sumarios = pd.DataFrame(columns=['item_Title','item_urlHTML','item_urlPDF'])

lista = []
for sumario in sumario_HTML.xpath('//*[@class="sumario"]'):
    lista.append(sumario.text_content().strip())

DOCM_sumarios['item_Title'] = lista

lista = []   
for link_HTML in sumario_HTML.xpath('//*[@title="Ver los datos detallados del documento"]'):
    link = link_HTML.xpath('./@href')
    #print(link)
    lista.append('https://docm.jccm.es/portaldocm' + str(link)[3:-2])

DOCM_sumarios['item_urlHTML'] = lista

lista = []   
for link_PDF in sumario_HTML.xpath('//div/a[@class="new-window"]'):
    link = link_PDF.xpath('./@href')
    #print(link)
    lista.append('https://docm.jccm.es/portaldocm' + str(link)[3:-2])

DOCM_sumarios['item_urlPDF'] = lista

# Consolida las columnas Referencias_palabra y Referencias_texto en una única frase
# for i, row in DOCM_sumarios.iterrows():
#     # carga página HTML y genera árbol
#     response = requests.get(row['item_urlHTML'])
#     sumario_HTML = html.fromstring(response.text)
#     HTML = html.tostring(sumario_HTML)
# 
#     #NID = sumario_HTML.xpath('//table[@class="tablaDetalle"]/tbody/tr[2]/td[2]/text()')
#     print(response.text)

#print(DOCM_sumarios['item_urlHTML'][0])

### Necesita libreria Selenium para renderizar JS script

options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(options=options)

driver.get(DOCM_sumarios['item_urlHTML'][0])
#print(driver.page_source)
response = driver.page_source

sumario_HTML = html.fromstring(response)
numero_diario = sumario_HTML.xpath('//table[@class="tablaDetalle"]/tbody/tr[1]/td[2]/text()')
numero_pagina = sumario_HTML.xpath('//table[@class="tablaDetalle"]/tbody/tr[3]/td[4]/text()')
NID = sumario_HTML.xpath('//table[@class="tablaDetalle"]/tbody/tr[2]/td[2]/text()')
rango = sumario_HTML.xpath('//table[@class="tablaDetalle"]/tbody/tr[5]/td[2]/text()')
organo_emisor = sumario_HTML.xpath('//table[@class="tablaDetalle"]/tbody/tr[7]/td[2]/text()')

#print(numero_diario[0].strip(), numero_pagina[0].strip(), NID[0].strip(), rango[0].strip(), organo_emisor[0].strip())
#print()

driver.quit()

print('Accediendo a página detalle de disposiciones')

### Recoge información de página de detalle con Selenium
### es necesario ya que la página se genera con un JS y
### hay que renderizarla con un headless web browser

options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(options=options)

DOCM_sumarios['NID'] = ''
DOCM_sumarios['numero_diario'] = ''
DOCM_sumarios['numero_pagina'] = ''
DOCM_sumarios['rango'] = ''
DOCM_sumarios['organo_emisor'] = ''
DOCM_sumarios['Fecha_publicacion'] = ''

for i, row in DOCM_sumarios.iterrows():
    # carga página HTML y genera árbol
    driver.get(row['item_urlHTML'])
    #print(driver.page_source)
    response = driver.page_source
    
    sumario_HTML = html.fromstring(response)
    numero_diario = sumario_HTML.xpath('//table[@class="tablaDetalle"]/tbody/tr[1]/td[2]/text()')
    numero_pagina = sumario_HTML.xpath('//table[@class="tablaDetalle"]/tbody/tr[3]/td[4]/text()')
    NID = sumario_HTML.xpath('//table[@class="tablaDetalle"]/tbody/tr[2]/td[2]/text()')
    rango = sumario_HTML.xpath('//table[@class="tablaDetalle"]/tbody/tr[5]/td[2]/text()')
    organo_emisor = sumario_HTML.xpath('//table[@class="tablaDetalle"]/tbody/tr[7]/td[2]/text()')
    item_itle = sumario_HTML.xpath('//table[@class="tablaDetalle"]/tbody/tr[9]/td[2]/text()')

    #print(numero_diario[0].strip(), numero_pagina[0].strip(), NID[0].strip(), rango[0].strip(), organo_emisor[0].strip())

    DOCM_sumarios['NID'][i] = NID[0].strip()
    DOCM_sumarios['numero_diario'][i] = numero_diario[0].strip()
    DOCM_sumarios['numero_pagina'][i] = numero_pagina[0].strip()
    DOCM_sumarios['rango'][i] = rango[0].strip()
    DOCM_sumarios['organo_emisor'][i] = organo_emisor[0].strip()

    DOCM_sumarios['Fecha_publicacion'][i] = datetime.strptime(str(today),"%Y-%m-%d").date()

driver.quit()

# # Salva PDFs y Genera DF con datos Análisis de cada PDF

print('Generando Tags de patrones encontrados en disposiciones')

# Crea nueva columna vacía de tipo lista en tabla_analisis
#DOCM_sumarios['Referencias_completas'] = [[] for i in range(len(tabla_analisis))]
DOCM_sumarios['Tags'] = [[] for i in range(len(DOCM_sumarios))]
DOCM_sumarios['Match_ASECORP_BBDD'] = [[] for i in range(len(DOCM_sumarios))]


pattern = ['Ley [0-9]+\/[0-9]+','Real Decreto [0-9]+\/[0-9]+','Real Decreto Legislativo [0-9]+\/[0-9]+','Real Decreto-ley [0-9]+\/[0-9]+','Orden [A-Z]+\/[0-9]+\/[0-9]+','Orden Circular [0-9]+\/[0-9]+','Reglamento \(UE\) [0-9]+\/[0-9]+', 'Reglamento de Ejeución \(UE\) [0-9]+\/[0-9]+' ,'Sentencia de [0-9]+ de [a-z]+ de [0-9]+','Sentencia [0-9]+\/[0-9]+','Orden de [0-9]+ de [a-z]+ de [0-9]+', 'Resolución de [0-9]+ de [a-z]+ de [0-9]+','Resolución [a-z]+\/[0-9]+\/[0-9]+', 'Nota de Servicio [0-9]+\/[0-9]+', 'Acuerdo multilateral M\-[0-9]+', 'Circular [0-9]+\/[0-9]+', 'Decisión \(UE\) [0-9]+\/[0-9]+', 'Decisión de Ejecución \(UE\) [0-9]+\/[0-9]+']

for i, row in DOCM_sumarios.iterrows():
    r = requests.get(row['item_urlPDF'])

    # Salva PDFs de enlaces a items
    filename = row['NID'].replace('/','-' )
    f = './DOCMs/' + 'DOCM_NID_' + filename + '.pdf'
    save_html(r.content, f)

    # Extrae texto de PDFs
    pdf_contents = pdf2txt(f)
    #print(pdf_contents)

    # Busca expresiones REGX coincidentes con Patrones definidos
    DOCM_sumarios['Tags'][i] = re.findall('|'.join(pattern), str(pdf_contents), flags=re.IGNORECASE)
    #print(DOCM_sumarios['Tags'][i])


# Elimina Tags duplicados
for i, row in DOCM_sumarios.iterrows():
    DOCM_sumarios['Tags'][i] = list(set(DOCM_sumarios['Tags'][i]))
    #print(DOCM_sumarios['Tags'][i])

# Aplica expresiones REGEX para búsqueda de leyes, decretos, etc. referenciadas anteriormente
regex_result = []
[ regex_result.append(tag) for tags in DOCM_sumarios['Tags'] for tag in tags ]

## Elimina duplicados
boletin_flat_list = list(set(regex_result))

print('Generando Tags de patrones encontrados en BBDD ASECORP')

# ## Importa BBDD ASECORP

# Inicializa datos de BBDD_ASECORP
boletin_ASECORP_flat_list = []
ASECORP_BBDD = pd.DataFrame()
ambitos = []

# Incluir en llamada a función el ambito territorial como lista
# si no se especifica ámbito los incluye todos
boletin_ASECORP_flat_list, ASECORP_BBDD, ambitos = tagea_BBDD_ASECORP(['España','Europa','Castilla la Mancha'])

#print(ambitos)

## Busca coincidencias entre lista boletines BOEs explorados y lista boletines de BBDD ASECORP
set(boletin_flat_list) & set(boletin_ASECORP_flat_list)

#DOCM_sumarios['Tags'].isin(ASECORP_BBDD_BOE['Tags'])
#for row_to_compare in DOCM_sumarios['Tags']:
#    for row_comparing in ASECORP_BBDD['Tags']:
#        if set(row_comparing) & set(row_to_compare):
#            print(set(row_comparing) & set(row_to_compare))

print('Realizando Matching entre Tags encontrados en disposiciones y en BBDD ASECORP')

for i, row_to_compare in DOCM_sumarios.iterrows():
    for j, row_comparing in ASECORP_BBDD.iterrows():
        if set(row_to_compare['Tags']) & set(row_comparing['Tags']):
            DOCM_sumarios['Match_ASECORP_BBDD'][i].append (ASECORP_BBDD['Codigo'][j])
            #print(str(set(row_to_compare['Tags']) & set(row_comparing['Tags'])) + ' ' + str(row_comparing['Codigo']))


# # Genera Fichero EXCEL de resultados

DOCM_sumarios_final = DOCM_sumarios

## Cambia orden de columnas y elimina las no necesarias  
DOCM_sumarios_final.rename(columns={'NID': 'Item_id', 'item_Title': 'Item_Title', 'item_urlPDF': 'PDF_Link'}, inplace=True)
DOCM_sumarios_final = DOCM_sumarios[['Item_id','Item_Title','PDF_Link','Fecha_publicacion','Tags','Match_ASECORP_BBDD']]

## Aplica función de conversión de listas a strings
DOCM_sumarios_final = DOCM_sumarios_final.apply(lambda x: [list2Str(i) for i in x])

## Generar hyperlink a artículo BOE en CSV "=HYPERLINK("https://www.boe.es/boe/dias/2021/02/02/pdfs/BOE-A-2021-1474.pdf";"BOE-A-2021-1474")"
## https://www.boe.es/diario_boe/xml.php?id=## https://www.boe.es/boe/dias/2021/02/02/pdfs/BOE-A-2021-1474.pdf

DOCM_sumarios_final_CSV = DOCM_sumarios_final

DOCM_sumarios_final_CSV['Item_id'] = '=HIPERVINCULO(' + '"' + DOCM_sumarios_final_CSV['PDF_Link'] + '";' + '"' + DOCM_sumarios_final_CSV['Item_id'] + '")'                                                        

# Elimina columna PDF_Link
DOCM_sumarios_final_CSV = DOCM_sumarios_final_CSV[['Item_id','Item_Title','Fecha_publicacion','Tags','Match_ASECORP_BBDD']]

print('Guardando resultados en fichero')

DOCM_sumarios_final_CSV.to_csv("./ASECORP/Resultados_Matching_DOCM_" + today.strftime("%Y%m%d") + ".csv" ,index=False) 
