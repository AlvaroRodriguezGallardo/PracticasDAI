from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import consultas, obtenerInfoPrincipio,obtenerInfoPorCategoria,obtenerInfoCadena, obtenerCategorias, introducirProducto, obtenerCategoriasEleccion
from .forms import ProductoFormulario, LoginFormulario
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
import os
import logging
logger = logging.getLogger(__name__)

# Create your views here.

# Por defecto, con esto muestro html de enlaces
def index(request):
    lista_productos = obtenerInfoPrincipio()
    categs = obtenerCategorias()
    return render(request,'index.html',{'lista':lista_productos,'categorias':categs})


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
    for document in lista_prods_categoria:
        document['id'] = document.pop('_id')

    categs = obtenerCategorias()
    logger.info("Products of the category "+category)
    return render(request,'listing-products.html',{'lista':lista_prods_categoria,'categorias':categs})

def filtrarCadena(request):
    cadena = request.GET.get('cadena','')
    categs = obtenerCategorias()
    lista_prods_cadena = obtenerInfoCadena(cadena)
    for document in lista_prods_cadena:
        document['id'] = document.pop('_id')
        
    logger.info("Products with substring "+cadena)
    return render(request,'listing-products.html',{'lista':lista_prods_cadena,'categorias':categs})

@login_required(login_url='/etienda/formularioLogin')   #Lo pongo, aunque no se va a ver el botón a menos que esté iniciada la sesión (creo que es buena práctica en el diseño de la interfaz)
def formularioInsertarProducto(request):
    #¿Devolver lista con las categorías para la selección si es de categoría existente?
    form = ProductoFormulario()
    categs = obtenerCategorias()
    #categs_elegir = obtenerCategoriasEleccion()
    logger.info("Insert page for new products")
    return render(request,'insert_product_form.html',{'form':form,'categorias':categs})

@login_required(login_url='/etienda/formularioLogin')
def insertarProducto(request):  # Accesible por petición POST de formulario
    logger.info("Inserting products within a data base")

    if request.method == 'POST' and request.FILES['imagen']:
        form = ProductoFormulario(request.POST,request.FILES)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            precio = form.cleaned_data['precio']
            descripcion = form.cleaned_data['descripcion']
            categoria = form.cleaned_data['categoria']
            nueva_categoria = form.cleaned_data['nueva_categoria']
            imagen = form.cleaned_data['imagen']

            im_name = imagen.name
            guardarImagen(imagen)

            #if not nombre[0].isupper():
            #    messages.error(request,'First letter of the name must be a capital letter')
            #    return render(request,'insert_product_form.html',{'form':form})

            if nueva_categoria == '' and categoria == '':
                messages.error(request,'You have to select a category or introduce a new one!')
                return render(request,'insert_product_form.html',{'form':form})


            if nueva_categoria != '':
                categoria = nueva_categoria #Con MongoDB no tengo porqué comprobar que no esté esa categoría ya

            imagen_ruta = 'imagenes/'+str(im_name)
            my_id,exito = introducirProducto(nombre,precio,descripcion,categoria,imagen_ruta)
            if exito>0:
                messages.success(request,'Product has been storaged!')
            else:
                messages.error(request,'An error happened storaging the product. Check fields! First letter of the name must be a capital letter. You have given '+nombre)
                return render(request,'insert_product_form.html',{'form':form})
            form = ProductoFormulario()
            return render(request,'insert_product_form.html',{'form':form})
        else:
            nombre_errors = form.errors.get('nombre',None)

            if nombre_errors and 'Invalid.' in nombre_errors:
                messages.error(request,'Name must start with capital letter')
            else:
                messages.error(request,'Check fields. Something is not correct. Fill all marked fields')

            #form = ProductoFormulario()

    return render(request,'insert_product_form.html',{'form':form})

def formularioLogin(request):   # Lo hago para poder usar la funcionalidad de los formulario en DJango
    form = LoginFormulario()
    categs = obtenerCategorias()
    logger.info("Page for logging action")

    return render(request,'registration/login.html',{'form':form,'categorias':categs})


def comprobarDatosLogin(request):
    logger.info("Checking if a user is in DB")
    
    if request.method == 'POST':
        form = LoginFormulario(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['contrasenia']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/etienda")
            else:
                messages.error(request, "User given is not registered")
        else:
            messages.error(request, 'Please, fill all inputs')

            # Imprime los errores del formulario para depurar
            print(form.errors)
    else:
        form = LoginFormulario()

    return render(request, 'registration/login.html', {'form': form})

# -----------------------------------------------------------------------------------------------------------------------------------------------------------

# FUNCIONES AUXILIARES

def guardarImagen(imagen):
    saving = 'imagenes/'+imagen.name
    default_storage.save(saving,ContentFile(imagen.read()))

    return 1
