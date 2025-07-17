from django.urls import path
from . import views

app_name = 'projetos' 

urlpatterns = [
    #URLs principais
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
    path('<int:projeto_id>/cadastro_bia/', views.cadastro_bia_view, name='cadastro_bia'),
    path('<int:projeto_id>/parametrizacao/', views.parametrizacao_bia_view, name='parametrizacao_bia'),
    path('<int:projeto_id>/sistemas_ti/', views.sistemas_ti_bia_view, name='sistemas_ti_bia'),

    path('editar/<int:id>/', views.editar_projeto, name='editar_projeto'),

    #URLs MOVER DREXUS P/ BIA P/ FINALIZADOS
    path('drexus/mover/<int:drexus_id>/', views.mover_drexus, name='mover_drexus'),
    path('finalizar/<int:id>/', views.finalizar_projeto, name='finalizar_projeto'),

    #URLs Deletar BIA/ PROJETOS/ FINALIZADOS
    path('projeto/deletar/<int:pk>/', views.deletar_projeto, name='deletar_projeto'),
    path('drexus/deletar/<int:pk>/', views.deletar_drexus, name='deletar_drexus'),
]