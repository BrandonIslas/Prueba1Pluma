from django import forms
from django.contrib.auth.models import User
from .models import Archivos, OrigenDestino

class SignupForm(forms.Form):
    """Sign up form."""

    username = forms.CharField(min_length=3, max_length=20)

    password = forms.CharField(
        min_length=3,
        max_length=20,
        widget=forms.PasswordInput()
    )
    password_confirmation = forms.CharField(
        min_length=3,
        max_length=20,
        widget=forms.PasswordInput()
    )

    first_name = forms.CharField(min_length=3, max_length=20,required=True)
    last_name = forms.CharField(min_length=3, max_length=20,required=True)

    email = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.EmailInput()
    )

    def clean_username(self):
        """Username must be unique."""
        username = self.cleaned_data['username']
        username_taken = User.objects.filter(username=username).exists()
        if username_taken:
            raise forms.ValidationError('Username is already in use.')
        return username

    def clean(self):
        """Verify password confirmation match."""
        data = super().clean()

        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Passwords do not match.')

        return data

    def save(self):
        """Create user and profile."""
        data = self.cleaned_data
        data.pop('password_confirmation')

        user = User.objects.create_user(**data)

class SubidaArchivosForm(forms.ModelForm):
    class Meta:
        model= Archivos
        fields= '__all__'

class OrigenDestinoForm(forms.ModelForm):
    class Meta:
        model=OrigenDestino
        fields='__all__'

    def clean(self):
        """Verify password confirmation match."""
        data = super().clean()

        oringen = data['origen']
        destino = data['destino']

        return data
