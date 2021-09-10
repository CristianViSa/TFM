import matplotlib.pyplot as plt
import json
import datetime
import sys
import numpy as np
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
from bson.json_util import dumps
from pymongo import MongoClient
from os import getcwd
from sklearn.preprocessing import MinMaxScaler
import datetime
# Paths necesarios
path_ayuntamiento = "C:\\Users\\crist\\OneDrive - UPV\\TFM - Cristian Villarroya\\datos\\datos_vehiculos\\ayuntamiento\\"
path_web = "C:\\Users\\crist\\OneDrive - UPV\\TFM - Cristian Villarroya\\datos\\datos_vehiculos\\web\\"
path_mapa = "C:\\Users\\crist\\OneDrive - UPV\\TFM - Cristian Villarroya\\datos\\datos_vehiculos\\mapa\\"

"""
Este script permite crear mapas de la ciudad de valencia por calles y graficas de diferentes tipos.

Los mapas que permite crear varian en funcion del conteo de vehiculos, las opciones disponibles son, para una fecha y hora:
	- Mapa por barrios 
	- Mapa por tipo de calle
	- Mapa completo

Las graficas que permite son:
	- Comparativa ATA en diferentes fechas (los datos 15minutales agregados en horarios y promediados)
	- ATA en una fecha
	- Comparativa ATA en diferentes fechas (datos 15 minutales completos)
	- Comparativa fechas en un barrio (datos 15 minutales completos)
	- Comparativa barrios en una fecha (datos 15 minutales completos)
	- Comparativa fechas en un barrio (los datos 15minutales agregados en horarios y promediados)
	- Comparativa barrios en una fecha (los datos 15minutales agregados en horarios y promediados)
	"""


#####################		CARGA DE DATOS 	#############################
# Redondea la hora, necesario para los datos 15 minutales.
def round_minutes(dt, direction, resolution):
    new_minute = (dt.minute // resolution + (1 if direction == 'up' else 0)) * resolution
    return dt + datetime.timedelta(minutes=new_minute - dt.minute)

##	Lee el fichero json con los datos horarios y lo carga en la BD
def cargar_datos_horarios(fichero):
	######		Conexion de Mongo 		######
	client = MongoClient(port=27017)
	db=client.test3
	datos = []
	######		Leer e importar			######
	with open(fichero, encoding='utf-8') as json_file:
		for data in json_file:
			obj = json.loads(data)
			# Para evitar duplicados
			#if obj not in datos:
			if 1 == 1:
				try:
					db.test.insert_one(obj)
					datos.append(obj)
				except Exception as e:
					print("Unexpected error:", type(e), e)
			else:
				with open("errores_horarios.json", encoding='utf-8') as error_file:
					json.dump(obj, error_file)
					error_file.write('\n')

##	Lee el fichero json con los datos 15minutales y lo carga en la BD
def cargar_datos_15minutos(fichero):
	######		Conexion de Mongo 		######
	client = MongoClient(port=27017)
	db=client.final
	datos = []
	######		Leer e importar			######
	with open(fichero, encoding='utf-8') as json_file:
		for data in json_file:
			obj = json.loads(data)
			# Para evitar duplicados
			#if obj not in datos:
			if 1==1:
				try:
					# Para redondear la hora, no siempre mete cada 15 minutos exactos.
					time = obj['hora']
					time = time[:-3]
					time = datetime.datetime.strptime(time, '%H:%M')
					time = round_minutes(time, 'up', 15)
					obj['hora'] = str(time.time())
					obj['fecha'] = str(datetime.datetime.strptime(obj['fecha'], '%d/%m/%Y').date())
					#obj['fecha'] = str(datetime.datetime.strptime(obj['fecha'], '%Y-%m-%d').date())
					db.test3.insert_one(obj)
					#datos.append(obj)
				except Exception as e:
					print("Unexpected error:", type(e), e)
			else:
				with open("errores_web_15.json", encoding='utf-8') as error_file:
					json.dump(obj, error_file)
					error_file.write('\n')

# Carga el mapa en formato json de un fichero
def cargar_mapa(fichero):
	with open(fichero, encoding='utf-8') as f:
		mapa = json.load(f)
		return mapa

#####################		LECTURA DE DATOS 	#############################
# Devuelve las horas, para pintar las graficas
def get_horas(bd):
	minutales = ["00:15:00", "00:30:00", "00:45:00", "01:00:00", "01:15:00", "01:30:00", "01:45:00", "02:00:00", "02:15:00", "02:30:00", "02:45:00", "03:00:00", "03:15:00", "03:30:00", "03:45:00", 
		"04:00:00", "04:15:00", "04:30:00", "04:45:00", "05:00:00", "05:15:00", "05:30:00", "05:45:00", "06:00:00", "06:15:00", "06:30:00", "06:45:00", "07:00:00", "07:15:00", "07:30:00", "07:45:00", 
		"08:00:00", "08:15:00", "08:30:00", "08:45:00", "09:00:00", "09:15:00", "09:30:00", "09:45:00", "10:00:00", "10:15:00", "10:30:00", "10:45:00", "11:00:00", "11:15:00", "11:30:00", "11:45:00", 
		"12:00:00", "12:15:00", "12:30:00", "12:45:00", "13:00:00", "13:15:00", "13:30:00", "13:45:00", "14:00:00", "14:15:00", "14:30:00", "14:45:00", "15:00:00", "15:15:00", "15:30:00", "15:45:00", 
		"16:00:00", "16:15:00", "16:30:00", "16:45:00", "17:00:00", "17:15:00", "17:30:00", "17:45:00", "18:00:00", "18:15:00", "18:30:00", "18:45:00", "19:00:00", "19:15:00", "19:30:00", "19:45:00", 
		"20:00:00", "20:15:00", "20:30:00", "20:45:00", "21:00:00", "21:15:00", "21:30:00", "21:45:00", "22:00:00", "22:15:00", "22:30:00", "22:45:00", "23:00:00", "23:15:00", "23:30:00", "23:45:00", "00:00:00"]

	horarios = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]
	if (bd == "horarios"):
		return horarios
	return minutales
# Devuelve los vehiculos contados para un dia en todas las calles
def get_vehiculos_dia(ATA, fecha, bd):
	######		Conexion de Mongo 		######
	client = MongoClient(port=27017)
	if bd == 'horarios':
		db=client.test
		dbcol = db["test"]
	else:
		db = client.final
		dbcol = db["test3"]
	print(fecha)
	myquery = { "ATA": ATA, "fecha": fecha}
	resultado = {}
	mydoc = dbcol.find(myquery)
	horas = get_horas(bd)
	if(mydoc != None):
		for doc in mydoc:
			#print(doc)
			resultado[doc['hora']] = int(doc['coches'])
	"""
	if (bd == "15min"):
		for i in range(len(horas)):
			if horas[i] not in resultado.keys() or resultado[horas[i]] == -1:
				if i==0:
					resultado[horas[i]] = 0
				else:
					resultado[horas[i]] = resultado[horas[i-1]]
	"""
	return resultado

# Devuelve los vehiculos contados en un momento determinado
def get_vehiculos_fecha_hora(fecha, hora, bd):
	######		Conexion de Mongo 		######
	client = MongoClient(port=27017)
	if bd == 'horarios':
		db=client.test
		dbcol = db["test"]
	else:
		db = client.final
		dbcol = db["test3"]
	myquery = { "fecha": fecha, "hora": hora }
	resultado = {}
	mydoc = dbcol.find(myquery)
	if(mydoc != None):
		for doc in mydoc:
			resultado[doc['ATA']] = int(doc['coches'])
	return resultado


# Devuelve los vehiculos contados en un momento determinado en una calle
def get_vehiculos_fecha_hora_ATA(ATA, fecha, hora):
	######		Conexion de Mongo 		######
	client = MongoClient(port=27017)
	db = client.final
	dbcol = db["test3"]
	myquery = { "ATA": ATA, "fecha": fecha, "hora": str(hora) }
	resultado = {}
	mydoc = dbcol.find(myquery)
	if(mydoc != None):
		for doc in mydoc:
			if  int(doc['coches']) < 25000:
				return int(doc['coches'])
			else:
				return -1
	return -1

# Devuelve los vehiculos durante una hora en la base de datos 15minutales
def get_vehiculos_fecha_hora_agregado(ATA, fecha, hora):
	######		Conexion de Mongo 		######
	client = MongoClient(port=27017)
	db = client.final
	dbcol = db["test3"]
	myquery = { "fecha": fecha, "ATA": ATA}
	if (hora == "23"):
		hora2 = "00"
	else:
		if(int(hora) > 8):
			hora2 = str(int(hora)+1)
		else:
			hora2 = "0" + str(int(hora)+1)
	horas = [str(hora)+":15:00", str(hora)+":30:00", str(hora)+":45:00", hora2+":00:00"]
	resultado = {}
	mydoc = dbcol.find(myquery)
	if(mydoc != None):
		for doc in mydoc:
			if (doc['hora'] in horas):
				if int(doc['coches']) < 25000:
					resultado[doc['hora']] = int(doc['coches'])
				else:
					resultado[doc['hora']] = -1
	conteo = 0
	for key in resultado.keys():
		conteo = conteo + resultado[key]
	if len(resultado) == 0:
		return -1
	else:
		return conteo/len(resultado)


# Devuelve los vehiculos contados en un barrio en un momento determinado
def get_vehiculos_fecha_hora_barrio(fecha, hora, barrios, bd):
	######		Conexion de Mongo 		######
	client = MongoClient(port=27017)
	if bd == 'horarios':
		db=client.test
		dbcol = db["test"]
	else:
		db = client.final
		dbcol = db["test3"]
	myquery = { "fecha": fecha, "hora": hora }
	resultado = {}
	mydoc = dbcol.find(myquery)
	if(mydoc != None):
		for doc in mydoc:
			if doc['barrio'] in barrios:
				if int(doc['coches']) < 25000:
					resultado[doc['ATA']] = int(doc['coches'])
				else:
					resultado[doc['ATA']] = -1
			else:
				resultado[doc['ATA']] = -1
	return resultado

# Devuelve los vehiculos contados en un tipo de calle en un momento determinado
def get_vehiculos_fecha_hora_tipo_calle(fecha, hora, tipos, bd):
	######		Conexion de Mongo 		######
	client = MongoClient(port=27017)
	if bd == 'horarios':
		db=client.test
		dbcol = db["test"]
	else:
		db = client.final
		dbcol = db["test3"]
	myquery = { "fecha": fecha, "hora": hora }
	resultado = {}
	mydoc = dbcol.find(myquery)
	if(mydoc != None):
		for doc in mydoc:
			if doc['tipo'] in tipos:
				if int(doc['coches']) < 25000:
					resultado[doc['ATA']] = int(doc['coches'])
				else:
					resultado[doc['ATA']] = -1
			else:
				resultado[doc['ATA']] = -1
	return resultado


# Devuelve los vehiculos contados en un tipo de calle en un momento determinado
def get_vehiculos_fecha_barrio(fecha, barrios, bd):
	######		Conexion de Mongo 		######
	client = MongoClient(port=27017)
	if bd == 'horarios':
		db=client.test
		dbcol = db["test"]
	else:
		db = client.final
		dbcol = db["test3"]
	myquery = { "fecha": fecha}
	if bd == "horarios":
		horas = get_horas("horarios")
	else:
		horas = get_horas("15min")
	resultado = {}
	mydoc = dbcol.find(myquery)
	if(mydoc != None):
		for doc in mydoc:
			if doc['barrio'] in barrios:
				if int(doc['coches']) < 25000:
					if doc['hora'] in resultado.keys():
						resultado[doc['hora']] = resultado[doc['hora']] +  int(doc['coches'])
					else:
						resultado[doc['hora']] = int(doc['coches'])
				else:
					if doc['hora'] in resultado.keys():
						resultado[doc['hora']] += resultado[doc['hora']] / len(resultado[doc['hora']])
	if (bd == "15min"):
		for i in range(len(horas)):
			if horas[i] not in resultado.keys() or resultado[horas[i]] == -1:
				if i==0:
					resultado[horas[i]] = 0
				else:
					resultado[horas[i]] = resultado[horas[i-1]]
	return resultado

# Pinta un mapa completo en un momento determinado
def dibujar_mapa(fecha, hora, bd):
	mapa = cargar_mapa(path_mapa + "mapa_vacio.json")
	conteo = get_vehiculos_fecha_hora(fecha, hora, bd)
	for d in mapa['features']:
		#print(d['properties']['idtramo'])
		if(d['properties']['idtramo'] in conteo.keys()):
			d['properties']['lectura'] = conteo[d['properties']['idtramo']]
		else:
			d['properties']['idtramo'] = -1
	with open('mapa_test.json', 'w', encoding='utf-8') as json_file:
		json.dump(mapa, json_file, ensure_ascii=False)

# Pinta un mapa solo con las calles de un barrio
def dibujar_mapa_barrios(fecha, hora, barrios, bd):
	mapa = cargar_mapa(path_mapa + "mapa_vacio.json")
	conteo = get_vehiculos_fecha_hora_barrio(fecha, hora, barrios, bd)
	for d in mapa['features']:
		#print(d['properties']['idtramo'])
		if(d['properties']['idtramo'] in conteo.keys()):
			d['properties']['lectura'] = conteo[d['properties']['idtramo']]
		else:
			d['properties']['idtramo'] = -1
	with open('mapa_test.json', 'w', encoding='utf-8') as json_file:
		json.dump(mapa, json_file, ensure_ascii=False)

# Pinta un mapa solo con las calles de un tipo dado
def dibujar_mapa_tipo_calle(fecha, hora, tipos, bd):
	mapa = cargar_mapa(path_mapa + "mapa_vacio.json")
	conteo = get_vehiculos_fecha_hora_tipo_calle(fecha, hora, tipos, bd)
	for d in mapa['features']:
		if(d['properties']['idtramo'] in conteo.keys()):
			d['properties']['lectura'] = conteo[d['properties']['idtramo']]
		else:
			d['properties']['idtramo'] = -1
	with open('mapa_test.json', 'w', encoding='utf-8') as json_file:
		json.dump(mapa, json_file, ensure_ascii=False)

# Dibuja una grafica para una calle
def dibujar_grafica_calle(ATA, fecha, bd):
	conteo = get_vehiculos_dia(ATA, fecha, bd)
	y = conteo.values()
	x = get_horas(bd)
	fig, ax = plt.subplots()
	ax.set(xlabel='hora', ylabel='vehiculos',
	       title='Conteo horario de vehiculos en ' + ATA )
	ax.grid()
	if(bd == 'horarios'):
		ax.fmt_xdata = mdates.DateFormatter('%H')
		# Tipo 1
		#plt.stem(x, y, 'o--')

		# Tipo 2
		plt.plot(x, y, 'o--', color='blue')
		# Tipo 3
		#plt.step(x, y, where='post', label='post')
		#plt.plot(x, y, 'o--', color='grey', alpha=0.3)

		plt.xticks(rotation='horizontal')

	else:
		ax.fmt_xdata = mdates.DateFormatter('%H:%M')

		# Tipo 1
		#plt.stem(x, y, 'o--')

		# Tipo 2
		plt.plot(x, y, 'o--', color='blue')
		# Tipo 3
		#plt.step(x, y, where='post', label='post')
		#plt.plot(x, y, 'o--', color='grey', alpha=0.3)

		plt.xticks(rotation='vertical')
		plt.subplots_adjust(bottom=.3)
	etiqueta = mpatches.Patch(color='blue', label=fecha)
	plt.legend(handles=[etiqueta])
	plt.show()
	fig.savefig("test.png")


# Usado en el metodo de pintar multiples fechas en una grafica, en funcion de un indice, devuelve un color u otro, idem para el marcador
def definir_estilo(indice):
	color = 'purple'
	marcador = 'x--'
	if (indice == 0):
		color = 'blue'
		marcador = '.--'
	elif (indice == 1):
		color = 'red'
		marcador = 'o--'
	elif (indice == 2):
		color = 'green'
		marcador = 's--'
	elif (indice == 3):
		color = 'yellow'
		marcador = 'd--'
	elif (indice == 4):
		color = 'black'
		marcador = '<--'
	elif (indice == 5):
		color = 'cyan'
		marcador = ',--'
	elif (indice == 6):
		color = 'magenta'
		marcador = '*--'
	return marcador, color

# Muestra una grafica comparativa entre fechas para un ATA, ademas, permite escalar los datos entre 0 y 1.
def grafica_comparativa_fechas_ATA(ATA, fechas, escalado):
	datos = {}
	indice = 0
	for fecha in fechas:
		vehiculos = []
		if (datetime.datetime.strptime(fecha, '%Y-%m-%d') > datetime.datetime(2021, 1, 1)):
			vehiculos_minutales = get_vehiculos_dia(ATA, fecha, "15min").values()
			bloque = 0
			conteo = 0
			for cuenta in vehiculos_minutales:
				conteo += cuenta
				bloque += 1
				if bloque == 4:
					vehiculos.append(conteo / 4)
					bloque = 0
					conteo = 0
			horas = get_horas("horarios")
		else:
			vehiculos = get_vehiculos_dia(ATA, fecha, "horarios").values()
			horas = get_horas("horarios")
		datos[indice] = vehiculos
		indice += 1
	if (escalado):
		for key in datos.keys():
			vehiculos = datos[key]
			escalador = MinMaxScaler()
			np_vehiculos = np.array(vehiculos)
			np_vehiculos = np_vehiculos.reshape(-1, 1)
			escalador.fit(np_vehiculos)
			datos[key] = escalador.transform(np_vehiculos)
	fig, ax = plt.subplots()
	ax.set(xlabel='hora', ylabel='vehiculos',
	       title='Comparacion horaria de vehiculos en ' + ATA)
	ax.grid()
	etiquetas = []
	indice = 0
	for fecha in fechas:
		etiquetas.append(mpatches.Patch(color=definir_estilo(indice)[1], label=fecha))
		indice += 1
	indice = 0
	for key in datos.keys():
		vehiculos = datos[key]
		marcador, color = definir_estilo(indice)
		plt.plot(horas, vehiculos, marcador, color=color)
		indice += 1
	plt.legend(handles=etiquetas)
	plt.show()

# Muestra una grafica comparativa entre fechas para un ATA, ademas, permite escalar los datos entre 0 y 1.
def grafica_comparativa_fechas_ATA_15min(ATA, fechas, escalado):
	datos = {}
	indice = 0
	horas = []

	for fecha in fechas:
		if (len(horas) < 1):
			horas = get_horas("15min")
		datos[indice] = get_vehiculos_dia(ATA, fecha, "15min").values()
		indice += 1
	if (escalado):
		for key in datos.keys():
			vehiculos = list(datos[key])
			escalador = MinMaxScaler()
			np_vehiculos = np.array(vehiculos)
			np_vehiculos = np_vehiculos.reshape(-1, 1)
			escalador.fit(np_vehiculos)
			datos[key] = escalador.transform(np_vehiculos)
	fig, ax = plt.subplots()
	ax.set(xlabel='hora', ylabel='vehiculos',
	       title='Comparacion horaria de vehiculos en ' + ATA)
	ax.grid()
	ax.fmt_xdata = mdates.DateFormatter('%H')
	plt.xticks(rotation='vertical')
	etiquetas = []
	indice = 0
	for fecha in fechas:
		etiquetas.append(mpatches.Patch(color=definir_estilo(indice)[1], label=fecha))
		indice += 1
	indice = 0
	for key in datos.keys():
		vehiculos = datos[key]
		marcador, color = definir_estilo(indice)
		plt.plot(horas, vehiculos, marcador, color=color)
		indice += 1
	plt.legend(handles=etiquetas)
	plt.show()


# Muestra una grafica comparativa entre fechas para un ATA, ademas, permite escalar los datos entre 0 y 1.
def grafica_comparativa_fechas_barrio_15min(barrio, fechas, escalado):
	datos = {}
	indice = 0
	horas = []

	for fecha in fechas:
		if (len(horas) < 1):
			horas = get_horas("15min")
		datos[indice] = get_vehiculos_fecha_barrio(fecha, barrio, "15min").values()
		#datos[indice] = get_vehiculos_dia(barrio, fecha, "15min").values()
		indice += 1
	if (escalado):
		for key in datos.keys():
			vehiculos = list(datos[key])
			escalador = MinMaxScaler()
			np_vehiculos = np.array(vehiculos)
			np_vehiculos = np_vehiculos.reshape(-1, 1)
			escalador.fit(np_vehiculos)
			datos[key] = escalador.transform(np_vehiculos)
	fig, ax = plt.subplots()
	ax.set(xlabel='hora', ylabel='vehiculos',
	       title='Comparacion horaria de vehiculos en ' + barrio)
	ax.grid()
	ax.fmt_xdata = mdates.DateFormatter('%H')
	plt.xticks(rotation='vertical')
	etiquetas = []
	indice = 0
	for fecha in fechas:
		etiquetas.append(mpatches.Patch(color=definir_estilo(indice)[1], label=fecha))
		indice += 1
	indice = 0
	for key in datos.keys():
		vehiculos = datos[key]
		marcador, color = definir_estilo(indice)
		plt.plot(horas, vehiculos, marcador, color=color)
		indice += 1
	plt.legend(handles=etiquetas)
	plt.show()



# Muestra una grafica comparativa entre fechas para un ATA, ademas, permite escalar los datos entre 0 y 1.
def grafica_comparativa_fecha_barrios_15min(barrios, fecha, escalado):
	datos = {}
	indice = 0
	horas = []

	for barrio in barrios:
		if (len(horas) < 1):
			horas = get_horas("15min")
		datos[indice] = get_vehiculos_fecha_barrio(fecha, barrio, "15min").values()
		indice += 1
	if (escalado):
		for key in datos.keys():
			vehiculos = list(datos[key])
			escalador = MinMaxScaler()
			np_vehiculos = np.array(vehiculos)
			np_vehiculos = np_vehiculos.reshape(-1, 1)
			escalador.fit(np_vehiculos)
			datos[key] = escalador.transform(np_vehiculos)
	fig, ax = plt.subplots()
	ax.set(xlabel='hora', ylabel='vehiculos',
	       title='Comparacion horaria de vehiculos en ' + fecha)
	ax.grid()
	ax.fmt_xdata = mdates.DateFormatter('%H')
	plt.xticks(rotation='vertical')
	etiquetas = []
	indice = 0
	for barrio in barrios:
		etiquetas.append(mpatches.Patch(color=definir_estilo(indice)[1], label=barrio))
		indice += 1
	indice = 0
	for key in datos.keys():
		vehiculos = datos[key]
		marcador, color = definir_estilo(indice)
		plt.plot(horas, vehiculos, marcador, color=color)
		indice += 1
	plt.legend(handles=etiquetas)
	plt.show()



# Muestra una grafica comparativa entre fechas para un ATA, ademas, permite escalar los datos entre 0 y 1.
def grafica_comparativa_fechas_barrio(barrio, fechas, escalado):
	datos = {}
	indice = 0
	for fecha in fechas:
		vehiculos = []
		if (datetime.datetime.strptime(fecha, '%Y-%m-%d') > datetime.datetime(2021, 1, 1)):
			vehiculos_minutales = get_vehiculos_fecha_barrio(fecha, barrio,"15min").values()
			bloque = 0
			conteo = 0
			for cuenta in vehiculos_minutales:
				conteo += cuenta
				bloque += 1
				if bloque == 4:
					vehiculos.append(conteo / 4)
					bloque = 0
					conteo = 0
			horas = get_horas("horarios")
		else:
			vehiculos = get_vehiculos_fecha_barrio(fecha, barrio, "horarios").values()
			horas = get_horas("horarios")
		datos[indice] = vehiculos
		indice += 1
	if (escalado):
		for key in datos.keys():
			vehiculos = datos[key]
			escalador = MinMaxScaler()
			np_vehiculos = np.array(vehiculos)
			np_vehiculos = np_vehiculos.reshape(-1, 1)
			escalador.fit(np_vehiculos)
			datos[key] = escalador.transform(np_vehiculos)
	fig, ax = plt.subplots()
	ax.set(xlabel='hora', ylabel='vehiculos',
	       title='Comparacion horaria de vehiculos en ' + barrio)
	ax.grid()
	etiquetas = []
	indice = 0
	for fecha in fechas:
		etiquetas.append(mpatches.Patch(color=definir_estilo(indice)[1], label=fecha))
		indice += 1
	indice = 0
	for key in datos.keys():
		vehiculos = datos[key]
		marcador, color = definir_estilo(indice)
		plt.plot(horas, vehiculos, marcador, color=color)
		indice += 1
	plt.legend(handles=etiquetas)
	plt.show()



# Muestra una grafica comparativa entre fechas para un ATA, ademas, permite escalar los datos entre 0 y 1.
def grafica_comparativa_fecha_barrios(barrios, fecha, escalado):
	datos = {}
	indice = 0
	for barrio in barrios:
		vehiculos = []
		if (datetime.datetime.strptime(fecha, '%Y-%m-%d') > datetime.datetime(2021, 1, 1)):
			vehiculos_minutales = get_vehiculos_fecha_barrio(fecha, barrio,"15min").values()
			bloque = 0
			conteo = 0
			for cuenta in vehiculos_minutales:
				conteo += cuenta
				bloque += 1
				if bloque == 4:
					vehiculos.append(conteo / 4)
					bloque = 0
					conteo = 0
			horas = get_horas("horarios")
		else:
			vehiculos = get_vehiculos_fecha_barrio(fecha, barrio, "horarios").values()
			horas = get_horas("horarios")
		datos[indice] = vehiculos
		indice += 1
	if (escalado):
		for key in datos.keys():
			vehiculos = datos[key]
			escalador = MinMaxScaler()
			np_vehiculos = np.array(vehiculos)
			np_vehiculos = np_vehiculos.reshape(-1, 1)
			escalador.fit(np_vehiculos)
			datos[key] = escalador.transform(np_vehiculos)
	fig, ax = plt.subplots()
	ax.set(xlabel='hora', ylabel='vehiculos',
	       title='Comparacion horaria de vehiculos en ' + fecha)
	ax.grid()
	etiquetas = []
	indice = 0
	for barrio in barrios:
		etiquetas.append(mpatches.Patch(color=definir_estilo(indice)[1], label=barrio))
		indice += 1
	indice = 0
	for key in datos.keys():
		vehiculos = datos[key]
		marcador, color = definir_estilo(indice)
		plt.plot(horas, vehiculos, marcador, color=color)
		indice += 1
	plt.legend(handles=etiquetas)
	plt.show()


#cargar_datos_horarios(path_ayuntamiento + "datos_horarios.json")
#cargar_datos_15minutos(path_web + "datos_web_completo_transformado.json")
cargar_datos_15minutos(path_web + "datos_web_completo.json")
#cargar_mapa(path_mapa + "mapa_vacio.json")
#dibujar_mapa("06/02/2021", "12:15:00", "15min")
#dibujar_mapa("06/02/2019", "12", "horarios")
#dibujar_grafica_calle("A134", "23/02/2021", "15min")
#dibujar_grafica_calle("A1", "09/02/2019", "horarios")
#dibujar_mapa_tipo_calle("09/02/2021", "15:00:00", ["entrada", "salida", "primaria"], "15min")
#dibujar_mapa_barrios("09/02/2021", "12:15:00", "algiros", "15min")
"""
with open('ATAS_horarios.txt', 'r', encoding='utf-8') as file:
	ATAS = []
	for f in file:
		ata = f.split("\n")
		ATAS.append(ata[0])

	for ATA in ATAS:
		#grafica_comparativa_fechas_ATA(ATA, ["08/02/2021", "09/02/2021", "10/02/2021", "11/02/2021", "12/02/2021", "13/02/2021", "14/02/2021"], True)
		grafica_comparativa_fechas_ATA(ATA , ["08/02/2021", "15/02/2021", "22/02/2021"], True)
"""
#grafica_comparativa_fechas_ATA_15min("A111" ,  ["15/04/2021", "01/04/2021"], False)
#grafica_comparativa_fechas_ATA("A25" ,  ["2021-02-15",  "2021-06-14"], False)
#grafica_comparativa_fechas_ATA_15min("A111" ,  ["09/02/2021", "16/02/2021", "23/02/2021"], False)
#grafica_comparativa_fechas_ATA("A111" ,  ["09/02/2021", "16/02/2021", "23/02/2021"], False)
#grafica_comparativa_fechas_ATA("A111" , ["04/02/2019", "11/02/2019", "18/02/2019", "25/02/2019"], False)
#grafica_comparativa_fechas_barrio_15min("algiros" , ["09/02/2021", "16/02/2021", "23/02/2021"], False)
#grafica_comparativa_fecha_barrios_15min(["algiros", "ciutat vella", "extramuros"] , "23/02/2021", False)
#grafica_comparativa_fechas_barrio("ciutat vella" , ["09/02/2021", "16/02/2021", "23/02/2021"], False)
#grafica_comparativa_fechas_barrio("ciutat vella" , ["09/02/2019", "16/02/2019", "23/02/2019"], False)
#grafica_comparativa_fecha_barrios_15min(["algiros", "ciutat vella", "extramuros"] , "23/02/2021", False)
#grafica_comparativa_fecha_barrios(["algiros", "ciutat vella", "extramuros"] , "23/02/2019", False)
#limpiar_datos()