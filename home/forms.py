
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)
    catid = forms.IntegerField()


class SignUpForm(UserCreationForm):
    username = forms.CharField(label='User Name :', max_length=30)
    email = forms.EmailField(label='Email :', max_length=200)
    first_name = forms.CharField(label='First Name :', max_length=100, help_text='First Name')
    last_name = forms.CharField(label='Last Name :', max_length=100, help_text='Last Name')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
