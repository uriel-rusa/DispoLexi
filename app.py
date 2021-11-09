import os
from flask import Flask
import funciones
import json
#from flask import flash
from flask import request, url_for, send_from_directory
#from flask import make_response
from flask import redirect
from flask import render_template
#from flask_bootstrap import Bootstrap
#from werkzeug.utils import secure_filename
#import datetime
#import zipfile
import string
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import io 
import shutil
#import random
import get_idlv
import get_idlv as idlvmod
import get_idlv_st as idlvmodst



#from collections import Counter
#from math import pi
#import pandas as pd
#from bokeh.io import output_file, show
#from bokeh.palettes import Category20c
#from bokeh.plotting import figure
#from bokeh.transform import cumsum
#from bokeh.embed import components #biblioteca agregada 15/10/2020
#from bokeh.resources import CDN
import smtplib
from email.mime.text import MIMEText #agregado el 15/octubre 2021
from email.header import Header #agregado el 15/octubre 2021


app = Flask(__name__)


UPLOAD_FOLDER = os.path.abspath("./Archivos/")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

OUTPUT_FOLDER = os.path.abspath("./Output")
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

listaColoresUno = [
	'rgba(224,2,8,0.6)',
	'rgba(0,157,222,0.6)',
	'rgba(4,161,37,0.6)',
	'rgba(255,239,0,0.6)',
	'rgba(166,90,1,0.6)',
	'rgba(207,95,217,0.6)',
	'rgba(15,31,152,0.6)',
	'rgba(231,128,37,0.6)',
	'rgba(121,233,231,0.6)',
	'rgba(190,214,58,0.6)',
	'rgba(145,39,110,0.6)',
	'rgba(255,203,200,0.6)',
	'rgba(143,17,11,0.6)',
	'rgba(182,164,80,0.6)',
	'rgba(82,240,164,0.6)',
	'rgba(108,96,165,0.6)',
	'rgba(255,124,111,0.6)',
	'rgba(154,150,150,0.6)',
	'rgba(9,127,179,0.6)',
	'rgba(29,33,4,0.6)']

listaColoresDos = [
	'rgba(224,2,8,1)',
	'rgba(0,157,222,1)',
	'rgba(4,161,37,1)',
	'rgba(255,239,0,1)',
	'rgba(166,90,1,1)',
	'rgba(207,95,217,1)',
	'rgba(15,31,152,1)',
	'rgba(231,128,37,1)',
	'rgba(121,233,231,1)',
	'rgba(190,214,58,1)',
	'rgba(145,39,110,1)',
	'rgba(255,203,200,1)',
	'rgba(143,17,11,1)',
	'rgba(182,164,80,1)',
	'rgba(82,240,164,1)',
	'rgba(108,96,165,1)',
	'rgba(255,124,111,1)',
	'rgba(154,150,150,1)',
	'rgba(9,127,179,1)',
	'rgba(29,33,4,1)']


@app.route('/home')
@app.route('/')
def index():
	'''
	#Revisa si existen la carpeta de Archivos y de Output para que se pueda guardar el archivo del usuario
	if os.path.isdir('Archivos'):
		shutil.rmtree('Archivos') #Elimina la carpeta Archivos
		print("Se elimino la carpeta Archivos")
		os.mkdir('Archivos') #Crea una carpeta llamada Archivos
		print("Se creo la carpeta Archivos")
	else:
		os.mkdir('Archivos') #Crea una carpeta llamada Archivos
		print("Se creo la carpeta Archivos")
	



	if os.path.isdir('Output'):
		shutil.rmtree('Output') #Elimina la carpeta OUTPUT
		print("Se elimino la carpeta Output")
		os.mkdir('Output')   #Crea una carpeta llamada Output
		print("Se creo la carpeta Output")
	else:
		os.mkdir('Output')   #Crea una carpeta llamada Output
		print("Se creo la carpeta Output")
	'''

	
	return render_template('home.html')

@app.route('/acerca_del_proyecto')
def acerca_del_proyecto():
	return render_template('acerca_del_proyecto.html')

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html')



@app.route('/listasDL', methods=['GET', 'POST'])
def listasDL():
	if request.method == 'GET':
		dic_Poblaciones = funciones.abre_archivo_json_Poblaciones_datos()
		lista_poblaciones = funciones.lista_de_poblaciones(dic_Poblaciones)
		return render_template('selectListasDL.html', lista_poblaciones = lista_poblaciones, listaColoresUno = listaColoresUno, listaColoresDos = listaColoresDos)

	elif request.method == 'POST':
		dic_Poblaciones = funciones.abre_archivo_json_Poblaciones_datos()
		lista_poblaciones_seleccionadas = request.form.getlist("my_checkbox")
		#opcion_tipo_palabras = request.form.get("gridRadios")
		cantidad_palabras = int(request.form.get("cantidad_palabras"))
		
		lista = list(dic_Poblaciones[lista_poblaciones_seleccionadas[0]]['Palabras'].values())

		#print("Poblaciones:",lista_poblaciones_seleccionadas)
		#print("Opcion: ", opcion_tipo_palabras)
		#print("cantidad de palabras,", cantidad_palabras, lista)


		return render_template('listasDL.html',OUTPUT_FOLDER = OUTPUT_FOLDER, cantidad_palabras = cantidad_palabras, lista_poblaciones = lista_poblaciones_seleccionadas, dic_Poblaciones = dic_Poblaciones)




@app.route('/prueba')
def prueba():
	return render_template('pruebaD3.html')

@app.route('/contacto',methods=['GET','POST'])
def contacto():
	if request.method == 'POST':
		nombre = request.form.get('validarNombre')
		asunto = request.form.get('validarAsunto')
		email = request.form.get('validarEmail')
		telefono = request.form.get('validarTelefono')
		mensaje = request.form.get('validationMensaje')

		contenido = 'Hola, este es un mensaje enviado desde la página de dispolexi.'
		contenido += '\nNombre: ' + nombre
		contenido += '\nEmail: ' + email
		contenido += '\nTelefono: ' + telefono
		contenido += '\nMensaje: ' + mensaje

		#Envía correo a lyr.dti@correo.cua.uam.mx
		coding = 'latin-1' 
		msg = MIMEText(contenido.encode(coding), 'plain', coding)
		msg['From']    = 'dispolexi@gmail.com'
		msg['To']      = 'lyr.dti@correo.cua.uam.mx'
		msg['Subject'] = Header(u''+asunto, coding)  # la 'ñ' no se puede codificar en ASCII

		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login('dispolexi@gmail.com','URIELdispolexi')
		server.sendmail('dispolexi@gmail.com', 'lyr.dti@correo.cua.uam.mx',msg.as_string())
		server.quit()
		

		#Envía correo a uriel.rusa@hotmail.com
		coding = 'latin-1' 
		msg = MIMEText(contenido.encode(coding), 'plain', coding)
		msg['From']    = 'dispolexi@gmail.com'
		msg['To']      = 'uriel.rusa@hotmail.com'
		msg['Subject'] = Header(u''+asunto, coding)  # la 'ñ' no se puede codificar en ASCII

		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login('dispolexi@gmail.com','URIELdispolexi')
		server.sendmail('dispolexi@gmail.com', 'uriel.rusa@hotmail.com',msg.as_string())
		server.quit()


		return render_template('contacto.html',valor = 'correcto')
	else:
		#print("No es Post")
		return render_template('contacto.html')

@app.route('/mensaje', methods=['POST'])
def mensaje():
	return render_template('home.html')

@app.route('/disponibilidad_lexica')
def disponibilidad_lexica():
	return render_template('disponibilidad_lexica.html')

@app.route('/aplicacion')
def aplicacion(valida = 0):
	#print("Valida: ", valida)
	return render_template('aplicacion.html', valida = valida)


@app.route('/subeArchivoPrueba')
def subeArchivoPrueba():
	diccionario_carpetas_archivos = {}
	nombre_carpeta = ""
	#Revisa si existen la carpeta de Archivos y de Output para que se pueda guardar el archivo del usuario
	if os.path.exists('./Archivos'):
		shutil.rmtree('./Archivos') #Elimina la carpeta Archivos

	os.mkdir('./Archivos') #Crea una carpeta llamada Archivos
	#resolution = request.form['resolution'] #Obtiene un mumero del campo resolution en el html
		
	#Variable que contiene el directorio de archivos
	contenedor = app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
	shutil.copy('./static/archivos/Mañaneras.zip', contenedor )#Copia el arcivo de prueba (Mañaneras) en la carpeta contenedora (app/Archivos)
	#file name contiene el nombre del archivo zip
	filename = 'Mañaneras.zip'#Se usa la funcion para guardar el archivo zip seleccionado por el usuario y regresa el nombre del zip
	#print("$$$$$$$$$",filename)
	#ruta_carpeta_contenedora tiene la ruta de donde se extrajeron los archivos del zip
	ruta_carpeta_contenedora = funciones.extrae_zip(contenedor,filename)
	##Se extraen los nombre de carpetas
	lista_de_archivos = list(get_idlv.load_files_names(ruta_carpeta_contenedora)) #Crea una lista de rutas, cada ruta corresponde a un archivo
	lista_de_carpetas = [] #Lista vacia para guardar los nombres de las carpetas que hay en el archivo zip
			
	for archivo in lista_de_archivos: #Se recorre la lista de rutas de archivos 
		archivo = archivo.split('\\') #Se diivide la ruta de los archivos por partes para obtener el nombre de la carpeta
		extrae_nombre_carpeta = archivo[-2] #Se extrae el nombre de la carpeta SE PONE -2 PORQUE SE TOMA EL PENULTIMO VALOR DE LA LISTA DE archivo[]
		#print("++++++++++EXTRAE CARPETA:", extrae_nombre_carpeta)

		if extrae_nombre_carpeta not in lista_de_carpetas: #Si el normbre de carpeta extraido no se encuentra en la lista de carpetas, se añade a la lista 
			lista_de_carpetas.append(extrae_nombre_carpeta) #Se agrega el nombre extraido de la carpeta a la lista de carpetas
			ruta_carpeta = ruta_carpeta_contenedora + '\\' + extrae_nombre_carpeta #Se crea la ruta para acceder a la carpeta seleccionada y poder contar los archivos que tiene
					
			lista = []
			lista.append(len(os.listdir(ruta_carpeta)))
			lista.append(funciones.color_aleatorio())

			#Se añade al diccionario los valores de extrae_nombre_carpeta y de la cantidad de archivos que contiene la carpeta
			#diccionario_carpetas_archivos.setdefault(extrae_nombre_carpeta,len(os.listdir(ruta_carpeta))) #Se usa para grafica_de_bokeh
			diccionario_carpetas_archivos.setdefault(extrae_nombre_carpeta,lista)


	#Se declaraun arreglo de caracteres vacio para pasar la lista de carpetas para poderla mandar al html y despues recuperar el valor en el procesamiento
	lista_carpetas_array = "" #Se declara el array vacio
	for x in lista_de_carpetas: #For que va a iterar la lista de nombre de carpeta
		if not lista_carpetas_array: #Si el arreglo aun no tiene nada escrito
			lista_carpetas_array = lista_carpetas_array + x  #Se concatena el arrego vacio con el elemento x de la lista de carpetas
		else: #Si el arreglo ya contiene un valor
			lista_carpetas_array = lista_carpetas_array + '.' + x #Se concatena lo que tiene el arreglo y el valor de x, separandolos por un '.'

	nombre_carpeta = 'Mañaneras'

	#scriptGraficaPie, divPie, cdn_js, cdn_csss = funciones.crea_grafica_pie(diccionario_carpetas_archivos)#Se usa para grafica_de_bokeh

	return render_template("elige_archivo.html",filename = filename, nombre_carpeta = nombre_carpeta, diccionario_carpetas_archivos = diccionario_carpetas_archivos, lista_de_carpetas = lista_carpetas_array, ruta_carpeta_contenedora = ruta_carpeta_contenedora, listaColoresUno = listaColoresUno)


@app.route('/elige_poblaciones', methods=['GET', 'POST'])
def elige_poblaciones(): #funcion para subir el archivo señalado
	diccionario_carpetas_archivos = {}
	if request.method == 'POST':
		nombre_carpeta = ""
		#Revisa si existen la carpeta de Archivos y de Output para que se pueda guardar el archivo del usuario
		if os.path.exists('./Archivos'):
			shutil.rmtree('./Archivos') #Elimina la carpeta Archivos

		#Obtenemos el archivo desde el form seleccionado por el usuario
		file = request.files['archivo'] #Obtiene el archivo seleccionado por el usuario
		#print("#################################\n",file)
		#Verifica que la extension del archivo sea valida utilizando la funcion allowed_file
		if funciones.allowed_file(file.filename):#Si es una extension permitida, hará las siguientes instrucciones
			#print("Extension valida")

			os.mkdir('./Archivos') #Crea una carpeta llamada Archivos
			#resolution = request.form['resolution'] #Obtiene un mumero del campo resolution en el html
			
			#Variable que contiene el directorio de archivos
			contenedor = app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
			#file name contiene el nombre del archivo zip
			filename = funciones.guarda_zip(contenedor, file)#Se usa la funcion para guardar el archivo zip seleccionado por el usuario y regresa el nombre del zip

			#ruta_carpeta_contenedora tiene la ruta de donde se extrajeron los archivos del zip
			ruta_carpeta_contenedora = funciones.extrae_zip(contenedor,filename)
			#print("CARPETA CONTENEDORA: ",ruta_carpeta_contenedora)

			##Se extraen los nombre de carpetas
			lista_de_archivos = list(get_idlv.load_files_names(ruta_carpeta_contenedora)) #Crea una lista de rutas, cada ruta corresponde a un archivo
			lista_de_carpetas = [] #Lista vacia para guardar los nombres de las carpetas que hay en el archivo zip
			
			for archivo in lista_de_archivos: #Se recorre la lista de rutas de archivos 
				archivo = archivo.split('\\') #Se diivide la ruta de los archivos por partes para obtener el nombre de la carpeta
				extrae_nombre_carpeta = archivo[-2] #Se extrae el nombre de la carpeta SE PONE -2 PORQUE SE TOMA EL PENULTIMO VALOR DE LA LISTA DE archivo[]
				#print("++++++++++EXTRAE CARPETA:", extrae_nombre_carpeta)

				if extrae_nombre_carpeta not in lista_de_carpetas: #Si el normbre de carpeta extraido no se encuentra en la lista de carpetas, se añade a la lista 
					lista_de_carpetas.append(extrae_nombre_carpeta) #Se agrega el nombre extraido de la carpeta a la lista de carpetas
					ruta_carpeta = ruta_carpeta_contenedora + '\\' + extrae_nombre_carpeta #Se crea la ruta para acceder a la carpeta seleccionada y poder contar los archivos que tiene
					
					lista = []
					lista.append(len(os.listdir(ruta_carpeta)))
					lista.append(funciones.color_aleatorio())

					#Se añade al diccionario los valores de extrae_nombre_carpeta y de la cantidad de archivos que contiene la carpeta
					#diccionario_carpetas_archivos.setdefault(extrae_nombre_carpeta,len(os.listdir(ruta_carpeta))) #Se usa para grafica_de_bokeh
					diccionario_carpetas_archivos.setdefault(extrae_nombre_carpeta,lista)

			
			#print("Lista de nombres de carpetas:", lista_de_carpetas)	
			#print("Diccionario ultimoooooo: ", diccionario_carpetas_archivos)
			#print("COLORES UNO: ", listaColoresUno[0])
			#print("COLORES DOS: ", listaColoresDos[0])

			#Se declaraun arreglo de caracteres vacio para pasar la lista de carpetas para poderla mandar al html y despues recuperar el valor en el procesamiento
			lista_carpetas_array = "" #Se declara el array vacio
			for x in lista_de_carpetas: #For que va a iterar la lista de nombre de carpeta
				if not lista_carpetas_array: #Si el arreglo aun no tiene nada escrito
					lista_carpetas_array = lista_carpetas_array + x  #Se concatena el arrego vacio con el elemento x de la lista de carpetas
				else: #Si el arreglo ya contiene un valor
					lista_carpetas_array = lista_carpetas_array + '.' + x #Se concatena lo que tiene el arreglo y el valor de x, separandolos por un '.'

		else:#En caso de que la extension no sea permitida
			print("Extension no valida")
			return render_template("aplicacion.html", valida = 1)

		nombre_carpeta = file.filename.split('.')[0]

		#scriptGraficaPie, divPie, cdn_js, cdn_csss = funciones.crea_grafica_pie(diccionario_carpetas_archivos)#Se usa para grafica_de_bokeh

		return render_template("elige_archivo.html",filename = filename, nombre_carpeta = nombre_carpeta, diccionario_carpetas_archivos = diccionario_carpetas_archivos, lista_de_carpetas = lista_carpetas_array, ruta_carpeta_contenedora = ruta_carpeta_contenedora, listaColoresUno = listaColoresUno)

@app.route('/Select_files', methods=['GET', 'POST'])
def Select_files(): #funcion para procesar los archivos señalados
	if request.method == 'POST':

		list_folders_selected = request.form.getlist('my_checkbox')
		ruta_contenedora = request.form.get('val_ruta_carpeta_contenedora')
		lista_carpetas_poblaciones = request.form.get('val_lista_de_carpetas').split('.')
		cantidad_folders_seleccionados = len(list_folders_selected)
		contenedor = app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
		filename = request.form.get('filename')
		#print("FILENAME: ",filename)
		contador = 0

		#Se elimina la carpeta de Output si existe
		if os.path.exists(ruta_contenedora + "/" + "Texto_normalizado"):
			funciones.elimina_carpeta(ruta_contenedora + "/" + "Texto_normalizado") #Elimina una carpeta llamada Texto normalizado


		#Se revisa si existen las carpetas seleccionadas
		for carpeta in list_folders_selected:
			ruta_carpeta = ruta_contenedora + '\\' + carpeta
			if os.path.exists(ruta_carpeta):
				contador += 1

		#print("+ carpetas seleccionadas", list_folders_selected)
		#print("+ Ruta contenedora: ", ruta_contenedora)
		#print("+ lista carpetas poblaciones: ", lista_carpetas_poblaciones)

		#IF si el contador es menor al numero de carpetas seleccionadas es porque no están todas las carpetas
		if contador < cantidad_folders_seleccionados:
			print("No estan todas las carpetas seleccionadas", contador)
			ruta = contenedor + "\\" + filename.split('.')[0]
			funciones.elimina_carpeta(ruta)
			funciones.extrae_zip(contenedor,filename)

		elif contador == cantidad_folders_seleccionados:
			print("Estan todas las carpetas", contador)
		
		funciones.elimina_carpetas(lista_carpetas_poblaciones, list_folders_selected, ruta_contenedora)

		#PROCESO DE ARCHIVOS PARA OBTENER EL IDLV
		
		archivos = list(get_idlv.load_files_names(ruta_contenedora)) #Crea una lista de rutas, cada ruta corresponde a un archivo
		#print("archivos: ruta...")
		#print(archivos)
		if not os.path.exists(ruta_contenedora + "/" + "Texto_normalizado"):
			os.mkdir(ruta_contenedora + "/" + "Texto_normalizado") #Crea una carpeta llamada Texto_normalizado


		#print("LLEGA AQUI----------------- PRINT")
		
		rutaNormaliza = ruta_contenedora + "\\" + "Texto_normalizado" + "\\"
		stop_words = funciones.carga_stop_words()
		for z in archivos:

			#print("LLEGA AQUI----------------- ENTRA FOR") 
			#stop_words = set(stopwords.words('spanish')) 
			#print("LLEGA AQUI----------------- stopwords")
			#print(stopwords.words('spanish'))
			file = open(z,'r', encoding="utf-8") 
			#print("LLEGA AQUI----------------- abre archivo sasda", z)
			text = file.read()# Use this to read file content as a stream:
			#print("LLEGA AQUI-----------------lee archivo") 
			file.close()
			#print("LLEGA AQUI-----------------cierra archgivo")
			for x in text:
				text.replace('"','')
			# convirtiendo en palabras
			tokens = word_tokenize(text)
			# convertir a minúsculas
			tokens = [w.lower() for w in tokens]
			# prepare a regex para el filtrado de caracteres
			re_punc = re.compile('[%s]' % re.escape(string.punctuation))
			# eliminar la puntuación de cada palabra
			stripped = [re_punc.sub('', w) for w in tokens]
			# eliminar los tokens restantes que no estén en orden alfabético
			words = [word for word in stripped if word.isalpha()]
			
				
			#os.remove(z)#Se elimina el archivo z
			pala=z.split('\\') #Se separa el arreglo dividido por \
			nombre_carpeta = pala[len(pala)-2]#Se obtiene el nombre de carpeta para poder hacer un archivo despues

			
			for r in words: #Se recorre todas las palabras extraidas del archivo
			    if not r in stop_words: #Si la palabra no esta en la lista de stop_words se agregará al archivo nuevo de resultado
			        #appendFile1 = open(ruta_contenedora + "\\" + "Texto_normalizado" + "\\" + nombre_carpeta +".txt", 'a') #Esto abrira el archivo que este en rutacontenedora\Texto_normalizado\ nom_carpeta.txt  (si no se encuentra el archivo, se crea)
			        #appendFile1.write(" " + r) #Se ecribe la palabra separada por un espacio en el nuevo
			        #print("NORMALIZADAAAAAAAAAAAAAAAAAAAAAAA: ", rutaNormaliza)
			        appendFile = open(rutaNormaliza + nombre_carpeta + ".txt", 'a')
			        appendFile.write(" " + r) #Se ecribe la palabra separada por un espacio en el nuevo
			
			appendFile.write("\n")
			appendFile.close()
			#appendFile1.write("\n")
			#appendFile1.close()
		
			#shutil.rmtree(ruta_contenedora)


		funciones.crea_archivo_info_json(list_folders_selected, ruta_contenedora)#Usamos la funcion para crear un archivo json con informacion de las poblaciones subidas al sistema

		

		if os.path.exists('./Output'):
			shutil.rmtree('./Output') #Elimina la carpeta OUTPUT

		if os.path.exists('./static/csv'):
			shutil.rmtree('./static/csv') #Elimina la carpeta OUTPUT

		os.mkdir('./Output')   #Crea una carpeta llamada Output
		os.mkdir('./static/csv')   #Crea una carpeta llamada Output

		dirIn = rutaNormaliza
		dirOut = "./Output/"
		#resolution_r = int(resolution) #resolution_r guarda el valor de resolution convertido a entero
		k = 2
		w = 0.1
		m = 1.0
		idlvmod.main(dirIn, dirOut, 1) #Se manda a llamar a la funcion de cálculo de idlv
		#idlvmodst.main(dirIn, dirOut, 1,k,w,m) #Se manda a llamar a la funcion de cálculo de idlv
		

		archivos_Idlv = list(get_idlv.load_files_names(dirOut)) #Crea una lista de rutas, cada ruta corresponde a un archivo que esta en la carpeta Output


		####DICCIONARIO DE POBLACIONES Y VALORES IDLV--------------------------
		dic_Poblaciones = funciones.crea_diccionario_poblaciones(archivos_Idlv)#Usamos la funcion para crear un diccionario con las palabras y valores idlv de cada poblacion
		
		#print("Diccionario a guardar: ",dic_Poblaciones)
		funciones.crea_archivo_json_poblaciones(dic_Poblaciones)#Usamos esta funcion para crear un archivo json con la informacion de las poblaciones
		#MANDAMOS A LLAMAR A LA FUNCION PARA QUE NOS REGRESE UN DICCIONARIO CON LAS PALABRAS QUE COINCIDEN EN LAS POBLACOINES DADAS
		#La funcion recibe una lista de poblaciones y el diccionario de todas las poblaciones
		#dic_Palabras_iguales, numero_de_palabras = funciones.detecta_palabras_iguales(dic_Poblaciones, list_folders_selected,)
		#print("LAS PALABRAS IGUALES SON: ", dic_Palabras_iguales, "NUMERO DE PALABRAS: ",numero_de_palabras)


		listPobla = funciones.lista_de_poblaciones(dic_Poblaciones)



	#print("SE VAaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
	return redirect(url_for('resultados'))
	#return render_template('resultados.html',dic_Poblaciones = dic_Poblaciones, lista_poblaciones = list_folders_selected, dic_Palabras_iguales = dic_Palabras_iguales, numero_de_palabras = numero_de_palabras, numero_poblaciones = len(list_folders_selected))

#@app.route('/graficaBarVer', methods=['GET', 'POST'])
@app.route('/resultados')
def resultados():
	if os.path.isfile('./Archivos/Poblaciones.json'):
		#print("entra en resultado")
		return render_template('resultados.html')
	else:
		return redirect(url_for('aplicacion'))

@app.route('/graficaBarVer', methods=['GET', 'POST'])
def graficaBarVer():

	if request.method == 'GET': # este metodo es cuando se da clic en la grafica seleccionada y es la configuracion que muestra la grafica de ejemplo
		dic_Poblaciones = funciones.abre_archivo_json_Poblaciones_datos()
		lista_poblaciones = funciones.lista_de_poblaciones(dic_Poblaciones)
		dic_Palabras_iguales, numero_de_palabras = funciones.detecta_palabras_iguales(dic_Poblaciones, lista_poblaciones,5,'1')
		numero_poblaciones = len(lista_poblaciones)
		return render_template('graficaBarVerPrueba.html',lista_poblaciones = lista_poblaciones, dic_Palabras_iguales = dic_Palabras_iguales, numero_de_palabras = numero_de_palabras, numero_poblaciones = numero_poblaciones, listaColoresUno = listaColoresUno, listaColoresDos = listaColoresDos)

	elif request.method == 'POST':
		dic_Poblaciones = funciones.abre_archivo_json_Poblaciones_datos()
		lista_poblaciones_seleccionadas = request.form.getlist("my_checkbox")
		opcion_tipo_palabras = request.form.get("gridRadios")
		cantidad_palabras = int(request.form.get("cantidad_palabras"))
		dic_Palabras_iguales, numero_de_palabras = funciones.detecta_palabras_iguales(dic_Poblaciones, lista_poblaciones_seleccionadas, cantidad_palabras, opcion_tipo_palabras)
		numero_poblaciones = len(lista_poblaciones_seleccionadas)
		return render_template('graficaBarVer.html', dic_Palabras_iguales = dic_Palabras_iguales, lista_poblaciones = lista_poblaciones_seleccionadas, numero_de_palabras = numero_de_palabras, numero_poblaciones = numero_poblaciones, listaColoresUno = listaColoresUno, listaColoresDos = listaColoresDos)

@app.route('/graficaRadar', methods=['GET', 'POST'])
def graficaRadar():
	if request.method == 'GET':
		dic_Poblaciones = funciones.abre_archivo_json_Poblaciones_datos()
		lista_poblaciones = funciones.lista_de_poblaciones(dic_Poblaciones)
		return render_template('graficaRadarPrueba.html', lista_poblaciones = lista_poblaciones, listaColoresUno = listaColoresUno, listaColoresDos = listaColoresDos)

	elif request.method == 'POST':
		dic_Poblaciones = funciones.abre_archivo_json_Poblaciones_datos()
		lista_poblaciones_seleccionadas = request.form.getlist("my_checkbox")
		opcion_tipo_palabras = request.form.get("gridRadios")
		cantidad_palabras = int(request.form.get("cantidad_palabras"))
		#print("palabrasPob: ", lista_poblaciones_seleccionadas, "\nTipo de palabras: ",opcion_tipo_palabras, "\nCantidad de palabras: ", cantidad_palabras)
		lista_palabras = []
		dic_Palabras_iguales, numero_de_palabras = funciones.detecta_palabras_iguales(dic_Poblaciones, lista_poblaciones_seleccionadas, cantidad_palabras, opcion_tipo_palabras)
		lista_palabras = dic_Palabras_iguales['Palabras'];
		return render_template('graficaRadar.html',dic_Palabras_iguales = dic_Palabras_iguales, lista_poblaciones_seleccionadas = lista_poblaciones_seleccionadas,lista_palabras = lista_palabras, listaColoresUno = listaColoresUno, listaColoresDos = listaColoresDos)

@app.route('/graficaSankey', methods=['GET', 'POST'])
def graficaSankey():

	if request.method == 'GET': # este metodo es cuando se da clic en la grafica seleccionada y es la configuracion que muestra la grafica de ejemplo
		dic_Poblaciones = funciones.abre_archivo_json_Poblaciones_datos()
		lista_poblaciones = funciones.lista_de_poblaciones(dic_Poblaciones)
		dic_Palabras_iguales, numero_de_palabras = funciones.detecta_palabras_iguales(dic_Poblaciones, lista_poblaciones,5,'1')
		numero_poblaciones = len(lista_poblaciones)
		return render_template('graficaSankeyPrueba.html',lista_poblaciones = lista_poblaciones, dic_Palabras_iguales = dic_Palabras_iguales, numero_de_palabras = numero_de_palabras, numero_poblaciones = numero_poblaciones)

	elif request.method == 'POST':
		dic_Poblaciones = funciones.abre_archivo_json_Poblaciones_datos()
		lista_poblaciones_seleccionadas = request.form.getlist("my_checkbox")
		#opcion_tipo_palabras = request.form.get("gridRadios")
		#cantidad_palabras = int(request.form.get("cantidad_palabras"))
		#dic_Palabras_iguales, numero_de_palabras = funciones.detecta_palabras_iguales(dic_Poblaciones, lista_poblaciones_seleccionadas, cantidad_palabras, opcion_tipo_palabras)
		numero_poblaciones = len(lista_poblaciones_seleccionadas)
		funciones.sankey(dic_Poblaciones,lista_poblaciones_seleccionadas)
		#return render_template('graficaBarVer.html', dic_Palabras_iguales = dic_Palabras_iguales, lista_poblaciones = lista_poblaciones_seleccionadas, numero_de_palabras = numero_de_palabras, numero_poblaciones = numero_poblaciones)

		return render_template('graficaSankey.html')



if __name__ == '__main__':
	app.run()