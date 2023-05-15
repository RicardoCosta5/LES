
from django import forms
from django.forms import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User

from .models import Docente, Funcionario
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





class FuncionarioRegisterForm(UserCreationForm):

    class Meta:
        model = Funcionario
        fields = ('first_name','last_name', 'email', 'telefone')

    def clean(self):
        username = self.cleaned_data.get('username')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        telefone = self.cleaned_data.get('telefone')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        erros = []
        if email == "" or first_name=="" or last_name=="" or telefone=="":
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')

        if username and User.objects.filter(first_name=first_name).exists():
            erros.append(forms.ValidationError(f'O username já existe'))

        
        if password1==None or password2==None:
            if password1==None:
                raise forms.ValidationError(f'Todos os campos são obrigatórios!')
            if password1==None:
                raise forms.ValidationError(f'Todos os campos são obrigatórios!')
            else:
                erros.append(forms.ValidationError(f'As palavras-passe não correspondem'))


        if email==None:
            erros.append(forms.ValidationError(f'O email é inválido'))

        
        if telefone==None:
            erros.append(forms.ValidationError(f'Preencha corretamente o contacto'))    
        if len(erros)>0:
            raise ValidationError([erros])


class AdministradorRegisterForm(UserCreationForm):

    class Meta:
        model = Docente
        fields = ('first_name','last_name', 'email', 'telefone','ativo')

    def clean(self):
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        contacto = self.cleaned_data.get('contacto')
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

        
        if contacto==None:
            erros.append(forms.ValidationError(f'Preencha corretamente o contacto'))    
        if len(erros)>0:
            raise ValidationError([erros])

class DocenteRegisterForm(UserCreationForm):
    class Meta:
        model = Docente
        fields = ('first_name','last_name', 'email', 'telefone','ativo')

    def clean(self):
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        telefone = self.cleaned_data.get('telefone')
        gabinete = self.cleaned_data.get('gabinete')
        faculdade = self.cleaned_data.get('faculdade')
        departamento = self.cleaned_data.get('departamento')
        erros = []
        if email == "" or first_name=="" or last_name=="" or username==None or gabinete==None or faculdade==None or departamento==None:
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

        
        if contacto==None:
            erros.append(forms.ValidationError(f'Preencha corretamente o contacto'))    
        if len(erros)>0:
            raise ValidationError([erros])



    def clean(self):
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        contacto = self.cleaned_data.get('contacto')
        curso = self.cleaned_data.get('curso')
        faculdade = self.cleaned_data.get('faculdade')
        departamento = self.cleaned_data.get('departamento')
        erros = []
        if email == "" or first_name=="" or last_name=="" or username==None or curso==None or faculdade==None or departamento==None:
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

        
        if contacto==None:
            erros.append(forms.ValidationError(f'Preencha corretamente o contacto'))    
        if len(erros)>0:
            raise ValidationError([erros])

class LoginForm(AuthenticationForm):
    username=CharField(widget=TextInput(attrs={'class':'input','style':''}), label="Nome de Utilizador", max_length=255, required=False)
    password=CharField(widget=PasswordInput(attrs={'class':'input','style':''}), label= 'Senha', max_length=255, required=False)
