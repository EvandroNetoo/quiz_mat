from django import forms
from django.contrib.auth.forms import AuthenticationForm, BaseUserCreationForm

from accounts.models import User


class SignupForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = [
            'email',
            'name',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        return email.lower()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['autofocus'] = True

        placeholders = {
            'email': 'Digite seu email',
            'name': 'Digite seu nome',
            'password1': 'Digite sua senha',
            'password2': 'Confirme sua senha',
        }
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = placeholders[field_name]
            field.required = True


class SigninForm(AuthenticationForm):
    def get_invalid_login_error(self):
        return forms.ValidationError(
            'Credenciais inválidas.',
        )

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        return username.lower()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = True

        placeholders = {
            'username': 'Digite seu email',
            'password': 'Digite sua senha',
        }
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = placeholders[field_name]
