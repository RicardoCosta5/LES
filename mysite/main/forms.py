
from django import forms
from django.forms import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User

from .models import *
class ParticipanteForm(UserCreationForm):
    class Meta:
        model = Docente
        fields = '__all__'

class EmailValidationOnForgotPassword(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError(f'Este email não é válido!')
        return email



USER_CHOICES = (
    ("Utilizador", "Todos os Utilizadores"),
    ("Docente", "Docentes"),
    ("Funcionario", "Funcionarios"),
)

ESTADOS = (
    ("", "Todos os Estados"),
    ("T", "Confirmado"),
    ("F", "Pendente"),
    ("R", "Rejeitado"),
)




class UtilizadorFiltro(Form):
    filtro_tipo = ChoiceField(
        choices=USER_CHOICES,
        widget=Select(),
        required=False,
    )

    filtro_estado = ChoiceField(
        choices=ESTADOS,
        widget=Select(),
        required=False,
    )





from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Funcionario

class FuncionarioRegisterForm(UserCreationForm):
    class Meta:
        model = Funcionario
        fields = ('username', 'password1', 'password2', 'email',
                  'first_name', 'last_name', 'telefone')

    def clean(self):
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        telefone = self.cleaned_data.get('telefone')
        erros = []
        if email == "" or first_name=="" or last_name=="" or username==None:
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')

        if username and User.objects.filter(username=username).exists():
            erros.append(forms.ValidationError(f'O username já existe'))

        
        if password1==None or password2==None:
            if password1==None:
                raise forms.ValidationError(f'Todos os campos são obrigatórios!')
            if password1==None:
                raise forms.ValidationError(f'Todos os campos são obrigatórios!')
            else:
                erros.append(forms.ValidationError(f'As palavras-passe não correspondem'))


        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(f'O email já existe')
        elif email==None:
            erros.append(forms.ValidationError(f'O email é inválido'))

        
        if telefone==None:
            erros.append(forms.ValidationError(f'Preencha corretamente o telefone'))    
        if len(erros)>0:
            raise ValidationError([erros])

class FuncionarioAlterarPerfilForm(ModelForm):

    class Meta:
        model = Funcionario
        fields = ('email',
                  'first_name', 'last_name', 'telefone')

    def clean(self):
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        telefone = self.cleaned_data.get('telefone')
        erros = []
        if email == "" or first_name=="" or last_name=="":
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')
        
        if telefone==None:
            erros.append(forms.ValidationError(f'Preencha corretamente o telefone'))    
        if len(erros)>0:
            raise ValidationError([erros])

class AdministradorAlterarPerfilForm(ModelForm):

    class Meta:
        model = Administrador
        fields = ('email','first_name', 'last_name', 'telefone','gabinete')

    def clean(self):
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        telefone = self.cleaned_data.get('telefone')
        gabinete = self.cleaned_data.get('gabinete')
        erros = []
        if email == "" or first_name=="" or last_name=="" or gabinete==None:
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')
        
        if telefone==None:
            erros.append(forms.ValidationError(f'Preencha corretamente o telefone'))    
        if len(erros)>0:
            raise ValidationError([erros])
class AdministradorRegisterForm(UserCreationForm):

    class Meta:
        model = Administrador
        fields = ('username', 'password1', 'password2', 'email',
                  'first_name', 'last_name', 'telefone','gabinete')

    def clean(self):
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        telefone = self.cleaned_data.get('telefone')
        gabinete = self.cleaned_data.get('gabinete')
        erros = []
        if email == "" or first_name=="" or last_name=="" or username==None or gabinete==None:
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')

        if username and User.objects.filter(username=username).exists():
            erros.append(forms.ValidationError(f'O username já existe'))

        
        if password1==None or password2==None:
            if password1==None:
                raise forms.ValidationError(f'Todos os campos são obrigatórios!')
            if password1==None:
                raise forms.ValidationError(f'Todos os campos são obrigatórios!')
            else:
                erros.append(forms.ValidationError(f'As palavras-passe não correspondem'))


        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(f'O email já existe')
        elif email==None:
            erros.append(forms.ValidationError(f'O email é inválido'))

        
        if telefone==None:
            erros.append(forms.ValidationError(f'Preencha corretamente o telefone'))    
        if len(erros)>0:
            raise ValidationError([erros])


class DocenteRegisterForm(UserCreationForm):
    class Meta:
        model = Docente
        fields = ('username', 'password1', 'password2', 'email',
                  'first_name', 'last_name', 'telefone','gabinete', 'faculdade', 'departamento')

    def clean(self):
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        telefone = self.cleaned_data.get('telefone')
        gabinete = self.cleaned_data.get('gabinete')
        departamento = self.cleaned_data.get('departamento')
        faculdade = self.cleaned_data.get('faculdade')
        erros = []
        if email == "" or first_name=="" or last_name=="" or username==None:
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')

        if username and User.objects.filter(username=username).exists():
            erros.append(forms.ValidationError(f'O username já existe'))

        
        if password1==None or password2==None:
            if password1==None:
                raise forms.ValidationError(f'Todos os campos são obrigatórios!')
            if password1==None:
                raise forms.ValidationError(f'Todos os campos são obrigatórios!')
            else:
                erros.append(forms.ValidationError(f'As palavras-passe não correspondem'))


        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(f'O email já existe')
        elif email==None:
            erros.append(forms.ValidationError(f'O email é inválido'))

        
        if telefone==None:
            erros.append(forms.ValidationError(f'Preencha corretamente o telefone'))    
        if len(erros)>0:
            raise ValidationError([erros])


class DocenteAlterarPerfilForm(ModelForm):
    class Meta:
        model = Docente
        fields = ('email',
                  'first_name', 'last_name', 'telefone', 'gabinete','faculdade','departamento')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       



    def clean(self):
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        telefone = self.cleaned_data.get('telefone')
        gabinete = self.cleaned_data.get('gabinete')
        faculdade = self.cleaned_data.get('faculdade')
        departamento = self.cleaned_data.get('departamento')
        erros = []
        if email == "" or first_name=="" or last_name=="" or gabinete==None or faculdade==None or departamento==None:
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')
        
        if telefone==None:
            erros.append(forms.ValidationError(f'Preencha corretamente o telefone'))    
        if len(erros)>0:
            raise ValidationError([erros])

class LoginForm(AuthenticationForm):
    username=CharField(widget=TextInput(attrs={'class':'input','style':''}), label="Nome de Utilizador", max_length=255, required=False)
    password=CharField(widget=PasswordInput(attrs={'class':'input','style':''}), label= 'Senha', max_length=255, required=False)
