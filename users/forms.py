from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

my_choices = (
    ('1', "Admin"),
    ('2', "Buyer")
)


class SignUp(UserCreationForm):
    username = forms.CharField(max_length=40)
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)
    email = forms.EmailField(max_length=100)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]


class LoginForm(AuthenticationForm):

    choices = forms.ChoiceField(choices=my_choices)

    class Meta:
        fields = [
            'username',
            'choices',
            'password'
        ]
