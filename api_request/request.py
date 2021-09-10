import requests
import json
from pymongo import MongoClient
from datetime import datetime
import time
from datetime import date

URL= 'http://apigobiernoabiertortod.valencia.es/apirtod/rest/datasets/intensidad_tramos.json?items=389'
datos = ""

while(True):
	time.sleep(900)
	print(date.today())
	try:
		resp = requests.get(URL)
		data = resp.json()
	except Exception as e:
		print( 'La Exception >> ' + type(e).__name__ )
		raise e
	summary = data['summary']
	resources = data['resources']
	print(resources == datos)
	if datos != resources:
		datos = resources
		print("METE")
		for info in resources:
			description = info['des_tramo']
			ATA = info['idtramo']
			fecha  = info['modified']
			datetime_object = datetime.strptime(fecha[0:18], "%Y-%m-%dT%H:%M:%S")
			intensidad = info['lectura']
			obj = {
			'ATA' : ATA,
			'description' : description,
			'fecha' : datetime_object.strftime("%Y:%m:%d"),
			'hora' : datetime_object.strftime("%H:%M:%S"),
			'coches' : intensidad
			}
			with open('data.json', 'a') as json_file:
				json.dump(obj, json_file)