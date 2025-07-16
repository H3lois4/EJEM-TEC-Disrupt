from django.urls import path
from . import views

app_name = 'projetos' 

urlpatterns = [
    #urls.py principal
    path('', views.lista_projetos, name='lista_projetos'),
    path('<int:id>/', views.detalhe_projeto, name='detalhe_projeto'),
    path('<int:id>/planilha/', views.planilha_projeto, name='planilha_projeto'),
    path('novo/', views.criar_projeto, name='criar_projeto'),
    
    #URLs DREXUS
    path('drexus/novo/', views.criar_drexus, name='criar_drexus'), 
    path('drexus/formulario/', views.formulario_drexus_view, name='formulario'),
    path('drexus/resultado/<int:pk>/', views.resultado_view, name='resultado'),
    path('drexus/editar/<int:pk>/', views.editar_drexus, name='editar_drexus'),

    #URLs BIA
    path('<int:id>/AQI/', views.aqi_bia, name='AQI_BIA'),
    path('<int:id>/CQP/', views.cqp_bia, name='CQP_BIA'),
    path('<int:projeto_id>/cadastro/', views.cadastro_bia, name='CADASTRO_BIA'),
    path('<int:id>/PROBABILIDADE/', views.probabilidade_bia, name='PROBABILIDADE_BIA'),
]