import json

file_name = "mapa.json"
with open(file_name, encoding='utf-8') as f:
	data = json.load(f)

formato = data['type']
crs = data['crs']

geometrias = []
colores = []
propiedades = []
count = 0
ATAS = []
calles =  []
for d in data['features']:
	vehiculos = int(d['properties']['lectura'])
	d['properties']['lectura'] = 0
	geometrias.append(d['geometry'])
	if vehiculos < 100:
		color = "#000000"
	elif vehiculos < 500 and  vehiculos > 100:
		color = "#0000FF"
	elif vehiculos < 1000 and vehiculos > 500:
		color = "#FFFF00"
	else:
		color = "#FF0000"
	info = 	d['properties']
	ATAS.append(info['idtramo'])
	calles.append(info['des_tramo'])
	propiedad = {
		'idtramo' : info['idtramo'],
		'lectura' : vehiculos,
		'des_tramo': info['des_tramo'],
		'colour' : color
	}
	propiedades.append(propiedad)
	colores.append(color)
obj = {}
obj['type'] = formato
obj['crs'] = crs

obj['features'] = []

for i in range(len(geometrias)):
	obj['features'].append(
		{
			'type' : "Feature",

			'geometry' : geometrias[i],

			'properties' : propiedades[i]

		}
		)
with open('mapa_color.json', 'w') as outfile:
    json.dump(obj, outfile)
    outfile.write('\n')
for d in data:
	print(d)
with open('mapa_vacio.json', 'w') as outfile:
    json.dump(data, outfile)
    outfile.write('\n')

with open('calles.txt', 'w') as outfile:
    for i in range(len(calles)):
    	calle = calles[i]
    	ATA = ATAS[i]
    	texto = "ATA : " + str(ATA) + ", " + calle + "\n"
    	outfile.write(texto)
    	outfile.write('\n')


