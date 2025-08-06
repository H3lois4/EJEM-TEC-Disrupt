# models.py

from django.db import models

class Drexus(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    diagnostico = models.CharField(max_length=100,default="")
    diagnostico_maturidade = models.CharField(max_length=100,default="")
    diagnostico_cognitiva = models.CharField(max_length=100,default="")
    diagnostico_estrategica = models.CharField(max_length=100,default="")
    diagnostico_operacional = models.CharField(max_length=100,default="")
    diagnostico_cultural = models.CharField(max_length=100,default="")

    # Variáveis Float
    IF = models.FloatField(default=0)
    Cm = models.FloatField(default=0)
    Et = models.FloatField(default=0)
    DREq = models.FloatField(default=0)
    Lc = models.FloatField(default=0)
    Im = models.FloatField(default=0)
    Pv = models.FloatField(default=0)
    # Variaveis float de Dimensões
    maturidade_cognitiva = models.FloatField(default=0)
    maturidade_estrategica = models.FloatField(default=0)
    maturidade_operacional = models.FloatField(default=0)
    maturidade_cultural = models.FloatField(default=0)

    # Listas de notas (arrays com até 10 inteiros)
    IF_notas = models.JSONField(default=list)
    Cm_notas = models.JSONField(default=list)
    Et_notas = models.JSONField(default=list)
    DREq_notas = models.JSONField(default=list)
    Lc_notas = models.JSONField(default=list)
    Im_notas = models.JSONField(default=list)
    Pv_notas = models.JSONField(default=list)

    # Nota final
    nota_final = models.FloatField(default=0)

    def __str__(self):
        return self.nome

    # Funções para calcular cada variável com base nas suas notas
    def calcular_IF(self):
        if self.IF_notas:
            self.IF = (self.IF_notas[0] * 0.15 + self.IF_notas[1] * 0.1 + self.IF_notas[2] * 0.15+ self.IF_notas[3] * 0.1 + self.IF_notas[4] * 0.1 + self.IF_notas[5] * 0.1 + self.IF_notas[6] * 0.1 + self.IF_notas[7] * 0.05 + self.IF_notas[8] * 0.1 + self.IF_notas[9] * 0.05)/5
        else:
            self.IF = 0
        return self.IF

    def calcular_Cm(self):
        if self.Cm_notas:
            self.Cm =(self.Cm_notas[0] * 0.1 + self.Cm_notas[1] * 0.1 + self.Cm_notas[2] * 0.1+ self.Cm_notas[3] * 0.15 + self.Cm_notas[4] * 0.1 + self.Cm_notas[5] * 0.1 + self.Cm_notas[6] * 0.1 + self.Cm_notas[7] * 0.05 + self.Cm_notas[8] * 0.1 + self.Cm_notas[9] * 0.1) /5
        else:
            self.Cm = 0
        return self.Cm

    def calcular_Et(self):
        if self.Et_notas:
            self.Et = (self.Et_notas[0] * 0.10 + self.Et_notas[1] * 0.15 + self.Et_notas[2] * 0.10 + self.Et_notas[3] * 0.10 + self.Et_notas[4] * 0.10 + self.Et_notas[5] * 0.10 + self.Et_notas[6] * 0.10 + self.Et_notas[7] * 0.05 + self.Et_notas[8] * 0.10 + self.Et_notas[9] * 0.10)/5
        else:
            self.Et = 0
        return self.Et

    def calcular_DREq(self):
        if self.DREq_notas:
            self.DREq = (self.DREq_notas[0] * 0.10 + self.DREq_notas[1] * 0.10 + self.DREq_notas[2] * 0.15 + self.DREq_notas[3] * 0.10 + self.DREq_notas[4] * 0.10 + self.DREq_notas[5] * 0.10 + self.DREq_notas[6] * 0.05 + self.DREq_notas[7] * 0.10 + self.DREq_notas[8] * 0.10 + self.DREq_notas[9] * 0.10)/5
        else:
            self.DREq = 0
        return self.DREq

    def calcular_Lc(self):
        if self.Lc_notas:
            self.Lc = (self.Lc_notas[0] * 0.10 + self.Lc_notas[1] * 0.10 + self.Lc_notas[2] * 0.15 + self.Lc_notas[3] * 0.10 + self.Lc_notas[4] * 0.10 + self.Lc_notas[5] * 0.10 + self.Lc_notas[6] * 0.10 + self.Lc_notas[7] * 0.05 + self.Lc_notas[8] * 0.10 + self.Lc_notas[9] * 0.10)/5
        else:
            self.Lc = 0
        return self.Lc

    def calcular_Im(self):
        if self.Im_notas:
            self.Im = (self.Im_notas[0] * 0.15 + self.Im_notas[1] * 0.10 + self.Im_notas[2] * 0.10 + self.Im_notas[3] * 0.10 + self.Im_notas[4] * 0.10 + self.Im_notas[5] * 0.10 + self.Im_notas[6] * 0.05 + self.Im_notas[7] * 0.10 + self.Im_notas[8] * 0.10 + self.Im_notas[9] * 0.10)/5
        else:
            self.Im = 0
        return self.Im

    def calcular_Pv(self):
        if self.Pv_notas:
            self.Pv = (self.Pv_notas[0] * 0.10 + self.Pv_notas[1] * 0.15 + self.Pv_notas[2] * 0.10 + self.Pv_notas[3] * 0.10 + self.Pv_notas[4] * 0.10 + self.Pv_notas[5] * 0.10 + self.Pv_notas[6] * 0.10 + self.Pv_notas[7] * 0.05 + self.Pv_notas[8] * 0.10 + self.Pv_notas[9] * 0.10)/5
        else:
            self.Pv = 0
        return self.Pv
    
    def calcular_maturidade_cognitiva(self):
        #Maturidade_Cognitiva = (Lc × 0.5) + (Et × 0.3) + (DREq × 0.2)
        self.maturidade_cognitiva = (self.IF * 0.5) + (self.Et * 0.3) + (self.DREq * 0.2)
        return self.maturidade_cognitiva
    
    def calcular_maturidade_estrategica(self):
        #Maturidade_Estratégica = (Pv × 0.4) + (Im × 0.3) + (DREq × 0.3)
        self.maturidade_estrategica = (self.Pv * 0.4) + (self.Im * 0.3) + (self.DREq * 0.3)
        return self.maturidade_estrategica
        
    def calcular_maturidade_operacional(self):
        #Maturidade_Operacional = (If × 0.4) + (Cm × 0.3) + (Et × 0.3)
        self.maturidade_operacional = (self.IF * 0.4) + (self.Cm * 0.3) + (self.Et * 0.3)
        return self.maturidade_operacional
    
    def calcular_maturidade_cultural(self):
        #Maturidade_Cultural = (Et × 0.4) + (DREq × 0.3) + (Pv × 0.3)
        self.maturidade_cultural = (self.Et * 0.4) + (self.DREq * 0.3) + (self.Pv * 0.3)
        return self.maturidade_cultural
    
    def calcular_todas_variaveis(self):
        self.calcular_IF()
        self.calcular_Cm()
        self.calcular_Et()
        self.calcular_DREq()
        self.calcular_Lc()
        self.calcular_Im()
        self.calcular_Pv()
        self.calcular_maturidade_cognitiva()
        self.calcular_maturidade_estrategica()
        self.calcular_maturidade_operacional()
        self.calcular_maturidade_cultural()
        # Não chamar self.save() aqui!

    def calcular_nota_final(self):
        self.calcular_todas_variaveis()
        self.nota_final = (self.IF * self.Cm * self.Et) * (1 + self.DREq * (1 + self.Lc * self.Im * self.Pv))
        # Não chamar self.save() aqui!
        return self.nota_final
    
    def gerar_diagnosticos(self):
        #Gera o diaginotico da zona de maturidade
        if self.nota_final < 0.2:
            self.diagnostico = "Zona de Fragilidade Total"
        elif self.nota_final < 0.4:
            self.diagnostico = "Zona de Resiliência Reativa"
        elif self.nota_final < 0.6:
            self.diagnostico = "Zona de Maturidade Tática"
        elif self.nota_final < 0.8:
            self.diagnostico = "Zona de Resiliência Estratégica"
        else:
            self.diagnostico = "Zona de Antifragilidade Real"

        #Gera o diaginotico da maturidade ICE
        if self.nota_final < 1:
            self.diagnostico_maturidade = "Frágil"
        elif self.nota_final <= 1.5:
            self.diagnostico_maturidade = "Resiliente Linear"
        elif self.nota_final <= 2:
            self.diagnostico_maturidade = "Adaptativo"
        else:
            self.diagnostico_maturidade = "Antifrágil ICE³-R"
        
        #Gera o diaginotico da maturidade cognitiva
        if self.maturidade_cognitiva <= 0.4:
            self.diagnostico_cognitiva = "Zona Crítica (Imaturidade)"
        elif self.maturidade_cognitiva <= 0.6:
            self.diagnostico_cognitiva = "Nível Emergente"
        elif self.maturidade_cognitiva <= 0.8:
            self.diagnostico_cognitiva = "Nível Funcional"
        elif self.maturidade_cognitiva <= 0.9:
            self.diagnostico_cognitiva = "Nível Integrado"
        else:
            self.diagnostico_cognitiva = "Nível Regenerativo Exemplar"
        
        #Gera o diaginotico da maturidade estratégica
        if self.maturidade_estrategica <= 0.4:
            self.diagnostico_estrategica = "Zona Crítica (Imaturidade)"
        elif self.maturidade_estrategica <= 0.6:
            self.diagnostico_estrategica = "Nível Emergente"
        elif self.maturidade_estrategica <= 0.8:
            self.diagnostico_estrategica = "Nível Funcional"
        elif self.maturidade_estrategica <= 0.9:
            self.diagnostico_estrategica = "Nível Integrado"
        else:
            self.diagnostico_estrategica = "Nível Regenerativo Exemplar"

        #Gera o diaginotico da maturidade operacional
        if self.maturidade_operacional <= 0.4:
            self.diagnostico_operacional = "Zona Crítica (Imaturidade)"
        elif self.maturidade_operacional <= 0.6:
            self.diagnostico_operacional = "Nível Emergente"
        elif self.maturidade_operacional <= 0.8:
            self.diagnostico_operacional = "Nível Funcional"
        elif self.maturidade_operacional <= 0.9:
            self.diagnostico_operacional = "Nível Integrado"
        else:
            self.diagnostico_operacional = "Nível Regenerativo Exemplar"

        #Gera o diaginotico da maturidade 
        if self.maturidade_cultural <= 0.4:
            self.diagnostico_cultural = "Zona Crítica (Imaturidade)"
        elif self.maturidade_cultural <= 0.6:
            self.diagnostico_cultural = "Nível Emergente"
        elif self.maturidade_cultural <= 0.8:
            self.diagnostico_cultural = "Nível Funcional"
        elif self.maturidade_cultural <= 0.9:
            self.diagnostico_cultural = "Nível Integrado"
        else:
            self.diagnostico_cultural = "Nível Regenerativo Exemplar"

    def save(self, *args, **kwargs):
        # Calcula tudo antes de salvar, mas evita loop
        self.calcular_nota_final()
        self.gerar_diagnosticos()
        super().save(*args, **kwargs)
    
class Projeto(models.Model):
    STATUS_CHOICES = [
        ('andamento', 'Em Andamento'),
        ('finalizado', 'Finalizado'),
    ]
    
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='andamento',
    )

    def __str__(self):
        return self.nome

# --- Modelos BIA atualizados com base em perguntas_tabelas.py ---

class CadastroBia(models.Model):
    # Definindo as opções para o campo de probabilidade
    PROBABILIDADE_CHOICES = [
        ('Remota', 'Remota'),
        ('Possível', 'Possível'),
        ('Provável', 'Provável'),
        ('Muito Provável', 'Muito Provável'),
    ]

    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='cadastros_bia')
    processos = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    nicho = models.CharField(max_length=255)
    responsavel = models.CharField(max_length=255)
    cenario = models.TextField()
    
    probabilidade = models.CharField(
        max_length=20,
        choices=PROBABILIDADE_CHOICES,
        default='Remota' # Define um valor padrão
    )

    def __str__(self):
        return f"Cadastro BIA para {self.projeto.nome} - {self.processos}"

class AQIBia(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='aqis_bia')
    processo = models.CharField(max_length=255)
    rto = models.CharField(max_length=255, null=True, blank=True) 
    mtpd = models.CharField(max_length=255, null=True, blank=True) 
    
    # Todos os campos de impacto financeiro (Xh e REAL) para CharField
    impacto_financeiro_1h = models.CharField(max_length=255, null=True, blank=True)
    impacto_financeiro_4h = models.CharField(max_length=255, null=True, blank=True)
    impacto_financeiro_8h = models.CharField(max_length=255, null=True, blank=True)
    impacto_financeiro_24h = models.CharField(max_length=255, null=True, blank=True)
    impacto_financeiro_48h = models.CharField(max_length=255, null=True, blank=True)
    impacto_financeiro_REAL = models.CharField(max_length=255, null=True, blank=True)

    # Campos de impacto de imagem e reputação (já estão como CharField)
    impacto_img_rep_1h = models.CharField(max_length=255, null=True, blank=True)
    impacto_img_rep_4h = models.CharField(max_length=255, null=True, blank=True)
    impacto_img_rep_8h = models.CharField(max_length=255, null=True, blank=True)
    impacto_img_rep_24h = models.CharField(max_length=255, null=True, blank=True)
    impacto_img_rep_48h = models.CharField(max_length=255, null=True, blank=True)
    impacto_img_rep_REAL = models.CharField(max_length=255, null=True, blank=True)

    # Campos de impacto operacional (já estão como CharField)
    impacto_operacional_1h = models.CharField(max_length=255, null=True, blank=True)
    impacto_operacional_4h = models.CharField(max_length=255, null=True, blank=True)
    impacto_operacional_8h = models.CharField(max_length=255, null=True, blank=True)
    impacto_operacional_24h = models.CharField(max_length=255, null=True, blank=True)
    impacto_operacional_48h = models.CharField(max_length=255, null=True, blank=True)
    impacto_operacional_REAL = models.CharField(max_length=255, null=True, blank=True)

    # Campos de impacto legal (já estão como CharField)
    impacto_legal_1h = models.CharField(max_length=255, null=True, blank=True)
    impacto_legal_4h = models.CharField(max_length=255, null=True, blank=True)
    impacto_legal_8h = models.CharField(max_length=255, null=True, blank=True)
    impacto_legal_24h = models.CharField(max_length=255, null=True, blank=True)
    impacto_legal_48h = models.CharField(max_length=255, null=True, blank=True)
    impacto_legal_REAL = models.CharField(max_length=255, null=True, blank=True)

    # Campos de impacto ambiental (já estão como CharField)
    impacto_ambiental_1h = models.CharField(max_length=255, null=True, blank=True)
    impacto_ambiental_4h = models.CharField(max_length=255, null=True, blank=True)
    impacto_ambiental_8h = models.CharField(max_length=255, null=True, blank=True)
    impacto_ambiental_24h = models.CharField(max_length=255, null=True, blank=True)
    impacto_ambiental_48h = models.CharField(max_length=255, null=True, blank=True)
    impacto_ambiental_REAL = models.CharField(max_length=255, null=True, blank=True)

    base = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"AQI BIA para {self.processo} do Projeto {self.projeto.nome}"


class CQPBia(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='cqps_bia')
    classificacao_impacto = models.CharField(max_length=255)
    probabilidade = models.CharField(max_length=255) 
    total_criticidade = models.CharField(max_length=255) # Mudei para CharField para aceitar qualquer string
    processos = models.TextField(verbose_name='Quais são os Processos Envolvidos?')
    rto = models.CharField(max_length=255) # Mudei para CharField para aceitar qualquer string
    area = models.CharField(max_length=255)

    def __str__(self):
        return f"CQP BIA para {self.processos} do Projeto {self.projeto.nome}"

class EntrevistaBia(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='entrevistas_bia')
    area = models.CharField(max_length=255, verbose_name="Qual é a Área analisada?")
    macroprocesso = models.CharField(max_length=255, verbose_name="Qual é o Macroprocesso analisado?")
    processo = models.CharField(max_length=255, verbose_name="Qual é o Processo analisado?")
    subprocesso = models.CharField(max_length=255, verbose_name="Qual é o Subprocesso analisado?")
    descricao = models.TextField(verbose_name="Descreva resumidamente a atividade final!")
    aspectos_regulatorios = models.TextField(verbose_name="Aspectos Regulatórios", blank=True, null=True)
    aspectos_contratuais = models.TextField(verbose_name="Aspectos Contratuais", blank=True, null=True)
    entradas_interface = models.TextField(verbose_name="Entradas (Interfaces)", blank=True, null=True)
    saidas_interface = models.TextField(verbose_name="Saídas (Interfaces)", blank=True, null=True)
    volumetrias_interface = models.TextField(verbose_name="Volumetrias (Interfaces)", blank=True, null=True)
    volumetrias_criticas = models.TextField(verbose_name="Volumetrias Críticas", blank=True, null=True)
    slas_volumetrias = models.CharField(max_length=255, verbose_name="SLAs (Volumetrias) em horas", blank=True, null=True)
    rh = models.TextField(verbose_name="Recursos Humanos", blank=True, null=True)
    regime_operacao_equipe = models.TextField(verbose_name="Regime de Operação da Equipe", blank=True, null=True)
    equipe_critica = models.TextField(verbose_name="Equipe Crítica", blank=True, null=True)
    contingencias_rh = models.TextField(verbose_name="Contingências (RH)", blank=True, null=True)
    slas_rh = models.CharField(max_length=255, verbose_name="SLAs (RH) em horas", blank=True, null=True)
    fornecedores = models.TextField(verbose_name="Fornecedores", blank=True, null=True)
    lead_time_insumos = models.CharField(max_length=255, verbose_name="Lead Time (Insumos)", blank=True, null=True)
    contingencias_insumos = models.TextField(verbose_name="Contingências (Insumos)", blank=True, null=True)
    slas_insumos = models.CharField(max_length=255, verbose_name="SLAs (Insumos) em horas", blank=True, null=True)
    sistemas_ti_ta = models.TextField(verbose_name="Sistemas TI TA", blank=True, null=True)
    sistemas_criticos_usuario = models.TextField(verbose_name="Sistemas Críticos (Usuário)", blank=True, null=True)
    contingencias_sistemas = models.TextField(verbose_name="Contingências (Sistemas)", blank=True, null=True)
    slas_sistemas = models.CharField(max_length=255, verbose_name="SLAs (Sistemas) em horas", blank=True, null=True)
    equipamentos = models.TextField(verbose_name="Equipamentos Utilizados", blank=True, null=True)
    equipamentos_criticos = models.TextField(verbose_name="Equipamentos Críticos", blank=True, null=True)
    slas_equipamentos = models.CharField(max_length=255, verbose_name="SLAs (Equipamentos) em horas", blank=True, null=True)
    pontos_criticidade = models.TextField(verbose_name="Pontos de Criticidade", blank=True, null=True)
    pior_cenario = models.TextField(verbose_name="Pior Cenário", blank=True, null=True)
    mtpd_horas = models.CharField(max_length=255, verbose_name="MTPD em horas", blank=True, null=True)
    descricao_motivo_mtpd = models.TextField(verbose_name="Descrição do Motivo MTPD", blank=True, null=True)
    rto_horas = models.CharField(max_length=255, verbose_name="RTO em horas", blank=True, null=True)
    rpo_horas = models.CharField(max_length=255, verbose_name="RPO em horas", blank=True, null=True)
    observacoes = models.TextField(verbose_name="Observações Adicionais", blank=True, null=True)

    def __str__(self):
        return f"Entrevista BIA para {self.projeto.nome} - {self.macroprocesso}"


class ParametrizacaoBia(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='parametrizacoes_bia')
    
    valor_exposicao_1 = models.CharField(max_length=255, null=True, blank=True)
    img_rep_midias_1 = models.CharField(max_length=255, null=True, blank=True)
    img_rep_stakeholders_1 = models.CharField(max_length=255, null=True, blank=True)
    legal_penalidade_1 = models.CharField(max_length=255, null=True, blank=True)
    legal_contrato_1 = models.CharField(max_length=255, null=True, blank=True)
    amb_1 = models.CharField(max_length=255, null=True, blank=True)
    social_1 = models.CharField(max_length=255, null=True, blank=True)
    estrategia_1 = models.CharField(max_length=255, null=True, blank=True)

    valor_exposicao_2 = models.CharField(max_length=255, null=True, blank=True)
    img_rep_midias_2 = models.CharField(max_length=255, null=True, blank=True)
    img_rep_stakeholders_2 = models.CharField(max_length=255, null=True, blank=True)
    legal_penalidade_2 = models.CharField(max_length=255, null=True, blank=True)
    legal_contrato_2 = models.CharField(max_length=255, null=True, blank=True)
    amb_2 = models.CharField(max_length=255, null=True, blank=True)
    social_2 = models.CharField(max_length=255, null=True, blank=True)
    estrategia_2 = models.CharField(max_length=255, null=True, blank=True)

    valor_exposicao_3 = models.CharField(max_length=255, null=True, blank=True)
    img_rep_midias_3 = models.CharField(max_length=255, null=True, blank=True)
    img_rep_stakeholders_3 = models.CharField(max_length=255, null=True, blank=True)
    legal_penalidade_3 = models.CharField(max_length=255, null=True, blank=True)
    legal_contrato_3 = models.CharField(max_length=255, null=True, blank=True)
    amb_3 = models.CharField(max_length=255, null=True, blank=True)
    social_3 = models.CharField(max_length=255, null=True, blank=True)
    estrategia_3 = models.CharField(max_length=255, null=True, blank=True)

    valor_exposicao_4 = models.CharField(max_length=255, null=True, blank=True)
    img_rep_midias_4 = models.CharField(max_length=255, null=True, blank=True)
    img_rep_stakeholders_4 = models.CharField(max_length=255, null=True, blank=True)
    legal_penalidade_4 = models.CharField(max_length=255, null=True, blank=True)
    legal_contrato_4 = models.CharField(max_length=255, null=True, blank=True)
    amb_4 = models.CharField(max_length=255, null=True, blank=True)
    social_4 = models.CharField(max_length=255, null=True, blank=True)
    estrategia_4 = models.CharField(max_length=255, null=True, blank=True)

    valor_exposicao_5 = models.CharField(max_length=255, null=True, blank=True)
    img_rep_midias_5 = models.CharField(max_length=255, null=True, blank=True)
    img_rep_stakeholders_5 = models.CharField(max_length=255, null=True, blank=True)
    legal_penalidade_5 = models.CharField(max_length=255, null=True, blank=True)
    legal_contrato_5 = models.CharField(max_length=255, null=True, blank=True)
    amb_5 = models.CharField(max_length=255, null=True, blank=True)
    social_5 = models.CharField(max_length=255, null=True, blank=True)
    estrategia_5 = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return f"Parametrização BIA para Projeto {self.projeto.nome}"


class ProbabilidadeBia(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='probabilidades_bia')
    processos = models.CharField(max_length=255)
    nicho = models.CharField(max_length=255)

    def __str__(self):
        return f"Probabilidade BIA para {self.processos} do Projeto {self.projeto.nome}"

class SistemasTIBia(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='sistemas_ti_bia')
    subprocessos = models.CharField(max_length=255)
    aplicacoes_sistemas = models.CharField(max_length=255)
    url = models.URLField(max_length=200, blank=True, null=True) # URLField para URLs
    alternativa_manual = models.CharField(max_length=255) 
    
    # Campos de impacto de aplicações e sistemas (já estão como CharField, ótimo!)
    impacto_aplicacoes_30min = models.CharField(max_length=255, null=True, blank=True)
    impacto_aplicacoes_1h = models.CharField(max_length=255, null=True, blank=True)
    impacto_aplicacoes_2h = models.CharField(max_length=255, null=True, blank=True)
    impacto_aplicacoes_6h = models.CharField(max_length=255, null=True, blank=True)
    impacto_aplicacoes_8h = models.CharField(max_length=255, null=True, blank=True)
    impacto_aplicacoes_12h = models.CharField(max_length=255, null=True, blank=True)
    impacto_aplicacoes_24h = models.CharField(max_length=255, null=True, blank=True)
    impacto_aplicacoes_mais_24h = models.CharField(max_length=255, null=True, blank=True, verbose_name='impacto_aplicacoes_+24h')
    
    # RTO/RPO: De CharField para CharField (se aceitar string arbitrária)
    rto = models.CharField(max_length=255)
    rpo = models.CharField(max_length=255)
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Sistema de TI BIA para {self.aplicacoes_sistemas} do Projeto {self.projeto.nome}"
    
#parametrização
class OperacaoOperacional(models.Model):
    parametrizacao_bia = models.ForeignKey(
        'ParametrizacaoBia',
        on_delete=models.CASCADE,
        related_name='operacoes_operacionais', # Este related_name é importante para acessar as operações a partir de ParametrizacaoBia
        verbose_name="Parametrização BIA Associada"
    )
    nome_operacao = models.CharField(
        max_length=255,
        verbose_name="Qual o nome da operação a ser parametrizada?"
    )
    valor_nivel_1 = models.CharField(
        max_length=255,
        verbose_name="Qual o valor do operacional para o nível 1?"
    )
    valor_nivel_2 = models.CharField(
        max_length=255,
        verbose_name="Qual o valor do operacional para o nível 2?"
    )
    valor_nivel_3 = models.CharField(
        max_length=255,
        verbose_name="Qual o valor do operacional para o nível 3?"
    )
    valor_nivel_4 = models.CharField(
        max_length=255,
        verbose_name="Qual o valor do operacional para o nível 4?"
    )
    valor_nivel_5 = models.CharField(
        max_length=255,
        verbose_name="Qual o valor do operacional para o nível 5?"
    )

    def __str__(self):
        return f"Operação: {self.nome_operacao} (Parametrização ID: {self.parametrizacao_bia.id})"