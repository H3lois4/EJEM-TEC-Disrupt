from django.contrib import admin
from .models import Projeto

@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'descricao')
