from django.shortcuts import render
from django.http import HttpResponse
from .models import consultas, obtenerInfoPrincipio,obtenerInfoPorCategoria,obtenerInfoCadena

# Create your views here.

# Por defecto, con esto muestro html de enlaces
def index(request):
    lista_productos = obtenerInfoPrincipio()

    return render(request,'index.html',{'lista':lista_productos})


# Aquí hago lo respectivo a consultas y devolver plantillas

def funcionAuxP1(request):
    response = "<h1>Consultas</h1>"
    response += "<a href=/etienda/consultasP1/1/>Electrónica entre 100 y 200€, ordenados por precio</a><br>"
    response += "<a href=/etienda/consultasP1/2/>Productos que contengan la palabra 'pocket' en la descripción</a><br>"
    response += "<a href=/etienda/consultasP1/3/>Productos con puntuación mayor de 4</a><br>"
    response += "<a href=/etienda/consultasP1/4/>Ropa de hombre, ordenada por puntuación </a><br>"
    response += "<a href=/etienda/consultasP1/5/>Facturación total</a><br>"
    response += "<a href=/etienda/consultasP1/6/>Facturación por categoría de producto</a>"

    return HttpResponse(response)

def consultasP1(request,number):    
    devolv = consultas(number)
    response = "<p>Consulta número {}:</p>".format(number)
    if (number>=1 and number<=4):
        for prod in devolv:
            response+= f"<li>{prod}</li>"
    if number==5:
        response+="<p>La facturación total es de "+str(devolv)+"</p>"
    if number==6:
        response+="<p>La facturación por categoría es:</p>"
        for cat in devolv:
            response += "<p>" + cat + ": " + str(devolv[cat]) + "</p>"


    return HttpResponse(response)

def buscarCategoria(request,category):
    lista_prods_categoria = obtenerInfoPorCategoria(category)

    return render(request,'listing-products.html',{'lista':lista_prods_categoria})

def filtrarCadena(request):
    cadena = request.GET.get('cadena','')
    lista_prods_cadena = obtenerInfoCadena(cadena)
    
    return render(request,'listing-products.html',{'lista':lista_prods_cadena})