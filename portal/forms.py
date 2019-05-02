from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile
from radius.models import Radcheck
from django import forms

from django.contrib.auth import get_user_model

my_default_errors = {
    'required': 'Este campo é obrigatório',
    'invalid': 'Entre um valor válido',
    'password_mismatch': 'As duas senhas não coincidem.'
}

User = get_user_model()

class SignupForm(ModelForm):

    password2 = forms.PasswordInput()

    class Meta:
        model = User
        fields = ('username', 'password')

    def save(self, commit=True):
        obj = super(SignupForm, self).save(commit=False)

        obj.set_password(self.cleaned_data['password'])

        rad_user = Radcheck.objects.filter(username=self.cleaned_data['username'])
        if rad_user:
            return False

        new_rad_user = Radcheck.objects.create(
            username=self.cleaned_data['username'],
            attribute='Cleartext-Password',
            op=':=',
            value=self.cleaned_data['password'],
        )

        new_rad_user.save()

        if commit:
            obj.save()
        return obj


# class SignupForm(ModelForm):
#     password2 = forms.PasswordInput()
#
#     class Meta(UserForm.Meta):
#         fields = (UserForm.Meta.fields, 'password2',)
#
#     def save(self, commit=False):
#         if self.cleaned_data['password'] == self.cleaned_data['password2']:
#             UserForm.save(self)

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
