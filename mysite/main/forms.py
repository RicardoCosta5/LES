
from django import forms
from django.forms import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User

from .models import Docente, Funcionario, Administrador
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
    email = forms.EmailField(required=True)

    class Meta:
        model = Funcionario
        fields = ('first_name', 'last_name','username', 'email', 'telefone', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if Funcionario.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class AdministradorRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Administrador
        fields = ('first_name', 'last_name','username', 'email', 'telefone', 'password1', 'password2', 'gabinete')

    def clean_email(self):
        email = self.cleaned_data['email']
        if Funcionario.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class DocenteRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Docente
        fields = ('first_name', 'last_name','username', 'email', 'telefone', 'password1', 'password2', 'gabinete', 'faculdade', 'departamento')

    def clean_email(self):
        email = self.cleaned_data['email']
        if Funcionario.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username=CharField(widget=TextInput(attrs={'class':'input','style':''}), label="Nome de Utilizador", max_length=255, required=False)
    password=CharField(widget=PasswordInput(attrs={'class':'input','style':''}), label= 'Senha', max_length=255, required=False)
