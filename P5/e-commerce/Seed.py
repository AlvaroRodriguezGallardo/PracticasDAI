# Álvaro Rodríguez Gallardo
# Seed.py.
from pydantic import BaseModel, FilePath, Field, EmailStr, validator
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from typing import Any
import pathlib
import requests
import shutil
import subprocess
		
# https://requests.readthedocs.io/en/latest/
def getProductos(api):
	response = requests.get(api)
	return response.json()
				
# Esquema de la BD
# https://docs.pydantic.dev/latest/
# con anotaciones de tipo https://docs.python.org/3/library/typing.html
# https://docs.pydantic.dev/latest/usage/fields/

class Nota(BaseModel):
	puntuación: float = Field(ge=0., lt=5.)
	cuenta: int = Field(ge=1)
				
class Producto(BaseModel):
	_id: Any
	nombre: str
	precio: float
	descripción: str
	categoría: str
	imágen: str | None
	rating: Nota

#	@field_serializer('imágen')
#	def serializaPath(self, val) -> str:
#		if type(val) is pathlib.PosixPath:
#			return str(val)
#		return val	

	@validator('nombre')			# Nota extra: validar mayúscula
	def nombre_mayuscula(cls,nombre):
		if not nombre[0].isupper():
			raise ValueError("Nombre debe comenzar en mayuscula")
		
		return nombre

class Compra(BaseModel):
	_id: Any
	usuario: EmailStr
	fecha: datetime
	productos: list


dato = { 
	'nombre': "MBJ Women's Solid Short Sleeve Boat Neck V ", 
	'precio': 9.85, 
	'descripción': '95% RAYON 5% SPANDEX, Made in USA or Imported, Do Not Bleach, Lightweight fabric with great stretch for comfort, Ribbed on sleeves and neckline / Double stitching on bottom hem', 'category': "women's clothing", 
	'categoría': "women's clothing",
	'imágen': None, 
	'rating': {'puntuación': 4.7, 'cuenta': 130}
}

# Valida con el esquema:
# daría error si no corresponde algún tipo 
producto = Producto(**dato)

#print(producto.descripción)
#pprint(producto.model_dump()) # Objeto -> python dict


# Conexión con la BD				
# https://pymongo.readthedocs.io/en/stable/tutorial.html
client = MongoClient('mongo', 27017)

tienda_db = client.tienda                   # Base de Datos
productos_collection = tienda_db.productos  # Colección 
				
#productos_collection.insert_one(producto.model_dump()) 
#producto_ = Producto(**producto)
#productos_collection.insert_one(producto_)
productos_collection.drop()		
#print(productos_collection.count_documents({}))

# todos los productos

#for com in compras_collection.find():
#	pprint(com)

# Introduzco los productos en la BD					
productos = getProductos('https://fakestoreapi.com/products')

for p in productos:
	imgUrl = p['image']
	img = requests.get(imgUrl)
	name = imgUrl.split("/")[-1]

	with open(name, "wb") as f:
		f.write(img.content)

	nuevo = shutil.move(name,"imagenes")
	prod = { 
		'nombre': p['title'], 
		'precio': p['price'], 
		'descripción': p['description'], 
		'categoría': p['category'],
		'imágen': nuevo, 
		'rating': {'puntuación': p['rating']['rate'], 'cuenta': p['rating']['count']}
	}
	
	prod_ = Producto(**prod)
	productos_collection.insert_one(prod)



# PONGO ESTO AQUÍ PARA QUE FUNCIONE PARA LA CONSULTA

lista_productos_ids = []
for prod in productos_collection.find():
#	pprint(prod)
	print(prod.get('_id'))   # Autoinsertado por mongo
	aux = prod.get('_id')
	aux2 = {}
	aux2['productId'] = aux
	lista_productos_ids.append(aux2)
	
#print(lista_productos_ids)
	
nueva_compra = {
	'usuario': 'fulanito@correo.com',
	'fecha': datetime.now(),
	'productos': lista_productos_ids
}
	
# valida
compra = Compra(**nueva_compra)
#pprint(compra.model_dump())
# añade a BD
compras_collection = tienda_db.compras  # Colección
compras_collection.drop()
#compras_collection.insert_one(compra.model_dump())


# Introduzco las compras en la BD
compras = getProductos('https://fakestoreapi.com/carts')
aux_pro = productos_collection.find()
for p in compras:
	prods = []
	for q in p['products']:
		aux = {
			'productId':aux_pro[q['productId']-1]['_id'], 
			'quantity': q['quantity']
		}
		prods.append(aux)

	compr = {
		'usuario' : 'fulano@eee.es',
		'fecha' : p['date'],
		'productos' : prods
	}

	compr_ = Compra(**compr)
	#compras_collection.insert_one(compr_.model_dump())
	compras_collection.insert_one(compr)



print("Hay "+str(productos_collection.count_documents({}))+" productos en la tienda")
print("Hay "+str(compras_collection.count_documents({}))+" compras realizadas")

# Nota extra: Copia de seguridad de la BD
# docker exec p1-mongo-1 mongodump
# Para verlo, usar docker exec p1-mongo-1 ls /dump

client.close()