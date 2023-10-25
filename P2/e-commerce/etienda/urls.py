from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("consultasP1/<int:number>/",views.consultasP1,name="consultasP1")
]
