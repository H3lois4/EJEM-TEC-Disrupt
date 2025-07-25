from django import forms
from Disrupt.utils.perguntas_drexus import PERGUNTAS_DREXUS
from Disrupt.utils.perguntas_tabelas import PERGUNTAS_TABELAS
from .models import Projeto, Drexus, AQIBia, CadastroBia, CQPBia, ParametrizacaoBia, ProbabilidadeBia, SistemasTIBia
import json

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
        fields = ['nome', 'descricao']

# FORMs das tabelas BIA com labels personalizados
class AQIBiaForm(forms.ModelForm):
    class Meta:
        model = AQIBia
        exclude = ['projeto']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'AQI_BIA' in PERGUNTAS_TABELAS:
            aqi_perguntas = PERGUNTAS_TABELAS['AQI_BIA']
            for field_name, field in self.fields.items():
                if field_name in aqi_perguntas:
                    field.label = aqi_perguntas[field_name]

class CadastroBiaForm(forms.ModelForm):
    class Meta:
        model = CadastroBia
        exclude = ['projeto'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'CADASTRO_BIA' in PERGUNTAS_TABELAS:
            cadastro_perguntas = PERGUNTAS_TABELAS['CADASTRO_BIA']
            for field_name, field in self.fields.items():
                if field_name in cadastro_perguntas:
                    field.label = cadastro_perguntas[field_name]

class CQPBiaForm(forms.ModelForm):
    class Meta:
        model = CQPBia
        exclude = ['projeto'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'CQP_BIA' in PERGUNTAS_TABELAS:
            cqp_perguntas = PERGUNTAS_TABELAS['CQP_BIA']
            for field_name, field in self.fields.items():
                if field_name in cqp_perguntas:
                    field.label = cqp_perguntas[field_name]

class ParametrizacaoBiaForm(forms.ModelForm):
    class Meta:
        model = ParametrizacaoBia
        exclude = ['projeto']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'PARAMETRIZACAO' in PERGUNTAS_TABELAS:
            parametrizacao_perguntas = PERGUNTAS_TABELAS['PARAMETRIZACAO']
            for field_name, field in self.fields.items():
                if field_name in parametrizacao_perguntas:
                    field.label = parametrizacao_perguntas[field_name]

class ProbabilidadeBiaForm(forms.ModelForm):
    class Meta:
        model = ProbabilidadeBia
        exclude = ['projeto'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'PROBABILIDADE' in PERGUNTAS_TABELAS:
            probabilidade_perguntas = PERGUNTAS_TABELAS['PROBABILIDADE']
            for field_name, field in self.fields.items():
                if field_name in probabilidade_perguntas:
                    field.label = probabilidade_perguntas[field_name]

class SistemasTIBiaForm(forms.ModelForm):
    class Meta:
        model = SistemasTIBia
        exclude = ['projeto'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'SISTEMAS_TI' in PERGUNTAS_TABELAS:
            sistemas_ti_perguntas = PERGUNTAS_TABELAS['SISTEMAS_TI']
            for field_name, field in self.fields.items():
                if field_name in sistemas_ti_perguntas:
                    field.label = sistemas_ti_perguntas[field_name]