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
    id = models.IntegerField(primary_key=True,unique=True)  # ou use o ID
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='andamento',
    )

    def __str__(self):
        return self.nome
