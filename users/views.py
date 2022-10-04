from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from .forms import SignUp
from django.urls import reverse_lazy


# Create your views here.



class SignUpView(CreateView):
    form_class = SignUp
    success_url = reverse_lazy('book_list')
    template_name = 'users/register.html'





