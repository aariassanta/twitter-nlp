# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from lxml import etree, html
import pandas as pd
from datetime import date, datetime
import requests
import re
import os
import shutil

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

print(today.strftime("%d/%m/%Y"))


# %%
def save_txt(txt, path):
    with open(path, 'wt') as f:
        f.write(txt)


# %% [markdown]
# ## Importa BBDD ASECORP

# %%
ASECORP_BBDD = pd.read_csv('./ASECORP/ExportNormes_20210126.csv', delimiter=';')


# %%
ASECORP_BBDD


# %%
ASECORP_BBDD_BOE = ASECORP_BBDD.loc[ASECORP_BBDD['Ambito'] == 'España']


# %%
ASECORP_BBDD_BOE


# %%
# Crea nueva columna vacía de tipo lista en ASECORP_BBDD
#ASECORP_BBDD_BOE['Tags'] = [[] for i in range(len(ASECORP_BBDD_BOE))]
#[ASECORP_BBDD_BOE['Tags'][i] = [] for i in range(len(ASECORP_BBDD_BOE))]

#ASECORP_BBDD_BOE['Tags'] = [list() for x in range(len(ASECORP_BBDD_BOE.index))]
#ASECORP_BBDD_BOE['Tags'] = ASECORP_BBDD_BOE.apply(lambda x: [], axis=1)

#ASECORP_BBDD_BOE.loc[:,'Tags'] = [ [] for i in range(len(ASECORP_BBDD_BOE)) ]
ASECORP_BBDD_BOE.insert(loc=8, column='Tags', value=['' for i in range(ASECORP_BBDD_BOE.shape[0])])

# %%
# Define expresiones REGEX para búsqueda de leyes, decretos, etc. referenciadas anteriormente
pattern = ['Ley [0-9]+\/[0-9]+','Real Decreto [0-9]+\/[0-9]+','Real Decreto Legislativo [0-9]+\/[0-9]+','Real Decreto-ley [0-9]+\/[0-9]+','Orden [A-Z]+\/[0-9]+\/[0-9]+','Orden Circular [0-9]+\/[0-9]+','Reglamento \(UE\) [0-9]+\/[0-9]+','Sentencia de [0-9]+ de [a-z]+ de [0-9]+','Sentencia [0-9]+\/[0-9]+','Orden de [0-9]+ de [a-z]+ de [0-9]+', 'Resolución de [0-9]+ de [a-z]+ de [0-9]+','Resolución [a-z]+\/[0-9]+\/[0-9]+', 'Nota de Servicio [0-9]+\/[0-9]+', 'Acuerdo multilateral M\-[0-9]+', 'Circular [0-9]+\/[0-9]+']

titulo = []
for i, row in ASECORP_BBDD_BOE.iterrows():
    titulo.append(str(row['Titulo']) + str(re.findall('|'.join(pattern), str(row['Titulo']), flags=re.IGNORECASE)))
    ASECORP_BBDD_BOE['Tags'][i] = re.findall('|'.join(pattern), str(row['Titulo']), flags=re.IGNORECASE)


# %%
ASECORP_BBDD_BOE[1200:1250]


# %%
# titulo


# %%
len(titulo)


# %%
## Busca patrones regex definidos en columna títulos del DF 
boletin = []
for i, row in ASECORP_BBDD_BOE.iterrows():
    boletin.append(str(re.findall('|'.join(pattern), row['Titulo'], flags=re.IGNORECASE)))


# %%
boletin[0:25]


# %%
## Para cada fila de la BBDD recoge la expresión REGEX encontrada y si no existe no la incluye 
## en la lista resultante llamada 'boletin'. Además si no detecta expresión la cuenta como vacía
## en variable 'n_vacios', y la añade a la lista 'vacios' para inspeccionar posteriormente 
boletin = []
vacios = []
n_vacios = 0
for i, row in ASECORP_BBDD_BOE.iterrows():
    regex_result = re.findall('|'.join(pattern), row['Titulo'], flags=re.IGNORECASE)
    if len(regex_result) != 0:
        boletin.append(re.findall('|'.join(pattern), row['Titulo'], flags=re.IGNORECASE))
    else:
        n_vacios += 1
        vacios.append(row['Titulo'])


# %%
n_vacios


# %%
vacios[0:25]


# %%
boletin[0:25]


# %%
# Flatten list of lists
boletin_ASECORP_flat_list = [item for sublist in boletin for item in sublist]


# %%
boletin_ASECORP_flat_list[0:25]


# %%
## Elimina duplicados
boletin_ASECORP_flat_list = list(set(boletin_ASECORP_flat_list))


# %%
boletin_ASECORP_flat_list[0:25]


# %%
#DOCM_sumarios_final_CSV.to_csv("./ASECORP/Resultados_Matching_DOCM_" + today.strftime("%Y%m%d") + ".csv" ,index=False) 
save_txt(str(boletin_ASECORP_flat_list), "./ASECORP/Tags_BBDD_ASECORP.txt")