# Álvaro Rodríguez Gallardo

from pymongo import MongoClient

client = MongoClient('mongo', 27017)

def no_esta_incluido(lista,categ):
    no_esta = True

    for p in lista:
        if p==categ:
            no_esta = False

    return no_esta

tienda_db = client.tienda                   
productos_collection = tienda_db.productos  
compras_collection = tienda_db.compras

# Consulta 1: Electrónica entre 100 y 200€, ordenados por precio

print("CONSULTA 1: Electrónica entre 100 y 200€, ordenados por precio")
print("--------------------------------------------------------------------------------------------------------------------------------------------")
#query1 = { '$and': [ {'precio': {'$gt' : 100.0 }},{'precio': {'$lt' : 200.0 }}, {'categoría': {'eq' : 'electronics'}}]}
query1 = {
    '$and': [
        {'precio': {'$gt': 100.0}},
        {'precio': {'$lt': 200.0}},
        {'categoría': 'electronics'}
    ]
}

q1 = productos_collection.find(query1).sort('precio',1)

for p in q1:
    print(p)

print("--------------------------------------------------------------------------------------------------------------------------------------------")

# Consulta 2: Productos que contengan la palabra 'pocket' en la descripción

print("CONSULTA 2: Productos que contengan la palabra 'pocket' en la descripción")
print("--------------------------------------------------------------------------------------------------------------------------------------------")

#query2 = { '$and' : [{'descripción': {'$regex': 'pocket'}}, {'descripción' : {'$not': {'$regex': '$pockets'}}}]}
query2 = {
    'descripción': {'$regex': 'pocket', '$options': 'i'}    # Opción i para hacer insensible a mayúsculas y minúscula
}


q2 = productos_collection.find(query2)

for p in q2:
    print(p)

print("--------------------------------------------------------------------------------------------------------------------------------------------")

# Consulta 3: Productos con puntuación mayor de 4

print("CONSULTA 3: Productos con puntuación mayor de 4")
print("--------------------------------------------------------------------------------------------------------------------------------------------")

query3 = {'rating.puntuación': {'$gt': 4.0}}

q3 = productos_collection.find(query3)

for p in q3:
    print(p)

# Consulta 4: Ropa de hombre, ordenada por puntuación 
print("--------------------------------------------------------------------------------------------------------------------------------------------")

print("CONSULTA 4: Ropa de hombre, ordenada por puntuación" )
print("--------------------------------------------------------------------------------------------------------------------------------------------")

query4 = { '$and': [{'categoría' : {'$regex' : 'men'}}, {'categoría': {'$regex' : 'clothing'}}, {'categoría' : {'$not': {'$regex': 'women'}}}]}

q4 = productos_collection.find(query4).sort('rating.puntuación',1)

for p in q4:
    print(p)
print("--------------------------------------------------------------------------------------------------------------------------------------------")

# Consulta 5: Facturación total
print("CONSULTA 5: Facturación total")
print("--------------------------------------------------------------------------------------------------------------------------------------------")

facturacion_total = 0.0

for p in compras_collection.find():
    for compra in p['productos']:
        for prod in productos_collection.find():
            if prod['_id']==compra['productId']:
                facturacion_total+=prod['precio']*compra['quantity']

#pipeline = [
#    {
#        "$unwind": "$productos"
#    },
#    {
#        "$lookup": {
#            "from": "productos_collection",
#            "localField": "productos.productId",
#            "foreignField": "_id",
#            "as": "producto"
#        }
#    },
#    {
#        "$unwind": "$producto"
#    },
#    {
#        "$group": {
#            "_id": "$_id",
#            "facturacion_total": {
#                "$sum": "$producto.precio"
#            }
#        }
#    }
#]


#result = list(compras_collection.aggregate(pipeline))
#print(result)
print("La facturación total es "+str(facturacion_total))
print("--------------------------------------------------------------------------------------------------------------------------------------------")

# Consulta 6: Facturación por categoría de producto

print("CONSULTA 6: Facturación por categoría de producto")
print("--------------------------------------------------------------------------------------------------------------------------------------------")

# Obtengo una lista con las categorías que hay
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

        
print("La facturación por categorías es: ")
for cat in categor:
    print(cat+":"+str(fact_por_categ[cat]))
#pipeline_2 = [
#    {
#        "$unwind": "$productos"  # Deshacer la matriz de productos
#    },
#    {
#        "$lookup": {            # Reunión de SQL
#            "from": "productos_collection",  # Nombre de la otra colección
#            "localField": "productos.ProductId",  # Campo en la colección actual
#            "foreignField": "_id",  # Campo en la colección de productos
#            "as": "producto"
#        }
#    },
#    {
#        "$unwind": "$producto"  # Deshacer la matriz creada por $lookup
#    },
#    {
#        "$group": {
#            "_id": "$producto.categoría",  # Agrupar por categoría
#            "totalOrderValue": {
#                "$sum": {
#                        "$toDecimal": {"$multiply": ["$producto.precio", "$productos.quantity"]}
                    
#                }
#            }
#        }
#    }
#]

#res = list(compras_collection.aggregate(pipeline_2))

#for p in res:
#    print("Categoría "+p['_id']+" tiene una facturación de "+str(p['totalOrderValue']))
print("--------------------------------------------------------------------------------------------------------------------------------------------")

client.close()