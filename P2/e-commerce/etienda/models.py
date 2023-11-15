from django.db import models
from pymongo.errors import PyMongoError
from pydantic import BaseModel, FilePath, Field, EmailStr, field_serializer, field_validator
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from typing import Any
import pathlib
import requests
import shutil
import subprocess
import logging
logger = logging.getLogger(__name__)

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
	imágen: FilePath | None
	rating: Nota

	@field_serializer('imágen')
	def serializaPath(self, val) -> str:
		if type(val) is pathlib.PosixPath:
			return str(val)
		return val	

	@field_validator('nombre')			# Nota extra: validar mayúscula
	def nombre_mayuscula(cls,nombre):
		if not nombre[0].isupper():
			raise ValueError("Nombre debe comenzar en mayuscula")
		
		return nombre

class Compra(BaseModel):
	_id: Any
	usuario: EmailStr
	fecha: datetime
	productos: list

# Create your models here.

def connectingToBD():
    client = MongoClient('mongo', 27017)
    tienda_db = client.tienda                   

    return client,tienda_db

def closingDB(client):
    client.close()

def no_esta_incluido(lista,categ):
    no_esta = True

    for p in lista:
        if p==categ:
            no_esta = False

    return no_esta

def consultas(number):
    client = MongoClient('mongo', 27017)
    tienda_db = client.tienda                   
    productos_collection = tienda_db.productos  
    compras_collection = tienda_db.compras

    if number==1:
        query1 = {
            '$and': [
                {'precio': {'$gt': 100.0}},
                {'precio': {'$lt': 200.0}},
                {'categoría': 'electronics'}
            ]
        }
        q1 = productos_collection.find(query1).sort('precio',1)
        devolver = list(q1)
    if number==2:
        query2 = {
            'descripción': {'$regex': 'pocket', '$options': 'i'}    # Opción i para hacer insensible a mayúsculas y minúscula
        }
        q2 = productos_collection.find(query2)
        devolver = list(q2)
    if number==3:
        query3 = {'rating.puntuación': {'$gt': 4.0}}
        q3 = productos_collection.find(query3)
        devolver = list(q3)
    if number==4:
        query4 = { '$and': [{'categoría' : {'$regex' : 'men'}}, {'categoría': {'$regex' : 'clothing'}}, {'categoría' : {'$not': {'$regex': 'women'}}}]}
        q4 = productos_collection.find(query4).sort('rating.puntuación',1)
        devolver = list(q4)
    if number==5:
        facturacion_total = 0.0
        for p in compras_collection.find():
            for compra in p['productos']:
                for prod in productos_collection.find():
                    if prod['_id']==compra['productId']:
                        facturacion_total+=prod['precio']*compra['quantity']
        devolver = facturacion_total
    if number==6:
        categor = []
        for p in productos_collection.find():
            if no_esta_incluido(categor,p['categoría']):
                categor.append(p['categoría'])
        fact_por_categ = {}
        for cat in categor:
            fact_por_categ[cat] = 0.0
        for p in compras_collection.find():
            for compra in p['productos']:
                for prod in productos_collection.find():
                    if prod['_id']== compra['productId']:
                        fact_por_categ[prod['categoría']]+=compra['quantity']*prod['precio']
        devolver=fact_por_categ

    client.close()
    return devolver


#def obtenerInfoPrincipio():
#    client, db = connectingToBD()
#    productos_collection = db.productos
#
#    categorias = ["men's clothing","jewelery","electronics","women's clothing"]
#    lista = []
#    for categ in categorias:
#        query =  {'categoría': categ}
#        q = productos_collection.find(query).sort('rating.puntuación',1) #  Por puntuación
#        #lista.append(q)
#        for aux in q:
#            lista.append(aux)

  # closingDB(client)
#    return list(lista)

def obtenerCategorias():
    client,db = connectingToBD()
    productos_collection = db.productos

    categs = productos_collection.distinct('categoría')

    return list(categs)

def obtenerCategoriasEleccion():
    categs = obtenerCategorias()

    choices = [('', 'Select a category')] + [(categoria, categoria) for categoria in categs]

    return choices

def obtenerInfoPrincipio():
    client, db = connectingToBD()
    productos_collection = db.productos

    categorias = obtenerCategorias()
    lista = []

    # Parece que esto es de filosofía LIFO, así que para que no cambien la foto del menú principal tras insertar, cojo la primera incluida en la BD
    for categ in categorias:
        query = {'categoría': categ}
        q = productos_collection.find(query).sort('rating.puntuación',1)
        q = list(q)
        lista.append(q[0])  # Para el menú principal, solo quiero un elemento que me indique la propia categoría
    
    return list(lista)

def obtenerInfoPorCategoria(category):
    client, db = connectingToBD()
    productos_collection = db.productos

    query = {'categoría': category}
    q = productos_collection.find(query).sort('rating.puntuación',1)

    return list(q)

def obtenerInfoCadena(cadena):
    client,db = connectingToBD()
    productos_collection = db.productos

    query = { 
        'nombre': {'$regex': cadena, '$options': 'i'}    # Opción i para hacer insensible a mayúsculas y minúscula
    }
    q = productos_collection.find(query).sort('rating.puntuación',1)

    return list(q)

def introducirProducto(nombre,precio,descripcion,categoria,imagen_ruta):
    client,db = connectingToBD()
    productos_collection = db.productos

    prod = { 
		'nombre': nombre, 
		'precio': float(precio), 
		'descripción': descripcion, 
		'categoría': categoria,
		'imágen': imagen_ruta
	}

    try:
        if not nombre[0].isupper():
            raise ValueError("First letter must be a capital letter "+nombre)

        #prod_ = Producto(**prod)
        productos_collection.insert_one(prod)
    except ValueError as e:
        logger.error(". Error:"+str(e))
        return 0
    except PyMongoError as e:
        logger.error("- Error inserting in DB: "+str(e))
        return 0

    
  
    return 1