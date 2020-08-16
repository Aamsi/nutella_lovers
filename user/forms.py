from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth import password_validation

from .models import User
from nutella_lovers import settings


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, label="Prenom")
    last_name = forms.CharField(max_length=30, required=False, label="Nom")
    username = forms.CharField(label="Nom d'utilisateur")
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(
        label="Mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Confirmer mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="Entrez le meme mot de passe, pour verification"
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class SigninForm(forms.Form):
    email = forms.EmailField(
        label="Email",
    )
    password = forms.CharField(
        label='Mot de passe',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'})
    )

    class Meta:
        fields = ('username', 'password')
