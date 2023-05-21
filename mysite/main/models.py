import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Utilizador(User):
    telefone = models.IntegerField()
    valido = models.CharField(max_length=255, blank=False, null=False)

    def getProfiles(self):
        type = ''
        if Administrador.objects.filter(utilizador_ptr_id=self):
            type = self.concat(type=type, string='Administrador')
        if Docente.objects.filter(utilizador_ptr_id=self):
            type = self.concat(type=type, string='Docente')
        if Funcionario.objects.filter(utilizador_ptr_id=self):
            type = self.concat(type=type, string='Funcionário')
        return type

    def concat(self, type, string):
        if type == '':
            type = string
        else:
            type += ', '+string
        return type

    @property
    def firstProfile(self):
        return self.getProfiles().split(' ')[0]

    def getUser(self):
        user = User.objects.get(id=self.id)
        if user.groups.filter(name = "Docente").exists():
            result = Docente.objects.get(id=self.id)
        elif user.groups.filter(name = "Administrador").exists():
            result = Administrador.objects.get(id=self.id)
        elif user.groups.filter(name = "Funcionário").exists():
            result = Funcionario.objects.get(id=self.id)
        else:
            result = None
        return result   


    def getProfile(self):
        user = User.objects.get(id=self.id)
        if user.groups.filter(name = "Docente").exists():
            result = "Docente"
        elif user.groups.filter(name = "Administrador").exists():
            result = "Administrador"
        elif user.groups.filter(name = "Funcionário").exists():
            result = "Funcionário"
        else:
            result = None
        return result 

    def emailValidoUO(self,uo):
        user = User.objects.get(email=self.email)
        if user.groups.filter(name = "Docente").exists():
            utilizador = Docente.objects.get(email=self.email)
        elif user.groups.filter(name = "Administrador").exists():
            return True
        elif user.groups.filter(name = "Funcionário").exists():
            utilizador = Funcionario.objects.get(email=self.email)
        else:
            return False
        if utilizador.faculdade == uo:
            return True
        else:
            return False   

    def emailValidoParticipante(self):
        user = User.objects.get(email=self.email)
        if user.groups.filter(name = "Administrador").exists():
            return True
        else:
            return False    
    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name
    class Meta:
        db_table = 'Utilizador'


#Faculdade Departamento
class Faculdade(models.Model):
    nome = models.CharField(max_length=255, default="FCT - Faculdade de Ciencias e Tecnologia")

class Departamento(models.Model):
    nome = models.CharField(max_length=255, default="Departamento de Engenharia informática")
class Administrador(Utilizador):
    gabinete = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        db_table = 'Administrador'


class Funcionario(Utilizador):
    class Meta:
        db_table = 'Funcionário'


class Docente(Utilizador):
    gabinete = models.CharField(db_column='Gabinete', max_length=255, blank=False, null=False)

    faculdade = models.CharField(db_column='Faculdade', max_length=255, blank=False, null=False)

    departamento = models.CharField(db_column='Departamento', max_length=255, blank=False, null=False)

    def __str__(self):
        return str(self.gabinete) + ' ' + str(self.faculdade) + ' ' + str(self.departamento)
    class Meta:
        db_table = 'Docente'
 ### Literalmente nao é utilizado em nada ###   
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


### Ano letivo ###
class AnoLetivo(models.Model):
    anoletivo = models.CharField(max_length=9, default="2022/2023")
    ativo = models.BooleanField(default=False)
    datainicio = models.DateField()
    datafinal = models.DateField()  

### Parte mais importante deste models ####
class Pedido(models.Model):
    
    tipo = models.CharField(max_length=255,default="nossa")
    assunto = models.CharField(max_length=255, default="assunto")  
    desc = models.CharField(max_length=1200,default= "Default description")
    dia = models.DateField()
    status = models.CharField(max_length=255,default="Registado")
    atribuido = models.CharField(max_length=255, default="Não Atribuido")
    Funcionario=models.ForeignKey(Funcionario, on_delete=models.CASCADE, null=True)
    diaCriado = models.DateField(default=datetime.date.today)
    Docente = models.ForeignKey(Docente, on_delete=models.CASCADE, null=True)
    Rejeitarpedido = models.CharField(max_length=1000,default="Nao sei")
    Anoletivo = models.ForeignKey(AnoLetivo, on_delete=models.CASCADE, null=True)

    
### Pedidos ( Horario - Outros - UC - Sala) , desta parte esta ok
class PedidoHorario(models.Model):
   
    uc = models.CharField(max_length=255,default="LES")
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    descri = models.CharField(max_length=1200,default= "Default description")
    tarefa = models.CharField(max_length=255,default="Criar")
    dia = models.DateField(default=datetime.date.today)


class PedidosOutros(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, null=True)
    arquivo = models.FileField(blank=True, null=True)

class PedidoUC(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    uc = models.CharField(max_length=255,default="LES")
    descri = models.CharField(max_length=1200,default= "Default description")
    tipo = models.CharField(max_length=255, default = "Unidades Curriculares")
    tarefa = models.CharField(max_length=255,default="Criar")
    regente = models.CharField(max_length=1200,default= "Default description")

class PedidoSala(models.Model):
    edi = models.CharField(max_length=255, default = "Default name")
    sal = models.CharField(max_length=255, default = "Default name")
    uc = models.CharField(max_length=255,default="LES")
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)    
    hora_de_inicio = models.TimeField()
    status = models.CharField(max_length=255,default="Em Análise")
    hora_de_fim = models.TimeField()
    descri = models.CharField(max_length=1200, default="Default description")
    dia = models.DateField(default=datetime.date.today)
    tarefa = models.CharField(max_length=255,default="Criar")

### vai ser utilizado para obtermos as salas do edificio ###
class Edificio(models.Model):
    nome = models.CharField(max_length=255, default = "Default name")

    ### Literalmente nao é utilizado em nada ###
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

### ver o que é importante pegar ###
class Turma(models.Model):
    Periodo = models.CharField(max_length=255, default="2022/2023")
    codDisci = models.IntegerField()
    disciplina = models.CharField(max_length=255, default="2022/2023")
    instituto = models.CharField(max_length=255, default="2022/2023")
    turma = models.CharField(max_length=255, default="2022/2023")
    curso = models.CharField(max_length=255, default="2022/2023")
    codDocente = models.CharField(max_length=255)
    docente = models.CharField(max_length=255, default="2022/2023")
    departDocente = models.CharField(max_length=255, default="2022/2023")
    horasSem = models.CharField(max_length=255)
    Datainicial = models.CharField(max_length=255)
    DataFim = models.CharField(max_length=255) 

    ### ver o que é importante pegar ###
class UnidadesCurriculares(models.Model):
    
    AnoLetivo = models.CharField(max_length=255)
    Regência = models.CharField(max_length=255)
    Docentes = models.CharField(max_length=255, default="Zézinha")
    Tipo = models.CharField(max_length=200,default="Null")
    Horas = models.CharField(max_length=255, default="00h")
    Curso = models.CharField(max_length=255)
    Código = models.IntegerField(default=1)
    Descriçao = models.CharField(max_length=255)

    ### Importaçao de salas ver o que pegar daqui, alterar cenas btw ###
class Sala(models.Model):
    NomeInstituição = models.CharField(max_length=255, default = "Default name")
    DescEdifício = models.CharField(max_length=255, default = "Default name")
    DescSala = models.CharField(max_length=255, default = "Default name")
    DesCategoria = models.CharField(max_length=255, default = "Default name")
    IdTipoSala = models.CharField(max_length=255, default = "Default name")
    LotaçãoPresencialSala = models.CharField(max_length=255, default = "Default name")



###estatisticas dos Pedidos ###
class EstatisticaPedido(models.Model):
    Status = models.CharField(max_length=255, default="Em Análise")
    NmrPedido = models.IntegerField(default=1)
    TempoMedio = models.CharField(max_length=255, default="1 dia")
    VarTempo = models.CharField(max_length=255, default="3 dias")
    percetagem = models.CharField(max_length=255, default="40%")

