from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.contrib.auth import password_validation


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
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

class SigninForm(forms.Form):
    username = UsernameField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={'autofocus': True}),
    )
    password = forms.CharField(
        label='Mot de passe',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'})
    )

    class Meta:
        fields = ('username', 'password')
