# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .forms import DrexusForm, ProjetoForm
from .models import Projeto, Drexus
from django.contrib import admin
from .models import Drexus
from Disrupt.utils.perguntas_drexus import PERGUNTAS_DREXUS 

admin.site.register(Drexus)

# View que lista todos os projetos
# def lista_projetos(request):
#     projetos = Projeto.objects.all()
#     return render(request, 'projetos/lista_projetos.html', {'projetos': projetos})


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
            return redirect('resultado', pk=drexus.pk)
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


#Funções para as tabelas (ainda sem o banco de dados) --------------------------------------------------
def aqi_bia(request, id): 
    projeto = get_object_or_404(Projeto, id=id)
    context = {
        'projeto': projeto,      
    }
    return render(request, 'projetos/AQI_BIA.html', context)

def cqp_bia(request, id): 
    projeto = get_object_or_404(Projeto, id=id)
    context = {
        'projeto': projeto,     
    }
    return render(request, 'projetos/cqp_BIA.html', context)

def cadastro_bia_view(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    context = {
        'projeto': projeto,
    }
    return render(request, 'projetos/CADASTRO_BIA.html', context)

def parametrizacao_bia_view(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    context = {
        'projeto': projeto,
    }
    return render(request, 'projetos/PARAMETRIZACAO_BIA.html', context)

def sistemas_ti_bia_view(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    context = {
        'projeto': projeto,
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
        # 1. Encontra o Drexus que queremos promover
        drexus_a_mover = get_object_or_404(Drexus, id=drexus_id)

        # 2. Cria um NOVO objeto Projeto, copiando os dados
        novo_projeto = Projeto.objects.create(
            nome=drexus_a_mover.nome,
            descricao=drexus_a_mover.descricao,
            status='andamento' # Define o status inicial como 'Em Andamento'
        )

        # OBS: Ainda não sei como vamos organizar o banco de dados, por hora ta apagando todos os dados da drexus, 
        #talvez tenha q na própria parte de projetos_projetos ter um lugar para guardar esses dados
        drexus_a_mover.delete()

        # 3. Redireciona o usuário para a página de detalhes do NOVO projeto criado
        return redirect('projetos:detalhe_projeto', id=novo_projeto.id)

    # Se alguém tentar acessar a URL via GET, apenas redireciona para a lista
    return redirect('projetos:lista_projetos')

# Função para mover projetos em andamento para projetos finalizados
def finalizar_projeto(request, id):
    if request.method == 'POST':
        # 1. Encontra o projeto que queremos finalizar
        projeto = get_object_or_404(Projeto, id=id)

        # 2. Altera o status para 'finalizado'
        projeto.status = 'finalizado'

        # 3. Salva a mudança no banco de dados
        projeto.save()

        # 4. Redireciona o usuário de volta para a lista de projetos
        return redirect('projetos:lista_projetos')
    
    # Se alguém tentar acessar a URL diretamente, apenas redireciona
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