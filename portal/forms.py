from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from radius.models import Radcheck
from django import forms

from django.contrib.auth import get_user_model

my_default_errors = {
    'required': 'Este campo é obrigatório',
    'invalid': 'Entre um valor válido',
    'password_mismatch': 'As duas senhas não coincidem.'
}



class SignupForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Nome de Usuário',
                'id': 'auth_user',
            }

        ), label='',
        error_messages=my_default_errors,
    )

    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'placeholder': 'Senha',
            'id': 'auth_pass'
        }),
        error_messages=my_default_errors,
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'type': 'password',
                'placeholder': 'Confirmação da senha',
                'id': 'auth_pass2',
            }),
        error_messages=my_default_errors,
    )

    def save(self, commit=True):
        obj = super(SignupForm, self).save(commit=False)

        #import pdb
        #pdb.set_trace()
        #user = get_user_model().objects.create_user()

        rad_user = Radcheck.objects.filter(username=self.cleaned_data['username'])
        if rad_user:
            return False

        new_rad_user = Radcheck.objects.create(
            username=self.cleaned_data['username'],
            attribute='Cleartext-Password',
            op=':=',
            value=self.cleaned_data['password1'],
        )

        new_rad_user.save()

        if commit:
            obj.save()
        return obj


class LoginForm(forms.Form):
    auth_user = forms.CharField(
        max_length=254,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Insira seu nome de usuário',
                'id': 'auth_user',
            }
        ),
        label='',
        error_messages=my_default_errors,
    )
    auth_pass = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'placeholder': 'Insira sua Senha',
            'id': 'auth_pass',
        }),
        label='',
        error_messages=my_default_errors,)
