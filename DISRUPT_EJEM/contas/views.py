from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Página pública
def inicio(request):
    return render(request, 'contas/inicio.html')

# Cadastro de novo usuário
def cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar = request.POST.get('confirmar')

        # Verifica se senhas coincidem
        if senha != confirmar:
            messages.error(request, "As senhas não coincidem.")
            return redirect('cadastro')

        # Verifica se e-mail já está cadastrado
        if User.objects.filter(username=email).exists():
            messages.error(request, "Este e-mail já está cadastrado.")
            return redirect('cadastro')

        # Cria o usuário
        user = User.objects.create_user(username=email, email=email, password=senha, first_name=nome)
        login(request, user)
        return redirect('homepage')
    
    return render(request, 'contas/cadastro.html')

# Login de usuário existente
def logar(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = authenticate(request, username=email, password=senha)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'Email ou senha inválidos.')
            return redirect('login')
    
    return render(request, 'contas/login.html')

# Logout
def deslogar(request):
    logout(request)
    return redirect('inicio')

# Página protegida
@login_required(login_url='login')
def homepage(request):
    return render(request, 'contas/homepage.html', {'usuario': request.user})
