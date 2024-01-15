# etienda/api.py
from ninja_extra import NinjaExtraAPI, http_get
from ninja import Schema, Router
from bson.objectid import ObjectId
from etienda.models import obtenerProducto, introducirProducto, eliminarProducto, modificaProdBD, buscarListaAPI, modificarPuntuacion
from typing import List
from django.http import JsonResponse
from ninja.security import HttpBearer
import logging

logger = logging.getLogger(__name__)

class MyBearerAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "token_dai":
            return token
        else:
            raise Exception("Invalid token")

class Rate(Schema):
    rate: float
    count: int

class ProductSchema(Schema):
    id: str
    title: str
    price: float
    description: str
    category: str
    image: str = None
    rating: Rate

class ProductSchemaIn(Schema):
    title: str
    price: float
    description: str
    category: str
    rating: Rate

class ErrorSchema(Schema):
    message: str


api = NinjaExtraAPI(auth=MyBearerAuth(), csrf=True)

# GET para listar productos
@api.get("/productos", tags=['TIENDA DAI'], response={202: List[ProductSchema], 404: ErrorSchema})
def listarProductos(request, desde: str, hasta: str):    
    try:
        devolver = buscarListaAPI(desde, hasta)
        return JsonResponse({'data': devolver}, status=200)
    except Exception as e:
        logger.error("An error happened listing products in API: " + str(e))
        return JsonResponse({'error': 'Error getting list of products'}, status=500)

# POST para añadir producto
@api.post("/productos", tags=['TIENDA DAI'], response={202: ProductSchema, 404: ErrorSchema})
def aniadeProducto(request, new_producto: ProductSchemaIn):
    try:
        id__, exito = introducirProducto(
        nombre=new_producto.title,
        precio=new_producto.price,
        descripcion=new_producto.description,
        categoria=new_producto.category,
        imagen_ruta=None,
        rate=new_producto.rating
        )

    except Exception as e:
        return 404,{'message': 'Error inserting product: '+str(e)}
    
    new_product_out = {
        'id': str(id__),
        'title': new_producto.title,
        'price': float(new_producto.price),
        'description': new_producto.description,
        'category': new_producto.category,
        'image': None,
        'rating': new_producto.rating
    }

    return 202, new_product_out

# GET para obtener un producto
@api.get("/productos/{id}", tags=['TIENDA DAI'], response={202: ProductSchema, 404: ErrorSchema})
def obtenerProductoApi(request, id__: str):
    data = obtenerProducto(id__)

    if data == "Error":
        return JsonResponse({'message': 'Product not found'}, status=404)

    product = {
        'id': data['id'],
        'title': data['nombre'],
        'price': data['precio'],
        'description': data['descripción'],
        'category': data['categoría'],
        'image': data['imágen'],
        'rating': {
            'rate': data['rating']['rate'],
            'count': data['rating']['count']
        }
    }

    return JsonResponse({'data': product}, status=200)


# PUT para modificar un producto
@api.put("/productos/{id}", tags=['TIENDA DAI'], response={202: ProductSchema, 404: ErrorSchema})
def Modifica_producto(request, id: str, payload: ProductSchemaIn):
    try:
        data = obtenerProducto(id)

        for attr, value in payload.dict().items():
            logger.info(f'{attr} -> {value}')
            data[attr] = value

        del data["id"]
        # No asigno a _id porque MongoDB no deja alterarlo si se intenta
        # Ahora cambio los campos de data para tener un formato acorde a los que hay en el modelo
        mydata = {
            'nombre': data['title'],
            'precio': data['price'],
            'descripción': data['description'],
            'categoría': data['category'],
            'rating': {
                'puntuación': data['rating']['rate'],
                'cuenta': data['rating']['count']
            }
        }
        datos_modificados_en_la_BD_aux, exito = modificaProdBD(id, mydata)

        if exito == 1:
            datos_modificados_en_la_BD = {
                'id': str(id),
                'title': datos_modificados_en_la_BD_aux['nombre'],
                'price': float(datos_modificados_en_la_BD_aux['precio']),
                'description': datos_modificados_en_la_BD_aux['descripción'],
                'category': datos_modificados_en_la_BD_aux['categoría'],
                'image': datos_modificados_en_la_BD_aux['imágen'],
                'rating': {
                    'rate': datos_modificados_en_la_BD_aux['rating']['rate'],
                    'count': datos_modificados_en_la_BD_aux['rating']['count']
                }
            }
            return 202, datos_modificados_en_la_BD
        else:
            return 404, {'message': 'Product not found.'}

    except Exception as e:
        return 404, {'message': 'Error: ' + str(e)}



# DELETE para borrar un producto
@api.delete("/productos/{id}", tags=['TIENDA DAI'], response={202: ProductSchemaIn, 404: ErrorSchema})
def eliminaProducto(request, id: str):
    try:
        success = eliminarProducto(id)
    except Exception as e:
        logger.error("Problems deleting product: "+str(e))
        return 404, {'message': 'An error happened deleting product'}        

    product_deleted = {
        'title': success['nombre'],
        'price': float(success['precio']),
        'description': success['descripción'],
        'category': success['categoría'],
        'rating': {
            'rate': success['rating']['puntuación'],
            'count': success['rating']['cuenta']
        }
    }

    return 202, product_deleted

# PUT para modificar la calificación de un producto mediante JavaScript
@api.put("/puntuar",tags=['TIENDA DAI'], response={202: Rate, 404: ErrorSchema}) 
def aniadeCalificacion(request,id:str,calificacion: float):
    try:
        puntuac_y_cuenta = modificarPuntuacion(id,calificacion)

        return 202, puntuac_y_cuenta
    except:
        logger.error("An error happened rating product with id "+str(id))
        return 404,{'error': 'An error happened rating product with id '+str(id)}