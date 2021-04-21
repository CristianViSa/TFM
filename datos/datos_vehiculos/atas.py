import pandas as pd 
import openpyxl
import json
from datetime import datetime, date
from pymongo import MongoClient

# Paths necesarios
path_ayuntamiento = "C:\\Users\\crist\\OneDrive - UPV\\TFM - Cristian Villarroya\\datos\\datos_vehiculos\\ayuntamiento\\"
path_web = "C:\\Users\\crist\\OneDrive - UPV\\TFM - Cristian Villarroya\\datos\\datos_vehiculos\\web\\"

#	Dado una fecha (dd/mm/YYYY), comprueba si es festivo
def definir_festivo(fecha, dia):
	festivos_2019 = ["01/01/2019", "22/01/2019", "19/03/2019", "19/04/2019/", "22/04/2019", "29/04/2019", "01/05/2019", "24/06/2019", "15/08/2019", "09/10/2019", "12/10/2019",
		"01/11/2019", "06/12/2019"
	]
	fallas_2019 = ["01/03/2019", "02/03/2019", "03/03/2019", "04/03/2019", "05/03/2019", "06/03/2019", "07/03/2019", "08/03/2019", "09/03/2019", "10/03/2019", "11/03/2019",
	"12/03/2019", "13/03/2019", "14/03/2019", "15/03/2019", "16/03/2019" ,"17/03/2019" ,"18/03/2019" ,"19/03/2019"
	]

	festivos_2020 = ["01/01/2020", "06/01/2020", "22/01/2020", "19/03/2020", "10/04/2020/", "13/04/2020/", "20/04/2020", "01/05/2020", "24/06/2020", "15/08/2020", "09/09/2020", "12/10/2020",
		"08/12/2020", "25/12/2020"
	]

	festivos_2021 = ["01/01/2021", "06/01/2021", "22/01/2021", "19/03/2021", "02/04/2021", "05/04/2021", "12/01/2021", "01/05/2021", "24/06/2021", "09/10/2021", 
		"12/10/2021", "01/11/2021", "06/12/2021", "08/12/2021", "25/12/2021"
	]
	festivo = 0
	if (fecha in festivos_2019 or fecha in festivos_2020 or fecha in festivos_2021 or fecha in fallas_2019 or dia == "Domingo"):
		festivo = 1
	return festivo


#	Dado un dia en el formato del csv, le asigna el nombre del dia correspondiente
def definir_dia(dia):
	if dia == "(lu.)" or dia == 0:
		return "Lunes"	

	elif dia == "(ma.)" or dia == 1:
		return "Martes"	

	elif dia == "(mi.)" or dia == 2:
		return "Miercoles" 	

	elif dia == "(ju.)" or dia == 3:
		return "Jueves"	

	elif dia == "(vi.)" or dia == 4:
		return "Viernes"	

	elif dia == "(sá.)" or dia == 5:
		return "Sabado"	

	elif dia == "(do.)" or dia == 6:
		return "Domingo"


# Lee la informacion de las calles en el fichero y devuelve un diccionario con la informacion
def leer_info_calles(fichero):
	df = pd.read_csv('infocalles.csv')
	"""
		FORMATO CSV:
			ATA, DESCRIPCION, TIPO, BARRIO, CP, SENTIDO, CARRILES, VELOCIDAD LIMITE, COMENTARIO

			Tipo => primaria, secundaria, terciaria, resdiencial, entrada o salida.
			SENTIDO => 1 unico, 2 doble
			COMENTARIO => Calle pequeña, calle larga, avenida, puente, entrada, salida
	"""
	ATAS = {}
	barrios = []
	for row in df.itertuples():
		ATA = row[1]
		desc = row[2]
		tipo = row[3]
		barrio = row[4]
		cp = row[5]
		sentido = row[6]
		carriles = row[7]
		velocidad = row[8]
		comentario = row[9]
		if (barrio not in barrios):
			barrios.append(barrio)
		ATAS[ATA] = [desc, tipo, barrio, cp, sentido, carriles, velocidad, comentario]
	print(barrios)
	return ATAS

"""
	Lee el csv con la informacion del conteo de vehiculos propocionado por el ayuntamiento.
	A dicho csv antes hay que hacer un preproceso:
		- Por simplicidad, cambiar formato a csv
		- Quitar cabeceras
		- Quitar lineas en blanco (;;;...)
		- Volver a fichero xlsx
"""
def leer_csv_atas(fichero):
	libro = openpyxl.load_workbook(fichero) 
	hoja = libro.active 
	ATA = ""
	ATAS = []
	inserts = 0
	errores = 0
	info_ATAS = leer_info_calles("infocalles.csv")
	for fila in hoja.iter_rows(min_row= 1, min_col = 1):
		dia = ""
		fecha = ""
		intensidades = []
		horas = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14" , "15", "16", "17", "18", "19", "20", "21", "22", "23"]
		vacios = 0
		for columna in fila:
			if (isinstance(columna.value, str)):
				strings = columna.value.split(' ')
				# Para detectar el ATA
				if "ATA" in columna.value:
					ATA = strings[1]
					ATAS.append(ATA)
					if(ATA not in info_ATAS.keys()):
						print(ATA)
				# Para leer los datos diarios
				if ("/2020" in columna.value or "/2019" in columna.value):
					dia = definir_dia(strings[0])
					fecha = strings[1]
			elif (isinstance(columna.value, int) or isinstance(columna.value, float)):
				intensidad = round(columna.value)
				intensidades.append(intensidad)
			else:
				# Falta el dato
				vacios += 1
				intensidades.append(-1)
		# Si se tiene el dia entero
		if (len(intensidades) == len(horas)):
			# Leer y escribir todas las horas 
			#		ATA, DESCRIPCION, TIPO, BARRIO, CP, SENTIDO, CARRILES, VELOCIDAD LIMITE, COMENTARIO
			if ATA in info_ATAS.keys():
				desc = info_ATAS[ATA][0]
				tipo = info_ATAS[ATA][1]
				barrio = info_ATAS[ATA][2]
				cp = info_ATAS[ATA][3]
				sentido = info_ATAS[ATA][4]
				carriles = info_ATAS[ATA][5]
				velocidad = info_ATAS[ATA][6]
				comentario = info_ATAS[ATA][7]
				for i in range(len(horas)):
					# Si falta el valor, coger el valor de la hora anterior
					if i != 0:
						if intensidades[i] == 0:
							intensidades[i] = intensidades[i-1]
					obj = {
					'ATA' : ATA,
					'desc' : desc,
					'tipo' : tipo,
					'barrio' : barrio,
					'cp' : cp,
					'sentido' : sentido,
					'carriles' : carriles,
					'velocidad' : velocidad,
					'comentario' : comentario,
					'fecha' : fecha,
					'dia' : dia,
					'hora' : horas[i],
					'festivo' : definir_festivo(fecha, dia),
					'coches' : intensidades[i]
					}

					# Si no es un salto de linea, escribe
					if vacios < 24:
						# Escribe en un fichero el resultado
						with open(path_ayuntamiento + 'datos_horarios4.json', 'a') as json_file:
							json.dump(obj, json_file)
							json_file.write('\n')
							inserts += 1
						json_file.close()
					else:
						with open(path_ayuntamiento + 'errores.json', 'a') as file:
							json.dump(obj, file)
							file.write('\n')
							errores += 1	
						file.close()

	print("Insertados : " + str(inserts))
	print("Dias : " + str(inserts/24))
	print("Errores : " + str(errores))

	with open('ATAS.txt', 'w') as file:
		for ata in ATAS:
			file.write(ata)
			file.write('\n')

# Lee el json obtenido de la web del ayuntamiento con los datos 15 minutales
def leer_json_web(fichero):
	with open(fichero, encoding='iso-8859-1') as json_file:
		info_ATAS = leer_info_calles("infocalles.csv")
		inserts = 0
		valor_previo = 0
		for data in json_file:
			obj = json.loads(data)
			ATA = obj['ATA'].upper()
			fecha = obj['fecha']
			time = datetime.strptime(fecha, '%Y:%m:%d')
			fecha = time.strftime('%d/%m/%Y')
			dia = time.weekday()
			dia = definir_dia(dia)
			intensidades = []
			horas = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14" , "15", "16", "17", "18", "19", "20", "21", "22", "23"]
			
			if ATA in info_ATAS.keys():
				desc = info_ATAS[ATA][0]
				tipo = info_ATAS[ATA][1]
				barrio = info_ATAS[ATA][2]
				cp = info_ATAS[ATA][3]
				sentido = info_ATAS[ATA][4]
				carriles = info_ATAS[ATA][5]
				velocidad = info_ATAS[ATA][6]
				comentario = info_ATAS[ATA][7]
				# Hay datos erroneos muy elevados
				if int(obj['coches']) > 15000 or int(obj['coches']) < 0:
					obj['coches'] = valor_previo
				obj = {
				'ATA' : ATA,
				'desc' : desc,
				'tipo' : tipo,
				'barrio' : barrio,
				'cp' : cp,
				'sentido' : sentido,
				'carriles' : carriles,
				'velocidad' : velocidad,
				'comentario' : comentario,
				'fecha' : fecha,
				'dia' : dia,
				'hora' : obj['hora'],
				'festivo' : definir_festivo(fecha, dia),
				'coches' : obj['coches']
				}
				valor_previo = obj['coches']
				# Escribe en un fichero el resultado
				with open(path_web + 'datos_web_completo.json', 'a', encoding='utf-8') as json_file:
					json.dump(obj, json_file, ensure_ascii=False)
					json_file.write('\n')
					inserts += 1
				json_file.close()

		print("Insertados : " + str(inserts))
		print("Dias : " + str(inserts/24))

#ficheros = ["enejun2019.xlsx", "juldic2019.xlsx", "enejun2020.xlsx", "juldic2020.xlsx" ]
#ficheros = ["enejun2020.xlsx"]
#for fichero in ficheros:	
#	leer_csv_atas(path_ayuntamiento + fichero)
#leer_info_calles("a")
#ficheros_web = ["data_web_bueno.json", "datos_web_bueno_2.json"]
ficheros_web = ["data_web_bueno.json", "datav2.json"]
for fichero_web in ficheros_web:	
	leer_json_web(path_web + fichero_web)
"""
with open('ATAS.txt', 'r') as file:
	ATAS = []
	for ata in file:
		if ata in ATAS:
			print("SI")
		else:
			ATAS.append(ata)
"""