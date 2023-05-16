import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class FuncionarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class Funcionario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, default="gnomo")
    first_name = models.CharField(max_length=255, default="gnomo")
    last_name = models.CharField(max_length=255, default="gnomo")
    email = models.CharField(max_length=255, default="gnomo", unique=True)
    telefone = models.IntegerField()
    ativo = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'telefone', 'ativo', 'username']

    objects = FuncionarioManager()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='funcionario_group_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
        related_query_name='funcionario_group'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='funcionario_permission_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
        related_query_name='funcionario_permission'
    )
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    @property
    def is_staff(self):
        return self.is_superuser

class AdministradorManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class Administrador(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, default="gnomo")
    first_name = models.CharField(max_length=255, default="gnomo")
    last_name = models.CharField(max_length=255, default="gnomo")
    email = models.CharField(max_length=255, default="gnomo", unique=True)
    telefone = models.IntegerField()
    ativo = models.BooleanField(default=True)
    gabinete = models.CharField(max_length=255, default="C1.54")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'telefone', 'ativo', 'username', 'gabinete']

    objects = AdministradorManager()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='administrador_group_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
        related_query_name='administrador_group'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='administrador_permission_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
        related_query_name='administrador_permission'
    )
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    @property
    def is_staff(self):
        return self.is_superuser

### ver o que é importante pegar ###
class DocenteManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class Docente(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, default="gnomo")
    first_name = models.CharField(max_length=255, default="gnomo")
    last_name = models.CharField(max_length=255, default="gnomo")
    email = models.CharField(max_length=255, default="gnomo", unique=True)
    telefone = models.IntegerField()
    ativo = models.BooleanField(default=True)
    gabinete = models.CharField(max_length=255, default="C1.2")
    faculdade = models.CharField(max_length=255, default="FCT")
    departamento = models.CharField(max_length=255, default="Engenharia")


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'telefone', 'ativo', 'username', 'faculdade', 'departamento', 'gabinete']

    objects = DocenteManager()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='docente_group_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
        related_query_name='docente_group'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='docente_permission_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
        related_query_name='docente_permission'
    )
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    @property
    def is_staff(self):
        return self.is_superuser
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

### Parte mais importante deste models ####
class Pedido(models.Model):
    
    tipo = models.CharField(max_length=255,default="nossa")
    assunto = models.CharField(max_length=255, default="assunto")  
    desc = models.CharField(max_length=1200,default= "Default description")
    dia = models.DateField()
    status = models.CharField(max_length=255,default="Em Análise")
    atribuido = models.CharField(max_length=255, default="Não Atribuido")
    Funcionario=models.ForeignKey(Funcionario, on_delete=models.CASCADE, null=True)
    diaCriado = models.DateField(default=datetime.date.today)
    Docente = models.ForeignKey(Docente, on_delete=models.CASCADE, null=True)
    
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

### Ano letivo ###
class AnoLetivo(models.Model):
    anoletivo = models.CharField(max_length=9, default="2022/2023")
    ativo = models.BooleanField(default=True)
    datainicio = models.DateField()
    datafinal = models.DateField()  

###estatisticas dos Pedidos ###
class EstatisticaPedido(models.Model):
    Status = models.CharField(max_length=255, default="Em Análise")
    NmrPedido = models.IntegerField(default=1)
    TempoMedio = models.CharField(max_length=255, default="1 dia")
    VarTempo = models.CharField(max_length=255, default="3 dias")
    percetagem = models.CharField(max_length=255, default="40%")



#Faculdade Departamento
class Faculdade(models.Model):
    nome = models.CharField(max_length=255, default="FCT - Faculdade de Ciencias e Tecnologia")

class Departamento(models.Model):
    nome = models.CharField(max_length=255, default="Departamento de Engenharia informática")