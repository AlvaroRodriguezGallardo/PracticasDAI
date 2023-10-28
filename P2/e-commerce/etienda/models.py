from django.db import models
from pydantic import BaseModel, FilePath, Field, EmailStr, field_serializer, field_validator
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

def obtenerInfoPrincipio():
    client, db = connectingToBD()
    productos_collection = db.productos

    categorias = ["men's clothing","women's clothing","jewelery","electronics"]
    lista = []

    # Voy a usar la primera foto que haya para cada categoría :)
    for categ in categorias:
        query = {'categoría': categ}
        q = productos_collection.find(query).sort('rating.puntuación',1)
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