from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from .forms import DrexusForm, ProjetoForm, CadastroBiaForm, AQIBiaForm, CQPBiaForm, EntrevistaBiaForm, ParametrizacaoBiaForm, ProbabilidadeBiaForm, SistemasTIBiaForm, OperacaoOperacionalFormSet
from .models import Projeto, Drexus, CadastroBia, AQIBia, CQPBia, EntrevistaBia, ParametrizacaoBia, ProbabilidadeBia, SistemasTIBia, OperacaoOperacional
from django.contrib import admin
from .models import Drexus
from Disrupt.utils.perguntas_drexus import PERGUNTAS_DREXUS 
from django.forms import inlineformset_factory
from xhtml2pdf import pisa
import io 

from .models import (
    Projeto, CadastroBia, AQIBia, CQPBia, ParametrizacaoBia,
    ProbabilidadeBia, SistemasTIBia
)

admin.site.register(Drexus)

def lista_projetos(request):
    projetos_drexus = Drexus.objects.filter(status='ativo')
    projetos_andamento = Projeto.objects.filter(status__icontains="andamento")
    projetos_finalizados = Projeto.objects.filter(status__icontains="finalizado")

    for projeto in projetos_andamento:
        etapas_concluidas = 0
        if CadastroBia.objects.filter(projeto=projeto).exists():
            etapas_concluidas += 1
        # if EntrevistaBia.objects.filter(projeto=projeto).exists():
        #     etapas_concluidas += 1
        if SistemasTIBia.objects.filter(projeto=projeto).exists():
            etapas_concluidas += 1
        if AQIBia.objects.filter(projeto=projeto).exists():
            etapas_concluidas += 1
        if CQPBia.objects.filter(projeto=projeto).exists():
            etapas_concluidas += 1
        if ParametrizacaoBia.objects.filter(projeto=projeto).exists():
            etapas_concluidas += 1
        if ProbabilidadeBia.objects.filter(projeto=projeto).exists():
            etapas_concluidas += 1
        # if TemposBia.objects.filter(projeto=projeto).exists():
        #     etapas_concluidas += 1

        projeto.progresso = etapas_concluidas * 12.5

    return render(request, 'projetos/lista_projetos.html', {
        'projetos_drexus': projetos_drexus,
        'projetos_andamento': projetos_andamento,
        'projetos_finalizados': projetos_finalizados,
    })

# View de detalhe de um projeto específico

def detalhe_projeto(request, id):
    projeto = get_object_or_404(Projeto, id=id)

    etapas_concluidas = 0

    if CadastroBia.objects.filter(projeto=projeto).exists():
        etapas_concluidas += 1
    #if EntrevistaBia.objects.filter(projeto=projeto).exists():
    # etapas_concluidas += 1
    if SistemasTIBia.objects.filter(projeto=projeto).exists():
        etapas_concluidas += 1
    if AQIBia.objects.filter(projeto=projeto).exists():
        etapas_concluidas += 1
    if CQPBia.objects.filter(projeto=projeto).exists():
        etapas_concluidas += 1
    if ParametrizacaoBia.objects.filter(projeto=projeto).exists():
        etapas_concluidas += 1
    if ProbabilidadeBia.objects.filter(projeto=projeto).exists():
        etapas_concluidas += 1
    #if TemposBia.objects.filter(projeto=projeto).exists():
    # etapas_concluidas += 1

    progresso = etapas_concluidas * 12.5  # 12.5% por etapa

    return render(request, 'projetos/detalhe_projeto.html', {
        'projeto': projeto,
        'progresso': progresso
    })


def criar_projeto(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')

        if nome:
            Projeto.objects.create(nome=nome, descricao=descricao)
            return redirect('projetos:lista_projetos')

    return render(request, 'projetos/criar_projeto.html')

def criar_drexus(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')

        Drexus.objects.create(
            nome=nome,
            descricao=descricao
        )
        return redirect('projetos:lista_projetos')
    
    return render(request, 'projetos/criar_drexus.html')

def planilha_projeto(request, id):
    projeto = get_object_or_404(Projeto, pk=id)
    return render(request, 'projetos/planilha_projeto.html', {'projeto': projeto})

# Aqui estão as coisas que montaão o formulario da DREXUS
def formulario_drexus_view(request, pk=None):
    if pk:
        drexus = get_object_or_404(Drexus, pk=pk)
    else:
        drexus = None

    if request.method == 'POST':
        form = DrexusForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data.pop('nome')
            descricao = form.cleaned_data.pop('descricao')

            if drexus is None:
                drexus = Drexus(nome=nome, descricao=descricao)
            else:
                drexus.nome = nome
                drexus.descricao = descricao
                # Zera listas antigas
                for grupo in ['IF', 'Cm', 'Et', 'DREq', 'Lc', 'Im', 'Pv']:
                    setattr(drexus, f"{grupo}_notas", [])

            # Preenche as novas notas
            for key, value in form.cleaned_data.items():
                grupo, _ = key.split("_")
                notas = getattr(drexus, f"{grupo}_notas", [])
                notas.append(int(value))
                setattr(drexus, f"{grupo}_notas", notas)

            drexus.save()
            return redirect('projetos:resultado', pk=drexus.pk)
    else:
        if drexus:
            # Preenche dados atuais do objeto no formulário
            initial_data = {
                'nome': drexus.nome,
                'descricao': drexus.descricao,
            }
            for grupo in ['IF', 'Cm', 'Et', 'DREq', 'Lc', 'Im', 'Pv']:
                notas = getattr(drexus, f"{grupo}_notas", [])
                for i, nota in enumerate(notas, start=1):
                    initial_data[f"{grupo}_{i}"] = nota
            form = DrexusForm(initial=initial_data)
        else:
            form = DrexusForm()

    return render(request, 'projetos/formulario_drexus.html', {'form': form})

def editar_drexus(request, pk):
    drexus = get_object_or_404(Drexus, pk=pk)

    if request.method == 'POST':
        form = DrexusForm(request.POST)
        if form.is_valid():
            drexus.nome = form.cleaned_data.pop('nome')
            drexus.descricao = form.cleaned_data.pop('descricao')

            for key, value in form.cleaned_data.items():
                grupo, _ = key.split("_")
                notas = getattr(drexus, f"{grupo}_notas")
                idx = int(key.split("_")[1]) - 1
                while len(notas) <= idx:
                    notas.append(0)
                notas[idx] = int(value)
                setattr(drexus, f"{grupo}_notas", notas)

            drexus.save()
            return redirect('projetos:resultado', pk=drexus.pk) 
    else:
        initial_data = {
            'nome': drexus.nome,
            'descricao': drexus.descricao
        }

        for grupo, perguntas in PERGUNTAS_DREXUS.items():
            notas = getattr(drexus, f"{grupo}_notas", [])
            for i in range(1, len(perguntas) + 1):
                if i <= len(notas):
                    initial_data[f"{grupo}_{i}"] = notas[i - 1]
                else:
                    initial_data[f"{grupo}_{i}"] = None

        form = DrexusForm(initial=initial_data)

    return render(request, 'projetos/formulario_drexus.html', {'form': form, 'editar': True})


def resultado_view(request, pk):
    drexus = get_object_or_404(Drexus, pk=pk)
    context = {'drexus': drexus}
    return render(request, 'projetos/resultado.html', context)


# Funções para as tabelas BIA (agora buscam dados) --------------------------------------------------
def aqi_bia(request, id): 
    projeto = get_object_or_404(Projeto, id=id)
    entradas_aqi = AQIBia.objects.filter(projeto=projeto).order_by('id') 
    context = {
        'projeto': projeto, 
        'entradas_aqi': entradas_aqi, 
    }
    return render(request, 'projetos/AQI_BIA.html', context)

def cqp_bia(request, id): 
    projeto = get_object_or_404(Projeto, id=id)
    entradas_cqp = CQPBia.objects.filter(projeto=projeto).order_by('id')
    context = {
        'projeto': projeto, 
        'entradas_cqp': entradas_cqp, 
    }
    return render(request, 'projetos/cqp_BIA.html', context)

def cadastro_bia_view(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    entradas_cadastro = CadastroBia.objects.filter(projeto=projeto).order_by('id')
    context = {
        'projeto': projeto,
        'entradas_cadastro': entradas_cadastro, 
    }
    return render(request, 'projetos/CADASTRO_BIA.html', context)

def parametrizacao_bia_view(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    
    entradas_parametrizacao = ParametrizacaoBia.objects.filter(projeto=projeto).order_by('id').prefetch_related('operacoes_operacionais')
    
    parametrizacoes_para_template = []
    
    # Definir os nomes das classificações de impacto para cada nível
    fix_classificacao_data = {
        '1': 'Muito Alto',
        '2': 'Alto',
        '3': 'Médio',
        '4': 'Baixo',
        '5': 'Muito Baixo',
    }
    
    for entrada in entradas_parametrizacao:
        operacoes_operacionais = entrada.operacoes_operacionais.all().order_by('id')
        
        nomes_operacoes_colunas = [op.nome_operacao for op in operacoes_operacionais]
        
        # Estrutura para armazenar todos os dados da tabela por nível para esta ParametrizacaoBia
        dados_tabela_por_nivel = []

        for nivel_idx in range(1, 6): # Para cada nível de 1 a 5
            nivel_str = str(nivel_idx)
            
            # Coletar dados da ParametrizacaoBia para o nível atual
            row_data = {
                'nivel': nivel_str,
                'classificacao': fix_classificacao_data[nivel_str], # Usando o dicionário fixo
                
                # Acessando atributos diretamente do objeto 'entrada'
                'valor_exposicao': getattr(entrada, f'valor_exposicao_{nivel_str}', '-'),
                'img_rep_midias': getattr(entrada, f'img_rep_midias_{nivel_str}', '-'),
                'img_rep_stakeholders': getattr(entrada, f'img_rep_stakeholders_{nivel_str}', '-'),
                
                'legal_penalidade': getattr(entrada, f'legal_penalidade_{nivel_str}', '-'),
                'legal_contrato': getattr(entrada, f'legal_contrato_{nivel_str}', '-'),
                
                'amb': getattr(entrada, f'amb_{nivel_str}', '-'),
                'social': getattr(entrada, f'social_{nivel_str}', '-'),
                'estrategia': getattr(entrada, f'estrategia_{nivel_str}', '-'),
                
                'operacionais': [] # Lista para os valores de operações operacionais neste nível
            }

            # Coletar dados das OperacaoOperacional para o nível atual
            for op in operacoes_operacionais:
                valor_do_nivel = getattr(op, f'valor_nivel_{nivel_str}', '-')
                row_data['operacionais'].append(valor_do_nivel)
            
            dados_tabela_por_nivel.append(row_data)

        parametrizacoes_para_template.append({
            'parametrizacao': entrada, # Mantemos o objeto ParametrizacaoBia para links de edição/exclusão
            'nomes_operacoes_colunas': nomes_operacoes_colunas,
            'dados_tabela_por_nivel': dados_tabela_por_nivel, # Passa a estrutura completa da tabela por nível
        })

    context = {
        'projeto': projeto,
        'parametrizacoes_com_operacoes': parametrizacoes_para_template,
    }
    return render(request, 'projetos/PARAMETRIZACAO_BIA.html', context)

def sistemas_ti_bia_view(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    entradas_sistemas_ti = SistemasTIBia.objects.filter(projeto=projeto).order_by('id')
    context = {
        'projeto': projeto,
        'entradas_sistemas_ti': entradas_sistemas_ti, 
    }
    return render(request, 'projetos/SISTEMAS_TI_BIA.html', context)


# Função de editar projeto ------------------------------------------------------------------
def editar_projeto(request, id):
    projeto = get_object_or_404(Projeto, id=id)
    if request.method == 'POST':
        form = ProjetoForm(request.POST, instance=projeto)
        if form.is_valid():
            form.save() 
            return redirect('projetos:detalhe_projeto', id=projeto.id)     
    else:
        form = ProjetoForm(instance=projeto)
    context = {
        'form': form,
        'projeto': projeto
    }
    return render(request, 'projetos/editar_projeto.html', context)

# Função para mover da drexus para projetos em andamento
def mover_drexus(request, drexus_id):
    if request.method == 'POST':
        drexus_a_mover = get_object_or_404(Drexus, id=drexus_id)
        
        # 1. Cria o novo projeto BIA, passando o vínculo para a análise original
        novo_projeto = Projeto.objects.create(
            nome=drexus_a_mover.nome,
            descricao=drexus_a_mover.descricao,
            status='andamento',
            analise_drexus_original=drexus_a_mover 
        )
        
        # 2. Muda o status do Drexus para "movido"
        drexus_a_mover.status = 'movido'
        drexus_a_mover.save()
        
        return redirect('projetos:detalhe_projeto', id=novo_projeto.id)
    return redirect('projetos:lista_projetos')

def ver_resultado_drexus(request, projeto_id):
    # Pega o projeto BIA pelo ID
    projeto = get_object_or_404(Projeto, id=projeto_id)
    # Acessa a análise Drexus vinculada a ele
    drexus_original = projeto.analise_drexus_original
    
    context = {
        # Passa o objeto Drexus para o mesmo template que você já usa!
        'drexus': drexus_original,
        'projeto_bia_relacionado': projeto # Opcional, para um link de "voltar"
    }
    # Reutiliza o seu template de resultado já existente!
    return render(request, 'projetos/resultado.html', context)

# Função para mover projetos em andamento para projetos finalizados
def finalizar_projeto(request, id):
    if request.method == 'POST':
        projeto = get_object_or_404(Projeto, id=id)
        projeto.status = 'finalizado'
        projeto.save()
        return redirect('projetos:lista_projetos')
    return redirect('projetos:detalhe_projeto', id=id)

# Função para deletar projetos em andamento ou finalizados
def deletar_projeto(request, pk):
    projeto = get_object_or_404(Projeto, pk=pk)
    if request.method == 'POST':
        projeto.delete()
        return redirect('projetos:lista_projetos')
    return redirect('projetos:detalhe_projeto', id=projeto.pk)

# Função para deletar drexus
def deletar_drexus(request, pk):
    drexus = get_object_or_404(Drexus, pk=pk)
    if request.method == 'POST':
        drexus.delete()
        return redirect('projetos:lista_projetos')
    return redirect('projetos:lista_projetos')

def probabilidade_bia(request, id):
    projeto = get_object_or_404(Projeto, id=id)
    entradas_probabilidade = ProbabilidadeBia.objects.filter(projeto=projeto).order_by('id')
    context = {
        'projeto': projeto,
        'entradas_probabilidade': entradas_probabilidade, 
    }
    return render(request, 'projetos/PROBABILIDADE_BIA.html', context)


#--------- FORMULÁRIOS PARA ADCICIONAR AQI ------------------------------------------------------------------------------------#
def adicionar_aqi_bia(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    if request.method == 'POST':
        form = AQIBiaForm(request.POST)
        if form.is_valid():
            novo_cadastro = form.save(commit=False)
            novo_cadastro.projeto = projeto
            novo_cadastro.save()
            # Redireciona para a URL de visualização da tabela AQI_BIA
            return redirect('projetos:AQI_BIA', id=projeto.id) 
    else:
        form = AQIBiaForm()

    context = {
        'form': form,
        'projeto': projeto
    }
    return render(request, 'projetos/adicionar_aqi_bia.html', context)

#-------------------- Views para Edição e Exclusão de AQIBia --------------------
def editar_aqi_bia(request, projeto_id, aqi_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    aqi_entrada = get_object_or_404(AQIBia, id=aqi_id, projeto=projeto)

    if request.method == 'POST':
        form = AQIBiaForm(request.POST, instance=aqi_entrada)
        if form.is_valid():
            form.save()
            # Redireciona para a URL de visualização da tabela AQI_BIA
            return redirect('projetos:AQI_BIA', id=projeto.id) 
    else:
        form = AQIBiaForm(instance=aqi_entrada)
    
    context = {
        'form': form,
        'projeto': projeto,
        'aqi_entrada': aqi_entrada, 
    }
    # Reutilize o template de adicionar para a página de edição
    return render(request, 'projetos/adicionar_aqi_bia.html', context) 

def deletar_aqi_bia(request, projeto_id, aqi_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    aqi_entrada = get_object_or_404(AQIBia, id=aqi_id, projeto=projeto)
    
    if request.method == 'POST':
        aqi_entrada.delete()
        # Redireciona para a URL de visualização da tabela AQI_BIA após a exclusão
        return redirect('projetos:AQI_BIA', id=projeto.id)
    
    # Se alguém tentar acessar a URL via GET, apenas redireciona para a lista
    return redirect('projetos:AQI_BIA', id=projeto.id) 

#------------------------ FORMULÁRIOS PARA ADICIONAR CADASTRO -----------------------------------------------------#
def adicionar_cadastro_bia(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    if request.method == 'POST':
        form = CadastroBiaForm(request.POST)
        if form.is_valid():
            novo_cadastro = form.save(commit=False)
            novo_cadastro.projeto = projeto
            novo_cadastro.save()
            return redirect('projetos:cadastro_bia', projeto_id=projeto.id)
    else:
        form = CadastroBiaForm()

    context = {
        'form': form,
        'projeto': projeto
    }
    return render(request, 'projetos/adicionar_cadastro_bia.html', context)

#-------------------- Views para Edição e Exclusão de CADASTRO --------------------
def editar_cadastro_bia(request, projeto_id, cadastro_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    cadastro_entrada = get_object_or_404(CadastroBia, id=cadastro_id, projeto=projeto)

    if request.method == 'POST':
        form = CadastroBiaForm(request.POST, instance=cadastro_entrada)
        if form.is_valid():
            form.save()
            return redirect('projetos:cadastro_bia', projeto_id=projeto.id) 
    else:
        form = CadastroBiaForm(instance=cadastro_entrada)
    
    context = {
        'form': form,
        'projeto': projeto,
        'cadastro_entrada': cadastro_entrada, 
    }
    # Reutiliza o template de adicionar para a página de edição
    return render(request, 'projetos/adicionar_cadastro_bia.html', context) 


def deletar_cadastro_bia(request, projeto_id, cadastro_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    cadastro_entrada = get_object_or_404(CadastroBia, id=cadastro_id, projeto=projeto)
    
    if request.method == 'POST':
        cadastro_entrada.delete()
        return redirect('projetos:cadastro_bia', projeto_id=projeto.id)
    
    # Se o método não for POST, apenas redireciona de volta para a lista
    return redirect('projetos:cadastro_bia', projeto_id=projeto.id)

#------------------------ FORMULÁRIO PARA ADICONAR CQP ---------------------------------------------------#
def adicionar_cqp_bia(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    if request.method == 'POST':
        form = CQPBiaForm(request.POST)
        if form.is_valid():
            novo_cadastro = form.save(commit=False)
            novo_cadastro.projeto = projeto
            novo_cadastro.save()
            return redirect('projetos:CQP_BIA', id=projeto.id) 
    else:
        form = CQPBiaForm()

    context = {
        'form': form,
        'projeto': projeto
    }
    return render(request, 'projetos/adicionar_cqp_bia.html', context)

#-------------------- Views para Edição e Exclusão de CQPBia --------------------
def editar_cqp_bia(request, projeto_id, cqp_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    cqp_entrada = get_object_or_404(CQPBia, id=cqp_id, projeto=projeto)

    if request.method == 'POST':
        form = CQPBiaForm(request.POST, instance=cqp_entrada)
        if form.is_valid():
            form.save()
            return redirect('projetos:CQP_BIA', id=projeto.id) 
    else:
        form = CQPBiaForm(instance=cqp_entrada)
    
    context = {
        'form': form,
        'projeto': projeto,
        'cqp_entrada': cqp_entrada, 
    }
    return render(request, 'projetos/adicionar_cqp_bia.html', context) 

def deletar_cqp_bia(request, projeto_id, cqp_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    cqp_entrada = get_object_or_404(CQPBia, id=cqp_id, projeto=projeto)
    
    if request.method == 'POST':
        cqp_entrada.delete()
        return redirect('projetos:CQP_BIA', id=projeto.id)
    
    # Se alguém tentar acessar a URL via GET, apenas redireciona para a lista
    return redirect('projetos:CQP_BIA', id=projeto.id) 

#--------------------- FORMULÁRIO PARA ADICIONAR PARAMETRIZAÇÃO ------------------------------------------#
def adicionar_parametrizacao_bia(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    
    if request.method == 'POST':
        form = ParametrizacaoBiaForm(request.POST)
        formset = OperacaoOperacionalFormSet(request.POST, prefix='operacoes', instance=ParametrizacaoBia()) 

        if form.is_valid() and formset.is_valid():
            # ... (sua lógica de salvamento existente) ...
            parametrizacao = form.save(commit=False)
            parametrizacao.projeto = projeto
            parametrizacao.save()
            
            operacoes_salvas = formset.save(commit=False) 
            for operacao in operacoes_salvas:
                operacao.parametrizacao_bia = parametrizacao
                operacao.save()
            
            for obj in formset.deleted_objects:
                obj.delete()

            return redirect('projetos:parametrizacao_bia', projeto_id=projeto.id)
        else:
            # >>>>> ADICIONE ESTAS DUAS LINHAS PARA VER OS ERROS DE VALIDAÇÃO <<<<<
            print("\n----- ERROS DO FORMULÁRIO PRINCIPAL -----")
            print(form.errors)
            print("\n----- ERROS DO FORMSET -----")
            print(formset.errors)
            print("------------------------------------------\n")
    else: # GET request
        form = ParametrizacaoBiaForm()
        formset = OperacaoOperacionalFormSet(prefix='operacoes', instance=ParametrizacaoBia()) 

    context = {
        'form': form,
        'formset': formset,
        'projeto': projeto
    }
    return render(request, 'projetos/adicionar_parametrizacao_bia.html', context)

#-------------------- Views para Edição e Exclusão de ParametrizacaoBia --------------------
def editar_parametrizacao_bia(request, projeto_id, parametrizacao_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    parametrizacao_entrada = get_object_or_404(ParametrizacaoBia, id=parametrizacao_id, projeto=projeto)

    if request.method == 'POST':
        form = ParametrizacaoBiaForm(request.POST, instance=parametrizacao_entrada)
        formset = OperacaoOperacionalFormSet(request.POST, prefix='operacoes', instance=parametrizacao_entrada)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save() 
            return redirect('projetos:parametrizacao_bia', projeto_id=projeto.id)
        else:
            # >>>>> ADICIONE ESTAS DUAS LINHAS PARA VER OS ERROS DE VALIDAÇÃO <<<<<
            print("\n----- ERROS DO FORMULÁRIO PRINCIPAL (EDIÇÃO) -----")
            print(form.errors)
            print("\n----- ERROS DO FORMSET (EDIÇÃO) -----")
            print(formset.errors)
            print("--------------------------------------------------\n")
    else: # GET request
        form = ParametrizacaoBiaForm(instance=parametrizacao_entrada)
        formset = OperacaoOperacionalFormSet(prefix='operacoes', instance=parametrizacao_entrada)
    
    context = {
        'form': form,
        'formset': formset,
        'projeto': projeto,
        'parametrizacao_entrada': parametrizacao_entrada, 
    }
    return render(request, 'projetos/adicionar_parametrizacao_bia.html', context) 

#-------------------- Views para Edição e Exclusão de ParametrizacaoBia --------------------
def editar_parametrizacao_bia(request, projeto_id, parametrizacao_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    parametrizacao_entrada = get_object_or_404(ParametrizacaoBia, id=parametrizacao_id, projeto=projeto)

    if request.method == 'POST':
        form = ParametrizacaoBiaForm(request.POST, instance=parametrizacao_entrada)
        formset = OperacaoOperacionalFormSet(request.POST, prefix='operacoes', instance=parametrizacao_entrada)
        
        if form.is_valid() and formset.is_valid():
            form.save() # Salva o formulário principal
            
            # formset.save() sem commit=False já lida com tudo (criação, atualização, exclusão)
            # Ele retorna uma tupla de (new_objects, changed_objects, deleted_objects)
            # mas você não precisa iterar sobre eles manualmente para associar o pai,
            # já que o formset sabe quem é o pai (parametrizacao_entrada).
            formset.save() 
            
            return redirect('projetos:parametrizacao_bia', projeto_id=projeto.id)
        else:
            # Se o formulário ou formset não são válidos, eles são renderizados novamente com erros.
            print("Formulário principal erros:", form.errors)
            print("Formset erros:", formset.errors)
    else: # GET request
        form = ParametrizacaoBiaForm(instance=parametrizacao_entrada)
        formset = OperacaoOperacionalFormSet(prefix='operacoes', instance=parametrizacao_entrada)
    
    context = {
        'form': form,
        'formset': formset,
        'projeto': projeto,
        'parametrizacao_entrada': parametrizacao_entrada, 
    }
    return render(request, 'projetos/adicionar_parametrizacao_bia.html', context) 

def deletar_parametrizacao_bia(request, projeto_id, parametrizacao_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    parametrizacao_entrada = get_object_or_404(ParametrizacaoBia, id=parametrizacao_id, projeto=projeto)

    if request.method == 'POST':
        parametrizacao_entrada.delete()
        return redirect('projetos:parametrizacao_bia', projeto_id=projeto.id)

    # Se alguém tentar acessar a URL via GET, apenas redireciona para a lista
    return redirect('projetos:parametrizacao_bia', projeto_id=projeto.id)

#---------------------- FORMULÁRIO PARA ADICIONAR PROBABILIDADE -----------------------------------------------#
def adicionar_probabilidade_bia(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    if request.method == 'POST':
        form = ProbabilidadeBiaForm(request.POST)
        if form.is_valid():
            novo_cadastro = form.save(commit=False)
            novo_cadastro.projeto = projeto
            novo_cadastro.save()
            return redirect('projetos:PROBABILIDADE_BIA', id=projeto.id) 
    else:
        form = ProbabilidadeBiaForm()

    context = {
        'form': form,
        'projeto': projeto
    }
    return render(request, 'projetos/adicionar_probabilidade_bia.html', context)

#------------------------FORMULÁRIO PARA ADICIONAR SISTEMAS DE TI ----------------------------------------------#
def adicionar_sistemas_ti_bia(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    if request.method == 'POST':
        form = SistemasTIBiaForm(request.POST)
        if form.is_valid():
            novo_cadastro = form.save(commit=False)
            novo_cadastro.projeto = projeto
            novo_cadastro.save()
            return redirect('projetos:sistemas_ti_bia', projeto_id=projeto.id)
    else:
        form = SistemasTIBiaForm()

    context = {
        'form': form,
        'projeto': projeto
    }
    return render(request, 'projetos/adicionar_sistemas_ti_bia.html', context)

#-------------------- Views para Edição e Exclusão de Sistemas de TI --------------------
def editar_sistemas_ti_bia(request, projeto_id, sistema_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    sistema_entrada = get_object_or_404(SistemasTIBia, id=sistema_id, projeto=projeto)

    if request.method == 'POST':
        form = SistemasTIBiaForm(request.POST, instance=sistema_entrada)
        if form.is_valid():
            form.save()
            return redirect('projetos:sistemas_ti_bia', projeto_id=projeto.id) 
    else:
        form = SistemasTIBiaForm(instance=sistema_entrada)
    
    context = {
        'form': form,
        'projeto': projeto,
        'sistema_entrada': sistema_entrada, 
    }
    # Reutiliza o mesmo template do formulário de adicionar
    return render(request, 'projetos/adicionar_sistemas_ti_bia.html', context) 

def deletar_sistemas_ti_bia(request, projeto_id, sistema_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    sistema_entrada = get_object_or_404(SistemasTIBia, id=sistema_id, projeto=projeto)
    
    if request.method == 'POST':
        sistema_entrada.delete()
        return redirect('projetos:sistemas_ti_bia', projeto_id=projeto.id)
    
    # Se o método não for POST, apenas redireciona de volta para a lista
    return redirect('projetos:sistemas_ti_bia', projeto_id=projeto.id)


#-------------------------------------------------------
def lista_entrevistas_bia(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    entrevistas = EntrevistaBia.objects.filter(projeto=projeto).order_by('id')
    context = {
        'projeto': projeto,
        'entrevistas': entrevistas,
    }
    return render(request, 'projetos/ENTREVISTA_BIA.html', context)


def adicionar_entrevista_bia(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    if request.method == 'POST':
        form = EntrevistaBiaForm(request.POST)
        if form.is_valid():
            entrevista = form.save(commit=False)
            entrevista.projeto = projeto
            entrevista.save()
            return redirect('projetos:lista_entrevistas_bia', projeto_id=projeto.id) # Redireciona para a lista de entrevistas
        else:
            print("Erros no formulário da Entrevista BIA:", form.errors) # Para depuração
    else:
        form = EntrevistaBiaForm()

    context = {
        'form': form,
        'projeto': projeto,
    }
    return render(request, 'projetos/adicionar_entrevista_bia.html', context)

# Você também vai precisar de uma view para editar a entrevista, similar a editar_parametrizacao_bia
def editar_entrevista_bia(request, projeto_id, entrevista_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    entrevista = get_object_or_404(EntrevistaBia, id=entrevista_id, projeto=projeto)

    if request.method == 'POST':
        form = EntrevistaBiaForm(request.POST, instance=entrevista)
        if form.is_valid():
            form.save()
            return redirect('projetos:lista_entrevistas_bia', projeto_id=projeto.id)
        else:
            print("Erros no formulário de edição da Entrevista BIA:", form.errors)
    else:
        form = EntrevistaBiaForm(instance=entrevista)

    context = {
        'form': form,
        'projeto': projeto,
        'entrevista': entrevista,
    }
    return render(request, 'projetos/adicionar_entrevista_bia.html', context) # Reutiliza o template de adicionar


# E uma view para deletar, similar a deletar_parametrizacao_bia
def deletar_entrevista_bia(request, projeto_id, entrevista_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    entrevista = get_object_or_404(EntrevistaBia, id=entrevista_id, projeto=projeto)

    if request.method == 'POST':
        entrevista.delete()
        return redirect('projetos:lista_entrevistas_bia', projeto_id=projeto.id)
    
    return redirect('projetos:lista_entrevistas_bia', projeto_id=projeto.id)

# Função para gerar relatório BIA

def gerar_pdf(request, id):
    projeto = get_object_or_404(Projeto, id=id)

    # Coleta por related_name (os que você já tem):
    cadastros = projeto.cadastros_bia.all()
    aqis = projeto.aqis_bia.all()
    cqps = projeto.cqps_bia.all()
    parametrizacoes = projeto.parametrizacoes_bia.all()
    probabilidades = projeto.probabilidades_bia.all()
    sistemas_ti = projeto.sistemas_ti_bia.all()

    entrevistas_manager = getattr(projeto, 'entrevistas_bia', None)
    entrevistas = entrevistas_manager.all() if entrevistas_manager else []

    tempos_manager = getattr(projeto, 'tempos_bia', None)
    tempos = tempos_manager.all() if tempos_manager else []

    context = {
        'projeto': projeto,
        'cadastros': cadastros,
        'aqis': aqis,
        'cqps': cqps,
        'parametrizacoes': parametrizacoes,
        'probabilidades': probabilidades,
        'sistemas_ti': sistemas_ti,
        'entrevistas': entrevistas,
        'tempos': tempos,
    }

    # Renderiza o template HTML
    template = get_template('projetos/relatorio_projeto.html')
    html = template.render(context)

    # Gera o PDF na memória
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="relatorio_projeto_{projeto.id}.pdf"'

    result = io.BytesIO()
    pisa_status = pisa.CreatePDF(
        src=html,
        dest=result,
        encoding='utf-8',
        link_callback=None  # podemos adicionar função p/ arquivos estáticos depois
    )

    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=500)

    response.write(result.getvalue())
    return response

