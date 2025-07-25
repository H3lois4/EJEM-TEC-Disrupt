from django.shortcuts import render, get_object_or_404, redirect
from .forms import DrexusForm, ProjetoForm, CadastroBiaForm, AQIBiaForm, CQPBiaForm, ParametrizacaoBiaForm, ProbabilidadeBiaForm, SistemasTIBiaForm
from .models import Projeto, Drexus, CadastroBia, AQIBia, CQPBia, ParametrizacaoBia, ProbabilidadeBia, SistemasTIBia 
from django.contrib import admin
from .models import Drexus
from Disrupt.utils.perguntas_drexus import PERGUNTAS_DREXUS 

admin.site.register(Drexus)

def lista_projetos(request):
    projetos_drexus = Drexus.objects.all()
    projetos_andamento = Projeto.objects.filter(status__icontains="andamento")
    projetos_finalizados = Projeto.objects.filter(status__icontains="finalizado")

    return render(request, 'projetos/lista_projetos.html', {
        'projetos_drexus': projetos_drexus,
        'projetos_andamento': projetos_andamento,
        'projetos_finalizados': projetos_finalizados,
    })

# View de detalhe de um projeto específico
def detalhe_projeto(request, id):
    projeto = get_object_or_404(Projeto, id=id)
    return render(request, 'projetos/detalhe_projeto.html', {'projeto': projeto})

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
    entradas_parametrizacao = ParametrizacaoBia.objects.filter(projeto=projeto).order_by('id')
    context = {
        'projeto': projeto,
        'entradas_parametrizacao': entradas_parametrizacao, # Passa todas as entradas para o template
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
        novo_projeto = Projeto.objects.create(
            nome=drexus_a_mover.nome,
            descricao=drexus_a_mover.descricao,
            status='andamento'
        )
        drexus_a_mover.delete()
        return redirect('projetos:detalhe_projeto', id=novo_projeto.id)
    return redirect('projetos:lista_projetos')

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
        if form.is_valid():
            novo_cadastro = form.save(commit=False)
            novo_cadastro.projeto = projeto
            novo_cadastro.save()
            # Redireciona para a URL de visualização da tabela Parametrizacao_BIA
            return redirect('projetos:parametrizacao_bia', projeto_id=projeto.id)
    else:
        form = ParametrizacaoBiaForm()

    context = {
        'form': form,
        'projeto': projeto
    }
    return render(request, 'projetos/adicionar_parametrizacao_bia.html', context)

#-------------------- Views para Edição e Exclusão de ParametrizacaoBia --------------------
def editar_parametrizacao_bia(request, projeto_id, parametrizacao_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    parametrizacao_entrada = get_object_or_404(ParametrizacaoBia, id=parametrizacao_id, projeto=projeto)

    if request.method == 'POST':
        form = ParametrizacaoBiaForm(request.POST, instance=parametrizacao_entrada)
        if form.is_valid():
            form.save()
            return redirect('projetos:parametrizacao_bia', projeto_id=projeto.id) 
    else:
        form = ParametrizacaoBiaForm(instance=parametrizacao_entrada)
    
    context = {
        'form': form,
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