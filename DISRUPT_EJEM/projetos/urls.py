from django.urls import path
from . import views

app_name = 'projetos' 

urlpatterns = [
    #URLs principais
    path('', views.lista_projetos, name='lista_projetos'),
    path('<int:id>/', views.detalhe_projeto, name='detalhe_projeto'),
    path('<int:id>/planilha/', views.planilha_projeto, name='planilha_projeto'),
    path('novo/', views.criar_projeto, name='criar_projeto'),
    path('projetos/<int:projeto_id>/resultado-drexus/', views.ver_resultado_drexus, name='ver_resultado_drexus'),
    
    #URLs DREXUS
    path('drexus/novo/', views.criar_drexus, name='criar_drexus'), 
    path('drexus/formulario/', views.formulario_drexus_view, name='formulario'),
    path('drexus/resultado/<int:pk>/', views.resultado_view, name='resultado'),
    path('drexus/editar/<int:pk>/', views.editar_drexus, name='editar_drexus'),

    #URLs BIA - Visualização das Tabelas
    path('<int:id>/AQI/', views.aqi_bia, name='AQI_BIA'),
    path('<int:id>/CQP/', views.cqp_bia, name='CQP_BIA'),
    path('<int:projeto_id>/cadastro_bia/', views.cadastro_bia_view, name='cadastro_bia'),
    path('<int:projeto_id>/entrevistas_bia/', views.lista_entrevistas_bia, name='lista_entrevistas_bia'),
    path('<int:projeto_id>/parametrizacao/', views.parametrizacao_bia_view, name='parametrizacao_bia'),
    path('<int:projeto_id>/sistemas_ti/', views.sistemas_ti_bia_view, name='sistemas_ti_bia'),
    path('<int:id>/PROBABILIDADE/', views.probabilidade_bia, name='PROBABILIDADE_BIA'),

    path('editar/<int:id>/', views.editar_projeto, name='editar_projeto'),

    #URLs formulários BIA - Adicionar
    path('<int:projeto_id>/aqi_bia/adicionar/', views.adicionar_aqi_bia, name='adicionar_aqi_bia'),
    path('<int:projeto_id>/cadastro_bia/adicionar/', views.adicionar_cadastro_bia, name='adicionar_cadastro_bia'),
    path('<int:projeto_id>/cqp_bia/adicionar/', views.adicionar_cqp_bia, name='adicionar_cqp_bia'),
    path('<int:projeto_id>/entrevistas_bia/adicionar/', views.adicionar_entrevista_bia, name='adicionar_entrevista_bia'),
    path('<int:projeto_id>/parametrizacao_bia/adicionar/', views.adicionar_parametrizacao_bia, name='adicionar_parametrizacao_bia'),
    path('<int:projeto_id>/probabilidade_bia/adicionar/', views.adicionar_probabilidade_bia, name='adicionar_probabilidade_bia'),
    path('<int:projeto_id>/sistemas_ti_bia/adicionar/', views.adicionar_sistemas_ti_bia, name='adicionar_sistemas_ti_bia'),

    # URLs para Editar Bia
    path('<int:projeto_id>/aqi_bia/editar/<int:aqi_id>/', views.editar_aqi_bia, name='editar_aqi_bia'),
    path('<int:projeto_id>/cqp_bia/editar/<int:cqp_id>/', views.editar_cqp_bia, name='editar_cqp_bia'),
    path('<int:projeto_id>/entrevistas_bia/editar/<int:entrevista_id>/', views.editar_entrevista_bia, name='editar_entrevista_bia'),
    path('<int:projeto_id>/parametrizacao_bia/editar/<int:parametrizacao_id>/', views.editar_parametrizacao_bia, name='editar_parametrizacao_bia'),
    path('<int:projeto_id>/sistemas_ti_bia/editar/<int:sistema_id>/', views.editar_sistemas_ti_bia, name='editar_sistemas_ti_bia'),
    path('<int:projeto_id>/cadastro_bia/editar/<int:cadastro_id>/', views.editar_cadastro_bia, name='editar_cadastro_bia'),

    # URLs para Deletar Bia
    path('<int:projeto_id>/aqi_bia/deletar/<int:aqi_id>/', views.deletar_aqi_bia, name='deletar_aqi_bia'),
    path('<int:projeto_id>/cqp_bia/deletar/<int:cqp_id>/', views.deletar_cqp_bia, name='deletar_cqp_bia'),
    path('<int:projeto_id>/entrevistas_bia/deletar/<int:entrevista_id>/', views.deletar_entrevista_bia, name='deletar_entrevista_bia'),
    path('<int:projeto_id>/parametrizacao_bia/deletar/<int:parametrizacao_id>/', views.deletar_parametrizacao_bia, name='deletar_parametrizacao_bia'),
    path('<int:projeto_id>/sistemas_ti_bia/deletar/<int:sistema_id>/', views.deletar_sistemas_ti_bia, name='deletar_sistemas_ti_bia'),
    path('<int:projeto_id>/cadastro_bia/deletar/<int:cadastro_id>/', views.deletar_cadastro_bia, name='deletar_cadastro_bia'),
    
    #URLs MOVER DREXUS P/ BIA P/ FINALIZADOS
    path('drexus/mover/<int:drexus_id>/', views.mover_drexus, name='mover_drexus'),
    path('finalizar/<int:id>/', views.finalizar_projeto, name='finalizar_projeto'),

    #URLs Deletar BIA/ PROJETOS/ FINALIZADOS
    path('projeto/deletar/<int:pk>/', views.deletar_projeto, name='deletar_projeto'),
    path('drexus/deletar/<int:pk>/', views.deletar_drexus, name='deletar_drexus'),

    #URL para gerar PDF
    path('<int:id>/relatorio/', views.gerar_pdf, name='gerar_pdf'),

]