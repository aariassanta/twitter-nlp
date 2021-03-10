from lxml import etree, html
import pandas as pd
from datetime import date, datetime
import requests
import re
import os
import shutil


def save_txt(txt, path):
	with open(path, 'wt') as f:
		f.write(txt)

# Define expresiones REGEX para búsqueda de leyes, decretos, etc. referenciadas anteriormente
pattern = ['Ley [0-9]+\/[0-9]+',
           'Ley Orgánica [0-9]+\/[0-9]+',
           'Decreto [0-9]+\/[0-9]+',
           'Real Decreto [0-9]+\/[0-9]+',
           'Real Decreto Legislativo [0-9]+\/[0-9]+','Real Decreto-ley [0-9]+\/[0-9]+',
           'Orden [A-Z]+\/[0-9]+\/[0-9]+','Orden [0-9]+\/[0-9]+',
           'Orden de [0-9]+\/[0-9]+\/[0-9]+','Orden Circular [0-9]+\/[0-9]+',
           'Directiva [0-9]+\/[0-9]+','Directiva [0-9]+\/[0-9]+\/CE','Directiva \(UE\) [0-9]+\/[0-9]+',
           'Reglamento [0-9]+\/[0-9]+','Reglamento n\º [0-9]+\/[0-9]+','Reglamento \(UE\) [0-9]+\/[0-9]+','Reglamento \(UE\) n\º [0-9]+\/[0-9]+','Reglamento \(CE\) n\º [0-9]+\/[0-9]+','Reglamento \(CEE\) n\º [0-9]+\/[0-9]+',
           'Reglamento n\.\º [0-9]+\/[0-9]+','Reglamento \(UE\) n\.\º [0-9]+\/[0-9]+','Reglamento \(CE\) n\.\º [0-9]+\/[0-9]+','Reglamento \(CEE\) n\.\º [0-9]+\/[0-9]+',
           'Reglamento de Ejecución \(UE\) [0-9]+\/[0-9]+','Reglamento de Ejecución \(UE\) n\º [0-9]+\/[0-9]+','Reglamento de Ejecución [0-9]+\/[0-9]+',
           'Reglamento de Ejecución \(UE\) n\.\º [0-9]+\/[0-9]+',
           'Reglamento Delegado [0-9]+\/[0-9]+','Reglamento Delegado \(UE\) [0-9]+\/[0-9]+','Reglamento Delegado \(UE\) n\º [0-9]+\/[0-9]+',
           'Reglamento Delegado \(UE\) n\.\º [0-9]+\/[0-9]+',
           'Sentencia de [0-9]+ de [a-z]+ de [0-9]+','Sentencia [0-9]+\/[0-9]+',
           'Orden de [0-9]+ de [a-z]+ de [0-9]+', 
           'Resolución de [0-9]+ de [a-z]+ de [0-9]+','Resolución [a-z]+\/[0-9]+\/[0-9]+','Resolución de [0-9]+\/[0-9]+\/[0-9]+', 
           'Nota de Servicio [0-9]+\/[0-9]+', 
           'Acuerdo multilateral M\-[0-9]+', 'Acuerdo Multilateral RID [0-9]+\/[0-9]+', 
           'Circular [0-9]+\/[0-9]+', 
           'Decisión [0-9]+\/[0-9]+','Decisión \(UE\) [0-9]+\/[0-9]+', 'Decisión de Ejecución \(UE\) [0-9]+\/[0-9]+',
           'Instrucción IS\-[0-9]+']

def devuelve_patrones():
    return (pattern)

def tagea_BBDD_ASECORP(ambitos=['todos']):

	# ## Importa BBDD ASECORP
	ASECORP_BBDD = pd.read_csv(
		'./ASECORP/ExportNormes_20210126.csv', delimiter=';')

	# Elimina filas con Nombre de Título vacío
	ASECORP_BBDD.dropna(subset=['Titulo'], inplace=True)

	# crea lista de ámbitos teritoriales
	lista_ambitos = []
	if ambitos == ['todos']:
		# recoge valores de columna Ambito
		[lista_ambitos.append(ambito) for ambito in ASECORP_BBDD['Ambito']]
		# crea lista con valores únicos
		ambitos = set(lista_ambitos)

	# ## Selecciona registros por ámbito territorial
	ASECORP_BBDD_FINAL = ASECORP_BBDD[ASECORP_BBDD['Ambito'].isin(ambitos)]

	# Crea nueva columna de vacía de tipo lista en ASECORP_BBDD
	ASECORP_BBDD_FINAL.insert(loc=8, column='Tags', value=[
							  '' for i in range(ASECORP_BBDD_FINAL.shape[0])])

	# Define expresiones REGEX para búsqueda de leyes, decretos, etc. referenciadas anteriormente
	#pattern = ['Ley [0-9]+\/[0-9]+',
    #         'Ley Orgánica [0-9]+\/[0-9]+',
    #         'Decreto [0-9]+\/[0-9]+', 
    #         'Real Decreto [0-9]+\/[0-9]+', 
    #         'Real Decreto Legislativo [0-9]+\/[0-9]+', 
    #         'Real Decreto-ley [0-9]+\/[0-9]+', 
    #         'Orden [A-Z]+\/[0-9]+\/[0-9]+', 
    #         'Orden Circular [0-9]+\/[0-9]+',
    #         'Reglamento \(UE\) [0-9]+\/[0-9]+', 
    #         'Reglamento de Ejeución \(UE\) [0-9]+\/[0-9]+', 
    #         'Sentencia de [0-9]+ de [a-z]+ de [0-9]+', 
    #         'Sentencia [0-9]+\/[0-9]+', 
    #         'Orden de [0-9]+ de [a-z]+ de [0-9]+', 
    #         'Resolución de [0-9]+ de [a-z]+ de [0-9]+',
    #         'Resolución [a-z]+\/[0-9]+\/[0-9]+', 
    #         'Nota de Servicio [0-9]+\/[0-9]+',
    #         'Acuerdo multilateral M\-[0-9]+', 
    #         'Acuerdo Multilateral RID [0-9]+\/[0-9]+', 
    #         'Circular [0-9]+\/[0-9]+', 
    #         'Decisión \(UE\) [0-9]+\/[0-9]+', 
    #         'Decisión de Ejecución \(UE\) [0-9]+\/[0-9]+', 
    #         'Instrucción IS\-[0-9]+']
	
	# Genera Tags en columna creada
	titulo = []
	for i, row in ASECORP_BBDD_FINAL.iterrows():
		titulo.append(str(row['Titulo']) + str(re.findall('|'.join(pattern),
														  str(row['Titulo']), flags=re.IGNORECASE)))
		ASECORP_BBDD_FINAL['Tags'][i] = re.findall(
			'|'.join(pattern), str(row['Titulo']), flags=re.IGNORECASE)

	# Busca patrones regex definidos en columna títulos del DF
	boletin = []
	for i, row in ASECORP_BBDD_FINAL.iterrows():
		boletin.append(
			str(re.findall('|'.join(pattern), row['Titulo'], flags=re.IGNORECASE)))

	# Para cada fila de la BBDD recoge la expresión REGEX encontrada y si no existe no la incluye
	# en la lista resultante llamada 'boletin'. Además si no detecta expresión la cuenta como vacía
	# en variable 'n_vacios', y la añade a la lista 'vacios' para inspeccionar posteriormente
	boletin = []
	vacios = []
	n_vacios = 0
	for i, row in ASECORP_BBDD_FINAL.iterrows():
		regex_result = re.findall(
			'|'.join(pattern), row['Titulo'], flags=re.IGNORECASE)
		if len(regex_result) != 0:
			boletin.append(re.findall('|'.join(pattern),
									  row['Titulo'], flags=re.IGNORECASE))
		else:
			n_vacios += 1
			vacios.append(row['Titulo'])

	# Flatten list of lists
	boletin_ASECORP_flat_list = [
		item for sublist in boletin for item in sublist]

	# Elimina duplicados
	boletin_ASECORP_flat_list = list(set(boletin_ASECORP_flat_list))

	#DOCM_sumarios_final_CSV.to_csv("./ASECORP/Resultados_Matching_DOCM_" + today.strftime("%Y%m%d") + ".csv" ,index=False)
	#save_txt(str(boletin_ASECORP_flat_list), "./ASECORP/Tags_BBDD_ASECORP.txt")

	return (str(boletin_ASECORP_flat_list), ASECORP_BBDD_FINAL, ambitos)


if __name__ == "__main__":

	tagea_BBDD_ASECORP()
