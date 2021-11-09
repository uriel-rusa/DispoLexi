import os
from flask import Flask
import json
'''from flask import flash
from flask import request, url_for, send_from_directory
from flask import make_response
from flask import redirect
from flask import render_template
from flask_bootstrap import Bootstrap'''
#from werkzeug.utils import secure_filename
#from app import get_idlv
import datetime
import zipfile
import shutil
#import string
#import re
from nltk.tokenize import word_tokenize
#from nltk.corpus import stopwords
import io 
#import shutil
import random

#from collections import Counter
'''from math import pi
import pandas as pd
from bokeh.io import output_file, show
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.embed import components #biblioteca agregada 15/10/2020
from bokeh.resources import CDN'''
import csv #agregado el 9/oct/21
#from flask_mail import Mail, Message#Instalado con pip3 octubre 2021




ALLOWED_EXTENSIONS = {'zip'}

#Verifica si el archivo a subir tiene la extension valida
def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def carga_stop_words():
	file = open('app/stop_words.txt', 'r', encoding="latin-1")
	text = file.read()
	file.close()

	tokens = word_tokenize(text)
	#print("INICIO DE LISTA")
	#print(tokens)
	#print("FIN DE LISTA")
	stop_words = set ('')
	for x in tokens:
		stop_words.add(x)
	#print("INICIO LISTA DE STOPWORDS")
	#print(stop_words)
	#print("FIN LISTA DE STOPWORDS")
	return stop_words
		
def cantidad_de_palabras_iguales(lista_palabras_uno, lista_palabras_dos):
	#print("funcion de palabras iguales")
	contador = 0
	for palabra in lista_palabras_uno:
		if palabra in lista_palabras_dos:
			contador +=1

	return contador

def crea_archivo_csv(lista):
	archivo_csv = open('./app/static/csv/DiagramaSankey.csv', 'w', newline ='')
	with archivo_csv:
		writer = csv.writer(archivo_csv)
		writer.writerows(lista)
	archivo_csv.close()

def creaCSVlista(lista_de_palabras, lista_IDLV, poblacion):
	#print("########################### Poblacion: ",poblacion)
	#print("LISTA IDLV: ",lista_IDLV)
	#print("LISTA DE PALABRAS:",lista_de_palabras)
	lista = []
	lista.append(['palabras', 'valor'])
	for x, n in zip(lista_de_palabras, lista_IDLV):
		lista.append([x,n])

	#print("LISTA:",lista)
	ruta = 'app/static/csv/' + poblacion + '.csv'
	archivo_csv = open(ruta, 'w', newline ='')
	with archivo_csv:
		writer = csv.writer(archivo_csv)
		writer.writerows(lista)
	archivo_csv.close()
	#print("Se escribio el archivo csv....")

def sankey(dic_Poblaciones, lista_poblaciones):
	dic_palabras = dic_Poblaciones[lista_poblaciones[0]]['Palabras'] #Se crea un diccionario que contiene el diccionario de palabras de la primer poblacion
	lista_palabras = []
	lista_palabras_reversed = []
	poblaciones = len(lista_poblaciones)
	informacion_csv = []
	informacion_csv.append(["source","target","value"])
	#print("--------------LISTA: ",informacion_csv)
	#print("++++++++++LISTA POBLACIONES: ",lista_poblaciones)
	#print("++++++++++CANTIDAD DE POBLACIONES: ",poblaciones)


	contador = 1
	for x in range (0,len(lista_poblaciones)-1):#Primer for para empezar con la primer poblacion, se repetirán las instrucciones el número de ploblaciones que haya
		lista_palabras = dic_Poblaciones[lista_poblaciones[x]]['Palabras']
		lista_palabras = list(lista_palabras.keys()) # lista de palabras total
		total_palabras = len(lista_palabras)
		division = total_palabras // 4
		#print("total de palabras: ", total_palabras)
		#print("division: ", division)

		lista_palabras_uno = []# Se declara para guardar el numero de palabras introducido por el usuario por población
		lista_palabras_dos = []
		lista_palabras_tres = []
		lista_palabras_cuatro = []
		listas_palabras_poblacion = []
		contador_dos = 0
		for z in lista_palabras:#Es para separar las palabras de la población en cuatro catro listas
			contador_dos += 1

			if contador_dos <= division:
				lista_palabras_uno.append(z) #Contiene las palabras que se van a usar de la lista de palabras de la poblacion a comparar
			if (contador_dos <= division*2) and (division < contador_dos):
				lista_palabras_dos.append(z)
			if (contador_dos <= division*3) and (division*2 < contador_dos):
				lista_palabras_tres.append(z)
			if (contador_dos <= division*4) and (division*3 < contador_dos):
				lista_palabras_cuatro.append(z)

		#print("PALABRAS UNO DE POBLACION ", lista_poblaciones[x], ": \n", lista_palabras_uno)
		#print("PALABRAS DOS DE POBLACION ", lista_poblaciones[x], ": \n", lista_palabras_dos)
		#print("PALABRAS TRES DE POBLACION ", lista_poblaciones[x], ": \n", lista_palabras_tres)
		#print("PALABRAS CUATRO DE POBLACION ", lista_poblaciones[x], ": \n", lista_palabras_cuatro)
		listas_palabras_poblacion.append(lista_palabras_uno)
		listas_palabras_poblacion.append(lista_palabras_dos)
		listas_palabras_poblacion.append(lista_palabras_tres)
		listas_palabras_poblacion.append(lista_palabras_cuatro)

		for k in range(contador, len(lista_poblaciones)):
			lista_palabras_temp = []
			lista_palabras_temp = dic_Poblaciones[lista_poblaciones[k]]['Palabras']
			lista_palabras_temp = list(lista_palabras_temp.keys()) # lista de palabras total de la población k
			division = len(lista_palabras_temp)//4


			lista_palabras_uno_temp = []# Se declara para guardar el numero de palabras introducido por el usuario por población
			lista_palabras_dos_temp = []
			lista_palabras_tres_temp = []
			lista_palabras_cuatro_temp = []

			contador_dos = 0
			for j in lista_palabras_temp:
				contador_dos += 1

				if contador_dos <= division:
					lista_palabras_uno_temp.append(j)
				if (contador_dos <= division*2) and (division < contador_dos):
					lista_palabras_dos_temp.append(j)
				if (contador_dos <= division*3) and (division*2 < contador_dos):
					lista_palabras_tres_temp.append(j)
				if (contador_dos <= division*4) and (division*3 < contador_dos):
					lista_palabras_cuatro_temp.append(j)


			listas_palabras_temp = []
			listas_palabras_temp.append(lista_palabras_uno_temp)
			listas_palabras_temp.append(lista_palabras_dos_temp)
			listas_palabras_temp.append(lista_palabras_tres_temp)
			listas_palabras_temp.append(lista_palabras_cuatro_temp)

			#print("LISTA DE LISTAS: ",listas_palabras_temp)
			#print("///////////POBLACION: ",lista_poblaciones[k])
			#print("///////////BUMERO PALABRAS: ",len(lista_palabras_temp))
			#print("///////////DIVISION: ",division)
			
			cantidad_de_palabras = cantidad_de_palabras_iguales(listas_palabras_poblacion[0], listas_palabras_temp[0])
			#print ("Cantidad de palabras iguales: ", cantidad_de_palabras)
			for n in range(0,4):
				for m in range(0,4):
					cantidad_de_palabras = cantidad_de_palabras_iguales(listas_palabras_poblacion[n],listas_palabras_temp[m])
					#Los siguiguientes if son para ver en que grupo de relevancia se encuentran las palabras iguales de las dos listas comparadas
					#Los primeros cuatro if son para el grupo de palabras muy relevantes de la poblacion x y se va cambiando en cada if la relevancia de la poblacion k
					if (n == 0) and (m == 0):
						texto_uno = lista_poblaciones[x] + " (Palabras muy relevantes)"
						texto_dos = lista_poblaciones[k] + " (Palabras muy relevantes)"
						informacion_csv.append([texto_uno, texto_dos, cantidad_de_palabras])
						#print("INFORMACION CSV: ",informacion_csv)
					if (n == 0) and (m == 1):
						texto_uno = lista_poblaciones[x] + " (Palabras muy relevantes)"
						texto_dos = lista_poblaciones[k] + " (Palabras relevantes)"
						informacion_csv.append([texto_uno, texto_dos, cantidad_de_palabras])
						#print("INFORMACION CSV: ",informacion_csv)
					if (n == 0) and (m == 2):
						texto_uno = lista_poblaciones[x] + " (Palabras muy relevantes)"
						texto_dos = lista_poblaciones[k] + " (Palabras poco relevantes)"
						informacion_csv.append([texto_uno, texto_dos, cantidad_de_palabras])
						#print("INFORMACION CSV: ",informacion_csv)
					if (n == 0) and (m == 3):
						texto_uno = lista_poblaciones[x] + " (Palabras muy relevantes)"
						texto_dos = lista_poblaciones[k] + " (Palabras muy poco relevantes)"
						informacion_csv.append([texto_uno, texto_dos, cantidad_de_palabras])
						#print("INFORMACION CSV: ",informacion_csv)


					'''Los siguientes if son para el grupo de palabras relevantes de la poblacion x 
					y se va cambiando la relevancia de la  poblacion k'''
					if (n == 1) and (m == 0):
						texto_uno = lista_poblaciones[x] + " (Palabras relevantes)"
						texto_dos = lista_poblaciones[k] + " (Palabras muy relevantes)"
						informacion_csv.append([texto_uno, texto_dos, cantidad_de_palabras])
						#print("INFORMACION CSV: ",informacion_csv)
					if (n == 1) and (m == 1):
						texto_uno = lista_poblaciones[x] + " (Palabras relevantes)"
						texto_dos = lista_poblaciones[k] + " (Palabras relevantes)"
						informacion_csv.append([texto_uno, texto_dos, cantidad_de_palabras])
						#print("INFORMACION CSV: ",informacion_csv)
					if (n == 1) and (m == 2):
						texto_uno = lista_poblaciones[x] + " (Palabras relevantes)"
						texto_dos = lista_poblaciones[k] + " (Palabras poco relevantes)"
						informacion_csv.append([texto_uno, texto_dos, cantidad_de_palabras])
						#print("INFORMACION CSV: ",informacion_csv)
					if (n == 1) and (m == 3):
						texto_uno = lista_poblaciones[x] + " (Palabras relevantes)"
						texto_dos = lista_poblaciones[k] + " (Palabras muy poco relevantes)"
						informacion_csv.append([texto_uno, texto_dos, cantidad_de_palabras])
						#print("INFORMACION CSV: ",informacion_csv)


					'''Los siguientes if son para el grupo de palabras poco relevantes de la poblacion x 
					y se va cambiando la relevancia de la  poblacion k'''
					if (n == 2) and (m == 0):
						texto_uno = lista_poblaciones[x] + " (Palabras poco relevantes)"
						texto_dos = lista_poblaciones[k] + " (Palabras muy relevantes)"
						informacion_csv.append([texto_uno, texto_dos, cantidad_de_palabras])
						#print("INFORMACION CSV: ",informacion_csv)
					if (n == 2) and (m == 1):
						texto_uno = lista_poblaciones[x] + " (Palabras poco relevantes)"
						texto_dos = lista_poblaciones[k] + " (Palabras relevantes)"
						informacion_csv.append([texto_uno, texto_dos, cantidad_de_palabras])
						#print("INFORMACION CSV: ",informacion_csv)
					if (n == 2) and (m == 2):
						texto_uno = lista_poblaciones[x] + " (Palabras poco relevantes)"
						texto_dos = lista_poblaciones[k] + " (Palabras poco relevantes)"
						informacion_csv.append([texto_uno, texto_dos, cantidad_de_palabras])
						#print("INFORMACION CSV: ",informacion_csv)
					if (n == 2) and (m == 3):
						texto_uno = lista_poblaciones[x] + " (Palabras poco relevantes)"
						texto_dos = lista_poblaciones[k] + " (Palabras muy poco relevantes)"
						informacion_csv.append([texto_uno, texto_dos, cantidad_de_palabras])
						#print("INFORMACION CSV: ",informacion_csv)


					'''Los siguientes if son para el grupo de palabras muy poco relevantes de la poblacion x 
					y se va cambiando la relevancia de la  poblacion k'''
					if (n == 3) and (m == 0):
						texto_uno = lista_poblaciones[x] + " (Palabras muy poco relevantes)"
						texto_dos = lista_poblaciones[k] + " (Palabras muy relevantes)"
						informacion_csv.append([texto_uno, texto_dos, cantidad_de_palabras])
						#print("INFORMACION CSV: ",informacion_csv)
					if (n == 3) and (m == 1):
						texto_uno = lista_poblaciones[x] + " (Palabras muy poco relevantes)"
						texto_dos = lista_poblaciones[k] + " (Palabras relevantes)"
						informacion_csv.append([texto_uno, texto_dos, cantidad_de_palabras])
						#print("INFORMACION CSV: ",informacion_csv)
					if (n == 3) and (m == 2):
						texto_uno = lista_poblaciones[x] + " (Palabras muy poco relevantes)"
						texto_dos = lista_poblaciones[k] + " (Palabras poco relevantes)"
						informacion_csv.append([texto_uno, texto_dos, cantidad_de_palabras])
						#print("INFORMACION CSV: ",informacion_csv)
					if (n == 3) and (m == 3):
						texto_uno = lista_poblaciones[x] + " (Palabras muy poco relevantes)"
						texto_dos = lista_poblaciones[k] + " (Palabras muy poco relevantes)"
						informacion_csv.append([texto_uno, texto_dos, cantidad_de_palabras])
						




		contador += 1
	#print("CSV",informacion_csv)
	crea_archivo_csv(informacion_csv)




	#lista_palabras = list(dic_palabras.keys())#Se enlistan las palabras del diccionario de la primer poblacion, esto se hace para que después se puedan comparar esas palabras con las demas listas de palabras de las otras poblaciones	
	#for x in reversed(dic_palabras):
		#lista_palabras_reversed.append(x)

def detecta_palabras_iguales(dic_Poblaciones, lista_poblaciones, cantidad_de_palabras, opcion_tipo_palabras):
	regresa_dic = {} #Se declara el diccionario que al final contendrá las palabras que coincideo y sus respectivos valores de idlv por palabra de poblacion
	lista_palabras_nueva = []#Se declara la lista que contendrá las palabras que conciden en todas las poblaciones 
	idlv_lista = []#Se declara la lista que contendra los valores de idlv de las palabras que coinciden
	dic_palabras = dic_Poblaciones[lista_poblaciones[0]]['Palabras'] #Se crea un diccionario que contiene el diccionario de palabras de la primer poblacion
	lista_palabras = []


	#Se revisa si la opcion es 1 o 2, si es 1 se buscan las palabras con mayor IDLV y si es 2 se buscan las de menor IDLV
	if opcion_tipo_palabras == '1':
		#print("OPCION 1")
		lista_palabras = list(dic_palabras.keys())#Se enlistan las palabras del diccionario de la primer poblacion, esto se hace para que después se puedan comparar esas palabras con las demas listas de palabras de las otras poblaciones	
	
	elif opcion_tipo_palabras == '2':#Si la opcion es 2, se enlistan las palabras pero de menor a mayor IDLV
		#print("OPCION 2")
		for x in reversed(dic_palabras):
			lista_palabras.append(x)

	for z in lista_palabras:#Se inicializa el for para iterar z en la lista de palabras que sacamos de una poblacion
		contador = 0#Contador que nos ayudará a saber en cuantas poblaciones esta la palabra de la variable z
		for x in lista_poblaciones:#Otro for para iterar en la distintas poblacines que hay
			contador_dos = 1
			palabras = dic_Poblaciones[x]['Palabras'] #Se extrae el diccionario de las palabras de la poblacion x
			palabras = list(palabras.keys())#Se enlistan las palabras que contiene el diccionario de palabras
			if z in palabras: #Condicional para saber si la palabra z esta en la lista de palabras de la poblacion x
				#print("la palabra: ", z, "esta en: ", x)
				contador += 1 #Si la palabra se encuentra en la poblacion x, el contador se incrementa en 1 y revisará la siguienta palabra z de la lista_palabras
		
		#Despues de revisar todas las palabras de lista_palabras en la lista de palabras de pla poblacion x se procede a revisar si estuvo en todas las poblaciones la palabra
		if contador == len(lista_poblaciones) and len(lista_palabras_nueva) < cantidad_de_palabras: #Si el contador es igual al numero de poblaciones, quiere decir que estuvo la palabra en todas las listas de palabras de las poblaciones
			#print ("LA PALABRA ",z,"ESTA EN TODAS LAS POBLACIONES")
			lista_palabras_nueva.append(z) #Se agrega la palabra a la lista de palabras lista_palabras_nueva
			#Al final se obtiene una lista de todas las palabras que coinciden en todas las poblaciones

	#print("LISTA PALABRAS: ",lista_palabras_nueva)
	regresa_dic['Palabras'] = lista_palabras_nueva # se agrega la clave 'Palabras' y la lista de palabras lista_palabras_nueva al diccionario regresa_dic

	#Ahora necesitamos sacar los valore de IDLV de cada palabra de la lista nueva y por poblacion
	for x in lista_poblaciones:#el for recorre las poblaciones
		idlv_lista = []#Se inicializa la lista idlv_lista en vacio
		dic_palabras = dic_Poblaciones[x]['Palabras'] #se extrae el diccionario de palabras de la poblacion x
		#Teniendo el diccionario de palabras de la poblacion x, se procede a extraer el valor de idlv por palabra
		for z in lista_palabras_nueva: #Se recorre la lista de palabras nueva que contiene las palabras que coinciden en todas las poblaciones
			idlv_lista.append(dic_palabras[z]) #Se agrega el valor de idlv a la lista idlv_lista, se extrae con dic_palabras[z] donde z es la clave para buscar el valor
		#print("VALOR IDLV de ",x, idlv_lista)
		
		dic_temporal = {}#Contiene el valor de IDLV y color
		color = "rgba("
		for k in range(3):
			color = color + str(random.randrange(255)) + ","

		#dic_Palabras[x]['Color'] = color
		#print("color poblacion",x,color)
		dic_temporal['Color'] = color
		dic_temporal['IDLV'] = idlv_lista 
		regresa_dic[x] = dic_temporal #Se crea una clave con el nombre de la poblacion x en el diccionario regresa_dic y se le agrega la lista idlv_lista


	#print("DICCIONARIO DE REGRESA", regresa_dic)
	return regresa_dic, len(lista_palabras_nueva) #Se regresa el diccionario que contiene una clave'Palabras' que contiene la lista de palabras en comun y contiene una clave con el nombre de cada poblacion con la lista de valores de idlv de las palabras

def detecta_palabras_iguales_por_palabras(dic_Poblaciones, lista_poblaciones, lista_palabras):
	regresa_dic = {} #Se declara el diccionario que al final contendrá las palabras que coincideo y sus respectivos valores de idlv por palabra de poblacion
	lista_palabras_nueva = []
	lista_Palabras_no_esta = []#Se declara la lista que contendrá las palabras que conciden en todas las poblaciones 
	idlv_lista = []#Se declara la lista que contendra los valores de idlv de las palabras que coinciden
	#dic_palabras = dic_Poblaciones[lista_poblaciones[0]]['Palabras'] #Se crea un diccionario que contiene el diccionario de palabras de la primer poblacion
	#lista_palabras = list(dic_palabras.keys())#Se enlistan las palabras del diccionario de la primer poblacion, esto se hace para que después se puedan comparar esas palabras con las demas listas de palabras de las otras poblaciones
	#print("PALABRASSSS: ", lista_palabras, len(lista_poblaciones), lista_poblaciones)
	
	for z in lista_palabras:#Se inicializa el for para iterar z en la lista de palabras que sacamos de una poblacion
		contador = 0#Contador que nos ayudará a saber en cuantas poblaciones esta la palabra de la variable z
		for x in lista_poblaciones:#Otro for para iterar en la distintas poblacines que hay
			palabras = dic_Poblaciones[x]['Palabras'] #Se extrae el diccionario de las palabras de la poblacion x
			palabras = list(palabras.keys())#Se enlistan las palabras que contiene el diccionario de palabras
			if z in palabras: #Condicional para saber si la palabra z esta en la lista de palabras de la poblacion x
				#print("la palabra: ", z, "esta en: ", x)
				contador += 1 #Si la palabra se encuentra en la poblacion x, el contador se incrementa en 1 y revisará la siguienta palabra z de la lista_palabras
		
		#Despues de revisar todas las palabras de lista_palabras en la lista de palabras de pla poblacion x se procede a revisar si estuvo en todas las poblaciones la palabra
		if contador == len(lista_poblaciones) and len(lista_palabras_nueva)<20: #Si el contador es igual al numero de poblaciones, quiere decir que estuvo la palabra en todas las listas de palabras de las poblaciones
			#print ("LA PALABRA ",z,"ESTA EN TODAS LAS POBLACIONES")
			lista_palabras_nueva.append(z) #Se agrega la palabra a la lista de palabras lista_palabras_nueva
			#Al final se obtiene una lista de todas las palabras que coinciden en todas las poblaciones
		else:
			lista_Palabras_no_esta.append(z)#Se agrega a la lista de palabras que no estuvo
	#print("LISTA PALABRAS: ",lista_palabras_nueva)
	regresa_dic['Palabras'] = lista_palabras_nueva # se agrega la clave 'Palabras' y la lista de palabras lista_palabras_nueva al diccionario regresa_dic

	#Ahora necesitamos sacar los valore de IDLV de cada palabra de la lista nueva y por poblacion
	for x in lista_poblaciones:#el for recorre las poblaciones
		idlv_lista = []#Se inicializa la lista idlv_lista en vacio
		dic_palabras = dic_Poblaciones[x]['Palabras'] #se extrae el diccionario de palabras de la poblacion x
		#Teniendo el diccionario de palabras de la poblacion x, se procede a extraer el valor de idlv por palabra
		for z in lista_palabras: #Se recorre la lista de palabras nueva que contiene las palabras que coinciden en todas las poblaciones
			if z in lista_palabras_nueva:
				idlv_lista.append(dic_palabras[z]) #Se agrega el valor de idlv a la lista idlv_lista, se extrae con dic_palabras[z] donde z es la clave para buscar el valor
			else:
				idlv_lista.append("0")
		#print("VALOR IDLV de ",x, idlv_lista)
		
		dic_temporal = {}#Contiene el valor de IDLV y color
		color = "rgba("
		for k in range(3):
			color = color + str(random.randrange(255)) + ","

		#dic_Palabras[x]['Color'] = color
		#print("color poblacion",x,color)
		dic_temporal['Color'] = color
		dic_temporal['IDLV'] = idlv_lista 
		regresa_dic[x] = dic_temporal #Se crea una clave con el nombre de la poblacion x en el diccionario regresa_dic y se le agrega la lista idlv_lista


	#print("DICCIONARIO DE REGRESA", regresa_dic)
	return regresa_dic, len(lista_palabras_nueva) #Se regresa el diccionario que contiene una clave'Palabras' que contiene la lista de palabras en comun y contiene una clave con el nombre de cada poblacion con la lista de valores de idlv de las palabras

def total_de_palabras_archivo(ruta):
	file = open(ruta,'r', encoding="latin-1")
	text = file.read()
	file.close()
	palabras = text.split()
	numero_de_palabras = len(palabras)

	return numero_de_palabras

def crea_archivo_info_json(list_folders_selected, ruta_contenedora):
	dic_Poblaciones_Info={} 
	dic_Poblaciones_Info['poblaciones'] = list_folders_selected
	dic_Poblaciones_Info['ruta_contenedora'] = ruta_contenedora + "\\"
	for x in list_folders_selected:
		dic_Poblacion_Info = {}
		path = ruta_contenedora + "\\" + x + "\\"
		contenido = os.listdir(path)
		numero_archivos = len(contenido)
		dic_Poblacion_Info['numero_de_archivos'] = numero_archivos
		numero_de_palabras = total_de_palabras_archivo(ruta_contenedora + "\\" + "Texto_normalizado" + "\\" + x + ".txt")
		dic_Poblacion_Info['numero_de_palabras'] = numero_de_palabras
		dic_Poblaciones_Info[x] = dic_Poblacion_Info

	with open('app/Archivos/Poblaciones_Info_Files.json','w') as f:
		json.dump(dic_Poblaciones_Info, f, indent = 4) 

def crea_archivo_json_poblaciones(dic_Poblaciones):
	with open('app/Archivos/Poblaciones.json','w') as f:
		json.dump(dic_Poblaciones, f, indent = 4)

def crea_archivo_json_archivo(file):
	with open('app/Archivos/file.json','w') as f:
		json.dump(file, f, indent = 4)

def crea_diccionario_poblaciones(archivos_Idlv):
	dic_Poblaciones = {} #Declaramos un diccionario que contendra las poblaciones con sus palabras y valores de IDLV
	for x in archivos_Idlv: #Este for recorrerá cada archivo de la carpeta Output
		dic_Poblacion = {} #Diccionario que contendra las poblaciones
		dic_Palabras = {} #Diccionario que contendrá las palavras de cada poblacion
		lista_de_palabras = [] #lista para almacenar las palabras de los archivos de poblaciones
		lista_IDLV =[] #lista para los valores de IDLV de cada palabra
		file = open(x,'r', encoding="utf8") #Se abre el archivo txt de la carpeta output
		tokens = file.read().split() #Se lee el archivo y se separa por tokens
		file.close() #Se cierra el archivo
		poblacion = x.split('_')[-2] #Solo contiene el nombre de la poblacion

		for token in tokens: #Se recorren todos los tokens
			if token[0] =='0': #Si el primer caracter del token es un 0, entonces es valor IDLV
				lista_IDLV.append(token) #Se guarda en la lista de IDlv
			else: #Si no es un 0 entonces es una palabra y se guarda en la lista de palabras
				lista_de_palabras.append(token)
			
		#print("LISTA IDLV de: ",poblacion ,lista_IDLV)
		#print("LISTA DE PALABRAS de: ",poblacion ,lista_de_palabras)

		creaCSVlista(lista_de_palabras, lista_IDLV, poblacion)


		for palabra, idlv in zip(lista_de_palabras, lista_IDLV): #En este for se recorre al mismo tiempo la lista de palabras y valor de IDLV
			dic_Palabras[palabra] = idlv #Se guardan los dos valores en el diccionario de Palabras
				
		dic_Poblacion['Palabras'] = dic_Palabras # Creamos un diccionario llamado dic_Poblacion que contendrá las palabras de la poblacion en la que nos encontramos en el for
		#dic_Poblacion['IDLV'] = lista_IDLV # Le agregamos la lista de IDLV al diccionario
		#print(dic_Poblacion)
		dic_Poblaciones[poblacion] = dic_Poblacion#Se agrega al dicionario de poblaciones el diccionario de cada poblacion con sus palabras y valores de IDLV

	return dic_Poblaciones

def lista_de_poblaciones(dic_Poblaciones):
	poblaciones = list(dic_Poblaciones.keys())

	return poblaciones

def abre_archivo_json_Poblaciones_datos():
	diccionario = {}
	with open('app/Archivos/Poblaciones.json', 'r') as f:
		diccionario = json.load(f)

	return diccionario

def abre_archivo_json_Poblaciones_info():
	diccionario = {}
	with open('app/Archivos/Poblaciones_Info_Files.json', 'r') as f:
		diccionario = json.load(f)

	return diccionario

def color_aleatorio():
	color = "rgba("
	for k in range(3):
		color = color + str(random.randrange(255)) + ","
	color = color + "0.7)"
	return color	
'''
def crea_grafica_pie(diccionario_carpetas_archivos):
	#Creacion de grafica pie
	data = pd.Series(diccionario_carpetas_archivos).reset_index(name='value').rename(columns={'index':'country'})
	data['angle'] = data['value']/data['value'].sum() * 2*pi
	data['color'] = Category20c[len(diccionario_carpetas_archivos)]

	p = figure(plot_height=500, plot_width=800, toolbar_location=None,
		           tools="hover", tooltips="@country: @value", x_range=(-0.5, 1.0))
	p.wedge(x=0, y=1, radius=0.4,
		        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
		        line_color="white", fill_color='color', legend_field='country', source=data)
			
	p.axis.axis_label=None
	p.axis.visible=False
	p.grid.grid_line_color = None
			

	scriptGraficaPie, divPie = components(p)
	#output_file("pie.html")
	#show(p)
		
	cdn_js = CDN.js_files[0]
	cdn_csss = CDN.css_files

	return scriptGraficaPie, divPie, cdn_js, cdn_csss
'''
def elimina_carpeta(ruta_contenedora):
	if os.path.exists(ruta_contenedora):
		shutil.rmtree(ruta_contenedora) #Elimina la carpeta que hay en la ruta 'elimina'
		#print("SE ELIMINO LA CARPETA: ", elimina)
	else:
		print("No se elimino la carpeta porque no existe: ", ruta_contenedora)

def elimina_carpetas(lista_carpetas_poblaciones, list_folders_selected, ruta_contenedora):
	for carpeta in lista_carpetas_poblaciones:
		if carpeta not in list_folders_selected:
			elimina = ruta_contenedora + '\\' + carpeta
			elimina_carpeta(elimina)

def guarda_zip(contenedor, file):
	
	#Se extrae la hora y fecha actual del sistenma
	fecha_hora = datetime.datetime.now()
	#Se modifica la manera de imprimir la hora y fecha
	fecha_y_hora = fecha_hora.strftime('%d%m%Y %H%M%S')
			
	filename = fecha_y_hora + "=" + file.filename #Se guarda la fecha y hora junto con el nombre del archivo para crear un nuevo nombre al archivo guardado.
	file.save(os.path.join(contenedor, filename)) #Guarda el archivo que seleccionamos del explorador de archivos. Lo guarda en la ruta de app.config con el nombre de filename
	#print("LLega nombre: ",file)
	#print("contenedor: ",contenedor)
	#print("nombre: ",filename)
	return filename

def extrae_zip(contenedor, filename):
	'''
	contenedor: tiene la ruta de donde se encuentra el archivo zip
	filename: contiene el nombre del archivo zip
	'''
	#ruta_archivo_comprimido contiene la ruta del archivo .zip dentro de la carpeta Archivos
	ruta_archivo_comprimido = contenedor + '\\' + filename
	#ruta_destino_de_archivo contiene dos cadenas, con split se separa la ruta del archivo.zip en dos cadenas
	#la primera contiene la ruta del archivo pero sin el ".zip" y la segunda cadena contiene solo el ".zip"
	ruta_destino_de_archivo = ruta_archivo_comprimido.split('.')
	#os.mkdir crea una ruta 'carpeta' y se basa en la ruta que hay en ruta_destino_de_archivo[0]
	os.mkdir(ruta_destino_de_archivo[0])
	#print("RUTAAAAAAAA:", ruta_carpeta_contenedora)


	#Se utiliza el archivo .zip que se guardo en la carpeta Archivos
	archivo_zip = zipfile.ZipFile(ruta_archivo_comprimido)
	#Se extrae los archivos del zip en la ruta dada
	archivo_zip.extractall(ruta_destino_de_archivo[0])
	#Se cierra el archivo
	archivo_zip.close()

	ruta_de_carpeta = ruta_destino_de_archivo[0]
	return ruta_de_carpeta

