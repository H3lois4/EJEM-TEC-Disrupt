from django import forms
from Disrupt.utils.perguntas_drexus import PERGUNTAS_DREXUS
from .models import Projeto, Drexus, AQIBia, CadastroBia, CQPBia, ParametrizacaoBia, ProbabilidadeBia, SistemasTIBia

class DrexusForm(forms.Form):
    nome = forms.CharField(
        label="Nome do Projeto",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Digite o nome do projeto"})
    )

    descricao = forms.CharField(
        label="Descrição do Projeto",
        required=True,
        widget=forms.Textarea(attrs={"placeholder": "Descreva brevemente o projeto"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        choices=[
            (0, "0 = Discordo totalmente / Inexistente"),
            (1, "1 = Muito fraco / Emergente"),
            (2, "2 = Fraco / Iniciado"),
            (3, "3 = Razoável / Em desenvolvimento"),
            (4, "4 = Forte / Estabilizado"),
            (5, "5 = Excelente / Altamente integrado"),
        ]

        for bloco, perguntas in PERGUNTAS_DREXUS.items():
            for idx, texto in enumerate(perguntas, 1):
                field_name = f"{bloco}_{idx}"
                self.fields[field_name] = forms.ChoiceField(
                    label=texto,
                    choices=choices,
                     widget=forms.RadioSelect(attrs={"class": "radio-inline"}),
                    required=True,  # garante que o campo seja obrigatório
                )

    def clean(self):
        cleaned_data = super().clean()
        for field_name, value in cleaned_data.items():
            if value in [None, '', []]:
                self.add_error(field_name, 'Este campo é obrigatório.')
        return cleaned_data

class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        # Defina os campos que o usuário poderá editar
        fields = ['nome', 'descricao']

#FORMs das tabelas bia
class AQIBiaForm(forms.ModelForm):
    class Meta:
        model = AQIBia
        # Inclui todos os campos do modelo, menos o 'projeto' que será associado automaticamente
        exclude = ['projeto']

class CadastroBiaForm(forms.ModelForm):
    class Meta:
        model = CadastroBia
        # Inclui todos os campos do modelo, menos o 'projeto' que será associado automaticamente
        exclude = ['projeto'] 

class CQPBiaForm(forms.ModelForm):
    class Meta:
        model = CQPBia
        # Inclui todos os campos do modelo, menos o 'projeto' que será associado automaticamente
        exclude = ['projeto'] 

class ParametrizacaoBiaForm(forms.ModelForm):
    class Meta:
        model = ParametrizacaoBia
        # Inclui todos os campos do modelo, menos o 'projeto' que será associado automaticamente
        exclude = ['projeto']

class ProbabilidadeBiaForm(forms.ModelForm):
    class Meta:
        model = ProbabilidadeBia
        # Inclui todos os campos do modelo, menos o 'projeto' que será associado automaticamente
        exclude = ['projeto'] 

class SistemasTIBiaForm(forms.ModelForm):
    class Meta:
        model = SistemasTIBia
        # Inclui todos os campos do modelo, menos o 'projeto' que será associado automaticamente
        exclude = ['projeto']