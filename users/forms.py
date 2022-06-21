from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email',
                  'password1', 'password2', 'first_name', 'last_name', ]
        labels = {
            'first_name': 'Imie',
            'last_name': 'Nazwisko',
            'email': 'Adres e-mail:',
            'username': 'Login',
        }

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        for key, value in self.fields.items():
            value.widget.attrs.update(
                {'class': 'input'})


class EditUserForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'email', 'nickname', 'location', 'status',
                  'biography', 'image', 'github', 'linkedin', 'site']
        labels = {
            'full_name' : 'Nazwisko i imię',
            'email': 'Adres e-mail',
            'nickname': 'Login',
            'location': 'Bieżąca lokalizacja',
            'status': 'Stanowisko',
            'biography': 'Opis',
            'image': 'Zdjęcie profilowe',
            'github': 'Link do GitHub',
            'linkedin': 'Link do konta LinkedIn',
            'site': 'Twoja strona'
        }

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)

        for key, value in self.fields.items():
            value.widget.attrs.update(
                {'class': 'input'}
            )


class CreateTechnologyForm(ModelForm):
    class Meta:
        model = Technology
        fields = ['name', 'description']

        labels = {
            'name': 'Nazwa',
            'description': 'Opis',
        }

    def __init__(self, *args, **kwargs):
        super(CreateTechnologyForm, self).__init__(*args, **kwargs)

        for key, value in self.fields.items():
            value.widget.attrs.update(
                {'class': 'input'}
            )


class EditTechnologyForm(ModelForm):
    class Meta:
        model = Technology
        fields = ['name', 'description']

        labels = {
            'name': 'Nazwa',
            'description': 'Opis',
        }

        def __init__(self, *args, **kwargs):
            super(EditTechnologyForm, self).__init__(*args, **kwargs)

            for key, value in self.fields.items():
                value.widget.attrs.update(
                    {'class': 'input'}
                )
