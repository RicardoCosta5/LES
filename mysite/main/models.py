import datetime
from django.db import models
from django.utils import timezone

class Docente(models.Model):
    codigo = models.IntegerField()
    docente = models.CharField(max_length=255)
    ativo = models.CharField(max_length=2)
    nome = models.CharField(max_length=255)
    individuo = models.IntegerField()
    data_nascimento = models.CharField(max_length=255)
    sexo = models.CharField(max_length=2)
    tipo_identificacao = models.IntegerField()
    identificacao = models.CharField(max_length=255)
    data_emissao_identificacao = models.CharField(max_length=255)
    nacionalidade = models.IntegerField()
    arquivo = models.CharField(max_length=255)
    data_validade_identificacao = models.CharField(max_length=255)
    nif = models.CharField(max_length=9)
    pais_fiscal = models.CharField(max_length=255)
    digito_verificacao = models.CharField(max_length=255)
    nbsp = models.CharField(max_length=255)

class Funcionario(models.Model):
    nome = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    telefone = models.IntegerField()
    ativo = models.BooleanField()
    
class Horario(models.Model):
    data = models.DateField()
    tipo = models.IntegerField()
    pedido_unidades_curriculares_id = models.IntegerField()
    pedido_horario_id = models.IntegerField()
    pedido_horario_pedido_id = models.IntegerField()
    pedido_horario_pedido_funcionario_id = models.IntegerField()
    pedido_horario_pedido_docente_id = models.IntegerField()
    class Meta:
        unique_together = (
            ('id', 'pedido_unidades_curriculares_id', 'pedido_horario_id', 
             'pedido_horario_pedido_id', 'pedido_horario_pedido_funcionario_id', 
             'pedido_horario_pedido_docente_id'),
        )

class Outros(models.Model):
    desc_pedido = models.CharField(max_length=255)
    pedido_unidades_curriculares_id = models.IntegerField()
    pedidos_outros_id = models.IntegerField()
    pedidos_outros_pedido_id = models.IntegerField()
    pedidos_outros_pedido_funcionario_id = models.IntegerField()
    pedidos_outros_pedido_docente_id = models.IntegerField()
    class Meta:
        unique_together = (
            ('id', 'pedido_unidades_curriculares_id', 'pedidos_outros_id', 
             'pedidos_outros_pedido_id', 'pedidos_outros_pedido_funcionario_id', 
             'pedidos_outros_pedido_docente_id'),
        )

class Pedido(models.Model):
    
    tipo = models.CharField(max_length=255,default="nossa")
    assunto = models.CharField(max_length=255, default="assunto")  
    desc = models.CharField(max_length=1200,default= "Default description")
    dia = models.DateField()
    status = models.CharField(max_length=255,default="Em Análise")
    atribuido = models.CharField(max_length=255, default="Não Atribuido")
    Funcionario=models.ForeignKey(Funcionario, on_delete=models.CASCADE, default=Funcionario.objects.first().id)
    


class PedidoHorario(models.Model):
   
    uc = models.CharField(max_length=255,default="LES")
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    descri = models.CharField(max_length=1200,default= "Default description")
    tarefa = models.CharField(max_length=255,default="Criar")
    dia = models.DateField(default=datetime.date.today)
    

  
class Edificio(models.Model):
    nome = models.CharField(max_length=255, default = "Default name")

class Sala(models.Model):
    id = models.IntegerField(primary_key=True, default=1)

    Edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE)
    TipoSala = models.CharField(max_length=255)
    Capacidade = models.IntegerField()
    NumeroSala = models.FloatField()

class PedidoSala(models.Model):
    edi = models.CharField(max_length=255, default = "Default name")
    sal = models.CharField(max_length=255, default = "Default name")
    tipo = models.CharField(max_length=255, default = "Sala")
    assunto = models.CharField(max_length=255, default="assunto")  
    dia = models.DateField()
    hora_de_inicio = models.TimeField()
    hora_de_fim = models.TimeField()
    desc = models.CharField(max_length=1200, default="Default description")


class PedidosOutros(models.Model):
    tipo = models.CharField(max_length=255, default = "Outros")
    assunto = models.CharField(max_length=255)
    descricao = models.CharField(max_length=1200)
    dia = models.DateField()

class PedidoUC(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, default=Funcionario.objects.first().id)
    uc = models.CharField(max_length=255,default="LES")
    descri = models.CharField(max_length=1200,default= "Default description")
    tipo = models.CharField(max_length=255, default = "Unidades Curriculares")
    tarefa = models.CharField(max_length=255,default="Criar")
    regente = models.CharField(max_length=1200,default= "Default description")
 


class UnidadesCurriculares(models.Model):
    
    AnoLetivo = models.CharField(max_length=255)
    Regência = models.CharField(max_length=255)
    Docentes = models.CharField(max_length=255, default="Zézinha")
    Tipo = models.CharField(max_length=200,default="Null")
    Horas = models.CharField(max_length=255, default="00h")
    Curso = models.CharField(max_length=255)
    Código = models.IntegerField(default=1)
    Descriçao = models.CharField(max_length=255)
    

class EstatisticaPedido(models.Model):
    Status = models.CharField(max_length=255, default="Em Análise")
    NmrPedido = models.IntegerField(default=1)
    TempoMedio = models.CharField(max_length=255, default="1 dia")
    VarTempo = models.CharField(max_length=255, default="3 dias")
    percetagem = models.CharField(max_length=255, default="40%")

class AnoLetivo(models.Model):
    anoletivo = models.CharField(max_length=9, default="2022/2023")
    ativo = models.BooleanField(default=True)
    datainicio = models.DateField()
    datafinal = models.DateField()    

class DSD(models.Model):
    Periodo = models.CharField(max_length=9, default="2022/2023")
    codDisci = models.IntegerField()
    disciplina = models.CharField(max_length=9, default="2022/2023")
    instituic = models.CharField(max_length=9, default="2022/2023")
    instituto = models.CharField(max_length=9, default="2022/2023")
    departamento = models.CharField(max_length=9, default="2022/2023")
    turma = models.CharField(max_length=9, default="2022/2023")
    codCurso = models.CharField(max_length=9)
    curso = models.CharField(max_length=9, default="2022/2023")
    codDocente = models.CharField(max_length=9)
    docente = models.CharField(max_length=9, default="2022/2023")
    funcDocente = models.CharField(max_length=9, default="2022/2023")
    instDocente = models.CharField(max_length=9, default="2022/2023")
    departDocente = models.CharField(max_length=9, default="2022/2023")
    horasSem = models.CharField(max_length=9)
    horasPeri = models.CharField(max_length=9)
    factor = models.CharField(max_length=9, default="2022/2023")
    horasServ = models.CharField(max_length=9)
    Datainicial = models.CharField(max_length=9)
    DataFim = models.CharField(max_length=9)
    Nome = models.CharField(max_length=9, default="2022/2023")
    Agrupamento = models.CharField(max_length=9, default="2022/2023")    