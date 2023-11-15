from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("consultasP1/<int:number>/",views.consultasP1,name="consultasP1"),
    path("buscarCategoria/<str:category>/",views.buscarCategoria,name="buscarCategoria"),
    path("filtrarCadena",views.filtrarCadena,name="filtrarCadena"),
    path("formularioInsertarProducto",views.formularioInsertarProducto,name="formularioInsertarProducto"),
    path("insertarProducto",views.insertarProducto,name="insertarProducto"),
    path("comprobarDatosLogin",views.comprobarDatosLogin,name="comprobarDatosLogin"),
    path("formularioLogin",views.formularioLogin,name="formularioLogin")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)