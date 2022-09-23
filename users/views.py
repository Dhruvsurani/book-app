from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from .forms import SignUp, LoginForm
from django.urls import reverse_lazy


# Create your views here.


class IndexView(TemplateView):
    template_name = 'users/base.html'


class SignUpView(CreateView):
    form_class = SignUp
    success_url = reverse_lazy('index')
    template_name = 'users/register.html'


class HomeView(TemplateView):
    template_name = 'users/home.html'


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('home')
    form_class = LoginForm
