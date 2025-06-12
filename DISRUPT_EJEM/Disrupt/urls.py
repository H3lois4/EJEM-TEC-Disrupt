"""
URL configuration for Disrupt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from projetos import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('contas.urls')),
    path('projetos/', views.lista_projetos, name='lista_projetos'),
    path('projetos/<int:id>/', views.detalhe_projeto, name='detalhe_projeto'),
    path('projetos/<int:id>/planilha/', views.planilha_projeto, name='planilha_projeto'),
    path('projetos/novo/', views.criar_projeto, name='criar_projeto'),
    path('drexus/novo/', views.criar_drexus, name='criar_drexus'), 
    path('formulario/', views.formulario_drexus_view, name='formulario'),
    path('resultado/<int:pk>/', views.resultado_view, name='resultado'),
    path('editarDrexus/<int:pk>/', views.editar_drexus, name='editar_drexus'),
    path('contas/', include('contas.urls'))
]