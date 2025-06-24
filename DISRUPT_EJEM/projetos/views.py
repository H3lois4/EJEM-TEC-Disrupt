# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .forms import DrexusForm
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
            return redirect('lista_projetos')

    return render(request, 'projetos/criar_projeto.html')


def criar_drexus(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')

        # ✅ Criação simples do objeto
        Drexus.objects.create(
            nome=nome,
            descricao=descricao
        )

        return redirect('lista_projetos')
    
    return render(request, 'criar_drexus.html')


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
            return redirect('resultado', pk=drexus.pk)
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