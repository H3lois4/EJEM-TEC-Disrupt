from django import forms
from django.forms import inlineformset_factory
from Disrupt.utils.perguntas_drexus import PERGUNTAS_DREXUS
from Disrupt.utils.perguntas_tabelas import PERGUNTAS_TABELAS
from Disrupt.utils.perguntas_bia import PERGUNTAS_BIA
from .models import Projeto, Drexus, AQIBia, CadastroBia, CQPBia, ParametrizacaoBia, ProbabilidadeBia, SistemasTIBia, OperacaoOperacional, EntrevistaBia
from django.db import models
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

class EntrevistaBiaForm(forms.ModelForm):
    class Meta:
        model = EntrevistaBia
        exclude = ['projeto'] # O campo 'projeto' será preenchido na view
        # O Django irá criar campos de formulário para todos os campos do modelo EntrevistaBia
        # exceto 'projeto'.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dicionário de mapeamento: (bloco_do_PERGUNTAS_BIA, chave_do_campo_no_bloco) -> 'nome_do_campo_no_modelo'
        # Isso garante que campos com nomes repetidos no dicionário perguntas_bia.py
        # sejam mapeados para os nomes de campo ÚNICOS no modelo EntrevistaBia.
        campo_mapeamento = {
            ('GERAL', 'area'): 'area',
            ('GERAL', 'macroprocesso'): 'macroprocesso',
            ('GERAL', 'processo'): 'processo',
            ('GERAL', 'subprocesso'): 'subprocesso',
            ('GERAL', 'descricao'): 'descricao',

            ('ASPECTOS_REGULATÓRIOS', 'aspectos_regulatorios'): 'aspectos_regulatorios',
            ('ASPECTOS_CONTRATUAIS', 'aspectos_regulatorios'): 'aspectos_contratuais', # Mapeia para o campo correto no modelo

            ('INTERFACES_COM_OUTROS_PROCESSOS', 'entradas'): 'entradas_interface',
            ('INTERFACES_COM_OUTROS_PROCESSOS', 'saidas'): 'saidas_interface',
            ('INTERFACES_COM_OUTROS_PROCESSOS', 'volumetrias'): 'volumetrias_interface',

            ('VOLUMETRIAS_CRÍTICAS_DO_PROCESSO', 'volumetrias'): 'volumetrias_criticas',
            ('VOLUMETRIAS_CRÍTICAS_DO_PROCESSO', 'SLAs'): 'slas_volumetrias',

            ('RECURSOS_HUMANOS', 'rh'): 'rh',

            ('REGIME_DE_OPERAÇÃO_DA_ EQUIPE', 'regime_operacao_equipe'): 'regime_operacao_equipe',

            ('DEPENDÊNCIA_DE_RECURSOS_HUMANOS_CRÍTICOS', 'equipe'): 'equipe_critica',
            ('DEPENDÊNCIA_DE_RECURSOS_HUMANOS_CRÍTICOS', 'contingencias'): 'contingencias_rh',
            ('DEPENDÊNCIA_DE_RECURSOS_HUMANOS_CRÍTICOS', 'SLAs'): 'slas_rh',

            ('FORNECEDORES', 'fornecedores'): 'fornecedores',

            ('DEPENDÊNCIA_DE_INSUMOS_CRÍTICOS', 'lead_time'): 'lead_time_insumos',
            ('DEPENDÊNCIA_DE_INSUMOS_CRÍTICOS', 'contingencias'): 'contingencias_insumos',
            ('DEPENDÊNCIA_DE_INSUMOS_CRÍTICOS', 'SLAs'): 'slas_insumos',

            ('SISTEMAS_TI_TA', 'sistemas_ti_ta'): 'sistemas_ti_ta',

            ('DEPENDENCIA_SISTEMAS_TI_TA_CRITICOS', 'sistemas_criticos_usuario'): 'sistemas_criticos_usuario',
            ('DEPENDENCIA_SISTEMAS_TI_TA_CRITICOS', 'contingencias'): 'contingencias_sistemas',
            ('DEPENDENCIA_SISTEMAS_TI_TA_CRITICOS', 'SLAs'): 'slas_sistemas',

            ('EQUIPAMENTOS_UTILIZADOS', 'equipamentos'): 'equipamentos',
            
            ('EQUIPAMENTOS_CRITICOS', 'equipamentos_criticos'): 'equipamentos_criticos',
            ('EQUIPAMENTOS_CRITICOS', 'SLAs'): 'slas_equipamentos',
            
            ('CRITICIDADE_PROCESSO', 'pontos_criticidade'): 'pontos_criticidade',
            
            ('PIOR_CENARIO', 'pior_cenario'): 'pior_cenario',
            
            ('MTPD', 'mtpd_horas'): 'mtpd_horas',
            
            ('MOTIVADORES_MTPD', 'descricao_motivo_mtpd'): 'descricao_motivo_mtpd',
            
            ('RTO', 'rto_horas'): 'rto_horas',
            
            ('RPO', 'rpo_horas'): 'rpo_horas',
            
            ('OBSERVACOES', 'observacoes'): 'observacoes',
        }

        # Aplicar labels e widgets a partir do mapeamento
        for bloco, perguntas_bloco in PERGUNTAS_BIA.items():
            for campo_chave_dicionario, pergunta_texto in perguntas_bloco.items():
                
                # Usa o mapeamento para obter o nome REAL do campo no modelo
                nome_campo_modelo = campo_mapeamento.get((bloco, campo_chave_dicionario))
                
                if nome_campo_modelo and nome_campo_modelo in self.fields:
                    field = self.fields[nome_campo_modelo]
                    field.label = pergunta_texto
                    field.widget.attrs.update({'placeholder': ''}) # Placeholder vazio

                    # Ajustar widget para Textarea se for TextField no modelo
                    if isinstance(self.instance, EntrevistaBia) and \
                       isinstance(self.instance._meta.get_field(nome_campo_modelo), models.TextField):
                        field.widget = forms.Textarea(attrs={'rows': 4, 'placeholder': ''})

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

class OperacaoOperacionalForm(forms.ModelForm):
    class Meta:
        model = OperacaoOperacional
        fields = [
            'nome_operacao',
            'valor_nivel_1', 'valor_nivel_2', 'valor_nivel_3',
            'valor_nivel_4', 'valor_nivel_5'
        ]
        widgets = {
            'nome_operacao': forms.TextInput(attrs={'placeholder': ''}),
            'valor_nivel_1': forms.TextInput(attrs={'placeholder': ''}),
            'valor_nivel_2': forms.TextInput(attrs={'placeholder': ''}),
            'valor_nivel_3': forms.TextInput(attrs={'placeholder': ''}),
            'valor_nivel_4': forms.TextInput(attrs={'placeholder': ''}),
            'valor_nivel_5': forms.TextInput(attrs={'placeholder': ''}),
        }

# FORMSET PARA OPERAÇÕES OPERACIONAIS
OperacaoOperacionalFormSet = inlineformset_factory(
    ParametrizacaoBia,
    OperacaoOperacional,
    form=OperacaoOperacionalForm,
    extra=0,
    can_delete=True,  # <-- MUDE ISTO PARA TRUE!
    min_num=1,
    validate_min=True,
    widgets={'DELETE': forms.HiddenInput()}, # <-- ADICIONE ESTA LINHA DE VOLTA!
)