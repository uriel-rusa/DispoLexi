from flask import Flask
import os
from flask_bootstrap import Bootstrap  #estilos

app = Flask(__name__)
bootstrap = Bootstrap(app)

from app import routes

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


#app.run(debug=True)