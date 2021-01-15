# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
from lxml import etree, html
import pandas as pd
from datetime import date
import requests
import streamlit as st
import re

# %%
doc = etree.parse('BOE-A-2020-14372.xml')


# %%
raiz=doc.getroot()
#raiz.tag


# %%
#len(raiz)


# %%
libro=raiz[0]
#libro.tag


# %%
libro=raiz[0]
#libro[0].text


# %%
libro=raiz[1]
#libro[0].tag


# %%
libro=raiz[1]
#libro[0].text


# %%
Identificador=raiz.find("metadatos/identificador")
Titulo=raiz.find("metadatos/titulo")
URL_pdf=raiz.find("metadatos/url_pdf")


# %%
#print(Identificador.text)
#print(Titulo.text)
#print("https://www.boe.es" + URL_pdf.text)


# %%
materia=raiz.find("analisis/materias/materia")
#materia.text


# %%
#materias=raiz.findall("analisis/materias/materia")
#for materia in materias:
    #print(materia.text)





# %%
#alertas = raiz.findall("analisis/alertas/alerta")
#for alerta in alertas:
#    print(alerta.text)

# %% [markdown]
# # Recoge resumen diario del BOE de hoy

# %%

today = date.today()

# dd/mm/YYYY
hoy = today.strftime("%Y%m%d")
print("Fecha de Hoy =", hoy)

# dd
d = today.strftime("%d")
print("dia =", d)

# mm
m = today.strftime("%m")
print("mes =", m)

# YYYY
Y = today.strftime("%Y")
print("año =", Y)


# %%
URL_XML_resumen =  "https://www.boe.es/diario_boe/xml.php?id=BOE-S-" + str(hoy)


# %%
#URL_XML_resumen


# %%
#pip install requests for installation


url = URL_XML_resumen
r = requests.get(url)


# %%
def save_html(html, path):
    with open(path, 'wb') as f:
        f.write(html)
        
        
save_html(r.content, './BOEs/Resumen-BOE-' + hoy + '.xml')


# %%
#r.encoding


# %%
resumen = etree.parse('./BOEs/Resumen-BOE-' + hoy + '.xml')


# %%
raiz=resumen.getroot()
#raiz.tag


# %%
seccion = raiz.findall("sumario/diario/seccion")
#seccion


# %%
#secciones = raiz.findall("sumario/diario/seccion")
#for seccion in secciones:
    #print(seccion.text)


# %%
tabla_resumen = pd.DataFrame()


# %%
for seccion in raiz.xpath('//seccion[contains(@nombre, "I. Disposiciones generales")]'):
#for seccion in raiz.xpath('//seccion[contains(@nombre, "III. Otras disposiciones") or contains(@nombre, "I. Disposiciones generales")]'):
#for seccion in raiz.xpath('//seccion'):
    nombre_seccion = seccion.xpath('@nombre')

    for departamento in seccion:
        nombre_departamento = departamento.xpath('@nombre') 

        for epigrafe in departamento:
            nombre_epigrafe = epigrafe.xpath('@nombre')

            for item in epigrafe:
                item_id = item.xpath('@id')
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


# %%
#tabla_resumen.sort_values('Item_id')

# %% [markdown]
# # Descarga ficheros XML asociados

# %%
for item_URL in tabla_resumen['Item_URL_XML']:
    #print(URL)
    r = requests.get(item_URL)
    f = './BOEs/' + item_URL[-16:] + '.xml'
    save_html(r.content, f)


# %%

import glob
BOEs = glob.glob('./BOEs/BOE*.xml')
#print (BOEs)


# %%
tabla_materias = pd.DataFrame()

for BOE in BOEs:
    #print (BOE)
    BOE_XML = etree.parse(BOE)
    raiz=BOE_XML.getroot()

    materias = [materia.text for materia in raiz.findall('analisis/materias/materia')]
    alertas = [alerta.text for alerta in raiz.findall('analisis/alertas/alerta')]
    Item_Id = raiz.xpath(".//identificador/text()")
 
    tabla_materias = tabla_materias.append({'Item_id': Item_Id,
                                            'Materias' : materias,
                                            'Alertas' : alertas},
                                            ignore_index=True)


# %%
tabla_materias.sort_values('Item_id')


# %%
#print(raiz.tag)


# %%
for materias in raiz.xpath('.//materias'):
    materia = seccion.xpath('.//materia/text()')
    #print(materia)


# %%
#materias=raiz.findall("analisis/materias/materia")
#for materia in materias:
#    print(materia.text)


# %%
#alertas=raiz.findall("analisis/alertas/alerta")
#for alerta in alertas:
#    print(alerta.text)


# %%
#print(tabla_resumen.loc[tabla_resumen['Item_id'] == '[BOE-A-2020-14457]'])


# %%
#BOE[7:23]


# %%
#tabla_resumen['Item_id']


# %%
#tabla_materias['Item_id']


# %%
#tabla_resumen.dtypes


# %%
#tabla_resumen.set_index('Item_id').filter(like='14457', axis=0)


# %%
#tabla_resumen.dtypes


# %%
#tabla_resumen.sort_values('Item_id')


tabla_resumen['Item_id'] = tabla_resumen['Item_id'].astype(str)
tabla_materias['Item_id'] = tabla_materias['Item_id'].astype(str)
tabla_resultados = tabla_resumen.set_index('Item_id').join(tabla_materias.set_index('Item_id'))


# %%
tabla_resultados.to_csv('./BOEs/Resultados-BOE-' + hoy + '.csv', index=False)

# %% [markdown]
# ## Hace Split de Alertas y crea una fila para cada una y ordena por nombre Alerta

# %%
#tabla_resultados.reset_index()
tabla_resultados_split = tabla_resultados.Alertas.apply(pd.Series) \
    .merge(tabla_resultados, left_index = True, right_index = True) \
    .drop(["Alertas"], axis = 1) \
    .reset_index() \
    .melt(id_vars = ['Item_id','Item_Nombre','Seccion','Departamento','Epigrafe','Item_URL_XML','Materias',], value_name = "Alerta") \
    .drop("variable", axis = 1) \
    .dropna() \
    .sort_values('Alerta')

#st.write(tabla_resultados_split)

# %%

#st.markdown(
#    """<head>
#  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
#  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
#  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
#  <title></title>
#  <style>
#  body{
#      background-color: #fff;
#      font-size: 40px;
#  }
#  </style>
#</head>""", unsafe_allow_html=True
#)

st.markdown('''
<div class="jumbotron text-center" style='background-color: #fff'>
  <h1 style="margin: auto; width: 100%; text-align: center">Análisis <font color="red">BOE</font> Interactive Dashboard</h1>
  <h2></h2><p style="margin: auto; font-weight: bold; text-align: center; width: 100%;">Data Source: BOE Página Web</p>
  <h2></h2><p style="margin: auto; font-weight: 400; text-align: center; width: 100%;">Last Updated: <font color="red">''' + today.strftime("%d/%m/%Y") + '''</font></p>
  <h2></h2><p style="margin: auto; font-weight: 400; text-align: center; width: 100%;">( Best viewed on Desktop. Use Landscape mode for Mobile View. )</p>
  <h2></h2><p style="margin: auto; font-weight: bold; text-align: center; width: 100%;">______</p>
</div>

''', unsafe_allow_html=True)


def modifica_tabla_resultados(tabla):
    tabla = tabla.reset_index(drop=True)
    #tabla = tabla [['Item_id','Item_Nombre','Materias','Alerta']] # reordena columnas de tabla 
    tabla['Item_id'] = '<a href=' + "https://www.boe.es/boe/dias/" + Y + "/" + m + "/" + d + "/" + "pdfs/" + str(tabla['Item_id'][0])[2:-2] + ".pdf"+ ' ' + 'target="_blank"' + '><div>' + tabla['Item_id'] + '</div></a>' # Añade url link  pdf a Item_id
    #tabla['Item_id'] = '<a href=' + tabla['Item_URL_XML'] + ' ' + 'target="_blank"' + '><div>' + tabla['Item_id'] + '</div></a>' # Añade url link XML a Item_id
    tabla.drop(['Epigrafe','Departamento','Seccion','Item_URL_XML'], axis='columns', inplace=True)
    df_html = tabla.reset_index(drop=True).to_html(index='True', classes="table-hover", escape=False) # Utiliza Clase table-hover de Bootstrap
    df_html = df_html.replace("dataframe", "")  # Elimina clase por defecto dataframe
    df_html = df_html.replace('border="1"', 'border="2"')  # Incrementa tamaño línea borde tabla
    df_html = df_html.replace("<table", '<table style="font-size:12px; text-align: center; width: 100%" ') # Cambia tamaño fuente a 15px
    df_html = df_html.replace("<th>"+ tabla.columns[0], '<th style="text-align: center">'+ tabla.columns[0]) # Cambia alineación a header Columna 1
    df_html = df_html.replace("<th>"+ tabla.columns[1], '<th style="text-align: center">'+ tabla.columns[1]) # Cambia alineación a header Columna 2
    df_html = df_html.replace("<th>"+ tabla.columns[2], '<th style="text-align: center">'+ tabla.columns[2]) # Cambia alineación a header Columna 2
    df_html = df_html.replace("<th>"+ tabla.columns[2], '<th style="text-align: center">'+ tabla.columns[3]) # Cambia alineación a header Columna 2

    return df_html

#st.header('Tabla Resultados')
#st.write(tabla_resultados.reset_index())
#st.write(modifica_tabla_resultados(tabla_resultados.reset_index()), unsafe_allow_html=True)

# Selecciona Alertas de filtro

st.header('')
st.header('Selecciona Alertas')

options =  list(tabla_resultados_split['Alerta'].unique())
defecto= list(tabla_resultados_split['Alerta'].unique())

if st.button('Selecciona todas'):
    defecto = list(tabla_resultados_split['Alerta'].unique())

Alerta = st.multiselect('', options, default=defecto) 
#st.write('Has seleccionado:', Alerta)

st.header('')
st.header('Tabla Resultante')

#st.markdown('''
#<div class="jumbotron text-center" style='background-color: #fff'>
#  <h2></h2><p style="margin: auto; font-weight: 400; text-align: left; width: 100%;">Tabla Resultante</p>
#</div>
#
#''', unsafe_allow_html=True)

# st.header('Tabla Resultante')

# Procesa tabla_resultados_split para presentación

tabla_resultados_presentacion = modifica_tabla_resultados(tabla_resultados_split[tabla_resultados_split['Alerta'].isin(Alerta)])

st.write(tabla_resultados_presentacion, unsafe_allow_html=True)


#tabla_resultados_split = tabla_resultados_split.reset_index(drop=True).drop(['Epigrafe','Departamento','Seccion','Item_URL_XML'], axis='columns')

# --------------------------------------------------------------------------------------
# DOGC
# --------------------------------------------------------------------------------------

URL_HTML_resumen =  "https://dogc.gencat.cat/es/index.html?newLang=es_ES&language=es_ES"

## carga página HTML y genera árbol

response = requests.get(URL_HTML_resumen)
tree = html.fromstring(response.text)

## Recoge Nombre Secciones Sumario

secciones = tree.xpath('//*[@id="sumari"]/ul/li')
#print(secciones)
df_secciones_sumarios = pd.DataFrame()
for seccion in secciones:
    seccion = seccion.xpath('./form/a/text()')
    seccion = re.sub('(\\r|\\n|\\t)+', '', seccion[0])
    print(seccion[1:-1])
    df_secciones_sumarios = df_secciones_sumarios.append({'Seccion': seccion[1:-1]}, ignore_index=True)

## Recoge Valores para formar URLs Secciones Sumario

URL_base_sumario = tree.xpath('//*[@id="sumari"]/ul/li[1]/form/@action')

df_URL_sumarios = pd.DataFrame()
for seccion in secciones:    
    cadena = ''
    for input in seccion.xpath('./form'):
        argumentos = input.xpath('./input/@name')
        valores = input.xpath('./input/@value')
        #print(argumentos, valores)

    for indice in range(len(argumentos)):
        cadena += argumentos[indice] + '=' + valores[indice] + '&'

    URL_sumario = 'https://dogc.gencat.cat' + str(URL_base_sumario[0]) + '?' + str(cadena[:-1])
    print(URL_sumario)
    df_URL_sumarios = df_URL_sumarios.append({'URL_Seccion': URL_sumario}, ignore_index=True)

## Concatena en df columnas Sccion y URL de sumarios 

df_sumarios = pd.concat([df_secciones_sumarios, df_URL_sumarios], axis=1)

### Recoge Items en Seccion Disposiciones

response = requests.get(df_sumarios['URL_Seccion'][0])
sumario_HTML = html.fromstring(response.text)

#seccion = sumario_HTML.xpath('//*[@id="disposicions"]/div[1]/text()')
seccion = sumario_HTML.xpath('//*[@id="disposicions"]/div/text()')
bloques = sumario_HTML.xpath('//*[@id="disposicions"]')
df_disposiciones = pd.DataFrame(columns=['Seccion','Item_Name','PDF_link'])
for bloque in bloques: 
    item_name = bloque.xpath('./div/p/text()')
    #item_name = re.sub('(\\r|\\n|\\t)+', '', item_name[0])
    pdf_link = bloque.xpath('./div/div/a[4]/@href')

for row in range(len(pdf_link)):
    df_disposiciones = df_disposiciones.append({'Item_Name': re.sub('(\\r|\\n|\\t)+', '', item_name[row]),
                                            'PDF_link' : pdf_link[row],
                                            'Seccion' : seccion[0][:-1]},
                                            ignore_index=True)

#df_disposiciones

def modifica_tabla_resultados_DOGC(tabla):
    tabla = tabla.reset_index(drop=True)
    tabla['Item_Name'] = '<a href=' + tabla['PDF_link'] + ' ' + 'target="_blank"' + '><div>' + tabla['Item_Name'] + '</div></a>' # Añade url link  pdf a Item_id
    tabla.drop(['PDF_link'], axis='columns', inplace=True)
    df_html = tabla.reset_index(drop=True).to_html(index='True', classes="table-hover", escape=False) # Utiliza Clase table-hover de Bootstrap
    df_html = df_html.replace("dataframe", "")  # Elimina clase por defecto dataframe
    df_html = df_html.replace('border="1"', 'border="2"')  # Incrementa tamaño línea borde tabla
    df_html = df_html.replace("<table", '<table style="font-size:12px; text-align: center; width: 100%" ') # Cambia tamaño fuente a 15px
    df_html = df_html.replace("<th>"+ tabla.columns[0], '<th style="text-align: center">'+ tabla.columns[0]) # Cambia alineación a header Columna 1
    df_html = df_html.replace("<th>"+ tabla.columns[1], '<th style="text-align: center">'+ tabla.columns[1]) # Cambia alineación a header Columna 2
    
    return df_html

st.header('')
st.header('DOGC disposiciones')


tabla_resultados_presentacion_DOGC = modifica_tabla_resultados_DOGC(df_disposiciones)

st.write(tabla_resultados_presentacion_DOGC, unsafe_allow_html=True)

# --------------------------------------------------------------------------------------
# DOUE
# --------------------------------------------------------------------------------------

URL_HTML_resumen =  "https://eur-lex.europa.eu/oj/direct-access.html?locale=es"

## carga página HTML y genera árbol

response = requests.get(URL_HTML_resumen)
tree = html.fromstring(response.text)

## Recoge Nombre Secciones Sumario

secciones = tree.xpath('//*[@id="MainContent"]/div[2]/div[2]/div/table/tbody/tr[1]')
#print(secciones)

## Recoge Valores para formar URLs Secciones Sumario

df_secciones_sumarios = pd.DataFrame()
for seccion in secciones:
    seccion_name = seccion.xpath('./td[2]/a/text()')
    seccion_URL = seccion.xpath('./td[2]/a/@href')
    #seccion = re.sub('(\\r|\\n|\\t)+', '', seccion)
    #print(seccion_name)
    #print(seccion_URL)

for row in range(len(seccion_name)):
    df_secciones_sumarios = df_secciones_sumarios.append({'Seccion': seccion_name[row],
                                            'Seccion_link' : 'https://eur-lex.europa.eu' + seccion_URL[row][4:]},
                                            ignore_index=True)

df_legislaciones = pd.DataFrame()

for URL in df_secciones_sumarios['Seccion_link']:
    
    ### Recoge Items en Seccion Legislación

    #print(URL)
    response = requests.get(URL)
    sumario_HTML = html.fromstring(response.text)

    documentos = sumario_HTML.xpath('//*[@class="oj-ti-doc-dur"]/a[1]/text()[1]')
    documentos_URL = sumario_HTML.xpath('//*[@class="oj-ti-doc-dur"]/a[1]/@href')

    for row in range(len(documentos)):
        df_legislaciones = df_legislaciones.append({'Seccion': 'L' + documentos_URL[row][-7:-4],
                                        'Item_Name': documentos[row],
                                        'Item_Link': 'https://eur-lex.europa.eu' + documentos_URL[row][10:],
                                        'PDF_Link': ''},
                                        ignore_index=True)


### Recoge PDF link en Items Legislación

row = 0
for link in df_legislaciones['Item_Link']:

    response = requests.get(link)
    sumario_HTML = html.fromstring(response.text)

    PDF_Link = sumario_HTML.xpath('//*[@id="format_language_table_PDF_ES"]/@href')
    df_legislaciones['PDF_Link'].iloc[row] = 'https://eur-lex.europa.eu' + PDF_Link[0][10:]

    row += 1

### Ordena columnas    

df_legislaciones = df_legislaciones[['Seccion', 'Item_Name', 'Item_Link', 'PDF_Link']]

def modifica_tabla_resultados_DOUE(tabla):
    tabla = tabla.reset_index(drop=True)
    tabla['Item_Name'] = '<a href=' + tabla['PDF_Link'] + ' ' + 'target="_blank"' + '><div>' + tabla['Item_Name'] + '</div></a>' # Añade url link  pdf a Item_id
    tabla.drop(['PDF_Link', 'Item_Link'], axis='columns', inplace=True)
    df_html = tabla.reset_index(drop=True).to_html(index='True', classes="table-hover", escape=False) # Utiliza Clase table-hover de Bootstrap
    df_html = df_html.replace("dataframe", "")  # Elimina clase por defecto dataframe
    df_html = df_html.replace('border="1"', 'border="2"')  # Incrementa tamaño línea borde tabla
    df_html = df_html.replace("<table", '<table style="font-size:12px; text-align: center; width: 100%" ') # Cambia tamaño fuente a 15px
    df_html = df_html.replace("<th>"+ tabla.columns[0], '<th style="text-align: center">'+ tabla.columns[0]) # Cambia alineación a header Columna 1
    df_html = df_html.replace("<th>"+ tabla.columns[1], '<th style="text-align: center">'+ tabla.columns[1]) # Cambia alineación a header Columna 2
    
    return df_html

st.header('')
st.header('DOUE Legislación')


tabla_resultados_presentacion_DOUE = modifica_tabla_resultados_DOUE(df_legislaciones)

st.write(tabla_resultados_presentacion_DOUE, unsafe_allow_html=True)