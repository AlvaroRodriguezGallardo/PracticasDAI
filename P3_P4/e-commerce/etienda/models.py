from django.db import models
from pymongo.errors import PyMongoError
from pydantic import BaseModel, FilePath, Field, EmailStr, validator
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from typing import Any
import pathlib
import requests
import shutil
import subprocess
import logging
from bson import ObjectId
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

def introducirProducto(nombre,precio,descripcion,categoria,imagen_ruta,rate=None):
    client,db = connectingToBD()
    productos_collection = db.productos

    logger.info("Valor de rate es:    "+str(rate))
    if rate == None:
        prod = { 
            'nombre': nombre, 
            'precio': float(precio), 
            'descripción': descripcion, 
            'categoría': categoria,
            'imágen': imagen_ruta,
            'rating': {
                'puntuación': 0.0,
                'cuenta': 1
            }
	    }
    else:
        prod = { 
		'nombre': nombre, 
		'precio': float(precio), 
		'descripción': descripcion, 
		'categoría': categoria,
		'imágen': imagen_ruta,
        'rating': {
            'puntuación': rate.rate,
            'cuenta': rate.count
        }
	}       
    

    try:
        if not nombre[0].isupper():
            raise ValueError("First letter must be a capital letter "+nombre)

        #prod_ = Producto(**prod)
        res = productos_collection.insert_one(prod)

        return res.inserted_id,1
    except ValueError as e:
        logger.error(". Error: "+str(e))

        return -1,-1
    except PyMongoError as er:
        logger.error("- Error inserting in DB: "+str(er))

        return -1,-1
  
    return 1,1

def obtenerProducto(id):
    client, db = connectingToBD()
    productos_collection = db.productos

    try:
        prod_id = ObjectId(id)
        prod = productos_collection.find_one({"_id": prod_id})

        if prod:
            logger.info("Data got successfully")

            prod["id"] = str(prod.get('_id'))
            del prod["_id"]

            if 'rating' in prod:
                rating_data = prod['rating']
                prod["rating"] = {
                    'rate': rating_data.get('puntuación', 0),
                    'count': rating_data.get('cuenta', 0)
                }
            else:
                prod["rating"] = {"rate": 0, "count": 0}

            return prod
        else:
            return "Error"
    except PyMongoError as e:
        logger.error("Error happened getting product: " + str(e))
        return "Error"
        
def eliminarProducto(id):
    client,db = connectingToBD()
    productos_collection = db.productos

    try:
        res = productos_collection.find_one_and_delete({'_id':ObjectId(id)})
        logger.info("Product deleted successfully")
        return res
    except Exception as e:
        logger.error("An error happened deleting product :"+str(e))
        return -1

def modificaProdBD(id,data):    # Se suponen todos los campos del Schema
    client,db = connectingToBD()
    productos_collection = db.productos


    try:
        my_id = {"_id": ObjectId(id)}

        res = productos_collection.update_one(my_id, {"$set": data})
        prod = obtenerProducto(id)
        return prod,1
    except Exception as e:
        logger.error("An error happened modifying DB: "+str(e))
        return -1,-1

def buscarListaAPI(princ,fin):         #Solo se usa para la API
    client, db = connectingToBD()
    productos_collection = db.productos

    try:
        consulta = productos_collection.find({'_id': {'$gte': ObjectId(princ), '$lte': ObjectId(fin)}})
        
        # Inicializa la lista devolver
        devolver = []

        for prod in consulta:
            product = {
                'id': str(prod['_id']),
                'title': prod.get('nombre', ''),
                'price': prod.get('precio', 0),
                'description': prod.get('descripción', ''),
                'category': prod.get('categoría', ''),
                'image': prod.get('imágen', ''),
                'rating': {                             # Unos productos los metí sin puntuación 
                    'rate': prod['rating'].get('puntuación', 0) if 'rating' in prod else 0,
                    'count': prod['rating'].get('cuenta', 0) if 'rating' in prod else 0
                } if 'rating' in prod else {}
            }
            
            devolver.append(product)
            logger.info(f"Product {product} has been stored in the list")

        logger.info("List of products obtained successfully")
        return devolver

    except Exception as e:
        logger.error(f"Error finding list of products: {type(e).__name__} - {str(e)}")
        return []

def modificarPuntuacion(id, calificacion):
    client, db = connectingToBD()
    productos_collection = db.productos

    try:
        prod_calific_antigua = obtenerProducto(id)
        logger.info(prod_calific_antigua)
        calif_antigua = prod_calific_antigua['rating']['rate']
        cuenta_antigua = prod_calific_antigua['rating']['count']

        # Se supone calif_antigua es la media aritmética de los cuenta_antigua votos hechos ya
        suma = calif_antigua * cuenta_antigua
        suma_nueva = suma + calificacion
        cuenta_nueva = cuenta_antigua + 1
        calif_nueva = suma_nueva / cuenta_nueva

        # Introducir los datos calif_nueva y cuenta_nueva donde correspondan en la BD
        logger.info("La calificación nueva es " + str(calif_nueva) + " y los votos ya son " + str(cuenta_nueva))
        nueva_tupla_calif = {'rate': calif_nueva, 'count': cuenta_nueva}

        # Actualizar el documento en la colección
        # NO ESTÁ ACTIALIZANDO LA BASE DE DATOOOOOOOOOOOOOOOOOOOOOOOOOOS
        productos_collection.update_one({'_id': ObjectId(id)}, {'$set': {'rating': {
                                                                    'puntuación': calif_nueva,
                                                                    'cuenta': cuenta_nueva
                                                                        }
        }})

        return nueva_tupla_calif
    except Exception as e:
        logger.error(f"Error rating product with id " + str(id) + ". Error is: " + str(e))
        return []
